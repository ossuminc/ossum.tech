---
title: "Menu Management Context"
description: "Recipe development, pricing, and atomic menu distribution"
---

# Menu Management Context

The Menu Management context manages the corporate menu lifecycle
including recipe development, pricing, and atomic menu
distribution to all 500+ locations via the `MenuRelease` entity.
It addresses the Head Chef's monthly coordination bottleneck by
enabling versioned, atomic menu updates.

## Purpose

Every month, the Head Chef develops new recipes, adjusts pricing,
and needs to distribute the updated menu simultaneously to all
locations, the website, the printing service, and the photography
service. Previously, this required manual coordination across
multiple teams and systems.

## Interview Connection

From the [Head Chef's interview](../personas/head-chef.md):

> "The menu is decided on monthly and distributed via email."

> "The biggest headache is coordinating the monthly menu update
> across all locations, the website, the printers..."

The `MenuRelease` entity models this as an atomic operation:
changes are bundled, reviewed, and published simultaneously.

## Types

```riddl
type MenuItemId is Id(MenuManagement.MenuItem) with {
  briefly "Menu item identifier"
  described by "Unique identifier for a corporate menu item."
}

type MenuReleaseId is Id(MenuManagement.MenuRelease) with {
  briefly "Menu release identifier"
  described by "Unique identifier for a menu release."
}

type MenuItemCategory is any of {
  Appetizer,
  Entree,
  Side,
  Dessert,
  Beverage,
  Special
} with {
  briefly "Menu item category"
  described by "Category of the menu item."
}

type MenuItemLifecycle is any of {
  Draft,
  Active,
  Seasonal,
  Retired
} with {
  briefly "Menu item lifecycle"
  described by "Current lifecycle stage of a menu item."
}

type MenuReleaseStatus is any of {
  ReleaseDraftStatus,
  ReleaseFinalizedStatus,
  ReleasePublishedStatus,
  ReleaseRolledBackStatus
} with {
  briefly "Menu release status"
  described by "Current status of a menu release."
}

type RecipeInfo is {
  recipeInstructions is String(1, 5000)
  recipeIngredients is many String(1, 200)
  prepTime is Duration
  cookTime is Duration
  servings is Natural
} with {
  briefly "Recipe information"
  described by "Recipe details for a menu item."
}

type PriceInfo is {
  basePrice is Decimal(8, 2)
  costToMake is Decimal(8, 2)
  marginPercent is Decimal(5, 2)
} with {
  briefly "Price information"
  described by "Pricing and cost details for a menu item."
}
```

Note the `RecipeInfo` record uses `Duration` for prep and cook
times — a RIDDL predefined type — and `many String` for the
ingredients list.

## Entity: MenuItem

The `MenuItem` entity manages individual menu items:

```riddl
entity MenuItem is {

  command CreateMenuItem is {
    menuItemId is MenuItemId
    menuItemName is String(1, 200)
    menuItemCategory is MenuItemCategory
    menuItemDescription is String(1, 1000)
    recipe is RecipeInfo
    pricing is PriceInfo
  }

  command UpdateMenuItem is {
    menuItemId is MenuItemId
    updatedName is optional String(1, 200)
    updatedDescription is optional String(1, 1000)
    updatedRecipe is optional RecipeInfo
  }

  command SetPrice is {
    menuItemId is MenuItemId
    updatedPricing is PriceInfo
    effectiveDate is Date
  }

  command RetireMenuItem is {
    menuItemId is MenuItemId
    retiredReason is String(1, 500)
  }

  // Events: MenuItemCreated, MenuItemUpdated, PriceSet,
  //         MenuItemRetired

  state ActiveMenuItem of MenuItem.MenuItemStateData

  handler MenuItemHandler is {
    on command CreateMenuItem {
      morph entity MenuManagement.MenuItem to state
        MenuManagement.MenuItem.ActiveMenuItem
        with command CreateMenuItem
      tell event MenuItemCreated to
        entity MenuManagement.MenuItem
    }
    on command UpdateMenuItem {
      tell event MenuItemUpdated to
        entity MenuManagement.MenuItem
    }
    on command SetPrice {
      tell event PriceSet to
        entity MenuManagement.MenuItem
    }
    on command RetireMenuItem {
      tell event MenuItemRetired to
        entity MenuManagement.MenuItem
    }
  }
}
```

Note that `UpdateMenuItem` uses `optional` fields — you can
update the name, description, or recipe independently without
providing all fields every time.

## Entity: MenuRelease

The `MenuRelease` entity is the key innovation — it bundles
menu changes into an atomic release:

```riddl
entity MenuRelease is {

  command CreateMenuRelease is {
    menuReleaseId is MenuReleaseId
    releaseName is String(1, 200)
    releaseDescription is String(1, 1000)
    effectiveDate is Date
  }

  command AddItemToRelease is {
    menuReleaseId is MenuReleaseId
    releaseMenuItemId is MenuItemId
    releaseAction is String(1, 50)
  }

  command FinalizeRelease is {
    menuReleaseId is MenuReleaseId
    finalizedAt is TimeStamp
  }

  command PublishRelease is {
    menuReleaseId is MenuReleaseId
    publishedAt is TimeStamp
  }

  command RollbackRelease is {
    menuReleaseId is MenuReleaseId
    rollbackReason is String(1, 500)
    rolledBackAt is TimeStamp
  }

  // Events: MenuReleaseCreated, ItemAddedToRelease,
  //         ReleaseFinalized, ReleasePublished, ReleaseRolledBack

  state ActiveRelease of MenuRelease.MenuReleaseStateData

  handler MenuReleaseHandler is {
    on command CreateMenuRelease {
      morph entity MenuManagement.MenuRelease to state
        MenuManagement.MenuRelease.ActiveRelease
        with command CreateMenuRelease
      tell event MenuReleaseCreated to
        entity MenuManagement.MenuRelease
    }
    // ... remaining commands follow tell pattern
  }
}
```

The lifecycle: **Create → Add Items → Finalize → Publish →
(optional) Rollback**. The `releaseAction` field on
`AddItemToRelease` supports different actions per item: add,
update, remove, or price-change.

The `ReleasePublished` event is the key moment:

```riddl
event ReleasePublished is {
  menuReleaseId is MenuReleaseId
  releaseName is String(1, 200)
  effectiveDate is Date
  publishedAt is TimeStamp
} with {
  briefly "Release published"
  described by {
    | Emitted when a menu release is published to all
    | locations. This is the atomic distribution event
    | that updates menus chain-wide simultaneously.
  }
}
```

## Repositories

```riddl
repository MenuItemRepository is {
  schema MenuItemData is relational
    of menuItems as MenuItem
    index on field MenuItem.menuItemId
    index on field MenuItem.menuItemCategory
    index on field MenuItem.menuItemLifecycle
}

repository MenuReleaseRepository is {
  schema MenuReleaseData is relational
    of releases as MenuRelease
    index on field MenuRelease.menuReleaseId
    index on field MenuRelease.menuReleaseStatus
}
```

## Adaptor

Menu Management has an outbound adaptor for distributing menus:

```riddl
adaptor ToRestaurants to context Restaurant.FrontOfHouse is {
  handler MenuDistribution is {
    on command Restaurant.FrontOfHouse.TableOrder.CreateOrder {
      prompt "Distribute published menu updates to restaurant locations"
    }
  }
}
```

## Design Decisions

**Why atomic releases instead of individual item updates?**
Updating menu items one at a time risks inconsistency — some
locations might have the new price while others still show the
old one. The `MenuRelease` entity bundles all changes and
publishes them atomically, ensuring all 500+ locations update
simultaneously.

**Why separate MenuItem and MenuRelease entities?** MenuItems
represent the master catalog and evolve over time. MenuReleases
are point-in-time snapshots of changes to be distributed. An
item might be updated many times before being included in a
release.

**Solving the coordination bottleneck:** The Head Chef
described a manual process involving email coordination with
printers, web teams, and locations. The `MenuRelease` entity
replaces this with a structured workflow: draft → add items →
finalize (review gate) → publish (atomic distribution) → optional
rollback.

## Source

- [`MenuManagementContext.riddl`](https://github.com/ossuminc/riddl-models/tree/main/hospitality/food-service/reactive-bbq/corporate/MenuManagementContext.riddl)
- [`menu-types.riddl`](https://github.com/ossuminc/riddl-models/tree/main/hospitality/food-service/reactive-bbq/corporate/menu-types.riddl)
- [`MenuItem.riddl`](https://github.com/ossuminc/riddl-models/tree/main/hospitality/food-service/reactive-bbq/corporate/MenuItem.riddl)
- [`MenuRelease.riddl`](https://github.com/ossuminc/riddl-models/tree/main/hospitality/food-service/reactive-bbq/corporate/MenuRelease.riddl)
