---
title: "Corporate Domain"
description: "Corporate headquarters operations in the Reactive BBQ model"
---

# Corporate Domain

The Corporate domain handles operations that span all 500+
restaurant locations and are managed from headquarters. It contains
three bounded contexts and two external system integrations.

## Domain Definition

<!-- riddl: standalone -->
```riddl
domain Corporate is {
  author OssumInc is {
    name = "Ossum Inc."
    email = "info@ossuminc.com"
  } with {
    briefly "Author"
    described as {
      |Ossum Inc., creators of RIDDL.
    }
  }

  user CorporateHeadChef is "Head Chef managing recipes and menus"
  user ProcurementManager is "Manager handling vendor relationships"
  user MarketingManager is "Manager running promotions and campaigns"

  // include "MenuManagementContext.riddl", "SupplyChainContext.riddl",
  //         "MarketingContext.riddl", "external-contexts.riddl"

} with {
  briefly "Corporate operations domain"
  described as {
    |Covers menu management with atomic distribution to all locations,
    |supply chain and vendor management, and marketing campaigns.
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
