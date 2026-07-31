---
title: "Reporting Context"
description: "CQRS read-model projectors for sales, labor, and inventory reports"
---

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

```riddl
projector SalesReport is {

  record SalesReportEntry is {
    reportDate is Date
    totalRevenue is Decimal(12, 2)
    dineInRevenue is Decimal(12, 2)
    onlineRevenue is Decimal(12, 2)
    orderCount is Natural
    averageOrderValue is Decimal(10, 2)
  }

  handler SalesReportHandler is {
    on event Restaurant.FrontOfHouse.TableOrder.PaymentProcessed {
      prompt "Record dine-in sale in report"
    }
    on event Restaurant.OnlineOrdering.OnlineOrder.OnlinePaymentProcessed {
      prompt "Record online sale in report"
    }
  }
} with {
  briefly "Sales report projector"
  described by {
    | Builds sales reports from payment events across
    | dine-in and online channels. Isolated from production
    | so report generation never impacts peak-hour performance.
  }
}
```

The SalesReport listens to payment events from **two different
contexts** — FrontOfHouse (dine-in) and OnlineOrdering (online).
It aggregates them into a unified view with breakdowns by
channel.

## LaborReport Projector

```riddl
projector LaborReport is {

  record LaborReportEntry is {
    laborReportDate is Date
    totalHoursWorked is Decimal(8, 2)
    shiftsCompleted is Natural
    shiftsCancelled is Natural
    averageShiftDuration is Decimal(6, 2)
  }

  handler LaborReportHandler is {
    on event BackOffice.Scheduling.Shift.ClockedIn {
      prompt "Record shift start in labor report"
    }
    on event BackOffice.Scheduling.Shift.ClockedOut {
      prompt "Record shift end and calculate hours"
    }
    on event BackOffice.Scheduling.Shift.ShiftCancelled {
      prompt "Record shift cancellation"
    }
  }
}
```

The LaborReport listens to scheduling events from the same
BackOffice domain. It calculates hours worked by comparing
`ClockedIn` and `ClockedOut` event timestamps and tracks
shift cancellation rates.

## InventoryReport Projector

```riddl
projector InventoryReport is {

  record InventoryReportEntry is {
    inventoryReportDate is Date
    totalItemsTracked is Natural
    lowStockItems is Natural
    outOfStockItems is Natural
    totalStockValue is Decimal(14, 2)
  }

  handler InventoryReportHandler is {
    on event BackOffice.Inventory.InventoryItem.StockReceived {
      prompt "Update inventory report with receipt"
    }
    on event BackOffice.Inventory.InventoryItem.StockConsumed {
      prompt "Update inventory report with consumption"
    }
    on event BackOffice.Inventory.InventoryItem.StockAdjusted {
      prompt "Update inventory report with adjustment"
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
