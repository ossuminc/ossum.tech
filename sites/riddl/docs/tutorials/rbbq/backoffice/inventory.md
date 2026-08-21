---
title: "Inventory Context"
description: "Stock level tracking with automated kitchen integration"
---

<!-- riddl-domain-prelude
context Kitchen is {
  event TicketApproved is { kitchenTicketId: String(1,50) }
}
-->

<!-- riddl-prelude
type InventoryItemId is Id(InventoryItem)
type StockQuantity is Natural
record StoredInventoryItem is { inventoryItemId: InventoryItemId }
event StockReceived is { inventoryItemId: InventoryItemId }
event StockConsumed is { inventoryItemId: InventoryItemId }
event ConsumeStockRejected is { inventoryItemId: InventoryItemId, rejectionReason: String(1,500) }
type InventoryItemEvent is StockReceived | StockConsumed | ConsumeStockRejected
entity InventoryItem is { ??? }
repository InventoryItemRepository is { ??? }
command PersistStockConsumed is { inventoryItemId: InventoryItemId }
-->

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

<!-- riddl: in-context no-prelude=InventoryItemId,StockQuantity -->
```riddl
type InventoryItemId is Id(InventoryItem)

type StockQuantity is Natural
```

The `StockAdjustmentReason` enumeration captures why stock was
manually adjusted — essential for loss tracking and audit
compliance.

## Entity: InventoryItem

The `InventoryItem` entity has a 5-command lifecycle:

<!-- riddl: in-context no-prelude=InventoryItem,StockReceived,StockConsumed,ConsumeStockRejected,InventoryItemCommand,InventoryItemEvent -->
```riddl
event-sourced entity InventoryItem as flow is {

  // An event-sourced entity OWNS the commands and events that change it, so
  // they are declared INSIDE it, and every command names the event it yields.
  command ReceiveStock yields event StockReceived is { inventoryItemId: InventoryItemId }
  command ConsumeStock yields event StockConsumed is { inventoryItemId: InventoryItemId }

  event StockReceived is { inventoryItemId: InventoryItemId }
  event StockConsumed is { inventoryItemId: InventoryItemId }
  event ConsumeStockRejected is { inventoryItemId: InventoryItemId, rejectionReason: String(1,500) }

  record InventoryItemData is { inventoryItemId: InventoryItemId }

  // Lifecycle phases are named STATES, not a status field: each state
  // declares the commands it accepts, so the compiler knows the machine.
  initial state TrackedItem of record InventoryItemData is {
    handler TrackedItemHandler is {
      on cmd: command ConsumeStock is {
        yield event StockConsumed(inventoryItemId = cmd.inventoryItemId)
      }
      // `set` and `morph` may appear ONLY in an `on event` clause here:
      // replay has to re-apply exactly the same change.
      on evt: event StockConsumed is {
        morph entity InventoryItem to state Depleted
          with record InventoryItemData(inventoryItemId = evt.inventoryItemId)
      }
    }
  }

  state Depleted of record InventoryItemData is {
    handler DepletedHandler is {
      // A command this state does not accept is refused -- and the refusal
      // is PUBLISHED before it is raised, so the attempt is recorded.
      on cmd: command ConsumeStock is {
        send event ConsumeStockRejected(inventoryItemId = cmd.inventoryItemId,
          rejectionReason = "InventoryItem does not accept ConsumeStock in this state")
          to outlet InventoryItemEvents
        error "InventoryItem does not accept ConsumeStock in this state"
      }
    }
  }

  // A processor receives on its OWN inlet and publishes on its OWN outlet,
  // and a portlet's type must ADMIT everything that travels on it.
  type InventoryItemCommand is ReceiveStock | ConsumeStock
  type InventoryItemEvent is StockReceived | StockConsumed | ConsumeStockRejected

  inlet InventoryItemCommands is type InventoryItemCommand
  outlet InventoryItemEvents is type InventoryItemEvent
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

<!-- riddl: in-context no-prelude=InventoryItemRepository,StoredInventoryItem,PersistStockConsumed -->
```riddl
repository InventoryItemRepository as flow is {
  inlet InventoryItemRepositoryFromInventoryItem is type InventoryItemEvent
  outlet InventoryItemRepositoryResponses is type InventoryItemEvent

  record StoredInventoryItem is { inventoryItemId: InventoryItemId }

  // A repository that answers queries and declares NO index at all is a
  // sequential scan by construction, and draws a warning saying so.
  schema InventoryItemSchema is relational
    of rows as type StoredInventoryItem
      index on field StoredInventoryItem.inventoryItemId

  command PersistStockConsumed is { inventoryItemId: InventoryItemId }

  handler InventoryItemPersistence is {
    on command PersistStockConsumed is {
      do "update the stored inventoryItem row for this inventoryItemId"
    }
  }
}
```

The index on `inventoryItemStatus` enables quick queries for
low-stock and out-of-stock items.

## Adaptor: FromKitchen

The most interesting part of the Inventory context is its
cross-context integration with the Kitchen:

<!-- riddl: in-domain -->
```riddl
context Inventory is {
  // An adaptor is the translation seam at a context boundary: it is the only
  // place that knows the OTHER context's message shapes.
  adaptor FromKitchen from context Kitchen is {
    handler FromKitchenIntake is {
      on event Kitchen.TicketApproved is {
        do "decrement stock for the items the approved ticket consumed"
      }
      // Every adaptor handler must say what it does with what it does not
      // recognise. Silence is not an option in 2.0.
      on other is {
        error "Unexpected message from Kitchen"
      }
    }
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
