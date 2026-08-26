---
title: "Front of House Context"
description: "Reservations, table orders, and billing in the Restaurant domain"
---

<!-- riddl-domain-prelude
context Kitchen is {
  command ReceiveTicket is { kitchenTicketId: String(1,50) }
}
-->

<!-- riddl-prelude
type ReservationId is Id(Reservation)
type GuestName is String(1,100)
record StoredReservation is { reservationId: ReservationId }
event ReservationMade is { reservationId: ReservationId }
event ReservationConfirmed is { reservationId: ReservationId }
event ConfirmReservationRejected is { reservationId: ReservationId, rejectionReason: String(1,500) }
type ReservationEvent is ReservationMade | ReservationConfirmed | ConfirmReservationRejected
entity Reservation is { ??? }
repository ReservationRepository is { ??? }
command PersistReservationConfirmed is { reservationId: ReservationId }
record MenuItemInfo is { menuItemName: String(1,200) }
-->

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

<!-- riddl: in-context no-prelude=ReservationId,GuestName -->
```riddl
type ReservationId is Id(Reservation)

type GuestName is String(1,100)
```

Notice the `Id()` type constructor — `ReservationId` is typed as
an identifier *for* the `Reservation` entity. This gives the
compiler enough information to enforce type safety across context
boundaries.

The context also defines record types for structured data:

<!-- riddl: in-context no-prelude=MenuItemInfo -->
```riddl
// A LOCAL copy of what this context needs about a menu item, fed by an
// adaptor from Corporate. Front of House does not reach into MenuManagement
// for it -- that would bind the two contexts together.
record MenuItemInfo is {
  menuItemName: String(1,200)
  menuItemPrice: Decimal(10,2)
  menuItemAvailable: Boolean
}
```

## Reservation Entity

The `Reservation` entity models the full lifecycle from request
through confirmation, seating, or cancellation:

<!-- riddl: in-context no-prelude=Reservation,ReservationMade,ReservationConfirmed,ConfirmReservationRejected,ReservationCommand,ReservationEvent -->
```riddl
event-sourced entity Reservation as flow is {

  // An event-sourced entity OWNS the commands and events that change it, so
  // they are declared INSIDE it, and every command names the event it yields.
  command MakeReservation yields event ReservationMade is { reservationId: ReservationId }
  command ConfirmReservation yields event ReservationConfirmed is { reservationId: ReservationId }

  event ReservationMade is { reservationId: ReservationId }
  event ReservationConfirmed is { reservationId: ReservationId }
  event ConfirmReservationRejected is { reservationId: ReservationId, rejectionReason: String(1,500) }

  record ReservationData is { reservationId: ReservationId }

  // Lifecycle phases are named STATES, not a status field: each state
  // declares the commands it accepts, so the compiler knows the machine.
  initial state Requested of record ReservationData is {
    handler RequestedHandler is {
      on cmd: command ConfirmReservation is {
        yield event ReservationConfirmed(reservationId = cmd.reservationId)
      }
      // `set` and `morph` may appear ONLY in an `on event` clause here:
      // replay has to re-apply exactly the same change.
      on evt: event ReservationConfirmed is {
        morph entity Reservation to state Confirmed
          with record ReservationData(reservationId = evt.reservationId)
      }
    }
  }

  state Confirmed of record ReservationData is {
    handler ConfirmedHandler is {
      // A command this state does not accept is refused -- and the refusal
      // is PUBLISHED before it is raised, so the attempt is recorded.
      on cmd: command ConfirmReservation is {
        send event ConfirmReservationRejected(reservationId = cmd.reservationId,
          rejectionReason = "Reservation does not accept ConfirmReservation in this state")
          to outlet ReservationEvents
        error "Reservation does not accept ConfirmReservation in this state"
      }
    }
  }

  // A processor receives on its OWN inlet and publishes on its OWN outlet,
  // and a portlet's type must ADMIT everything that travels on it.
  type ReservationCommand is MakeReservation | ConfirmReservation
  type ReservationEvent is ReservationMade | ReservationConfirmed | ConfirmReservationRejected

  inlet ReservationCommands is type ReservationCommand
  outlet ReservationEvents is type ReservationEvent
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

<!-- riddl: in-context no-prelude=ReservationRepository,StoredReservation,PersistReservationConfirmed -->
```riddl
repository ReservationRepository as merge is {
  inlet ReservationRepositoryFromReservation is command PersistReservationConfirmed
  inlet ReservationRepositoryFromProjector is command PersistReservationConfirmed
  outlet ReservationRepositoryResponses is result ReservationResult

  // A repository answers with a RESULT, never an event.
  result ReservationResult is { found: Boolean }

  record StoredReservation is { reservationId: ReservationId }

  // A repository that answers queries and declares NO index at all is a
  // sequential scan by construction, and draws a warning saying so.
  schema ReservationSchema is relational
    of rows as record StoredReservation
      index on field StoredReservation.reservationId

  command PersistReservationConfirmed is { reservationId: ReservationId }

  handler ReservationPersistence is {
    on command PersistReservationConfirmed is {
      do "update the stored reservation row for this reservationId"
    }
    // An inlet admitting an alternation needs a clause that receives it.
    // Handling each member is not enough -- say what ARRIVING means.
    on other is {
      do "persist whatever else arrives on this inlet"
    }
  }
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

<!-- riddl: in-context no-prelude=ReservationBoard -->
```riddl
projector ReservationBoard as flow is {
  updates repository ReservationRepository
  inlet ReservationBoardFromReservation is type ReservationEvent
  outlet ReservationBoardOut is type ReservationEvent

  record ReservationBoardEntry is { reservationId: ReservationId }

  handler ReservationBoardHandler is {
    on evt: event ReservationMade is {
      tell command PersistReservationConfirmed(reservationId = evt.reservationId) to repository ReservationRepository
    }
    // The inlet admits an alternation, so the projector must say what
    // ARRIVING means -- handling each member individually is not enough.
    on other is {
      do "ignore any other event on this stream"
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

<!-- riddl: in-domain -->
```riddl
context FrontOfHouse is {
  // An adaptor is the translation seam at a context boundary: it is the only
  // place that knows the OTHER context's message shapes.
  adaptor ToKitchen to context Kitchen is {
    handler ToKitchenIntake is {
      on command Kitchen.ReceiveTicket is {
        do "turn the food lines of a submitted table order into a kitchen ticket"
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
