---
title: "Patterns"
description: "Cross-cutting RIDDL patterns demonstrated in the Reactive BBQ model"
---

# Patterns

The Reactive BBQ model demonstrates seven cross-cutting RIDDL
patterns. This page summarizes each pattern with real code
and links to where it appears in the model.

## Entity Lifecycle

Every entity follows the same structure: commands trigger state
transitions, events record what happened, state captures the
current data, and a handler wires it together.

```riddl
entity KitchenTicket is {
  // Commands define what can happen
  command ReceiveTicket is { ... }
  command AssignStation is { ... }

  // Events record what did happen
  event TicketReceived is { ... }
  event StationAssigned is { ... }

  // State captures current data
  state ActiveTicket of KitchenTicket.KitchenTicketStateData

  // Handler wires commands to state transitions
  handler KitchenTicketHandler is {
    on command ReceiveTicket {
      morph entity Kitchen.KitchenTicket to state
        Kitchen.KitchenTicket.ActiveTicket
        with command ReceiveTicket
      tell event TicketReceived to
        entity Kitchen.KitchenTicket
    }
    on command AssignStation {
      tell event StationAssigned to
        entity Kitchen.KitchenTicket
    }
  }
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

```riddl
type ReservationId is Id(FrontOfHouse.Reservation)
```

Typed identifiers link to specific entities, enabling
compile-time validation of cross-context references.

### Enumerations

```riddl
type DeliveryStatus is any of {
  DeliveryPending,
  DriverAssignedStatus,
  InTransit,
  Delivered,
  DeliveryFailed
}
```

Enumerations use `any of` to define a fixed set of values.
Each value is a constant.

### Records

```riddl
type GeoLocation is {
  latitude is Decimal(9, 6)
  longitude is Decimal(9, 6)
  recordedAt is TimeStamp
}
```

Records group related fields. They can use predefined types
like `Decimal(9, 6)`, `TimeStamp`, `Date`, `Duration`,
`Boolean`, `Natural`, `Integer`, `UUID`, and constrained
strings like `String(1, 200)`.

### Collections

```riddl
ticketItems is many TicketItem
deliveryAddress is optional DeliveryAddress
```

The `many` keyword denotes a collection. The `optional`
keyword makes a field nullable.

**Appears in:** Every context defines types. See
[Front of House](restaurant/front-of-house.md) for the most
comprehensive type catalog and
[Delivery](restaurant/delivery.md) for `GeoLocation`.

## Repository

Repositories define persistence schemas with indexes:

```riddl
repository KitchenTicketRepository is {
  schema KitchenTicketData is relational
    of tickets as KitchenTicket
    index on field KitchenTicket.kitchenTicketId
    index on field KitchenTicket.ticketStatus
    index on field KitchenTicket.assignedStation

  handler KitchenTicketPersistence is {
    on command KitchenTicket.ReceiveTicket {
      prompt "Store new kitchen ticket"
    }
    // ... handlers for each command
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
    // ...
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

```riddl
adaptor ToKitchen to context Restaurant.Kitchen is {
  handler KitchenRouting is {
    on command Restaurant.Kitchen.KitchenTicket.ReceiveTicket {
      prompt "Route food items from submitted order to kitchen"
    }
  }
}
```

Outbound adaptors send messages from this context to another.

### Inbound (`from`)

```riddl
adaptor FromFrontOfHouse from context Restaurant.FrontOfHouse is {
  handler FrontOfHouseIntake is {
    on event Restaurant.FrontOfHouse.TableOrder.OrderSubmitted {
      prompt "Convert submitted dine-in order into kitchen ticket"
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

```riddl
context PaymentGateway is {
  command AuthorizePayment is { ... }
  event PaymentAuthorized is { ... }
  command CapturePayment is { ... }
  event PaymentCaptured is { ... }
} with {
  option is external
  briefly "External payment gateway"
  described by "Third-party payment processing service."
}
```

The `option is external` metadata marks the context as
externally implemented. Only the interface is modeled.

**Appears in:** [External Contexts](external-contexts.md) —
PaymentGateway, NotificationService, HRSystem,
AccountingSystem, PrintingService, PhotographyService.

## Epics / Use Cases

Epics capture user journeys across contexts:

```riddl
epic KitchenWorkflow is {
  user Chef wants "to manage kitchen tickets digitally"
    so that "no orders are lost and cooks can read tickets clearly"
  case ProcessTicket is {
    user Chef wants "to process a kitchen ticket"
      so that "food is prepared correctly and on time"
    step from user Chef "receives digital ticket on kitchen display"
      to context Restaurant.Kitchen
    step from user Chef "assigns ticket to cooking station"
      to context Restaurant.Kitchen
    step from user Cook "prepares items and marks them ready"
      to context Restaurant.Kitchen
    step from user Chef "approves ticket and notifies server"
      to context Restaurant.Kitchen
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
