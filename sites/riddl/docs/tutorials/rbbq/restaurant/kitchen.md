---
title: "Kitchen Context"
description: "Kitchen ticket management and display in the Restaurant domain"
---

<!-- riddl-domain-prelude
context FrontOfHouse is {
  event OrderSubmitted is { tableOrderId: String(1,50) }
}
-->

<!-- riddl-prelude
type KitchenTicketId is Id(KitchenTicket)
type StationName is String(1,50)
type StationRouting is mapping from String to StationName
type DietaryFlags is set of String
type TicketSource is any of { DineIn, Online }
type TicketItem is {
  ticketMenuItemId: String(1,50)
  ticketItemName: String(1,200)
  ticketItemQuantity: Natural
  ticketItemNotes: String(1,500)?
  ticketItemReady: Boolean
}
record StoredKitchenTicket is {
  kitchenTicketId: KitchenTicketId
  currentStation: StationName?
}
event TicketReceived is { kitchenTicketId: KitchenTicketId }
event StationAssigned is { kitchenTicketId: KitchenTicketId }
event PreparationStarted is { kitchenTicketId: KitchenTicketId }
event ItemMarkedReady is { kitchenTicketId: KitchenTicketId }
event TicketApproved is { kitchenTicketId: KitchenTicketId }
event ServerNotified is { kitchenTicketId: KitchenTicketId }
type KitchenTicketEvent is TicketReceived | StationAssigned | PreparationStarted | ItemMarkedReady | TicketApproved | ServerNotified
entity KitchenTicket is { ??? }
repository KitchenTicketRepository is { ??? }
-->

# Kitchen Context

The Kitchen context manages the kitchen ticket queue, station
assignments, preparation tracking, and quality control. Its
centerpiece is the **KitchenDisplay** projector that replaces
handwritten tickets and prevents order loss during peak hours.

## Purpose

When a server submits a dine-in order or a customer places an
online order, the food items are routed to the Kitchen as a
digital ticket. The Chef assigns tickets to stations, cooks
prepare items and mark them ready, the Chef approves the
completed ticket, and the server is notified. Every step is
captured as an event, so tickets survive system crashes.

## Interview Connection

This context directly addresses pain points from the
[Chef](../personas/chef.md) and [Cook](../personas/cook.md)
interviews:

- **Order loss** — "Sometimes the system crashes and orders get
  lost. While it is down we don't know what needs to be made."
- **Illegible tickets** — "Handwritten tickets... I have to get
  her to explain to me what she has written."

The KitchenDisplay projector solves both problems by providing
a persistent, legible, digital ticket queue.

## Types

<!-- riddl: in-context no-prelude=KitchenTicketId,StationName,StationRouting,DietaryFlags,TicketSource,TicketItem -->
```riddl
type KitchenTicketId is Id(KitchenTicket)

type StationName is String(1,50)

// Which station cooks each menu category. A mapping and not a field on the
// item, because the same dish moves between stations as a kitchen is relaid
// or a station goes down -- the routing is a property of THIS kitchen on
// THIS night, not of the dish.
type StationRouting is mapping from String to StationName

// A SET, not a list: order is meaningless and a repeat carries no extra
// warning. A cook scanning a ticket must see each flag exactly once.
type DietaryFlags is set of String

type TicketSource is any of { DineIn, Online }

type TicketItem is {
  ticketMenuItemId: String(1,50)
  ticketItemName: String(1,200)
  ticketItemQuantity: Natural
  ticketItemNotes: String(1,500)?
  ticketItemReady: Boolean
}
```

The `TicketSource` enumeration distinguishes dine-in from online
orders — important because they arrive through different
adaptors and may have different preparation priorities.

## Entity: KitchenTicket

The `KitchenTicket` entity has a six-command lifecycle and is event-sourced.
Each lifecycle phase is a **named state** rather than a `status` field, so the
compiler knows which commands each phase accepts. Two of the six are shown
here; the others follow the same shape:

<!-- riddl: in-context no-prelude=KitchenTicket,TicketReceived,StationAssigned,PreparationStarted,ItemMarkedReady,TicketApproved,ServerNotified,KitchenTicketEvent -->
```riddl
event-sourced entity KitchenTicket as flow is {

  // An event-sourced entity OWNS the commands and events that change it, so
  // they are declared INSIDE it. Every command names the event it yields.
  command ReceiveTicket yields event TicketReceived is {
    kitchenTicketId: KitchenTicketId
    sourceOrderId: String(1,50)
    ticketSource: TicketSource
    ticketItems: TicketItem+
    receivedAt: TimeStamp
  }
  command AssignStation yields event StationAssigned is {
    kitchenTicketId: KitchenTicketId
    assignedStation: StationName
  }

  event TicketReceived is {
    kitchenTicketId: KitchenTicketId
    ticketItems: TicketItem+
    receivedAt: TimeStamp
  }
  event StationAssigned is {
    kitchenTicketId: KitchenTicketId
    assignedStation: StationName
    assignedAt: TimeStamp
  }
  // A rejection event for every command, so a refusal is recorded and not
  // merely returned. See the handler below.
  event AssignStationRejected is {
    kitchenTicketId: KitchenTicketId
    rejectionReason: String(1,500)
  }

  record KitchenTicketData is {
    kitchenTicketId: KitchenTicketId
    ticketItems: TicketItem+
    currentStation: StationName?
    receivedAt: TimeStamp
  }

  initial state Received of record KitchenTicketData is {
    handler ReceivedHandler is {
      on assignStation: command AssignStation is {
        yield event StationAssigned(
          kitchenTicketId = assignStation.kitchenTicketId,
          assignedStation = assignStation.assignedStation,
          assignedAt = prompt("when the station was assigned"))
      }
      // `set` and `morph` may appear ONLY in an `on event` clause of an
      // event-sourced entity: replay must re-apply the same change.
      on stationAssigned: event StationAssigned is {
        morph entity KitchenTicket to state Assigned
          with record KitchenTicketData(
            kitchenTicketId = stationAssigned.kitchenTicketId,
            ticketItems = KitchenTicketData.ticketItems,
            currentStation = KitchenTicketData.currentStation,
            receivedAt = KitchenTicketData.receivedAt)
      }
    }
  }

  state Assigned of record KitchenTicketData is {
    handler AssignedHandler is {
      // A command this state does not accept is refused -- and the refusal is
      // PUBLISHED before it is raised.
      on assignStation: command AssignStation is {
        send event AssignStationRejected(
          kitchenTicketId = assignStation.kitchenTicketId,
          rejectionReason = "KitchenTicket does not accept AssignStation in this state")
          to outlet KitchenTicketEvents
        error "KitchenTicket does not accept AssignStation in this state"
      }
    }
  }

  // An entity is a streamlet: it receives on its OWN inlet and publishes on
  // its OWN outlet, never on its context's. A portlet's type must ADMIT
  // everything that travels on it, rejections included -- which is what an
  // alternation is for.
  type KitchenTicketCommand is ReceiveTicket | AssignStation
  type KitchenTicketEvent is TicketReceived | StationAssigned | AssignStationRejected

  inlet KitchenTicketCommands is type KitchenTicketCommand
  outlet KitchenTicketEvents is type KitchenTicketEvent
}
```

The lifecycle flow is: **Receive → Assign → Start → Mark Items
Ready → Approve → Notify Server**. Each step emits an event,
and event sourcing means the complete ticket history survives
crashes. This directly addresses the Chef's concern about lost
orders.

## Repository

<!-- riddl: in-context no-prelude=KitchenTicketRepository,StoredKitchenTicket -->
```riddl
repository KitchenTicketRepository as merge is {
  inlet KitchenTicketRepositoryFromKitchenTicket is type KitchenTicketEvent
  inlet KitchenTicketRepositoryFromKitchenDisplay is type KitchenTicketEvent
  outlet KitchenTicketRepositoryResponses is type KitchenTicketEvent

  record StoredKitchenTicket is {
    kitchenTicketId: KitchenTicketId
    currentStation: StationName?
  }

  schema KitchenTicketSchema is relational
    of tickets as type StoredKitchenTicket
      index on field StoredKitchenTicket.kitchenTicketId
      index on field StoredKitchenTicket.currentStation

  command PersistStationAssigned is { kitchenTicketId: KitchenTicketId }

  handler KitchenTicketPersistence is {
    on command PersistStationAssigned is {
      do "update KitchenTicketSchema.tickets set currentStation =
        assignedStation where kitchenTicketId matches"
    }
  }
}
```

The index on `currentStation` enables the kitchen display to quickly filter
tickets by station — the grill station only sees grill tickets. A repository
that answers queries and declares no index at all draws a warning, because it
is a sequential scan by construction.

## Projector: KitchenDisplay

The KitchenDisplay projector provides the real-time screen that
replaces printed and handwritten tickets:

<!-- riddl: in-context -->
```riddl
projector KitchenDisplay as flow is {
  updates repository KitchenTicketRepository
  inlet KitchenDisplayFromKitchenTicket is type KitchenTicketEvent
  outlet KitchenDisplayOut is type KitchenTicketEvent

  record KitchenDisplayEntry is {
    kitchenTicketId: KitchenTicketId
    ticketSource: TicketSource
    ticketItems: TicketItem+
    ticketDisplayStatus: String(1,30)
    displayStation: StationName?
    receivedAt: TimeStamp
  }

  handler KitchenDisplayHandler is {
    on ticketReceived: event TicketReceived is {
      do "insert a KitchenDisplayEntry for this ticket"
    }
    on stationAssigned: event StationAssigned is {
      do "update the display with the station assignment"
    }
    on serverNotified: event ServerNotified is {
      do "remove the completed ticket from the active display"
    }
  }
}
```

## Adaptors

Kitchen has two inbound adaptors — one for dine-in orders from
Front of House, one for online orders:

<!-- riddl: in-domain -->
```riddl
context Kitchen is {
  adaptor FromFrontOfHouse from context FrontOfHouse is {
    handler FrontOfHouseIntake is {
      on event FrontOfHouse.OrderSubmitted is {
        do "convert a submitted dine-in order into a kitchen ticket"
      }
      on other is {
        error "Unexpected message from Front of House"
      }
    }
  }
}
```

Both adaptors convert their respective order formats into a
unified `KitchenTicket`. The kitchen doesn't need to know
whether an order came from a table or a website — it just
processes tickets.

## Design Decisions

**Why named states rather than a `ticketStatus` field?** A status field is
data the model cannot reason about: nothing stops a ticket being approved
before preparation started. As states, each phase declares the commands it
accepts, and one it does not is refused — after the refusal has been
*published* as a rejection event, so the attempt is recorded rather than lost.

**Why event sourcing for kitchen tickets?** The Chef's interview
made it clear that order loss during system crashes was the
biggest operational pain point. Event sourcing ensures that even
if the system restarts, all tickets can be reconstructed from
the event log. No more "orders get lost."

**Why a separate KitchenDisplay projector?** The display is a
CQRS read model. It can be rebuilt from events at any time, and
its read performance doesn't compete with the write-heavy ticket
processing. If the display crashes, it catches up from events
when it restarts.

**Why two separate adaptors instead of one?** Dine-in and online
orders have different structures (`OrderLine` vs `CartItem`) and
different source events. Separate adaptors make the translation
logic explicit and independently modifiable.

## Source

- [`KitchenContext.riddl`](https://github.com/ossuminc/riddl-models/tree/main/hospitality/food-service/reactive-bbq/restaurant/KitchenContext.riddl)
- [`kitchen-types.riddl`](https://github.com/ossuminc/riddl-models/tree/main/hospitality/food-service/reactive-bbq/restaurant/kitchen-types.riddl)
- [`KitchenTicket.riddl`](https://github.com/ossuminc/riddl-models/tree/main/hospitality/food-service/reactive-bbq/restaurant/KitchenTicket.riddl)
