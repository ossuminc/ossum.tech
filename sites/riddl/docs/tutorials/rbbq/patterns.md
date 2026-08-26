---
title: "Patterns"
description: "Cross-cutting RIDDL patterns demonstrated in the Reactive BBQ model"
---

<!-- riddl-domain-prelude
user Chef is "Kitchen chef managing order flow and quality"
context Kitchen is {
  command ReceiveTicket is { kitchenTicketId: String(1,50) }
}
context FrontOfHouse is {
  event OrderSubmitted is { tableOrderId: String(1,50) }
}
application context RestaurantApp is {
  group KitchenScreen is {
    input AssignStationInput acquires command Kitchen.ReceiveTicket
    output TicketQueueDisplay presents result KitchenView
  }
  result KitchenView is { queueDepth: Natural }
}
-->

<!-- riddl-prelude
type TicketItem is { ticketMenuItemId: String(1,50) }
type KitchenTicketId is Id(KitchenTicket)
type ReservationId is Id(Reservation)
entity KitchenTicket is { ??? }
entity Reservation is { ??? }
record StoredKitchenTicket is { kitchenTicketId: KitchenTicketId, currentStation: String(1,50)? }
event TicketReceived is { kitchenTicketId: KitchenTicketId }
event StationAssigned is { kitchenTicketId: KitchenTicketId }
event AssignStationRejected is { kitchenTicketId: KitchenTicketId, rejectionReason: String(1,500) }
type KitchenTicketEvent is TicketReceived | StationAssigned | AssignStationRejected
event ReservationMade is { reservationId: ReservationId }
type ReservationEvent is ReservationMade
repository KitchenTicketRepository is { ??? }
command PersistStationAssigned is { kitchenTicketId: KitchenTicketId }
-->

# Patterns

The Reactive BBQ model demonstrates seven cross-cutting RIDDL
patterns. This page summarizes each pattern with real code
and links to where it appears in the model.

## Entity Lifecycle

Every entity follows the same structure: commands trigger state
transitions, events record what happened, state captures the
current data, and a handler wires it together.

<!-- riddl: in-context no-prelude=KitchenTicket,TicketReceived,StationAssigned,AssignStationRejected,KitchenTicketEvent -->
```riddl
// The lifecycle is NAMED STATES, not a status field: each state declares the
// commands it accepts, so an out-of-order command is refused by construction.
event-sourced entity KitchenTicket as flow is {
  command AssignStation yields event StationAssigned is { kitchenTicketId: KitchenTicketId }

  event StationAssigned is { kitchenTicketId: KitchenTicketId }
  event TicketReceived is { kitchenTicketId: KitchenTicketId }
  event AssignStationRejected is {
    kitchenTicketId: KitchenTicketId
    rejectionReason: String(1,500)
  }

  record KitchenTicketData is { kitchenTicketId: KitchenTicketId }

  initial state Received of record KitchenTicketData is {
    handler ReceivedHandler is {
      on cmd: command AssignStation is {
        yield event StationAssigned(kitchenTicketId = cmd.kitchenTicketId)
      }
      on evt: event StationAssigned is {
        morph entity KitchenTicket to state Assigned
          with record KitchenTicketData(kitchenTicketId = evt.kitchenTicketId)
      }
    }
  }

  state Assigned of record KitchenTicketData is {
    handler AssignedHandler is {
      on cmd: command AssignStation is {
        send event AssignStationRejected(kitchenTicketId = cmd.kitchenTicketId,
          rejectionReason = "already assigned") to outlet KitchenTicketEvents
        error "KitchenTicket does not accept AssignStation in this state"
      }
    }
  }

  type KitchenTicketEvent is TicketReceived | StationAssigned | AssignStationRejected
  inlet KitchenTicketCommands is command AssignStation
  outlet KitchenTicketEvents is type KitchenTicketEvent
}
```

The first command uses `morph` to create the entity instance.
Subsequent commands use `tell` to emit events and update state.

**Appears in:** Every context — all 13 entities follow this
pattern. See [Kitchen](restaurant/kitchen.md) for the
canonical example.

## Type System

RIDDL provides a rich type system for modeling domain data:

### Id Types

<!-- riddl: in-context no-prelude=ReservationId -->
```riddl
type ReservationId is Id(Reservation)
```

Typed identifiers link to specific entities, enabling
compile-time validation of cross-context references.

### Enumerations

<!-- riddl: in-context -->
```riddl
// An enumeration's enumerators join the ENCLOSING namespace, so a name here
// can collide with a state or constant elsewhere in the same context.
type DeliveryStatus is any of {
  Pending,
  InTransit,
  Delivered,
  Failed
}
```

Enumerations use `any of` to define a fixed set of values.
Each value is a constant.

### Records

<!-- riddl: in-context -->
```riddl
record GeoLocation is {
  latitude: Decimal(9,6)
  longitude: Decimal(9,6)
}
```

Records group related fields. They can use predefined types
like `Decimal(9, 6)`, `TimeStamp`, `Date`, `Duration`,
`Boolean`, `Natural`, `Integer`, `UUID`, and constrained
strings like `String(1, 200)`.

### Collections

<!-- riddl: in-record -->
```riddl
ticketItems: TicketItem+
```

The `many` keyword denotes a collection. The `optional`
keyword makes a field nullable.

**Appears in:** Every context defines types. See
[Front of House](restaurant/front-of-house.md) for the most
comprehensive type catalog and
[Delivery](restaurant/delivery.md) for `GeoLocation`.

## Repository

Repositories define persistence schemas with indexes:

<!-- riddl: in-context no-prelude=KitchenTicketRepository,StoredKitchenTicket,PersistStationAssigned -->
```riddl
repository KitchenTicketRepository as flow is {
  inlet KitchenTicketRepositoryFromKitchenTicket is command PersistStationAssigned
  outlet KitchenTicketRepositoryResponses is result KitchenTicketResult

  // A repository answers with a RESULT, never an event.
  result KitchenTicketResult is { found: Boolean }

  record StoredKitchenTicket is {
    kitchenTicketId: KitchenTicketId
    currentStation: String(1,50)?
  }

  // A repository that answers queries and declares NO index at all is a
  // sequential scan by construction, and is warned about as one.
  schema KitchenTicketSchema is relational
    of tickets as record StoredKitchenTicket
      index on field StoredKitchenTicket.kitchenTicketId

  command PersistStationAssigned is { kitchenTicketId: KitchenTicketId }

  handler KitchenTicketPersistence is {
    on command PersistStationAssigned is {
      do "update the stored ticket's station"
    }
    // An inlet admitting an alternation needs a clause that receives it.
    // Handling each member is not enough -- say what ARRIVING means.
    on other is {
      do "persist whatever else arrives on this inlet"
    }
  }
}
```

The `schema` declares relational storage with named indexes.
The handler maps entity commands to persistence operations.

**Appears in:** Every context except
[Reporting](backoffice/reporting.md) (which has only
projectors). See [Inventory](backoffice/inventory.md) for
an example with stock-level indexing.

## Projector / CQRS

Projectors build read-optimized views from events:

<!-- riddl: in-context -->
```riddl
// A projector is the READ side: it owns its own shape and persists through a
// repository, so report queries never compete with ticket processing.
projector ReservationBoard as flow is {
  updates repository KitchenTicketRepository
  inlet ReservationBoardIn is type KitchenTicketEvent
  outlet ReservationBoardOut is type KitchenTicketEvent

  record ReservationBoardEntry is {
    kitchenTicketId: KitchenTicketId
    boardStation: String(1,50)?
  }

  handler ReservationBoardHandler is {
    on evt: event StationAssigned is {
      tell command PersistStationAssigned(kitchenTicketId = evt.kitchenTicketId)
        to repository KitchenTicketRepository
    }
    // The inlet admits an alternation, so the projector must say what
    // ARRIVING means -- handling each member individually is not enough.
    on other is {
      do "ignore any other event on this stream"
    }
  }
}
```

Projectors listen to events (not commands) and maintain a
denormalized view. They can be rebuilt from the event stream
at any time.

**Appears in:**

- [Front of House](restaurant/front-of-house.md) —
  `ReservationBoard`
- [Kitchen](restaurant/kitchen.md) — `KitchenDisplay`
- [Reporting](backoffice/reporting.md) — `SalesReport`,
  `LaborReport`, `InventoryReport`

## Adaptor Communication

Adaptors bridge bounded contexts. There are two directions:

### Outbound (`to`)

<!-- riddl: in-domain -->
```riddl
context FrontOfHouseSeam is {
  // OUTBOUND: an adaptor `to` a context handles that context's INPUT -- a
  // command. Handling an event here is an Error.
  adaptor ToKitchen to context Kitchen is {
    handler ToKitchenOuttake is {
      on command Kitchen.ReceiveTicket is {
        do "turn the food lines of a submitted table order into a kitchen ticket"
      }
      on other is { error "Unexpected message bound for Kitchen" }
    }
  }
}
```

Outbound adaptors send messages from this context to another.

### Inbound (`from`)

<!-- riddl: in-domain -->
```riddl
context KitchenSeam is {
  // INBOUND: an adaptor `from` a context handles that context's OUTPUT -- an
  // event. It is the only place that knows the other context's shapes.
  adaptor FromFrontOfHouse from context FrontOfHouse is {
    handler FrontOfHouseIntake is {
      on event FrontOfHouse.OrderSubmitted is {
        do "convert a submitted dine-in order into a kitchen ticket"
      }
      on other is { error "Unexpected message from Front of House" }
    }
  }
}
```

Inbound adaptors receive and transform messages from another
context.

**Appears in:** Most contexts. See
[Kitchen](restaurant/kitchen.md) for inbound adaptors,
[Front of House](restaurant/front-of-house.md) for outbound
adaptors, and [Loyalty](restaurant/loyalty.md) for the
most elegant use — consuming events without the source
knowing about the consumer.

## External Contexts

External contexts model third-party system boundaries:

<!-- riddl: in-domain -->
```riddl
// `external` marks a context the chain does not build. It still declares its
// OWN portlets, because a cross-context connector may not reach past it.
external context PaymentGateway as flow is {
  inlet PaymentGatewayIn is type PaymentGatewayEvent
  outlet PaymentGatewayOut is type PaymentGatewayEvent

  command AuthorizePayment yields event PaymentAuthorized is {
    paymentGatewayTransactionId: String(1,100)
  }
  event PaymentAuthorized is { paymentGatewayTransactionId: String(1,100) }
  type PaymentGatewayEvent is PaymentAuthorized

  handler PaymentGatewayHandler is {
    on cmd: command AuthorizePayment is {
      yield event PaymentAuthorized(
        paymentGatewayTransactionId = cmd.paymentGatewayTransactionId)
    }
    on other is { error "Unexpected message at the PaymentGateway boundary" }
  }
}
```

The `option is external` metadata marks the context as
externally implemented. Only the interface is modeled.

**Appears in:** [External Contexts](external-contexts.md) —
PaymentGateway, NotificationService, HRSystem,
AccountingSystem, PrintingService, PhotographyService.

## Epics / Use Cases

Epics capture user journeys across contexts:

<!-- riddl: in-domain -->
```riddl
epic KitchenWorkflow is {
  user Chef wants to "keep the ticket queue moving"
    so that "food leaves the pass while it is hot"

  case AssignAndPrepare is {
    user Chef wants to "assign a ticket to a station"
      so that "a cook can start on it"
    // A user interacts ONLY at the application boundary.
    step focus user Chef on group RestaurantApp.KitchenScreen
    step take input RestaurantApp.KitchenScreen.AssignStationInput from user Chef
    step show output RestaurantApp.KitchenScreen.TicketQueueDisplay to user Chef
  } with {
    briefly "Assign and prepare"
    described as {
      |The Chef assigns a ticket to a station and watches the queue.
    }
  }
} with {
  briefly "Kitchen workflow"
  described as {
    |Ticket intake through station assignment, preparation and approval.
  }
}
```

Epics reference `user` definitions and trace `step` sequences
through contexts. The `wants ... so that` syntax captures the
user's goal and motivation.

**Appears in:** [Domain Model](reactive-bbq.md) — four epics:
DineInExperience, OnlineOrderJourney, KitchenWorkflow,
LoyaltyEnrollment.

## Summary Table

| Pattern | RIDDL Construct | Count in Model |
|---------|----------------|---------------|
| Entity Lifecycle | `entity`, `command`, `event`, `state`, `handler` | 13 entities |
| Type System | `type`, `any of`, records, `many`, `optional` | ~40 types |
| Repository | `repository`, `schema`, `index` | 11 repositories |
| Projector / CQRS | `projector`, `updates`, event handlers | 5 projectors |
| Adaptor | `adaptor to`, `adaptor from` | 14 adaptors |
| External Context | `option is external` | 6 contexts |
| Epic | `epic`, `case`, `step`, `user` | 4 epics |
