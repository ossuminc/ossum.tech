---
title: "Delivery Context"
description: "Driver dispatch, GPS tracking, and offline-resilient delivery"
---

<!-- riddl-domain-prelude
context OnlineOrdering is {
  event OnlineOrderSubmitted is { onlineOrderId: String(1,50) }
}
-->

<!-- riddl-prelude
type DeliveryId is Id(DeliveryOrder)
type DriverId is UUID
record StoredDeliveryOrder is { deliveryId: DeliveryId }
event DeliveryCreated is { deliveryId: DeliveryId }
event DriverAssigned is { deliveryId: DeliveryId }
event AssignDriverRejected is { deliveryId: DeliveryId, rejectionReason: String(1,500) }
type DeliveryOrderEvent is DeliveryCreated | DriverAssigned | AssignDriverRejected
entity DeliveryOrder is { ??? }
repository DeliveryRepository is { ??? }
command PersistDriverAssigned is { deliveryId: DeliveryId }
-->

# Delivery Context

The Delivery context manages delivery driver dispatch, GPS
tracking, and offline-resilient delivery operations. Drivers can
cache order details locally and report issues when connectivity
resumes.

## Purpose

When an online customer selects delivery fulfillment, the Online
Ordering context creates a delivery via an adaptor. The Delivery
context handles everything from driver assignment through
dispatch, location tracking, delivery confirmation, payment
collection, and issue reporting.

## Interview Connection

From the [Delivery Driver's interview](../personas/delivery-driver.md):

> "Sometimes it doesn't work. I will be on the way to a customer
> site when suddenly it just stops... When that happens I lose
> everything."

The `DeliveryOrder` entity's 7-command lifecycle is designed for
offline resilience. The driver's app can cache the order details
locally, and location updates and issue reports can be queued
and synced when connectivity resumes.

## Types

<!-- riddl: in-context no-prelude=DeliveryId,DriverId -->
```riddl
type DeliveryId is Id(DeliveryOrder)

type DriverId is UUID
```

The `GeoLocation` type combines coordinates with a timestamp,
enabling the system to track the driver's route over time. The
`DeliveryIssueType` enumeration captures common delivery
problems — the driver mentioned several of these in their
interview.

## Entity: DeliveryOrder

The `DeliveryOrder` entity has a 7-command lifecycle — the
longest of any entity in the model:

<!-- riddl: in-context no-prelude=DeliveryOrder,DeliveryCreated,DriverAssigned,AssignDriverRejected,DeliveryOrderCommand,DeliveryOrderEvent -->
```riddl
event-sourced entity DeliveryOrder as flow is {

  // An event-sourced entity OWNS the commands and events that change it, so
  // they are declared INSIDE it, and every command names the event it yields.
  command CreateDelivery yields event DeliveryCreated is { deliveryId: DeliveryId }
  command AssignDriver yields event DriverAssigned is { deliveryId: DeliveryId }

  event DeliveryCreated is { deliveryId: DeliveryId }
  event DriverAssigned is { deliveryId: DeliveryId }
  event AssignDriverRejected is { deliveryId: DeliveryId, rejectionReason: String(1,500) }

  record DeliveryOrderData is { deliveryId: DeliveryId }

  // Lifecycle phases are named STATES, not a status field: each state
  // declares the commands it accepts, so the compiler knows the machine.
  initial state Pending of record DeliveryOrderData is {
    handler PendingHandler is {
      on cmd: command AssignDriver is {
        yield event DriverAssigned(deliveryId = cmd.deliveryId)
      }
      // `set` and `morph` may appear ONLY in an `on event` clause here:
      // replay has to re-apply exactly the same change.
      on evt: event DriverAssigned is {
        morph entity DeliveryOrder to state DriverAssignedState
          with record DeliveryOrderData(deliveryId = evt.deliveryId)
      }
    }
  }

  state DriverAssignedState of record DeliveryOrderData is {
    handler DriverAssignedStateHandler is {
      // A command this state does not accept is refused -- and the refusal
      // is PUBLISHED before it is raised, so the attempt is recorded.
      on cmd: command AssignDriver is {
        send event AssignDriverRejected(deliveryId = cmd.deliveryId,
          rejectionReason = "DeliveryOrder does not accept AssignDriver in this state")
          to outlet DeliveryOrderEvents
        error "DeliveryOrder does not accept AssignDriver in this state"
      }
    }
  }

  // A processor receives on its OWN inlet and publishes on its OWN outlet,
  // and a portlet's type must ADMIT everything that travels on it.
  type DeliveryOrderCommand is CreateDelivery | AssignDriver
  type DeliveryOrderEvent is DeliveryCreated | DriverAssigned | AssignDriverRejected

  inlet DeliveryOrderCommands is type DeliveryOrderCommand
  outlet DeliveryOrderEvents is type DeliveryOrderEvent
}
```

The lifecycle: **Create → Assign Driver → Dispatch → Track
Location → Confirm Delivery → Record Payment → (optional)
Report Issue**.

The `RecordDeliveryLocation` command can be sent multiple times
during a delivery, building up a GPS trail. The
`ReportDeliveryIssue` command can be sent at any point and
doesn't end the delivery — it records the issue while the
delivery continues.

## Repository

<!-- riddl: in-context no-prelude=DeliveryRepository,StoredDeliveryOrder,PersistDriverAssigned -->
```riddl
repository DeliveryRepository as flow is {
  inlet DeliveryRepositoryFromDeliveryOrder is command PersistDriverAssigned
  outlet DeliveryRepositoryResponses is result DeliveryResult

  // A repository answers with a RESULT, never an event.
  result DeliveryResult is { found: Boolean }

  record StoredDeliveryOrder is { deliveryId: DeliveryId }

  // A repository that answers queries and declares NO index at all is a
  // sequential scan by construction, and draws a warning saying so.
  schema DeliveryOrderSchema is relational
    of rows as record StoredDeliveryOrder
      index on field StoredDeliveryOrder.deliveryId

  command PersistDriverAssigned is { deliveryId: DeliveryId }

  handler DeliveryOrderPersistence is {
    on command PersistDriverAssigned is {
      do "update the stored deliveryOrder row for this deliveryId"
    }
    // An inlet admitting an alternation needs a clause that receives it.
    // Handling each member is not enough -- say what ARRIVING means.
    on other is {
      do "persist whatever else arrives on this inlet"
    }
  }
}
```

The index on `assignedDriverId` supports looking up all active
deliveries for a specific driver — essential for the driver's
app dashboard.

## Adaptor

Delivery has a single inbound adaptor:

<!-- riddl: in-domain -->
```riddl
context Delivery is {
  // An adaptor is the translation seam at a context boundary: it is the only
  // place that knows the OTHER context's message shapes.
  adaptor FromOnlineOrdering from context OnlineOrdering is {
    handler FromOnlineOrderingIntake is {
      on event OnlineOrdering.OnlineOrderSubmitted is {
        do "create a delivery for a submitted online order"
      }
      // Every adaptor handler must say what it does with what it does not
      // recognise. Silence is not an option in 2.0.
      on other is {
        error "Unexpected message from OnlineOrdering"
      }
    }
  }
}
```

The adaptor listens for `FulfillmentSelected` events and creates
a delivery only when the customer chose delivery fulfillment.
Pickup orders don't trigger this adaptor at all.

## Design Decisions

**Why separate from Online Ordering?** The delivery driver's
interview revealed that connectivity issues are the primary
pain point. Delivery needs offline-first design patterns that
would add unnecessary complexity to the online ordering flow.
Separating them means delivery can be designed for intermittent
connectivity while online ordering focuses on responsive UX.

**Why GPS tracking as repeated commands?** Rather than
maintaining a live connection, the driver's app periodically
sends `RecordDeliveryLocation` commands. If connectivity drops,
the locations queue up and sync when the connection resumes.
This is inherently more resilient than a streaming approach.

**Why `ReportDeliveryIssue` as a separate command?** Issues
don't necessarily end a delivery. A traffic delay is reported
but the delivery continues. A customer unavailable might lead
to a retry. Making it a separate command (not a state
transition) keeps the main lifecycle clean.

## Source

- [`DeliveryContext.riddl`](https://github.com/ossuminc/riddl-models/tree/main/hospitality/food-service/reactive-bbq/restaurant/DeliveryContext.riddl)
- [`delivery-types.riddl`](https://github.com/ossuminc/riddl-models/tree/main/hospitality/food-service/reactive-bbq/restaurant/delivery-types.riddl)
- [`Delivery.riddl`](https://github.com/ossuminc/riddl-models/tree/main/hospitality/food-service/reactive-bbq/restaurant/Delivery.riddl)
