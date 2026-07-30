---
title: "Kitchen Context"
description: "Kitchen ticket management and display in the Restaurant domain"
---

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

```riddl
type KitchenTicketId is Id(Kitchen.KitchenTicket) with {
  briefly "Kitchen ticket identifier"
  described by "Unique identifier for a kitchen ticket."
}

type StationName is String(1, 50) with {
  briefly "Station name"
  described by "Name of the kitchen station such as grill, fryer, prep."
}

type TicketStatus is any of {
  Received,
  Assigned,
  InPreparation,
  ItemsReady,
  Approved,
  ServerNotifiedTicket
} with {
  briefly "Ticket status"
  described by "Current status of a kitchen ticket."
}

type TicketSource is any of {
  DineIn,
  Online
} with {
  briefly "Ticket source"
  described by "Whether the ticket originated from dine-in or online."
}

type TicketItem is {
  ticketMenuItemId is String(1, 50)
  ticketItemName is String(1, 200)
  ticketItemQuantity is Natural
  ticketItemNotes is optional String(1, 500)
  ticketItemReady is Boolean
} with {
  briefly "Ticket item"
  described by "A single item on a kitchen ticket."
}
```

The `TicketSource` enumeration distinguishes dine-in from online
orders — important because they arrive through different
adaptors and may have different preparation priorities.

## Entity: KitchenTicket

The `KitchenTicket` entity has a 6-command lifecycle with event
sourcing:

```riddl
entity KitchenTicket is {

  command ReceiveTicket is {
    kitchenTicketId is KitchenTicketId
    sourceOrderId is String(1, 50)
    ticketSource is TicketSource
    ticketItems is many TicketItem
    receivedAt is TimeStamp
  }

  command AssignStation is {
    kitchenTicketId is KitchenTicketId
    assignedStation is StationName
  }

  command StartPreparation is {
    kitchenTicketId is KitchenTicketId
    startedAt is TimeStamp
  }

  command MarkItemReady is {
    kitchenTicketId is KitchenTicketId
    readyMenuItemId is String(1, 50)
    markedReadyAt is TimeStamp
  }

  command ApproveTicket is {
    kitchenTicketId is KitchenTicketId
    approvedAt is TimeStamp
  }

  command NotifyServer is {
    kitchenTicketId is KitchenTicketId
    notifiedAt is TimeStamp
  }

  // Events: TicketReceived, StationAssigned, PreparationStarted,
  //         ItemMarkedReady, TicketApproved, ServerNotified

  state ActiveTicket of KitchenTicket.KitchenTicketStateData

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
    on command StartPreparation {
      tell event PreparationStarted to
        entity Kitchen.KitchenTicket
    }
    on command MarkItemReady {
      tell event ItemMarkedReady to
        entity Kitchen.KitchenTicket
    }
    on command ApproveTicket {
      tell event TicketApproved to
        entity Kitchen.KitchenTicket
    }
    on command NotifyServer {
      tell event ServerNotified to
        entity Kitchen.KitchenTicket
    }
  }
}
```

The lifecycle flow is: **Receive → Assign → Start → Mark Items
Ready → Approve → Notify Server**. Each step emits an event,
and event sourcing means the complete ticket history survives
crashes. This directly addresses the Chef's concern about lost
orders.

## Repository

```riddl
repository KitchenTicketRepository is {
  schema KitchenTicketData is relational
    of tickets as KitchenTicket
    index on field KitchenTicket.kitchenTicketId
    index on field KitchenTicket.ticketStatus
    index on field KitchenTicket.assignedStation
}
```

The index on `assignedStation` enables the kitchen display to
quickly filter tickets by station — the grill station only sees
grill tickets.

## Projector: KitchenDisplay

The KitchenDisplay projector provides the real-time screen that
replaces printed and handwritten tickets:

```riddl
projector KitchenDisplay is {
  updates repository KitchenTicketRepository

  record KitchenDisplayEntry is {
    kitchenTicketId is KitchenTicketId
    ticketSource is TicketSource
    ticketItems is many TicketItem
    ticketStatus is TicketStatus
    displayStation is optional StationName
    receivedAt is TimeStamp
  }

  handler KitchenDisplayHandler is {
    on event KitchenTicket.TicketReceived {
      prompt "Add ticket to kitchen display"
    }
    on event KitchenTicket.StationAssigned {
      prompt "Update display with station assignment"
    }
    on event KitchenTicket.PreparationStarted {
      prompt "Update display to show preparation in progress"
    }
    on event KitchenTicket.ItemMarkedReady {
      prompt "Update item readiness on display"
    }
    on event KitchenTicket.TicketApproved {
      prompt "Mark ticket as approved on display"
    }
    on event KitchenTicket.ServerNotified {
      prompt "Remove completed ticket from active display"
    }
  }
}
```

## Adaptors

Kitchen has two inbound adaptors — one for dine-in orders from
Front of House, one for online orders:

```riddl
adaptor FromFrontOfHouse from context Restaurant.FrontOfHouse is {
  handler FrontOfHouseIntake is {
    on event Restaurant.FrontOfHouse.TableOrder.OrderSubmitted {
      prompt "Convert submitted dine-in order into kitchen ticket"
    }
  }
}

adaptor FromOnlineOrdering from context Restaurant.OnlineOrdering is {
  handler OnlineIntake is {
    on event Restaurant.OnlineOrdering.OnlineOrder.OnlineOrderSubmitted {
      prompt "Convert submitted online order into kitchen ticket"
    }
  }
}
```

Both adaptors convert their respective order formats into a
unified `KitchenTicket`. The kitchen doesn't need to know
whether an order came from a table or a website — it just
processes tickets.

## Design Decisions

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
