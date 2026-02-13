---
title: "Supply Chain Context"
description: "Vendor management and bulk ordering for the restaurant chain"
---

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

```riddl
type PurchaseOrderId is Id(SupplyChain.PurchaseOrder) with {
  briefly "Purchase order identifier"
  described by "Unique identifier for a purchase order."
}

type VendorId is UUID with {
  briefly "Vendor identifier"
  described by "Unique identifier for a vendor."
}

type PurchaseOrderStatus is any of {
  PoDraft,
  PoSubmitted,
  PoApproved,
  PoShipped,
  PoReceived,
  PoDisputed
} with {
  briefly "Purchase order status"
  described by "Current status of a purchase order."
}

type OrderLineItem is {
  lineItemName is String(1, 200)
  lineItemQuantity is Decimal(10, 2)
  lineItemUnit is String(1, 20)
  lineItemUnitPrice is Decimal(10, 2)
} with {
  briefly "Order line item"
  described by "A single item in a purchase order."
}
```

Note the `PoDisputed` status — if a shipment has quality
issues, the purchase order can be disputed rather than simply
accepted.

## Entity: PurchaseOrder

The `PurchaseOrder` entity has a 5-command lifecycle:

```riddl
entity PurchaseOrder is {

  command CreateBulkOrder is {
    purchaseOrderId is PurchaseOrderId
    vendorId is VendorId
    vendorName is String(1, 200)
    orderLineItems is many OrderLineItem
    requestedDeliveryDate is Date
  }

  command ApproveOrder is {
    purchaseOrderId is PurchaseOrderId
    approvedAt is TimeStamp
  }

  command ShipOrder is {
    purchaseOrderId is PurchaseOrderId
    shippedAt is TimeStamp
    trackingNumber is optional String(1, 100)
  }

  command ReceiveShipment is {
    purchaseOrderId is PurchaseOrderId
    receivedAt is TimeStamp
    receivedCondition is String(1, 200)
  }

  command ReportIssue is {
    purchaseOrderId is PurchaseOrderId
    purchaseOrderIssueType is String(1, 50)
    purchaseOrderIssueDescription is String(1, 1000)
    issueReportedAt is TimeStamp
  }

  // Events: BulkOrderCreated, OrderApproved, OrderShipped,
  //         ShipmentReceived, IssueReported

  state ActivePurchaseOrder of PurchaseOrder.PurchaseOrderStateData

  handler PurchaseOrderHandler is {
    on command CreateBulkOrder {
      morph entity SupplyChain.PurchaseOrder to state
        SupplyChain.PurchaseOrder.ActivePurchaseOrder
        with command CreateBulkOrder
      tell event BulkOrderCreated to
        entity SupplyChain.PurchaseOrder
    }
    on command ApproveOrder {
      tell event OrderApproved to
        entity SupplyChain.PurchaseOrder
    }
    on command ShipOrder {
      tell event OrderShipped to
        entity SupplyChain.PurchaseOrder
    }
    on command ReceiveShipment {
      tell event ShipmentReceived to
        entity SupplyChain.PurchaseOrder
    }
    on command ReportIssue {
      tell event IssueReported to
        entity SupplyChain.PurchaseOrder
    }
  }
}
```

The lifecycle: **Create → Approve → Ship → Receive → (optional)
Report Issue**.

The `ReportIssue` command can trigger a follow-up that
changes the order status to `PoDisputed`, initiating a
resolution process with the vendor.

## Repository

```riddl
repository PurchaseOrderRepository is {
  schema PurchaseOrderData is relational
    of purchaseOrders as PurchaseOrder
    index on field PurchaseOrder.purchaseOrderId
    index on field PurchaseOrder.vendorId
    index on field PurchaseOrder.purchaseOrderStatus
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
