---
title: "Reactive BBQ Domain"
description: "Top-level domain model for the Reactive BBQ restaurant chain"
---

# Reactive BBQ Domain

Everything in RIDDL revolves around creating domains and subdomains.
These are logical groupings of definitions that *belong* together,
presumably because they mimic an organization's structure or some
other logical, real-world groupings. Domains can be nested.

## The Top-Level Domain

The `ReactiveBBQ` domain defines the entire enterprise. It includes
an author, stakeholder personas as `user` definitions, key user
journeys as `epic` definitions, and three subdomain includes:

```riddl
domain ReactiveBBQ is {

  author OssumInc is {
    name is "Ossum Inc."
    email is "info@ossuminc.com"
  } with {
    briefly "Author of this model"
    described by "Ossum Inc., creators of RIDDL."
  }

  // ---- Stakeholder Personas ----

  user CEO is "CEO responsible for strategic initiatives and chain-wide performance" with {
    briefly "CEO"
    described by "Drives loyalty program, electronic menus, kitchen displays, and profitability."
  }

  user CorporateHeadChef is "Head Chef managing recipes and menus across 500+ locations" with {
    briefly "Corporate Head Chef"
    described by "Responsible for monthly menu updates, recipe standardization, and quality."
  }

  user Host is "Restaurant host managing reservations and seating" with {
    briefly "Host"
    described by "Manages walk-ins and reservations. Uses paper backup when systems slow."
  }

  user Server is "Wait staff serving tables and processing orders" with {
    briefly "Server"
    described by "Takes orders, coordinates with kitchen and bar, and processes payments."
  }

  user Bartender is "Bar staff preparing and serving drinks" with {
    briefly "Bartender"
    described by "Prepares drink orders and needs push notifications when drinks are ready."
  }

  user Chef is "Kitchen chef managing order flow and quality" with {
    briefly "Chef"
    described by "Oversees kitchen ticket queue, station assignments, and quality approval."
  }

  user Cook is "Line cook preparing menu items" with {
    briefly "Cook"
    described by "Prepares food at assigned station. Struggles with handwritten tickets."
  }

  user DeliveryDriver is "Driver delivering online orders" with {
    briefly "Delivery Driver"
    described by "Picks up and delivers orders. Needs offline resilience."
  }

  user OnlineCustomer is "Customer ordering through website or app" with {
    briefly "Online Customer"
    described by "Browses menu, builds cart, checks out, and chooses fulfillment."
  }

  // ---- Subdomain Includes ----

  include "restaurant/domain.riddl"
  include "backoffice/domain.riddl"
  include "corporate/domain.riddl"

} with {
  briefly "Reactive BBQ restaurant chain"
  described by {
    | A 500+ location BBQ restaurant chain modeled with
    | reactive, event-driven bounded contexts. Addresses
    | peak-hour performance, cascading failure isolation,
    | independent deployability, and unblocks strategic
    | initiatives: loyalty program, electronic menus, and
    | kitchen display screens.
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

```riddl
epic DineInExperience is {
  user Host wants "to seat guests quickly"
    so that "tables turn over efficiently during peak hours"
  case WalkInSeating is {
    user Host wants "to seat a walk-in party"
      so that "the table is occupied and orders can begin"
    step from user Host "checks table availability"
      to context Restaurant.FrontOfHouse
    step from user Host "seats the party and creates an order"
      to context Restaurant.FrontOfHouse
  } with {
    briefly "Walk-in seating"
    described by "Host seats a walk-in party."
  }
} with {
  briefly "Dine-in guest experience"
  described by {
    | Covers the full dine-in journey from reservation
    | or walk-in through seating, ordering, and payment.
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
