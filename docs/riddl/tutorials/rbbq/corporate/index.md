---
title: "Corporate Subdomain"
description: "Corporate headquarters operations in the Reactive BBQ domain model"
---

# Corporate Subdomain

The Corporate subdomain handles operations that span all restaurant locations
and are managed from the corporate headquarters.

## Bounded Contexts

### Menu Management

Centralized menu control as described by the [Head Chef](../personas/head-chef.md):

- **Recipe Development** - Creating and testing new dishes
- **Menu Updates** - Monthly menu changes
- **Pricing** - Setting prices across locations

Key entities:
- `Recipe` - Ingredients, preparation, and presentation
- `MenuItem` - Menu item with description and price
- `MenuRelease` - Scheduled menu update

### Supply Chain

Manages ingredient sourcing and distribution:

- **Vendor Management** - Approved supplier relationships
- **Bulk Ordering** - Centralized purchasing
- **Distribution** - Shipping to restaurants

Key entities:
- `Vendor` - Approved supplier with contracts
- `BulkOrder` - Large-scale purchase order
- `Shipment` - Delivery to restaurant locations

### Marketing

Coordinates brand and promotional activities:

- **Menu Photography** - Professional food images
- **Promotions** - Special offers and campaigns
- **Loyalty Program** - Customer rewards (planned feature)

## Integration Patterns

Corporate communicates with restaurants through message-based integration:

```riddl
context MenuManagement is {
  entity Menu is {
    handler MenuHandler is {
      on command PublishMenu {
        // Broadcast to all restaurant locations
        send event MenuPublished to all Restaurant.Kitchen
      }
    }
  }
}
```

The menu update process uses a publish/subscribe pattern so that:
- All locations receive updates simultaneously
- Individual locations can't be in inconsistent states
- Updates are atomic - either applied completely or not at all

## Challenges Addressed

From the [CEO interview](../personas/ceo.md):

| Challenge | Solution |
|-----------|----------|
| Menu coordination | Event-driven distribution |
| Loyalty program risk | Isolated context, incremental rollout |
| Electronic menu feasibility | Same menu data, different presentations |

## Source Code

See the Corporate subdomain implementation:
[corporate/domain.riddl](https://github.com/ossuminc/riddl-examples/tree/main/src/riddl/ReactiveBBQ/corporate)
