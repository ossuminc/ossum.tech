---
title: "Reactive BBQ Domain"
description: "Top-level domain model for the Reactive BBQ restaurant chain"
---

<!-- riddl-domain-prelude
user Host is "Restaurant host managing reservations and seating"
context FrontOfHouse is {
  result ReservationResult is { seated: Boolean }
  command MakeReservation is { partySize: Natural }
  command SeatParty is { partySize: Natural }
}
application context RestaurantApp is {
  group RestaurantScreen is {
    input MakeReservationInput acquires command FrontOfHouse.MakeReservation
    input SeatPartyInput acquires command FrontOfHouse.SeatParty
    output ReservationBoardDisplay presents result FrontOfHouse.ReservationResult
  }
}
-->

# Reactive BBQ Domain

Everything in RIDDL revolves around creating domains and subdomains.
These are logical groupings of definitions that *belong* together,
presumably because they mimic an organization's structure or some
other logical, real-world groupings. Domains can be nested.

## The Top-Level Domain

The `ReactiveBBQ` domain defines the entire enterprise. It includes
an author, stakeholder personas as `user` definitions, key user
journeys as `epic` definitions, and three subdomain includes:

<!-- riddl: standalone -->
```riddl
domain ReactiveBBQ is {
  author OssumInc is {
    name = "Ossum Inc."
    email = "info@ossuminc.com"
  } with {
    briefly "Author"
    described as {
      |Ossum Inc., creators of RIDDL.
    }
  }

  // The chain's model version, not the RIDDL language version. A definition's
  // precise version is its versioned ancestors composed root-to-leaf and
  // joined with '.', so this is the leading component for everything beneath.
  version 1

  // ---- Stakeholder Personas ----
  user CEO is "CEO responsible for strategic initiatives and chain-wide performance"
  user CorporateHeadChef is "Head Chef managing recipes and menus across 500+ locations"
  user Host is "Restaurant host managing reservations and seating"
  user Server is "Wait staff serving tables and processing orders"
  user Bartender is "Bar staff preparing and serving drinks"
  user Chef is "Kitchen chef managing order flow and quality"
  user Cook is "Line cook preparing menu items"
  user DeliveryDriver is "Driver delivering online orders"
  user OnlineCustomer is "Customer ordering through website or app"

  // ---- Subdomain Includes ----
  // include "restaurant/domain.riddl", "backoffice/domain.riddl",
  //         "corporate/domain.riddl"

} with {
  briefly "Reactive BBQ restaurant chain"
  described as {
    |A 500+ location BBQ restaurant chain modeled with reactive,
    |event-driven bounded contexts.
  }
}
```

## Stakeholder Personas in RIDDL

Notice the `user` definitions at the top of the domain. RIDDL uses
`user` (not "actor") following the Use Cases 2.0 terminology. Each
`user` definition captures a stakeholder persona with a one-line
description and metadata explaining their role.

These personas were derived from the
[stakeholder interviews](scenario.md). They serve two purposes:

1. **Documentation** — They make the model self-documenting by
   recording who uses the system and why
2. **Epic references** — They are referenced in `epic` definitions
   to specify who participates in each user journey

## Epics and Use Cases

The domain defines four key user journeys as `epic` definitions.
Each epic contains `case` definitions with `step` sequences that
trace the flow across contexts:

<!-- riddl: in-domain -->
```riddl
epic DineInExperience is {
  user Host wants to "seat guests quickly"
    so that "tables turn over efficiently during peak hours"

  case WalkInSeating is {
    user Host wants to "seat a walk-in party"
      so that "the table is occupied and orders can begin"

    // A user interacts ONLY at the application boundary: the steps name
    // the app's group, inputs and outputs, and the app reaches the domain.
    step focus user Host on group RestaurantApp.RestaurantScreen
    step show output RestaurantApp.RestaurantScreen.ReservationBoardDisplay
      to user Host

    // A refusal is a modeled outcome, not an omission.
    optional {
      step context FrontOfHouse refuses user Host
        "every table of that size is seated, so the party waits"
    }

    step take input RestaurantApp.RestaurantScreen.SeatPartyInput
      from user Host
  } with {
    briefly "Walk-in seating"
    described as {
      |Host seats a walk-in party.
    }
  }
} with {
  briefly "Dine-in guest experience"
  described as {
    |Covers the dine-in journey from reservation or walk-in through
    |seating, ordering, and payment.
  }
}
```

The four epics are:

| Epic | Primary User | Contexts Involved |
|------|-------------|-------------------|
| **DineInExperience** | Host | FrontOfHouse |
| **OnlineOrderJourney** | OnlineCustomer | OnlineOrdering |
| **KitchenWorkflow** | Chef, Cook | Kitchen |
| **LoyaltyEnrollment** | OnlineCustomer | Loyalty |

## Why Subdomains?

Separating the business into distinct subdomains provides several
benefits:

1. **Bounded Contexts** — Each subdomain can define its own
   ubiquitous language without ambiguity
2. **Team Alignment** — Development teams can own specific
   subdomains
3. **Independent Evolution** — Subdomains can be modified without
   affecting others
4. **Scalability** — Different subdomains can be deployed and
   scaled independently

## The Three Subdomains

- [Restaurant](restaurant/index.md) — Core restaurant and
  customer-facing operations (6 contexts)
- [BackOffice](backoffice/index.md) — Administrative and
  management functions (3 contexts)
- [Corporate](corporate/index.md) — Corporate-level operations
  spanning all locations (3 contexts)

## Cross-Domain Communication

The subdomains communicate through well-defined
[adaptors](../../concepts/adaptor.md). For example:

- **FrontOfHouse → Kitchen** — Submitted orders become kitchen
  tickets via the `ToKitchen` adaptor
- **FrontOfHouse → Bar** — Drink items from orders are routed
  via the `ToBar` adaptor
- **OnlineOrdering → Delivery** — Delivery-fulfillment orders
  are routed via the `ToDelivery` adaptor
- **Kitchen → Inventory** — Preparation events trigger automatic
  stock consumption via the `FromKitchen` adaptor
- **MenuManagement → Restaurants** — Published menu releases
  distribute atomically via the `ToRestaurants` adaptor

## Source Code

The complete RIDDL specification for Reactive BBQ is in the
[riddl-models repository](https://github.com/ossuminc/riddl-models/tree/main/hospitality/food-service/reactive-bbq).
See the
[README](https://github.com/ossuminc/riddl-models/blob/main/hospitality/food-service/reactive-bbq/README.md)
for an overview of the model structure.
