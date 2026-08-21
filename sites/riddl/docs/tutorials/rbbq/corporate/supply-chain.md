---
title: "Supply Chain Context"
description: "Vendor management and bulk ordering for the restaurant chain"
---


<!-- riddl-prelude
type PurchaseOrderId is Id(PurchaseOrder)
type VendorId is UUID
record StoredPurchaseOrder is { purchaseOrderId: PurchaseOrderId }
event BulkOrderCreated is { purchaseOrderId: PurchaseOrderId }
event OrderApproved is { purchaseOrderId: PurchaseOrderId }
event ApproveOrderRejected is { purchaseOrderId: PurchaseOrderId, rejectionReason: String(1,500) }
type PurchaseOrderEvent is BulkOrderCreated | OrderApproved | ApproveOrderRejected
entity PurchaseOrder is { ??? }
repository PurchaseOrderRepository is { ??? }
-->

# Supply Chain Context

The Supply Chain context manages vendor relationships and bulk
ordering for the restaurant chain. It coordinates with the
Inventory context to ensure adequate stock across locations.

## Purpose

A 500-location restaurant chain can't have each location ordering
independently — bulk purchasing saves money and ensures
consistency. The Supply Chain context handles the procurement
lifecycle from order creation through approval, shipping,
receipt, and issue reporting.

## Interview Connection

From the [Head Chef's interview](../personas/head-chef.md):

> "I source local ingredients required to prepare our menu items."

The Head Chef works at the corporate level to standardize
ingredients and manage supplier relationships. The Supply Chain
context formalizes this process with tracked purchase orders.

## Types

<!-- riddl: in-context no-prelude=PurchaseOrderId,VendorId -->
```riddl
type PurchaseOrderId is Id(PurchaseOrder)

type VendorId is UUID
```

Note the `PoDisputed` status — if a shipment has quality
issues, the purchase order can be disputed rather than simply
accepted.

## Entity: PurchaseOrder

The `PurchaseOrder` entity has a 5-command lifecycle:

<!-- riddl: in-context no-prelude=PurchaseOrder,BulkOrderCreated,OrderApproved,ApproveOrderRejected,PurchaseOrderCommand,PurchaseOrderEvent -->
```riddl
event-sourced entity PurchaseOrder as flow is {

  // An event-sourced entity OWNS the commands and events that change it, so
  // they are declared INSIDE it, and every command names the event it yields.
  command CreateBulkOrder yields event BulkOrderCreated is { purchaseOrderId: PurchaseOrderId }
  command ApproveOrder yields event OrderApproved is { purchaseOrderId: PurchaseOrderId }

  event BulkOrderCreated is { purchaseOrderId: PurchaseOrderId }
  event OrderApproved is { purchaseOrderId: PurchaseOrderId }
  event ApproveOrderRejected is { purchaseOrderId: PurchaseOrderId, rejectionReason: String(1,500) }

  record PurchaseOrderData is { purchaseOrderId: PurchaseOrderId }

  // Lifecycle phases are named STATES, not a status field: each state
  // declares the commands it accepts, so the compiler knows the machine.
  initial state ActivePurchaseOrder of record PurchaseOrderData is {
    handler ActivePurchaseOrderHandler is {
      on cmd: command ApproveOrder is {
        yield event OrderApproved(purchaseOrderId = cmd.purchaseOrderId)
      }
      // `set` and `morph` may appear ONLY in an `on event` clause here:
      // replay has to re-apply exactly the same change.
      on evt: event OrderApproved is {
        morph entity PurchaseOrder to state Approved
          with record PurchaseOrderData(purchaseOrderId = evt.purchaseOrderId)
      }
    }
  }

  state Approved of record PurchaseOrderData is {
    handler ApprovedHandler is {
      // A command this state does not accept is refused -- and the refusal
      // is PUBLISHED before it is raised, so the attempt is recorded.
      on cmd: command ApproveOrder is {
        send event ApproveOrderRejected(purchaseOrderId = cmd.purchaseOrderId,
          rejectionReason = "PurchaseOrder does not accept ApproveOrder in this state")
          to outlet PurchaseOrderEvents
        error "PurchaseOrder does not accept ApproveOrder in this state"
      }
    }
  }

  // A processor receives on its OWN inlet and publishes on its OWN outlet,
  // and a portlet's type must ADMIT everything that travels on it.
  type PurchaseOrderCommand is CreateBulkOrder | ApproveOrder
  type PurchaseOrderEvent is BulkOrderCreated | OrderApproved | ApproveOrderRejected

  inlet PurchaseOrderCommands is type PurchaseOrderCommand
  outlet PurchaseOrderEvents is type PurchaseOrderEvent
}
```

The lifecycle: **Create → Approve → Ship → Receive → (optional)
Report Issue**.

The `ReportIssue` command can trigger a follow-up that
changes the order status to `PoDisputed`, initiating a
resolution process with the vendor.

## Repository

<!-- riddl: in-context no-prelude=PurchaseOrderRepository,StoredPurchaseOrder -->
```riddl
repository PurchaseOrderRepository as flow is {
  inlet PurchaseOrderRepositoryFromPurchaseOrder is type PurchaseOrderEvent
  outlet PurchaseOrderRepositoryResponses is type PurchaseOrderEvent

  record StoredPurchaseOrder is { purchaseOrderId: PurchaseOrderId }

  // A repository that answers queries and declares NO index at all is a
  // sequential scan by construction, and draws a warning saying so.
  schema PurchaseOrderSchema is relational
    of rows as type StoredPurchaseOrder
      index on field StoredPurchaseOrder.purchaseOrderId

  command PersistOrderApproved is { purchaseOrderId: PurchaseOrderId }

  handler PurchaseOrderPersistence is {
    on command PersistOrderApproved is {
      do "update the stored purchaseOrder row for this purchaseOrderId"
    }
  }
}
```

The index on `vendorId` supports vendor-centric views — how
many orders are outstanding with a specific vendor, what's the
order history, etc.

## Design Decisions

**Why no adaptor to Inventory?** When a shipment is received
at a restaurant location, the Inventory context's
`ReceiveStock` command is called directly by the receiving
clerk. The supply chain tracks the corporate-level purchase
order, while inventory tracks the location-level stock. These
are different levels of abstraction that don't need tight
coupling.

**Why `many OrderLineItem`?** Bulk purchase orders typically
contain multiple items — different cuts of meat, sauces,
packaging, etc. The `many` keyword models a collection of line
items within a single order.

## Source

- [`SupplyChainContext.riddl`](https://github.com/ossuminc/riddl-models/tree/main/hospitality/food-service/reactive-bbq/corporate/SupplyChainContext.riddl)
- [`supply-chain-types.riddl`](https://github.com/ossuminc/riddl-models/tree/main/hospitality/food-service/reactive-bbq/corporate/supply-chain-types.riddl)
- [`PurchaseOrder.riddl`](https://github.com/ossuminc/riddl-models/tree/main/hospitality/food-service/reactive-bbq/corporate/PurchaseOrder.riddl)
