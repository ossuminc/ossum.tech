---
title: "Reporting Context"
description: "CQRS read-model projectors for sales, labor, and inventory reports"
---

<!-- riddl-prelude
event PaymentProcessed is { tableOrderId: String(1,50) }
event ClockedIn is { shiftId: String(1,50) }
event StockConsumed is { inventoryItemId: String(1,50) }
type ReportingEvent is PaymentProcessed | ClockedIn | StockConsumed
-->

# Reporting Context

The Reporting context is a **pure CQRS read-model** — it
contains only projectors, no entities. It builds reports
asynchronously from events emitted by production contexts,
ensuring that report generation never degrades peak-hour
restaurant performance.

## Purpose

Management needs sales reports, labor reports, and inventory
reports. In a monolithic system, generating these reports queries
the same database that handles live orders, causing slowdowns
during peak hours. The Reporting context solves this by
maintaining its own read-optimized views built from events.

## Design: No Entities

This is the only context in the entire Reactive BBQ model that
has **no entities**. It only has projectors. This is a deliberate
CQRS pattern — the Reporting context is the "query" side. The
"command" sides are the production contexts (FrontOfHouse,
OnlineOrdering, Scheduling, Inventory) that emit events.

## SalesReport Projector

<!-- riddl: in-context -->
```riddl
// The repository is a SINK: reports are written, never read back into the
// write side. The projector is its SOURCE.
repository SalesReportRepository as sink is {
  inlet SalesReportRepositoryFromSalesReport is type SalesReportCommand
  type SalesReportCommand is RecordDineInPayment

  record SalesReportRecord is {
    reportDate: Date
    totalRevenue: Decimal(12,2)
    orderCount: Natural
  }

  schema SalesReportData is relational
    of rows as type SalesReportRecord
      index on field SalesReportRecord.reportDate

  command RecordDineInPayment is { tableOrderId: String(1,50) }

  handler SalesReportPersistence is {
    on command RecordDineInPayment is {
      do "upsert the sales row for this date: increment orderCount and add the payment to totalRevenue"
    }
    // An inlet admitting an alternation needs a clause that receives it.
    // Handling each member is not enough -- say what ARRIVING means.
    on other is {
      do "persist whatever else arrives on this inlet"
    }
  }
}

projector SalesReport as source is {
  updates repository SalesReportRepository
  outlet SalesReportOut is type SalesReportCommand

  record SalesReportEntry is {
    reportDate: Date
    totalRevenue: Decimal(12,2)
    orderCount: Natural
  }

  handler SalesReportHandler is {
    on evt: event PaymentProcessed is {
      tell command RecordDineInPayment(tableOrderId = evt.tableOrderId) to repository SalesReportRepository
    }
  }
}
```

The SalesReport listens to payment events from **two different
contexts** — FrontOfHouse (dine-in) and OnlineOrdering (online).
It aggregates them into a unified view with breakdowns by
channel.

## LaborReport Projector

<!-- riddl: in-context -->
```riddl
// The repository is a SINK: reports are written, never read back into the
// write side. The projector is its SOURCE.
repository LaborReportRepository as sink is {
  inlet LaborReportRepositoryFromLaborReport is type LaborReportCommand
  type LaborReportCommand is RecordShiftHours

  record LaborReportRecord is {
    laborReportDate: Date
    hoursWorked: Decimal(10,2)
    laborCost: Decimal(12,2)
  }

  schema LaborReportData is relational
    of rows as type LaborReportRecord
      index on field LaborReportRecord.laborReportDate

  command RecordShiftHours is { shiftId: String(1,50) }

  handler LaborReportPersistence is {
    on command RecordShiftHours is {
      do "upsert the labor row for this date: add the shift's hours and cost"
    }
    // An inlet admitting an alternation needs a clause that receives it.
    // Handling each member is not enough -- say what ARRIVING means.
    on other is {
      do "persist whatever else arrives on this inlet"
    }
  }
}

projector LaborReport as source is {
  updates repository LaborReportRepository
  outlet LaborReportOut is type LaborReportCommand

  record LaborReportEntry is {
    laborReportDate: Date
    hoursWorked: Decimal(10,2)
    laborCost: Decimal(12,2)
  }

  handler LaborReportHandler is {
    on evt: event ClockedIn is {
      tell command RecordShiftHours(shiftId = evt.shiftId) to repository LaborReportRepository
    }
  }
}
```

The LaborReport listens to scheduling events from the same
BackOffice domain. It calculates hours worked by comparing
`ClockedIn` and `ClockedOut` event timestamps and tracks
shift cancellation rates.

## InventoryReport Projector

<!-- riddl: in-context -->
```riddl
// The repository is a SINK: reports are written, never read back into the
// write side. The projector is its SOURCE.
repository InventoryReportRepository as sink is {
  inlet InventoryReportRepositoryFromInventoryReport is type InventoryReportCommand
  type InventoryReportCommand is RecordStockMovement

  record InventoryReportRecord is {
    inventoryReportDate: Date
    itemsConsumed: Natural
    stockValue: Decimal(12,2)
  }

  schema InventoryReportData is relational
    of rows as type InventoryReportRecord
      index on field InventoryReportRecord.inventoryReportDate

  command RecordStockMovement is { inventoryItemId: String(1,50) }

  handler InventoryReportPersistence is {
    on command RecordStockMovement is {
      do "upsert the inventory row for this date: add the consumed quantity and revalue stock"
    }
    // An inlet admitting an alternation needs a clause that receives it.
    // Handling each member is not enough -- say what ARRIVING means.
    on other is {
      do "persist whatever else arrives on this inlet"
    }
  }
}

projector InventoryReport as source is {
  updates repository InventoryReportRepository
  outlet InventoryReportOut is type InventoryReportCommand

  record InventoryReportEntry is {
    inventoryReportDate: Date
    itemsConsumed: Natural
    stockValue: Decimal(12,2)
  }

  handler InventoryReportHandler is {
    on evt: event StockConsumed is {
      tell command RecordStockMovement(inventoryItemId = evt.inventoryItemId) to repository InventoryReportRepository
    }
  }
}
```

The InventoryReport provides a dashboard view of stock health
across the location — how many items are tracked, how many are
running low, and the total estimated stock value.

## Design Decisions

**Why no entities?** Reports don't have their own commands or
lifecycle. They are purely derived from events happening
elsewhere. Making them projectors without entities makes this
read-only nature explicit in the model.

**Why a separate context?** If reports were projectors inside
the FrontOfHouse or Scheduling contexts, they would share
resources with production workloads. Isolating them in their
own context means they can be deployed on separate
infrastructure, scaled independently, and even be temporarily
unavailable without affecting production.

**Cross-domain event consumption:** Notice that the Reporting
context listens to events from both the Restaurant domain
(payment events) and the BackOffice domain (scheduling and
inventory events). This cross-domain listening is exactly what
CQRS projectors are designed for — they aggregate data from
wherever it originates.

**Eventual consistency:** Reports are eventually consistent
with production data. There may be a brief delay between a
payment being processed and the sales report reflecting it.
This is acceptable for management reporting and is the key
trade-off that enables production isolation.

## Source

- [`ReportingContext.riddl`](https://github.com/ossuminc/riddl-models/tree/main/hospitality/food-service/reactive-bbq/backoffice/ReportingContext.riddl)
