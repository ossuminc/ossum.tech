---
title: "BackOffice Domain"
description: "Administrative operations in the Reactive BBQ model"
---

# BackOffice Domain

The BackOffice domain handles administrative and management functions
that support restaurant operations but aren't directly
customer-facing. It contains three bounded contexts and two external
system integrations.

## Domain Definition

```riddl
domain BackOffice is {

  author OssumInc is {
    name is "Ossum Inc."
    email is "info@ossuminc.com"
  } with {
    briefly "Author"
    described by "Ossum Inc."
  }

  user Manager is "Restaurant manager overseeing daily operations" with {
    briefly "Manager"
    described by "Manages scheduling, inventory, and reporting."
  }

  user InventoryClerk is "Staff member managing stock" with {
    briefly "Inventory Clerk"
    described by "Receives shipments, tracks stock levels, and reorders."
  }

  include "SchedulingContext.riddl"
  include "InventoryContext.riddl"
  include "ReportingContext.riddl"
  include "external-contexts.riddl"

} with {
  briefly "Back office operations domain"
  described by {
    | Covers staff scheduling, inventory management, and
    | operational reporting. Reporting is isolated in its
    | own context with CQRS projectors so that report
    | generation never degrades peak-hour performance.
  }
}
```

Notice the `user` definitions at the domain level — Manager and
InventoryClerk are personas specific to back-office operations.

## Bounded Contexts

| Context | Purpose | Entities | Details |
|---------|---------|----------|---------|
| [Scheduling](scheduling.md) | Shift planning, time tracking | Shift | 6-command lifecycle |
| [Inventory](inventory.md) | Stock levels, consumption | InventoryItem | Kitchen integration |
| [Reporting](reporting.md) | Sales, labor, inventory reports | *(none)* | Pure CQRS projectors |

Plus two [external contexts](../external-contexts.md):
**HRSystem** and **AccountingSystem**.

## Cross-Context Integration

The BackOffice domain integrates with the Restaurant domain in
two key ways:

1. **Inventory ← Kitchen** — The Inventory context has a
   `FromKitchen` adaptor that listens for
   `PreparationStarted` events. When the kitchen begins
   preparing an order, stock is automatically consumed.
   No manual tracking needed.

2. **Reporting ← Everything** — The Reporting context has
   projectors that listen to events from multiple contexts:
    - `SalesReport` ← payment events from FrontOfHouse and
      OnlineOrdering
    - `LaborReport` ← clock-in/out events from Scheduling
    - `InventoryReport` ← stock events from Inventory

## Design Decisions

**Why isolate Reporting?** The CEO's interview revealed that
report generation was slowing down production systems during
peak hours. By making Reporting a pure CQRS read-model context
with only projectors (no entities), reports are built
asynchronously from events and never compete with production
workloads.

**Why separate Scheduling from HR?** The HR system is modeled
as an external context (`option is external`). Scheduling owns
the operational shift data while HR owns the master employee
records. This separation means scheduling works independently
even if the HR system is down.

## Source

[`backoffice/domain.riddl`](https://github.com/ossuminc/riddl-models/tree/main/hospitality/food-service/reactive-bbq/backoffice)
