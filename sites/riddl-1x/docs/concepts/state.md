---
title: "States"
draft: false
---

A State defines a named state of an [entity](entity.md). It
references a [type](type.md) that defines the data structure
for the state, and optionally contains
[handlers](handler.md) that define how messages are processed
while the entity is in that state.

An [entity](entity.md) can have multiple state definitions.
When an entity has multiple states with their own handlers,
it naturally models a
[Finite State Machine](https://en.wikipedia.org/wiki/Finite-state_machine)
—each state responds to messages differently. Use the
[finite state machine](entity.md#finite-state-machine)
[option](option.md) to make this intent explicit.

States are branches in the AST, meaning they can contain
their own definitions. The `morph` statement transitions an
entity from one state to another, changing which handlers
are active.

### Syntax

```riddl
state ActiveOrder of ActiveOrderData is {
  handler ActiveOrderHandler is {
    on command CancelOrder { ??? }
    on command ShipOrder { ??? }
  }
}
```

The state body (with handlers) is optional—a state can also
be defined simply as:

```riddl
state ActiveOrder of ActiveOrderData
```

## Occurs In
* [Entities](entity.md)

## Contains
* [Handlers](handler.md)
* [Comments](comment.md)
