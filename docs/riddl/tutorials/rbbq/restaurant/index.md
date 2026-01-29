---
title: "Restaurant Subdomain"
description: "Core restaurant operations in the Reactive BBQ domain model"
---

# Restaurant Subdomain

The Restaurant subdomain handles the core operations that occur within each
Reactive BBQ location. This is where customers interact with the restaurant
through the front-of-house staff and where food is prepared in the kitchen.

## Bounded Contexts

Based on the [personnel interviews](../scenario.md), we identify several
bounded contexts within the Restaurant subdomain:

### Front of House

Handles customer-facing operations:

- **Reservations** - Taking and managing table reservations
- **Seating** - Tracking table availability and seating guests
- **Ordering** - Taking food and drink orders at tables
- **Payment** - Processing bills and collecting payments

Key entities:
- `Table` - Physical table with capacity and status
- `Reservation` - Booking with time, party size, preferences
- `Order` - Collection of items for a table
- `Bill` - Itemized charges for an order

### Kitchen

Handles food preparation:

- **Order Queue** - Tracking orders to be prepared
- **Station Management** - Assigning cooks to stations
- **Quality Control** - Chef approval before serving

Key entities:
- `Ticket` - Kitchen's view of an order to prepare
- `Station` - Prep station (grill, fryer, salad, etc.)
- `MenuItem` - Recipe and preparation instructions

### Bar

Handles drink service:

- **Drink Orders** - Preparing drinks for tables and bar customers
- **Bar Tabs** - Tracking charges for bar customers
- **Inventory** - Managing bar stock

## Communication Patterns

The Restaurant subdomain uses event-driven communication:

```riddl
context FrontOfHouse is {
  entity Order is {
    handler OrderHandler is {
      on command PlaceOrder {
        // Emit event for kitchen
        send event OrderPlaced to Kitchen.OrderQueue
      }
    }
  }
}
```

When a server places an order, an `OrderPlaced` event is sent to the Kitchen
context, which adds it to the preparation queue. This decoupling means the
front-of-house doesn't block waiting for the kitchen.

## Challenges Addressed

This design addresses issues from the interviews:

| Challenge | Solution |
|-----------|----------|
| Slow order entry | Async event-driven, no blocking |
| Terminal contention | Servers can use mobile devices |
| System failures | Event sourcing enables recovery |
| Kitchen order loss | Persistent event log |

## Source Code

See the Restaurant subdomain implementation:
[restaurant/domain.riddl](https://github.com/ossuminc/riddl-examples/tree/main/src/riddl/ReactiveBBQ/restaurant)
