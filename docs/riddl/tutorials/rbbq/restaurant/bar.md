---
title: "Bar Context"
description: "Drink order management with push notifications"
---

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

```riddl
type DrinkOrderId is Id(Bar.DrinkOrder) with {
  briefly "Drink order identifier"
  described by "Unique identifier for a drink order."
}

type DrinkOrderStatus is any of {
  DrinkReceived,
  DrinkInPreparation,
  DrinkReady,
  DrinkDelivered,
  DrinkCompleted
} with {
  briefly "Drink order status"
  described by "Current status of a drink order."
}

type DrinkItem is {
  drinkName is String(1, 200)
  drinkQuantity is Natural
  drinkNotes is optional String(1, 500)
} with {
  briefly "Drink item"
  described by "A single drink in an order."
}
```

## Entity: DrinkOrder

The `DrinkOrder` entity has a 5-command lifecycle:

```riddl
entity DrinkOrder is {

  command ReceiveDrinkOrder is {
    drinkOrderId is DrinkOrderId
    sourceOrderId is String(1, 50)
    drinkTableNumber is Natural
    drinkItems is many DrinkItem
    drinkReceivedAt is TimeStamp
  }

  command PrepareDrink is {
    drinkOrderId is DrinkOrderId
    drinkPreparationStartedAt is TimeStamp
  }

  command MarkDrinkReady is {
    drinkOrderId is DrinkOrderId
    drinkReadyAt is TimeStamp
  }

  command NotifyServerDrinksReady is {
    drinkOrderId is DrinkOrderId
    serverNotifiedAt is TimeStamp
  }

  command CompleteDrinkOrder is {
    drinkOrderId is DrinkOrderId
    drinkCompletedAt is TimeStamp
  }

  // Events: DrinkOrderReceived, DrinkPrepared, DrinkMarkedReady,
  //         ServerNotifiedDrinksReady, DrinkOrderCompleted

  state ActiveDrinkOrder of DrinkOrder.DrinkOrderStateData

  handler DrinkOrderHandler is {
    on command ReceiveDrinkOrder {
      morph entity Bar.DrinkOrder to state
        Bar.DrinkOrder.ActiveDrinkOrder
        with command ReceiveDrinkOrder
      tell event DrinkOrderReceived to
        entity Bar.DrinkOrder
    }
    on command PrepareDrink {
      tell event DrinkPrepared to
        entity Bar.DrinkOrder
    }
    on command MarkDrinkReady {
      tell event DrinkMarkedReady to
        entity Bar.DrinkOrder
    }
    on command NotifyServerDrinksReady {
      tell event ServerNotifiedDrinksReady to
        entity Bar.DrinkOrder
    }
    on command CompleteDrinkOrder {
      tell event DrinkOrderCompleted to
        entity Bar.DrinkOrder
    }
  }
}
```

The lifecycle: **Receive → Prepare → Mark Ready → Notify Server
→ Complete**. The key event is `ServerNotifiedDrinksReady`:

```riddl
event ServerNotifiedDrinksReady is {
  drinkOrderId is DrinkOrderId
  drinkTableNumber is Natural
  serverNotifiedAt is TimeStamp
} with {
  briefly "Server notified drinks ready"
  described by {
    | Emitted when the server receives a push notification
    | that drinks are ready, solving the melting-ice problem.
  }
}
```

## Repository

```riddl
repository DrinkOrderRepository is {
  schema DrinkOrderData is relational
    of drinkOrders as DrinkOrder
    index on field DrinkOrder.drinkOrderId
    index on field DrinkOrder.drinkOrderStatus
}
```

## Adaptor

Bar has a single inbound adaptor from Front of House:

```riddl
adaptor FromFrontOfHouse from context Restaurant.FrontOfHouse is {
  handler DrinkIntake is {
    on event Restaurant.FrontOfHouse.TableOrder.OrderSubmitted {
      prompt "Extract drink items from submitted order and create drink order"
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
