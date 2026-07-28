---
title: "States"
draft: false
---

A State defines a named state of an [entity](entity.md). It
references a **record** that defines the data structure
for the state, and optionally contains
[handlers](handler.md) and [invariants](invariant.md) that apply
while the entity is in that state.

!!! warning "A state is typed by a record, not by any type"
    As of RIDDL 2.0, `state X of …` takes a `record` reference specifically. A
    state is record-shaped data, so its data type must be a `record` rather
    than a plain `type` or a message. In 1.x any type reference was accepted.

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
initial state ActiveOrder of record ActiveOrderData is {
  invariant TotalIsPositive is total > Zero

  handler ActiveOrderHandler is {
    on command CancelOrder { ??? }
    on command ShipOrder { ??? }
  }
}
```

The state body is optional — a state can also be defined simply as:

```riddl
state ActiveOrder of record ActiveOrderData
```

## The `initial` Marker

An optional `initial` keyword marks the entity's starting state:

```riddl
entity Order is {
  initial state Pending of record PendingData is { ??? }
  state Active  of record ActiveData  is { ??? }
  state Shipped of record ShippedData is { ??? }
}
```

Without the marker, the first state *declared* is the starting state — which
means reordering states silently changes behavior. Marking it explicitly makes
the model safe to refactor, and is fully backward compatible with models that
omit it.

Declaring more than one `initial` state in an entity is an **Error**.

## State-Scoped Invariants

A state body may hold [invariants](invariant.md) constraining that state's
record data. This is what lets different states carry different rules — an
open account may hold any non-negative balance, while a closed one must hold
exactly nothing.

## Transitions

The `morph` statement transitions an entity from one state to another,
changing which handlers are active. Its payload is a **record** — the new
state's data — not the message that triggered the transition:

```riddl
on ship: command ShipOrder {
  morph entity Order to state Order.Shipped
    with record ShippedData(ship.trackingNumber)
}
```

## Occurs In
* [Entities](entity.md)

## Contains
* [Handlers](handler.md)
* [Invariants](invariant.md)
* [Comments](comment.md)
