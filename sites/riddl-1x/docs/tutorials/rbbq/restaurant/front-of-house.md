---
title: "Front of House Context"
description: "Reservations, table orders, and billing in the Restaurant domain"
---

# Front of House Context

The Front of House context manages the customer-facing operations
inside each restaurant — reservations, table seating, order
management, billing, and payment.

## Purpose

Every dine-in interaction flows through Front of House. When a
guest calls for a reservation, walks in, orders food and drinks,
and pays the bill, this context orchestrates it. It also serves as
the origin point for outbound messages to the Kitchen, Bar, and
Loyalty contexts.

## Interview Connection

This context was shaped by interviews with the
[Host](../personas/host.md) (reservations, seating),
[Server](../personas/server.md) (ordering, payment), and
[Online Customer](../personas/online-customer.md) (online
reservations). Key pain points addressed:

- The Host's reservation system was unresponsive and frequently
  crashed, forcing paper backups
- Servers contended for limited terminals during peak hours
- System failures caused cascading impacts across the restaurant

## Types

The context defines shared types for reservations, orders, and
payments:

```riddl
type ReservationId is Id(FrontOfHouse.Reservation) with {
  briefly "Reservation identifier"
  described by "Unique identifier for a reservation."
}

type TableOrderId is Id(FrontOfHouse.TableOrder) with {
  briefly "Table order identifier"
  described by "Unique identifier for a dine-in table order."
}

type TableNumber is Natural with {
  briefly "Table number"
  described by "Physical table number in the restaurant."
}

type PartySize is Natural with {
  briefly "Party size"
  described by "Number of guests in the party."
}

type ReservationStatus is any of {
  Requested,
  Confirmed,
  Seated,
  Completed,
  Cancelled,
  NoShow
} with {
  briefly "Reservation status"
  described by "Current status of a reservation."
}

type OrderStatus is any of {
  DraftStatus,
  SubmittedStatus,
  InPreparationStatus,
  ReadyToServeStatus,
  BillPresentedStatus,
  PaymentCompleteStatus,
  ClosedStatus
} with {
  briefly "Order status"
  described by "Current status of a table order."
}

type PaymentMethod is any of {
  Cash,
  CreditCard,
  DebitCard,
  MobilePayment,
  GiftCard
} with {
  briefly "Payment method"
  described by "Method used to pay for the order."
}
```

Notice the `Id()` type constructor — `ReservationId` is typed as
an identifier *for* the `Reservation` entity. This gives the
compiler enough information to enforce type safety across context
boundaries.

The context also defines record types for structured data:

```riddl
type MenuItemInfo is {
  itemCode is String(1, 50) with {
    briefly "Item code"
    described by "Identifier code for the menu item."
  }
  itemName is String(1, 200) with {
    briefly "Item name"
    described by "Display name of the menu item."
  }
  itemPrice is Decimal(8, 2) with {
    briefly "Price"
    described by "Price of the menu item."
  }
  itemCategory is String(1, 50) with {
    briefly "Category"
    described by "Category such as appetizer, entree, drink, dessert."
  }
} with {
  briefly "Menu item"
  described by "An item from the restaurant menu."
}

type OrderLine is {
  orderLineItem is MenuItemInfo with {
    briefly "Item"
    described by "The menu item ordered."
  }
  orderLineQuantity is Natural with {
    briefly "Quantity"
    described by "Number of this item ordered."
  }
  orderLineNotes is optional String(1, 500) with {
    briefly "Notes"
    described by "Special instructions for this item."
  }
} with {
  briefly "Order line"
  described by "A single line item in an order."
}

type PaymentInfo is {
  paymentMethod is PaymentMethod with {
    briefly "Method"
    described by "Payment method used."
  }
  paymentAmount is Decimal(10, 2) with {
    briefly "Amount"
    described by "Amount paid."
  }
  tipAmount is optional Decimal(8, 2) with {
    briefly "Tip"
    described by "Tip amount if applicable."
  }
  transactionRef is optional String(1, 100) with {
    briefly "Transaction reference"
    described by "External payment transaction reference."
  }
} with {
  briefly "Payment information"
  described by "Payment details for an order."
}
```

## Reservation Entity

The `Reservation` entity models the full lifecycle from request
through confirmation, seating, or cancellation:

```riddl
entity Reservation is {

  command MakeReservation is {
    reservationId is ReservationId
    guestName is GuestName
    guestPhone is GuestPhone
    partySize is PartySize
    reservationTime is TimeStamp
  }

  command ConfirmReservation is {
    reservationId is ReservationId
    confirmedTable is TableNumber
  }

  command CancelReservation is {
    reservationId is ReservationId
    cancellationReason is optional String(1, 500)
  }

  command SeatParty is {
    reservationId is ReservationId
    seatedTable is TableNumber
    seatedAt is TimeStamp
  }

  // Events mirror commands
  event ReservationMade is { ... }
  event ReservationConfirmed is { ... }
  event ReservationCancelled is { ... }
  event PartySeated is { ... }

  state ActiveReservation of Reservation.ReservationStateData

  handler ReservationHandler is {
    on command MakeReservation {
      morph entity FrontOfHouse.Reservation to state
        FrontOfHouse.Reservation.ActiveReservation
        with command MakeReservation
      tell event ReservationMade to
        entity FrontOfHouse.Reservation
    }
    on command ConfirmReservation {
      tell event ReservationConfirmed to
        entity FrontOfHouse.Reservation
    }
    on command CancelReservation {
      tell event ReservationCancelled to
        entity FrontOfHouse.Reservation
    }
    on command SeatParty {
      tell event PartySeated to
        entity FrontOfHouse.Reservation
    }
  }
}
```

The `morph` statement in `MakeReservation` creates the entity
instance, transitioning it from non-existence to the
`ActiveReservation` state. Subsequent commands use `tell` to emit
events that update the entity's state.

## TableOrder Entity

The `TableOrder` entity has a 7-command lifecycle covering the
full dine-in order flow:

| Command | What Happens |
|---------|-------------|
| `CreateOrder` | Server opens an order for a table |
| `AddItem` | Server adds a menu item |
| `RemoveItem` | Server removes a menu item |
| `SubmitOrder` | Order sent to kitchen and bar |
| `PresentBill` | Bill presented to the table |
| `ProcessPayment` | Payment collected |
| `CloseOrder` | Order finalized and closed |

The handler follows the same pattern — `morph` on creation,
`tell` for subsequent state transitions.

## Repositories

Two repositories persist the entity data:

```riddl
repository ReservationRepository is {
  schema ReservationData is relational
    of reservations as Reservation
    index on field Reservation.reservationId
    index on field Reservation.guestName
    index on field Reservation.reservationTime
}

repository TableOrderRepository is {
  schema TableOrderData is relational
    of orders as TableOrder
    index on field TableOrder.tableOrderId
    index on field TableOrder.tableNumber
}
```

The `schema` definition specifies storage as relational with
named indexes. The `index on field` clauses tell the system
which fields need fast lookup — essential for finding
reservations by guest name or time.

## Projector: ReservationBoard

The `ReservationBoard` projector provides a real-time read
model for the host's seating display, replacing the paper
backup system:

```riddl
projector ReservationBoard is {
  updates repository ReservationRepository

  record ReservationBoardEntry is {
    reservationId is ReservationId
    guestName is GuestName
    partySize is PartySize
    reservationTime is TimeStamp
    reservationStatus is ReservationStatus
    assignedTable is optional TableNumber
  }

  handler ReservationBoardHandler is {
    on event Reservation.ReservationMade {
      prompt "Add reservation to board"
    }
    on event Reservation.ReservationConfirmed {
      prompt "Update board entry to confirmed"
    }
    on event Reservation.ReservationCancelled {
      prompt "Remove cancelled reservation from board"
    }
    on event Reservation.PartySeated {
      prompt "Update board entry to seated"
    }
  }
}
```

This is a CQRS read model — it listens to reservation events
and projects them into a denormalized view optimized for the
host's display screen.

## Adaptors

Front of House has three outbound adaptors that route messages
to other contexts:

```riddl
adaptor ToKitchen to context Restaurant.Kitchen is {
  handler KitchenRouting is {
    on command Restaurant.Kitchen.KitchenTicket.ReceiveTicket {
      prompt "Route food items from submitted order to kitchen"
    }
  }
}

adaptor ToBar to context Restaurant.Bar is {
  handler BarRouting is {
    on command Restaurant.Bar.DrinkOrder.ReceiveDrinkOrder {
      prompt "Route drink items from submitted order to bar"
    }
  }
}

adaptor ToLoyalty to context Restaurant.Loyalty is {
  handler LoyaltyRouting is {
    on command Restaurant.Loyalty.LoyaltyAccount.AccruePoints {
      prompt "Send payment event to loyalty for point accrual"
    }
  }
}
```

When a table order is submitted, the `ToKitchen` adaptor extracts
the food items and creates a kitchen ticket, while the `ToBar`
adaptor extracts drink items and creates a drink order. When
payment is processed, the `ToLoyalty` adaptor triggers point
accrual.

## Design Decisions

**Why is Front of House separate from Kitchen and Bar?** These
are different bounded contexts with different ubiquitous
languages. A "ticket" in the kitchen is not the same concept as
an "order" at the table. Separating them means each context can
evolve independently — the kitchen display can be redesigned
without affecting table ordering.

**Why the ReservationBoard projector?** The Host's interview
revealed that when the reservation system crashes, they fall
back to paper. The projector provides a read-optimized view
that stays current through events. If the main entity processing
is slow, the board still shows the last known state.

## Source

- [`FrontOfHouseContext.riddl`](https://github.com/ossuminc/riddl-models/tree/main/hospitality/food-service/reactive-bbq/restaurant/FrontOfHouseContext.riddl)
- [`front-of-house-types.riddl`](https://github.com/ossuminc/riddl-models/tree/main/hospitality/food-service/reactive-bbq/restaurant/front-of-house-types.riddl)
- [`Reservation.riddl`](https://github.com/ossuminc/riddl-models/tree/main/hospitality/food-service/reactive-bbq/restaurant/Reservation.riddl)
- [`TableOrder.riddl`](https://github.com/ossuminc/riddl-models/tree/main/hospitality/food-service/reactive-bbq/restaurant/TableOrder.riddl)
