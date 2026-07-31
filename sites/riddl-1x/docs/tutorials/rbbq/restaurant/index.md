---
title: "Restaurant Domain"
description: "Core restaurant operations in the Reactive BBQ model"
---

# Restaurant Domain

The Restaurant domain covers all in-restaurant and customer-facing
operations. It is the largest of the three domains, containing six
bounded contexts and two external system integrations.

## Domain Definition

The Restaurant domain includes its contexts via RIDDL's `include`
mechanism, keeping each context in its own file for maintainability:

```riddl
domain Restaurant is {

  author OssumInc is {
    name is "Ossum Inc."
    email is "info@ossuminc.com"
  } with {
    briefly "Author"
    described by "Ossum Inc."
  }

  include "FrontOfHouseContext.riddl"
  include "KitchenContext.riddl"
  include "BarContext.riddl"
  include "OnlineOrderingContext.riddl"
  include "DeliveryContext.riddl"
  include "LoyaltyContext.riddl"
  include "external-contexts.riddl"

} with {
  briefly "Restaurant operations domain"
  described by {
    | Covers all in-restaurant and customer-facing operations
    | including front-of-house, kitchen, bar, online ordering,
    | delivery, and loyalty program.
  }
}
```

## Bounded Contexts

| Context | Purpose | Entities | Details |
|---------|---------|----------|---------|
| [Front of House](front-of-house.md) | Reservations, table orders, billing | Reservation, TableOrder | Projector: ReservationBoard |
| [Kitchen](kitchen.md) | Ticket queue, station assignment, QC | KitchenTicket | Projector: KitchenDisplay |
| [Bar](bar.md) | Drink orders with push notifications | DrinkOrder | Solves melting-ice problem |
| [Online Ordering](online-ordering.md) | Menu browsing, cart, checkout | OnlineOrder | Decoupled from delivery |
| [Delivery](delivery.md) | Driver dispatch, GPS tracking | DeliveryOrder | Offline resilient |
| [Loyalty](loyalty.md) | Points accrual and redemption | LoyaltyAccount | Incremental rollout |

Plus two [external contexts](../external-contexts.md):
**PaymentGateway** and **NotificationService**.

## Cross-Context Communication

The contexts communicate through adaptors, not direct calls. This
diagram shows the message flow:

```
FrontOfHouse ──ToKitchen──► Kitchen ◄──FromOnlineOrdering── OnlineOrdering
     │                                                           │
     ├──ToBar──────────► Bar                                     ├──ToKitchen──► Kitchen
     │                                                           │
     ├──ToLoyalty──────► Loyalty ◄──FromPayment (dine-in)        ├──ToDelivery─► Delivery
     │                          ◄──FromOnlinePayment (online)    │
     └─────────────────────────────────────────────────────      └──ToLoyalty──► Loyalty
```

Key patterns:

- **Outbound adaptors** (`to`) route messages from one context to
  another — e.g., `FrontOfHouse.ToKitchen` sends food items to
  the Kitchen context
- **Inbound adaptors** (`from`) receive and transform messages
  from another context — e.g., `Kitchen.FromFrontOfHouse`
  converts submitted orders into kitchen tickets
- **Multiple sources** — Kitchen receives tickets from both
  FrontOfHouse (dine-in) and OnlineOrdering (online), each
  through its own adaptor

## Challenges Addressed

Based on the [personnel interviews](../scenario.md):

| Persona | Challenge | Context Solution |
|---------|-----------|-----------------|
| [Host](../personas/host.md) | Unresponsive reservations | FrontOfHouse with event sourcing |
| [Server](../personas/server.md) | Terminal contention | Async event-driven ordering |
| [Chef](../personas/chef.md) | Lost orders on crash | Kitchen with persistent tickets |
| [Cook](../personas/cook.md) | Illegible handwritten tickets | KitchenDisplay projector |
| [Bartender](../personas/bartender.md) | Drinks sit and ice melts | Bar push notifications |
| [Delivery Driver](../personas/delivery-driver.md) | App drops connectivity | Delivery offline resilience |
| [Online Customer](../personas/online-customer.md) | Website unreliable | OnlineOrdering isolation |

## Source

[`restaurant/domain.riddl`](https://github.com/ossuminc/riddl-models/tree/main/hospitality/food-service/reactive-bbq/restaurant)
