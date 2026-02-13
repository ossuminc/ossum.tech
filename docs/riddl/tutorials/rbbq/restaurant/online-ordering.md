---
title: "Online Ordering Context"
description: "Online menu browsing, cart management, and checkout"
---

# Online Ordering Context

The Online Ordering context manages the online ordering experience
including menu browsing, cart management, fulfillment selection
(pickup or delivery), and checkout. It is deliberately decoupled
from the Delivery context so electronic menus can be developed
independently.

## Purpose

Online customers interact with the website or mobile app to browse
the menu, add items to a cart, choose pickup or delivery, and pay.
This context handles everything up to and including payment. If the
customer chose delivery, the order is handed off to the Delivery
context via an adaptor.

## Interview Connection

From the [Online Customer's interview](../personas/online-customer.md):

> "Their website and app aren't always working. Or if it is
> working it can be really slow."

> "When it doesn't work at all, I usually just don't bother.
> When that happens I will usually just order from the other
> place down the street."

Isolating online ordering in its own context means it can be
deployed, scaled, and maintained independently from the
restaurant's dine-in systems. A kitchen outage doesn't crash the
online menu.

## Types

```riddl
type OnlineOrderId is Id(OnlineOrdering.OnlineOrder) with {
  briefly "Online order identifier"
  described by "Unique identifier for an online order."
}

type CustomerId is UUID with {
  briefly "Customer identifier"
  described by "Unique identifier for the online customer."
}

type FulfillmentType is any of {
  PickupFulfillment,
  DeliveryFulfillment
} with {
  briefly "Fulfillment type"
  described by "Whether the order is for pickup or delivery."
}

type OnlineOrderStatus is any of {
  Browsing,
  CartReady,
  FulfillmentChosen,
  OnlineSubmitted,
  OnlinePaid,
  OnlineInPreparation,
  ReadyForPickup,
  OutForDelivery,
  OnlineCompleted
} with {
  briefly "Online order status"
  described by "Current status of an online order."
}

type CartItem is {
  cartMenuItemId is String(1, 50)
  cartItemName is String(1, 200)
  cartItemPrice is Decimal(8, 2)
  cartItemQuantity is Natural
  cartItemNotes is optional String(1, 500)
} with {
  briefly "Cart item"
  described by "An item in the online shopping cart."
}

type DeliveryAddress is {
  streetAddress is String(1, 200)
  deliveryCity is String(1, 100)
  deliveryState is String(2, 2)
  deliveryZipCode is String(5, 10)
  deliveryInstructions is optional String(1, 500)
} with {
  briefly "Delivery address"
  described by "Address for delivery fulfillment."
}
```

Note the 9-value `OnlineOrderStatus` enumeration — online orders
have more states than dine-in orders because they include
fulfillment tracking.

## Entity: OnlineOrder

The `OnlineOrder` entity has a 6-command lifecycle:

```riddl
entity OnlineOrder is {

  command BrowseMenu is {
    onlineOrderId is OnlineOrderId
    customerId is CustomerId
    browsedAt is TimeStamp
  }

  command AddToCart is {
    onlineOrderId is OnlineOrderId
    cartItem is CartItem
  }

  command RemoveFromCart is {
    onlineOrderId is OnlineOrderId
    removedCartItemId is String(1, 50)
  }

  command SelectFulfillment is {
    onlineOrderId is OnlineOrderId
    fulfillmentType is FulfillmentType
    deliveryAddress is optional DeliveryAddress
    requestedTime is optional TimeStamp
  }

  command SubmitOnlineOrder is {
    onlineOrderId is OnlineOrderId
    onlineSubmittedAt is TimeStamp
  }

  command ProcessOnlinePayment is {
    onlineOrderId is OnlineOrderId
    onlinePayment is OnlinePaymentInfo
  }

  // Events: MenuBrowsed, ItemAddedToCart, ItemRemovedFromCart,
  //         FulfillmentSelected, OnlineOrderSubmitted,
  //         OnlinePaymentProcessed

  state ActiveOnlineOrder of OnlineOrder.OnlineOrderStateData

  handler OnlineOrderHandler is {
    on command BrowseMenu {
      morph entity OnlineOrdering.OnlineOrder to state
        OnlineOrdering.OnlineOrder.ActiveOnlineOrder
        with command BrowseMenu
      tell event MenuBrowsed to
        entity OnlineOrdering.OnlineOrder
    }
    on command AddToCart {
      tell event ItemAddedToCart to
        entity OnlineOrdering.OnlineOrder
    }
    on command RemoveFromCart {
      tell event ItemRemovedFromCart to
        entity OnlineOrdering.OnlineOrder
    }
    on command SelectFulfillment {
      tell event FulfillmentSelected to
        entity OnlineOrdering.OnlineOrder
    }
    on command SubmitOnlineOrder {
      tell event OnlineOrderSubmitted to
        entity OnlineOrdering.OnlineOrder
    }
    on command ProcessOnlinePayment {
      tell event OnlinePaymentProcessed to
        entity OnlineOrdering.OnlineOrder
    }
  }
}
```

Note that `SelectFulfillment` uses `optional DeliveryAddress` —
the address is only required for delivery fulfillment, not
pickup. The `optional` keyword in RIDDL makes this explicit in
the model.

## Repository

```riddl
repository OnlineOrderRepository is {
  schema OnlineOrderData is relational
    of onlineOrders as OnlineOrder
    index on field OnlineOrder.onlineOrderId
    index on field OnlineOrder.customerId
    index on field OnlineOrder.onlineOrderStatus
}
```

The index on `customerId` supports order history lookups — the
online customer mentioned "they have all of that stuff on file
already."

## Adaptors

Online Ordering has three outbound adaptors:

```riddl
adaptor ToKitchen to context Restaurant.Kitchen is {
  handler OnlineKitchenRouting is {
    on command Restaurant.Kitchen.KitchenTicket.ReceiveTicket {
      prompt "Convert submitted online order into kitchen ticket"
    }
  }
}

adaptor ToDelivery to context Restaurant.Delivery is {
  handler DeliveryRouting is {
    on command Restaurant.Delivery.DeliveryOrder.CreateDelivery {
      prompt "Create delivery when delivery fulfillment is selected"
    }
  }
} with {
  briefly "Delivery adaptor"
  described by {
    | Sends orders with delivery fulfillment to the
    | delivery context. This decoupling enables electronic
    | menus to operate independently of delivery.
  }
}

adaptor ToLoyalty to context Restaurant.Loyalty is {
  handler OnlineLoyaltyRouting is {
    on command Restaurant.Loyalty.LoyaltyAccount.AccruePoints {
      prompt "Send online payment event to loyalty for point accrual"
    }
  }
}
```

## Design Decisions

**Why decouple from Delivery?** The CEO wanted electronic menus.
The Head Chef wanted streamlined menu distribution. If online
ordering and delivery were a single context, you couldn't ship
the electronic menu without also completing the delivery
rewrite. Decoupling means the menu experience can launch first,
with delivery improvements following independently.

**Why `BrowseMenu` creates the entity?** The `morph` on
`BrowseMenu` creates the online order session. This captures
the browsing-to-purchase funnel in the event stream, enabling
analytics on cart abandonment and conversion rates.

**Why separate from FrontOfHouse?** Online and dine-in orders
have different types (`CartItem` vs `OrderLine`), different
flows (cart + fulfillment selection vs table + server), and
different scalability requirements. A busy Friday night at the
restaurant shouldn't slow down the website.

## Source

- [`OnlineOrderingContext.riddl`](https://github.com/ossuminc/riddl-models/tree/main/hospitality/food-service/reactive-bbq/restaurant/OnlineOrderingContext.riddl)
- [`online-types.riddl`](https://github.com/ossuminc/riddl-models/tree/main/hospitality/food-service/reactive-bbq/restaurant/online-types.riddl)
- [`OnlineOrder.riddl`](https://github.com/ossuminc/riddl-models/tree/main/hospitality/food-service/reactive-bbq/restaurant/OnlineOrder.riddl)
