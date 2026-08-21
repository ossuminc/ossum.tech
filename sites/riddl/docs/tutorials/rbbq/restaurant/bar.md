---
title: "Bar Context"
description: "Drink order management with push notifications"
---

<!-- riddl-domain-prelude
context FrontOfHouse is {
  event OrderSubmitted is { tableOrderId: String(1,50) }
}
-->

<!-- riddl-prelude
type DrinkOrderId is Id(DrinkOrder)
type DrinkName is String(1,100)
record StoredDrinkOrder is { drinkOrderId: DrinkOrderId }
event DrinkOrderReceived is { drinkOrderId: DrinkOrderId }
event DrinkPrepared is { drinkOrderId: DrinkOrderId }
event PrepareDrinkRejected is { drinkOrderId: DrinkOrderId, rejectionReason: String(1,500) }
type DrinkOrderEvent is DrinkOrderReceived | DrinkPrepared | PrepareDrinkRejected
entity DrinkOrder is { ??? }
repository DrinkOrderRepository is { ??? }
command PersistDrinkPrepared is { drinkOrderId: DrinkOrderId }
event ServerNotifiedDrinksReady is { drinkOrderId: DrinkOrderId }
-->

# Bar Context

The Bar context manages drink order preparation and server
notification. Its key innovation is push notifications when
drinks are ready — solving the "melting-ice problem" caused by
communication gaps between bartenders and servers.

## Purpose

When a server submits a table order, the Front of House context
routes the drink items to the Bar via the `ToBar` adaptor.
The bartender prepares the drinks, marks them ready, and a push
notification alerts the server to pick them up immediately.

## Interview Connection

This context was driven by the
[Bartender's interview](../personas/bartender.md):

> "Sometimes drink orders will sit for a really long time...
> the ice is melting and it can really ruin a good drink."

> "It would be nice if there was a way to let the server know
> that their order is ready."

The `NotifyServerDrinksReady` command and its
`ServerNotifiedDrinksReady` event directly solve this problem.

## Types

<!-- riddl: in-context no-prelude=DrinkOrderId,DrinkName -->
```riddl
type DrinkOrderId is Id(DrinkOrder)

type DrinkName is String(1,100)
```

## Entity: DrinkOrder

The `DrinkOrder` entity has a 5-command lifecycle:

<!-- riddl: in-context no-prelude=DrinkOrder,DrinkOrderReceived,DrinkPrepared,PrepareDrinkRejected,DrinkOrderCommand,DrinkOrderEvent -->
```riddl
event-sourced entity DrinkOrder as flow is {

  // An event-sourced entity OWNS the commands and events that change it, so
  // they are declared INSIDE it, and every command names the event it yields.
  command ReceiveDrinkOrder yields event DrinkOrderReceived is { drinkOrderId: DrinkOrderId }
  command PrepareDrink yields event DrinkPrepared is { drinkOrderId: DrinkOrderId }

  event DrinkOrderReceived is { drinkOrderId: DrinkOrderId }
  event DrinkPrepared is { drinkOrderId: DrinkOrderId }
  event PrepareDrinkRejected is { drinkOrderId: DrinkOrderId, rejectionReason: String(1,500) }

  record DrinkOrderData is { drinkOrderId: DrinkOrderId }

  // Lifecycle phases are named STATES, not a status field: each state
  // declares the commands it accepts, so the compiler knows the machine.
  initial state Received of record DrinkOrderData is {
    handler ReceivedHandler is {
      on cmd: command PrepareDrink is {
        yield event DrinkPrepared(drinkOrderId = cmd.drinkOrderId)
      }
      // `set` and `morph` may appear ONLY in an `on event` clause here:
      // replay has to re-apply exactly the same change.
      on evt: event DrinkPrepared is {
        morph entity DrinkOrder to state InPreparation
          with record DrinkOrderData(drinkOrderId = evt.drinkOrderId)
      }
    }
  }

  state InPreparation of record DrinkOrderData is {
    handler InPreparationHandler is {
      // A command this state does not accept is refused -- and the refusal
      // is PUBLISHED before it is raised, so the attempt is recorded.
      on cmd: command PrepareDrink is {
        send event PrepareDrinkRejected(drinkOrderId = cmd.drinkOrderId,
          rejectionReason = "DrinkOrder does not accept PrepareDrink in this state")
          to outlet DrinkOrderEvents
        error "DrinkOrder does not accept PrepareDrink in this state"
      }
    }
  }

  // A processor receives on its OWN inlet and publishes on its OWN outlet,
  // and a portlet's type must ADMIT everything that travels on it.
  type DrinkOrderCommand is ReceiveDrinkOrder | PrepareDrink
  type DrinkOrderEvent is DrinkOrderReceived | DrinkPrepared | PrepareDrinkRejected

  inlet DrinkOrderCommands is type DrinkOrderCommand
  outlet DrinkOrderEvents is type DrinkOrderEvent
}
```

The lifecycle: **Receive → Prepare → Mark Ready → Notify Server
→ Complete**. The key event is `ServerNotifiedDrinksReady`:

<!-- riddl: in-context no-prelude=ServerNotifiedDrinksReady -->
```riddl
// The Bartender interview asked for a push, not a glance at the pass. The
// event carries who to notify, so the notification is derivable from it.
event ServerNotifiedDrinksReady is {
  drinkOrderId: DrinkOrderId
  notifiedServer: String(1,100)
  notifiedAt: TimeStamp
}
```

## Repository

<!-- riddl: in-context no-prelude=DrinkOrderRepository,StoredDrinkOrder,PersistDrinkPrepared -->
```riddl
repository DrinkOrderRepository as flow is {
  inlet DrinkOrderRepositoryFromDrinkOrder is type DrinkOrderEvent
  outlet DrinkOrderRepositoryResponses is type DrinkOrderEvent

  record StoredDrinkOrder is { drinkOrderId: DrinkOrderId }

  // A repository that answers queries and declares NO index at all is a
  // sequential scan by construction, and draws a warning saying so.
  schema DrinkOrderSchema is relational
    of rows as type StoredDrinkOrder
      index on field StoredDrinkOrder.drinkOrderId

  command PersistDrinkPrepared is { drinkOrderId: DrinkOrderId }

  handler DrinkOrderPersistence is {
    on command PersistDrinkPrepared is {
      do "update the stored drinkOrder row for this drinkOrderId"
    }
  }
}
```

## Adaptor

Bar has a single inbound adaptor from Front of House:

<!-- riddl: in-domain -->
```riddl
context Bar is {
  // An adaptor is the translation seam at a context boundary: it is the only
  // place that knows the OTHER context's message shapes.
  adaptor FromFrontOfHouse from context FrontOfHouse is {
    handler FromFrontOfHouseIntake is {
      on event FrontOfHouse.OrderSubmitted is {
        do "convert the drinks on a submitted table order into a drink order"
      }
      // Every adaptor handler must say what it does with what it does not
      // recognise. Silence is not an option in 2.0.
      on other is {
        error "Unexpected message from FrontOfHouse"
      }
    }
  }
}
```

This adaptor listens for `OrderSubmitted` events from table
orders and extracts the drink items to create a `DrinkOrder`.
The food items go to the Kitchen via a separate adaptor — Front
of House splits the order into its component parts.

## Design Decisions

**Why is Bar separate from Kitchen?** Bar and kitchen have
fundamentally different workflows. The bartender works alone,
makes drinks immediately, and needs to notify servers. The
kitchen has multiple stations, a ticket queue, and chef
approval. Combining them would create an awkward hybrid that
serves neither workflow well.

**Why is Bar separate from Front of House?** The Bar has its own
entity (DrinkOrder), its own lifecycle, and its own
communication pattern (push notifications). Embedding this in
Front of House would mix ordering concerns with preparation
concerns.

**The melting-ice problem** — Without push notifications, drinks
sit on the counter while servers are busy with customers. By the
time someone notices, the ice has melted and the drink quality
has degraded. The `NotifyServerDrinksReady` command triggers a
notification to the server's device, ensuring prompt pickup.

## Source

- [`BarContext.riddl`](https://github.com/ossuminc/riddl-models/tree/main/hospitality/food-service/reactive-bbq/restaurant/BarContext.riddl)
- [`bar-types.riddl`](https://github.com/ossuminc/riddl-models/tree/main/hospitality/food-service/reactive-bbq/restaurant/bar-types.riddl)
- [`DrinkOrder.riddl`](https://github.com/ossuminc/riddl-models/tree/main/hospitality/food-service/reactive-bbq/restaurant/DrinkOrder.riddl)
