---
title: "Inventory Context"
description: "Stock level tracking with automated kitchen integration"
---

# Inventory Context

The Inventory context manages stock levels, receiving,
consumption tracking, manual adjustments, and reorder
thresholds. It integrates with the Kitchen context to
automatically track consumption as items are prepared.

## Purpose

Every restaurant location tracks hundreds of ingredients and
supplies. The Inventory context provides the operational
foundation: receiving shipments, tracking consumption,
triggering reorder alerts, and creating purchase orders when
stock runs low.

## Types

```riddl
type InventoryItemId is Id(Inventory.InventoryItem) with {
  briefly "Inventory item identifier"
  described by "Unique identifier for an inventory item."
}

type UnitOfMeasure is any of {
  Each,
  Pound,
  Ounce,
  Gallon,
  Liter,
  Case,
  Box
} with {
  briefly "Unit of measure"
  described by "Measurement unit for inventory quantities."
}

type InventoryItemStatus is any of {
  InStock,
  LowStock,
  OutOfStock,
  Discontinued
} with {
  briefly "Inventory item status"
  described by "Current stock status of an inventory item."
}

type StockAdjustmentReason is any of {
  Spoilage,
  Breakage,
  Theft,
  CountCorrection,
  Donation,
  OtherAdjustment
} with {
  briefly "Stock adjustment reason"
  described by "Reason for a manual stock adjustment."
}
```

The `StockAdjustmentReason` enumeration captures why stock was
manually adjusted — essential for loss tracking and audit
compliance.

## Entity: InventoryItem

The `InventoryItem` entity has a 5-command lifecycle:

```riddl
entity InventoryItem is {

  command ReceiveStock is {
    inventoryItemId is InventoryItemId
    receivedQuantity is Decimal(10, 2)
    receivedUnit is UnitOfMeasure
    supplierRef is optional String(1, 100)
    stockReceivedAt is TimeStamp
  }

  command ConsumeStock is {
    inventoryItemId is InventoryItemId
    consumedQuantity is Decimal(10, 2)
    consumedUnit is UnitOfMeasure
    consumptionRef is optional String(1, 100)
  }

  command AdjustStock is {
    inventoryItemId is InventoryItemId
    adjustmentQuantity is Decimal(10, 2)
    adjustmentUnit is UnitOfMeasure
    adjustmentReason is StockAdjustmentReason
    adjustmentNotes is optional String(1, 500)
  }

  command SetReorderThreshold is {
    inventoryItemId is InventoryItemId
    reorderThreshold is Decimal(10, 2)
    reorderUnit is UnitOfMeasure
  }

  command CreatePurchaseOrder is {
    inventoryItemId is InventoryItemId
    orderQuantity is Decimal(10, 2)
    orderUnit is UnitOfMeasure
    preferredSupplier is optional String(1, 100)
  }

  // Events: StockReceived, StockConsumed, StockAdjusted,
  //         ReorderThresholdSet, PurchaseOrderCreated

  state TrackedItem of InventoryItem.InventoryItemStateData

  handler InventoryItemHandler is {
    on command ReceiveStock {
      morph entity Inventory.InventoryItem to state
        Inventory.InventoryItem.TrackedItem
        with command ReceiveStock
      tell event StockReceived to
        entity Inventory.InventoryItem
    }
    on command ConsumeStock {
      tell event StockConsumed to
        entity Inventory.InventoryItem
    }
    on command AdjustStock {
      tell event StockAdjusted to
        entity Inventory.InventoryItem
    }
    on command SetReorderThreshold {
      tell event ReorderThresholdSet to
        entity Inventory.InventoryItem
    }
    on command CreatePurchaseOrder {
      tell event PurchaseOrderCreated to
        entity Inventory.InventoryItem
    }
  }
}
```

Note that `ReceiveStock` uses `morph` — this is where an
inventory item first enters the system. Subsequent commands use
the standard `tell` pattern.

The `StockConsumed` event includes a `remainingStockLevel`
field, enabling downstream systems (like the Reporting context's
`InventoryReport` projector) to track stock levels without
querying the entity directly.

## Repository

```riddl
repository InventoryItemRepository is {
  schema InventoryItemData is relational
    of items as InventoryItem
    index on field InventoryItem.inventoryItemId
    index on field InventoryItem.inventoryItemStatus
}
```

The index on `inventoryItemStatus` enables quick queries for
low-stock and out-of-stock items.

## Adaptor: FromKitchen

The most interesting part of the Inventory context is its
cross-context integration with the Kitchen:

```riddl
adaptor FromKitchen from context Restaurant.Kitchen is {
  handler KitchenConsumptionIntake is {
    on event Restaurant.Kitchen.KitchenTicket.PreparationStarted {
      prompt "Consume stock for items being prepared"
    }
  }
} with {
  briefly "Kitchen adaptor"
  described by {
    | Receives preparation events from the kitchen to
    | automatically track stock consumption.
  }
}
```

When the Kitchen starts preparing a ticket
(`PreparationStarted` event), the Inventory context
automatically issues `ConsumeStock` commands for the ingredients
required. No manual tracking needed — stock consumption follows
directly from kitchen activity.

This is a powerful example of cross-context integration via
events. The Kitchen doesn't know about inventory. It just
prepares food and emits events. Inventory reacts to those
events to keep stock levels accurate.

## Design Decisions

**Why automatic consumption from Kitchen events?** Manual
stock tracking is error-prone and labor-intensive. By
listening to `PreparationStarted` events and looking up the
recipe's ingredient list, the system can automatically deduct
the right quantities. Discrepancies are handled through the
`AdjustStock` command with explicit reasons.

**Why `Decimal(10, 2)` for quantities?** Inventory items are
measured in fractional quantities (2.5 pounds of brisket,
0.75 gallons of sauce). Using `Decimal` instead of `Natural`
supports precise tracking with proper unit handling.

**Cross-domain relationship:** This context is in the
BackOffice domain but listens to events from the Restaurant
domain's Kitchen context. This cross-domain integration is
exactly what adaptors are designed for — they bridge context
boundaries cleanly.

## Source

- [`InventoryContext.riddl`](https://github.com/ossuminc/riddl-models/tree/main/hospitality/food-service/reactive-bbq/backoffice/InventoryContext.riddl)
- [`inventory-types.riddl`](https://github.com/ossuminc/riddl-models/tree/main/hospitality/food-service/reactive-bbq/backoffice/inventory-types.riddl)
- [`InventoryItem.riddl`](https://github.com/ossuminc/riddl-models/tree/main/hospitality/food-service/reactive-bbq/backoffice/InventoryItem.riddl)
