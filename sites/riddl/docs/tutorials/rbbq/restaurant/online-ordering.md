---
title: "Online Ordering Context"
description: "Online menu browsing, cart management, and checkout"
---

<!-- riddl-domain-prelude
context Kitchen is {
  command ReceiveTicket is { kitchenTicketId: String(1,50) }
}
-->

<!-- riddl-prelude
type OnlineOrderId is Id(OnlineOrder)
type CustomerId is UUID
record StoredOnlineOrder is { onlineOrderId: OnlineOrderId }
event MenuBrowsed is { onlineOrderId: OnlineOrderId }
event ItemAddedToCart is { onlineOrderId: OnlineOrderId }
event AddToCartRejected is { onlineOrderId: OnlineOrderId, rejectionReason: String(1,500) }
type OnlineOrderEvent is MenuBrowsed | ItemAddedToCart | AddToCartRejected
entity OnlineOrder is { ??? }
repository OnlineOrderRepository is { ??? }
command PersistItemAddedToCart is { onlineOrderId: OnlineOrderId }
-->

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

<!-- riddl: in-context no-prelude=OnlineOrderId,CustomerId -->
```riddl
type OnlineOrderId is Id(OnlineOrder)

type CustomerId is UUID
```

Note the 9-value `OnlineOrderStatus` enumeration — online orders
have more states than dine-in orders because they include
fulfillment tracking.

## Entity: OnlineOrder

The `OnlineOrder` entity has a 6-command lifecycle:

<!-- riddl: in-context no-prelude=OnlineOrder,MenuBrowsed,ItemAddedToCart,AddToCartRejected,OnlineOrderCommand,OnlineOrderEvent -->
```riddl
event-sourced entity OnlineOrder as flow is {

  // An event-sourced entity OWNS the commands and events that change it, so
  // they are declared INSIDE it, and every command names the event it yields.
  command BrowseMenu yields event MenuBrowsed is { onlineOrderId: OnlineOrderId }
  command AddToCart yields event ItemAddedToCart is { onlineOrderId: OnlineOrderId }

  event MenuBrowsed is { onlineOrderId: OnlineOrderId }
  event ItemAddedToCart is { onlineOrderId: OnlineOrderId }
  event AddToCartRejected is { onlineOrderId: OnlineOrderId, rejectionReason: String(1,500) }

  record OnlineOrderData is { onlineOrderId: OnlineOrderId }

  // Lifecycle phases are named STATES, not a status field: each state
  // declares the commands it accepts, so the compiler knows the machine.
  initial state Browsing of record OnlineOrderData is {
    handler BrowsingHandler is {
      on cmd: command AddToCart is {
        yield event ItemAddedToCart(onlineOrderId = cmd.onlineOrderId)
      }
      // `set` and `morph` may appear ONLY in an `on event` clause here:
      // replay has to re-apply exactly the same change.
      on evt: event ItemAddedToCart is {
        morph entity OnlineOrder to state FulfillmentChosen
          with record OnlineOrderData(onlineOrderId = evt.onlineOrderId)
      }
    }
  }

  state FulfillmentChosen of record OnlineOrderData is {
    handler FulfillmentChosenHandler is {
      // A command this state does not accept is refused -- and the refusal
      // is PUBLISHED before it is raised, so the attempt is recorded.
      on cmd: command AddToCart is {
        send event AddToCartRejected(onlineOrderId = cmd.onlineOrderId,
          rejectionReason = "OnlineOrder does not accept AddToCart in this state")
          to outlet OnlineOrderEvents
        error "OnlineOrder does not accept AddToCart in this state"
      }
    }
  }

  // A processor receives on its OWN inlet and publishes on its OWN outlet,
  // and a portlet's type must ADMIT everything that travels on it.
  type OnlineOrderCommand is BrowseMenu | AddToCart
  type OnlineOrderEvent is MenuBrowsed | ItemAddedToCart | AddToCartRejected

  inlet OnlineOrderCommands is type OnlineOrderCommand
  outlet OnlineOrderEvents is type OnlineOrderEvent
}
```

Note that `SelectFulfillment` uses `optional DeliveryAddress` —
the address is only required for delivery fulfillment, not
pickup. The `optional` keyword in RIDDL makes this explicit in
the model.

## Repository

<!-- riddl: in-context no-prelude=OnlineOrderRepository,StoredOnlineOrder,PersistItemAddedToCart -->
```riddl
repository OnlineOrderRepository as flow is {
  inlet OnlineOrderRepositoryFromOnlineOrder is type OnlineOrderEvent
  outlet OnlineOrderRepositoryResponses is type OnlineOrderEvent

  record StoredOnlineOrder is { onlineOrderId: OnlineOrderId }

  // A repository that answers queries and declares NO index at all is a
  // sequential scan by construction, and draws a warning saying so.
  schema OnlineOrderSchema is relational
    of rows as type StoredOnlineOrder
      index on field StoredOnlineOrder.onlineOrderId

  command PersistItemAddedToCart is { onlineOrderId: OnlineOrderId }

  handler OnlineOrderPersistence is {
    on command PersistItemAddedToCart is {
      do "update the stored onlineOrder row for this onlineOrderId"
    }
    // An inlet admitting an alternation needs a clause that receives it.
    // Handling each member is not enough -- say what ARRIVING means.
    on other is {
      do "persist whatever else arrives on this inlet"
    }
  }
}
```

The index on `customerId` supports order history lookups — the
online customer mentioned "they have all of that stuff on file
already."

## Adaptors

Online Ordering has three outbound adaptors:

<!-- riddl: in-domain -->
```riddl
context OnlineOrdering is {
  // An adaptor is the translation seam at a context boundary: it is the only
  // place that knows the OTHER context's message shapes.
  adaptor ToKitchen to context Kitchen is {
    handler ToKitchenIntake is {
      on command Kitchen.ReceiveTicket is {
        do "turn a submitted online order into a kitchen ticket"
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
