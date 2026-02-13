---
title: "Delivery Context"
description: "Driver dispatch, GPS tracking, and offline-resilient delivery"
---

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

```riddl
type DeliveryId is Id(Delivery.DeliveryOrder) with {
  briefly "Delivery identifier"
  described by "Unique identifier for a delivery."
}

type DriverId is UUID with {
  briefly "Driver identifier"
  described by "Unique identifier for a delivery driver."
}

type DeliveryStatus is any of {
  DeliveryPending,
  DriverAssignedStatus,
  InTransit,
  Delivered,
  DeliveryFailed
} with {
  briefly "Delivery status"
  described by "Current status of a delivery."
}

type GeoLocation is {
  latitude is Decimal(9, 6)
  longitude is Decimal(9, 6)
  recordedAt is TimeStamp
} with {
  briefly "Geographic location"
  described by "GPS coordinates with timestamp."
}

type DeliveryIssueType is any of {
  AddressNotFound,
  CustomerUnavailable,
  FoodDamaged,
  VehicleBreakdown,
  TrafficDelay,
  OtherIssue
} with {
  briefly "Delivery issue type"
  described by "Type of issue reported during delivery."
}
```

The `GeoLocation` type combines coordinates with a timestamp,
enabling the system to track the driver's route over time. The
`DeliveryIssueType` enumeration captures common delivery
problems — the driver mentioned several of these in their
interview.

## Entity: DeliveryOrder

The `DeliveryOrder` entity has a 7-command lifecycle — the
longest of any entity in the model:

```riddl
entity DeliveryOrder is {

  command CreateDelivery is {
    deliveryId is DeliveryId
    sourceOnlineOrderId is String(1, 50)
    deliveryCustomerName is String(1, 100)
    deliveryCustomerPhone is String(7, 20)
    deliveryDestination is DeliveryAddress
    requestedDeliveryTime is optional TimeStamp
  }

  command AssignDriver is {
    deliveryId is DeliveryId
    driverId is DriverId
    driverName is String(1, 100)
  }

  command DispatchDriver is {
    deliveryId is DeliveryId
    dispatchedAt is TimeStamp
  }

  command RecordDeliveryLocation is {
    deliveryId is DeliveryId
    driverLocation is GeoLocation
  }

  command ConfirmDelivery is {
    deliveryId is DeliveryId
    confirmedAt is TimeStamp
    deliverySignature is optional String(1, 200)
  }

  command RecordDeliveryPayment is {
    deliveryId is DeliveryId
    deliveryTip is optional Decimal(8, 2)
    deliveryPaidAt is TimeStamp
  }

  command ReportDeliveryIssue is {
    deliveryId is DeliveryId
    issueType is DeliveryIssueType
    issueDescription is String(1, 1000)
    reportedAt is TimeStamp
  }

  // Events: DeliveryCreated, DriverAssigned, DriverDispatched,
  //         DeliveryLocationRecorded, DeliveryConfirmed,
  //         DeliveryPaymentRecorded, DeliveryIssueReported

  state ActiveDelivery of DeliveryOrder.DeliveryStateData

  handler DeliveryHandler is {
    on command CreateDelivery {
      morph entity Restaurant.Delivery.DeliveryOrder to state
        Restaurant.Delivery.DeliveryOrder.ActiveDelivery
        with command CreateDelivery
      tell event DeliveryCreated to
        entity Restaurant.Delivery.DeliveryOrder
    }
    // ... remaining commands use tell pattern
  }
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

```riddl
repository DeliveryRepository is {
  schema DeliveryData is relational
    of deliveries as DeliveryOrder
    index on field DeliveryOrder.deliveryId
    index on field DeliveryOrder.deliveryStatus
    index on field DeliveryOrder.assignedDriverId
}
```

The index on `assignedDriverId` supports looking up all active
deliveries for a specific driver — essential for the driver's
app dashboard.

## Adaptor

Delivery has a single inbound adaptor:

```riddl
adaptor FromOnlineOrdering from context Restaurant.OnlineOrdering is {
  handler OnlineDeliveryIntake is {
    on event Restaurant.OnlineOrdering.OnlineOrder.FulfillmentSelected {
      prompt "Create delivery when delivery fulfillment is selected"
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
