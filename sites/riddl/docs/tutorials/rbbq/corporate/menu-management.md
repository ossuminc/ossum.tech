---
title: "Menu Management Context"
description: "Recipe development, pricing, and atomic menu distribution"
---

<!-- riddl-domain-prelude
context FrontOfHouse is {
  command RecordMenuItem is { menuItemId: String(1,50) }
}
-->

<!-- riddl-prelude
type MenuItemId is Id(MenuItem)
type MenuCategory is String(1,60)
record StoredMenuItem is { menuItemId: MenuItemId }
event MenuItemCreated is { menuItemId: MenuItemId }
event PriceSet is { menuItemId: MenuItemId }
event SetPriceRejected is { menuItemId: MenuItemId, rejectionReason: String(1,500) }
type MenuItemEvent is MenuItemCreated | PriceSet | SetPriceRejected
entity MenuItem is { ??? }
repository MenuItemRepository is { ??? }
command PersistPriceSet is { menuItemId: MenuItemId }
event ReleasePublished is { releaseId: UUID }
entity MenuRelease is { ??? }
-->

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

<!-- riddl: in-context no-prelude=MenuItemId,MenuCategory -->
```riddl
type MenuItemId is Id(MenuItem)

type MenuCategory is String(1,60)
```

Note the `RecipeInfo` record uses `Duration` for prep and cook
times — a RIDDL predefined type — and `many String` for the
ingredients list.

## Entity: MenuItem

The `MenuItem` entity manages individual menu items:

<!-- riddl: in-context no-prelude=MenuItem,MenuItemCreated,PriceSet,SetPriceRejected,MenuItemCommand,MenuItemEvent -->
```riddl
event-sourced entity MenuItem as flow is {

  // An event-sourced entity OWNS the commands and events that change it, so
  // they are declared INSIDE it, and every command names the event it yields.
  command CreateMenuItem yields event MenuItemCreated is { menuItemId: MenuItemId }
  command SetPrice yields event PriceSet is { menuItemId: MenuItemId }

  event MenuItemCreated is { menuItemId: MenuItemId }
  event PriceSet is { menuItemId: MenuItemId }
  event SetPriceRejected is { menuItemId: MenuItemId, rejectionReason: String(1,500) }

  record MenuItemData is { menuItemId: MenuItemId }

  // Lifecycle phases are named STATES, not a status field: each state
  // declares the commands it accepts, so the compiler knows the machine.
  initial state ActiveMenuItem of record MenuItemData is {
    handler ActiveMenuItemHandler is {
      on cmd: command SetPrice is {
        yield event PriceSet(menuItemId = cmd.menuItemId)
      }
      // `set` and `morph` may appear ONLY in an `on event` clause here:
      // replay has to re-apply exactly the same change.
      on evt: event PriceSet is {
        morph entity MenuItem to state Priced
          with record MenuItemData(menuItemId = evt.menuItemId)
      }
    }
  }

  state Priced of record MenuItemData is {
    handler PricedHandler is {
      // A command this state does not accept is refused -- and the refusal
      // is PUBLISHED before it is raised, so the attempt is recorded.
      on cmd: command SetPrice is {
        send event SetPriceRejected(menuItemId = cmd.menuItemId,
          rejectionReason = "MenuItem does not accept SetPrice in this state")
          to outlet MenuItemEvents
        error "MenuItem does not accept SetPrice in this state"
      }
    }
  }

  // A processor receives on its OWN inlet and publishes on its OWN outlet,
  // and a portlet's type must ADMIT everything that travels on it.
  type MenuItemCommand is CreateMenuItem | SetPrice
  type MenuItemEvent is MenuItemCreated | PriceSet | SetPriceRejected

  inlet MenuItemCommands is type MenuItemCommand
  outlet MenuItemEvents is type MenuItemEvent
}
```

Note that `UpdateMenuItem` uses `optional` fields — you can
update the name, description, or recipe independently without
providing all fields every time.

## Entity: MenuRelease

The `MenuRelease` entity is the key innovation — it bundles
menu changes into an atomic release:

<!-- riddl: in-context no-prelude=MenuRelease,ReleasePublished -->
```riddl
// A release is its own entity because the ATOMIC unit is the whole menu, not
// one item: 500+ locations must flip together or the chain is inconsistent.
event-sourced entity MenuRelease as flow is {
  command PublishRelease yields event ReleasePublished is { releaseId: UUID }
  event ReleasePublished is { releaseId: UUID }

  record MenuReleaseData is { releaseId: UUID }

  initial state ActiveRelease of record MenuReleaseData is {
    handler ActiveReleaseHandler is {
      on cmd: command PublishRelease is {
        yield event ReleasePublished(releaseId = cmd.releaseId)
      }
      on evt: event ReleasePublished is {
        set field MenuReleaseData.releaseId to "the published release id"
      }
    }
  }

  type MenuReleaseEvent is ReleasePublished
  inlet MenuReleaseCommands is type PublishRelease
  outlet MenuReleaseEvents is type MenuReleaseEvent
}
```

The lifecycle: **Create → Add Items → Finalize → Publish →
(optional) Rollback**. The `releaseAction` field on
`AddItemToRelease` supports different actions per item: add,
update, remove, or price-change.

The `ReleasePublished` event is the key moment:

<!-- riddl: in-context no-prelude=ReleasePublished -->
```riddl
event ReleasePublished is {
  releaseId: UUID
  releaseEffectiveAt: TimeStamp
  releaseItemCount: Natural
}
```

## Repositories

<!-- riddl: in-context no-prelude=MenuItemRepository,StoredMenuItem,PersistPriceSet -->
```riddl
repository MenuItemRepository as flow is {
  inlet MenuItemRepositoryFromMenuItem is type MenuItemEvent
  outlet MenuItemRepositoryResponses is type MenuItemEvent

  record StoredMenuItem is { menuItemId: MenuItemId }

  // A repository that answers queries and declares NO index at all is a
  // sequential scan by construction, and draws a warning saying so.
  schema MenuItemSchema is relational
    of rows as type StoredMenuItem
      index on field StoredMenuItem.menuItemId

  command PersistPriceSet is { menuItemId: MenuItemId }

  handler MenuItemPersistence is {
    on command PersistPriceSet is {
      do "update the stored menuItem row for this menuItemId"
    }
    // An inlet admitting an alternation needs a clause that receives it.
    // Handling each member is not enough -- say what ARRIVING means.
    on other is {
      do "persist whatever else arrives on this inlet"
    }
  }
}
```

## Adaptor

Menu Management has an outbound adaptor for distributing menus:

<!-- riddl: in-domain -->
```riddl
context MenuManagement is {
  // An adaptor is the translation seam at a context boundary: it is the only
  // place that knows the OTHER context's message shapes.
  adaptor ToRestaurants to context FrontOfHouse is {
    handler ToRestaurantsIntake is {
      on command FrontOfHouse.RecordMenuItem is {
        do "push the published menu to every location at once"
      }
      // Every adaptor handler must say what it does with what it does not
      // recognise. Silence is not an option in 2.0.
      on other is {
        error "Unexpected message from FrontOfHouse"
      }
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
