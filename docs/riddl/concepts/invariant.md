---
title: "Invariants"
draft: false
description: >-
  A logical expression that must always hold, declarable in any processor or
  inside an entity state body.
---

An invariant is a logical expression that must always hold true. Invariants
validate state changes in [entities](entity.md), or parameter values in
[functions](function.md).

## Syntax

As of RIDDL 2.0 an invariant's condition may be a structured
[boolean expression](value.md#boolean-expressions), not only an opaque quoted
string:

```riddl
invariant BalanceNonNegative is balance >= Zero
invariant InStock             is quantity > Zero
invariant Legacy              is "the account must be in good standing"
```

The quoted form remains available for rules that genuinely resist structure.

Because comparisons are reference-only, a threshold is named rather than
written inline:

```riddl
constant Zero is Natural = "0"
invariant BalanceNonNegative is balance >= Zero
```

## State-Scoped Invariants

An invariant may be declared inside an entity [state](state.md) body, where it
constrains that state's record-shaped data:

```riddl
entity Account is {
  initial state Open of record OpenData is {
    invariant BalanceNonNegative is balance >= Zero

    handler H is { ??? }
  }

  state Closed of record ClosedData is {
    invariant BalanceIsZero is balance == Zero
  }
}
```

This is what lets different states carry different rules — an open account may
hold any non-negative balance, while a closed one must hold exactly nothing.
An invariant declared at entity level instead applies in every state.

## Referencing an Invariant

A [handler](handler.md) asserts an invariant by name:

```riddl
on command Withdraw {
  require invariant BalanceNonNegative
  ???
}
```

!!! warning "Validation"
    An invariant defined but never referenced by any `require invariant`
    statement draws a **UsageWarning**. Declaring a rule the model never
    checks is almost always an oversight.

## Occurs In

* Any [processor](processor.md) — [entities](entity.md),
  [contexts](context.md), [repositories](repository.md),
  [projectors](projector.md), [adaptors](adaptor.md),
  [streamlets](streamlet.md)
* An entity [state](state.md) body
* [Modules](module.md)

## Contains

Nothing — but its condition is a [value](value.md).
