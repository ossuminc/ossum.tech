---
title: "Group"
draft: "false"
---

<!-- riddl-prelude
record CartLine is { sku is String, quantity is Natural }
type Clicked is Boolean
-->

A group is the abstract structuring concept for an application. Groups can be 
nested which allows them to form a hierarchy that defines the structure of a 
user interface. Each group can also contain UI elements such as 
[inputs](input.md) and
[outputs](output.md) as well as [types](type.md).
To make this more tangible, groups could be used to model the following 
implementation concepts:
* HTML forms, pages, containers, and sections
* mobile application screens, pages, forms and containers
* accordions (vertically stacked list of items with show/hide functionality)
* a spatial **zone** in a 3D or AR scene
* a **voice** dialogue turn, which has structure but no pixels

A UI designer is free to arrange the contained
elements in any fashion, but presumably in a way that is consistent with
their overall UI design theme.

!!! info "The triad is modality-free, and that is the point"
    It is tempting to read [group](group.md), [input](input.md) and
    [output](output.md) as *container*, *widget* and *widget* — screen things.
    They are not. The triad is the **modality-free logical core**: something
    is acquired from a user, something is presented to them, and things are
    grouped for cohesion. None of that mentions a screen.

    The alias sets say so out loud. A group may be a `scene`, a `space` or a
    `zone`; an input may be `voice`, `gesture` or `gaze`; an output may be
    `sound`, `speech` or `haptic`. A model that `speaks` a confirmation and
    `vibrates` on error is using exactly the same three concepts as one that
    renders a form — which is what lets a single model target a screen, a
    voice assistant and a headset without restructuring.

    The aliases are **closed lists** and carry **no structural difference**:
    they are directional heuristics for the reader and for a generator's
    choice of representation.

## Aliases

A group may be written with any of these keywords, all of which mean the same
thing structurally. Pick whichever reads best for what you are modeling:

`group`, `page`, `pane`, `dialog`, `menu`, `popup`, `frame`, `column`,
`window`, `section`, `tab`, `flow`, `block`, `scene`, `space`, `zone`

<!-- riddl: in-app-context -->
```riddl
page ShoppingCart is {
  list Items shows record CartLine
  button Checkout activates type Clicked
}
```

!!! warning "Groups require an application context"
    A group — under any of its aliases — may only appear in a
    [Context](context.md) declared with the `application`
    [intention](context.md#intention). A group in any other context is a hard
    **Error** as of RIDDL 2.0. In 1.x, any context containing a group was
    treated as an application.

## Design References

A group may carry a [figma reference](metadata.md#figma-references) linking it
to the exact frame that depicts it:

<!-- riddl: in-app-context -->
```riddl
page Checkout is { ??? } with {
  figma "aBcD1234" node "42:1337"
}
```

## Occurs In
* [Application](application.md) contexts
* [Group](group.md)

## Contains

```mermaid
flowchart TD
    Group(["Group"]) -->|nested| Group
    Group --> Input
    Group --> Output
    Group --> Defs["contains · shown by · Comment"]
```

* [Group](group.md) :material-recycle: — nested groups, and `contains` references to groups defined elsewhere
* [Input](input.md) and [Output](output.md)
* `shown by`, [Comment](comment.md)

