---
title: "Back Office Subdomain"
description: "Administrative operations in the Reactive BBQ domain model"
---

# Back Office Subdomain

The Back Office subdomain handles administrative and management functions
that support restaurant operations but aren't directly customer-facing.

## Bounded Contexts

### Scheduling

Manages staff schedules and shifts:

- **Shift Planning** - Creating weekly schedules
- **Time Tracking** - Recording hours worked
- **Coverage** - Ensuring adequate staffing

Key entities:
- `Employee` - Staff member with role and availability
- `Shift` - Time slot with required roles
- `Schedule` - Weekly assignment of employees to shifts

### Inventory

Tracks stock levels and supplies:

- **Stock Levels** - Current inventory counts
- **Reordering** - Automated low-stock alerts
- **Receiving** - Recording deliveries

Key entities:
- `InventoryItem` - Product with quantity and reorder point
- `StockTransaction` - Record of stock changes
- `PurchaseOrder` - Order to supplier

### Reporting

Generates management reports:

- **Sales Reports** - Daily, weekly, monthly summaries
- **Labor Reports** - Hours and costs by department
- **Inventory Reports** - Usage and waste tracking

## Integration Points

The Back Office subdomain integrates with:

- **Restaurant** - Receives sales data, provides schedules
- **Corporate** - Sends reports, receives policies

```riddl
context BackOffice is {
  adaptor RestaurantAdapter from context Restaurant is {
    // Transform Restaurant events into BackOffice commands
    on event SaleCompleted from Restaurant.FrontOfHouse {
      send command RecordSale to Reporting
    }
  }
}
```

## Challenges Addressed

| Challenge | Solution |
|-----------|----------|
| Report interference | Separate context, isolated resources |
| Peak hour impacts | Async processing, eventual consistency |
| Multi-timezone | Location-aware scheduling |

## Source Code

See the Back Office subdomain implementation:
[backoffice/domain.riddl](https://github.com/ossuminc/riddl-examples/tree/main/src/riddl/ReactiveBBQ/backoffice)
