---
title: "Corporate Domain"
description: "Corporate headquarters operations in the Reactive BBQ model"
---

# Corporate Domain

The Corporate domain handles operations that span all 500+
restaurant locations and are managed from headquarters. It contains
three bounded contexts and two external system integrations.

## Domain Definition

```riddl
domain Corporate is {

  author OssumInc is {
    name is "Ossum Inc."
    email is "info@ossuminc.com"
  } with {
    briefly "Author"
    described by "Ossum Inc."
  }

  user CorporateHeadChef is "Head Chef managing recipes and menus" with {
    briefly "Corporate Head Chef"
    described by "Develops recipes and coordinates monthly menu updates."
  }

  user ProcurementManager is "Manager handling vendor relationships" with {
    briefly "Procurement Manager"
    described by "Manages bulk ordering and supply chain operations."
  }

  user MarketingManager is "Manager running promotions and campaigns" with {
    briefly "Marketing Manager"
    described by "Creates and manages marketing campaigns."
  }

  include "MenuManagementContext.riddl"
  include "SupplyChainContext.riddl"
  include "MarketingContext.riddl"
  include "external-contexts.riddl"

} with {
  briefly "Corporate operations domain"
  described by {
    | Covers corporate-level functions including menu
    | management with atomic distribution to all locations,
    | supply chain and vendor management, and marketing
    | campaigns and promotions.
  }
}
```

The Corporate domain defines its own `user` personas:
CorporateHeadChef, ProcurementManager, and MarketingManager.

## Bounded Contexts

| Context | Purpose | Entities | Details |
|---------|---------|----------|---------|
| [Menu Management](menu-management.md) | Recipes, pricing, releases | MenuItem, MenuRelease | Atomic distribution |
| [Supply Chain](supply-chain.md) | Vendor ordering | PurchaseOrder | Bulk procurement |
| [Marketing](marketing.md) | Campaigns, promotions | Campaign | Multi-channel |

Plus two [external contexts](../external-contexts.md):
**PrintingService** and **PhotographyService**.

## Cross-Domain Integration

The Corporate domain publishes to the Restaurant domain:

- **MenuManagement → Restaurants** — The `ToRestaurants` adaptor
  distributes published menu releases atomically to all
  restaurant locations. This solves the Head Chef's monthly
  coordination bottleneck.

The Corporate domain also coordinates with BackOffice:

- **SupplyChain ↔ Inventory** — Purchase orders from Corporate
  supply chain result in stock receipts at individual restaurant
  inventory contexts.

## Design Decisions

**Why atomic menu distribution?** From the
[Head Chef interview](../personas/head-chef.md): monthly menu
updates required coordinating with printers, the website team,
and 500+ locations. The `MenuRelease` entity models this as an
atomic operation — menu changes are bundled into a release,
finalized, and published simultaneously to all locations.

**Why separate Marketing?** Marketing campaigns operate on
different timelines and with different stakeholders than menu
management. Keeping them separate means the marketing team
can create, schedule, and launch campaigns without touching
the menu management workflow.

## Source

[`corporate/domain.riddl`](https://github.com/ossuminc/riddl-models/tree/main/hospitality/food-service/reactive-bbq/corporate)
