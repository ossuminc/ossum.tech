---
title: "Sagas"
draft: false
---

A Saga is a distributed persistent transaction that uses the
[Saga Pattern](https://microservices.io/patterns/data/saga.html). Sagas are 
used to coordinate state changes across multiple components (typically 
entities) in a system. Every change (action) has a *compensating action* to 
undo the action. This permits an organized rollback if one component cannot 
proceed with the transaction.

## Signature

A saga's `requires` and `returns` may name an existing [type](type.md), the
same as a [function](function.md)'s:

```riddl
saga CheckoutProcess is {
  requires record CheckoutInputs
  returns  record CheckoutOutcome

  step ProcessPayment is {
    tell command ProcessPayment(orderId) to entity PaymentService
  } reverted by {
    tell command RefundPayment(orderId) to entity PaymentService
  }
} with {
  option is compensate
}
```

## Options

| Option | Meaning |
|--------|---------|
| `compensate` | On failure, run the accumulated steps' undo blocks in reverse |
| `parallel` | Start all steps at once; the coordinator gathers results asynchronously. Any one failure compensates in reverse order of the original sends. |

A saga is **sequential by definition**, so `parallel` declares the exception
and there is no `sequential` option — asking for the default said nothing, so
it was dropped in RIDDL 2.0.

Both options are contracts for the code generator rather than behavior
`riddlc` enforces.

## Scope

!!! warning "A saga stays within one domain"
    A saga orchestrates a multi-step transaction within **one bounded
    domain**. Every reference in a step — send/tell/yield message targets,
    `morph` entity and state, `become` entity and handler, `put` output, and
    any embedded `call` or `get` — must resolve to a definition within the
    saga's own enclosing [domain](domain.md).

    A reference resolving to a definition owned by a *different* domain
    crosses the saga's boundary and is an **Error**. A referent with no owning
    domain — a root or shared definition — is allowed.

!!! warning "A saga needs at least two steps"
    One step is an **Error**: *"Sagas must define at least 2 steps"*. A
    single-step transaction has nothing to coordinate and no ordering to
    compensate in reverse, so it wants a plain handler instead.

!!! warning "One failure point per step"
    A step's do/undo is all-or-nothing: the compensation assumes all or none
    of the do-block happened. So a step should have **at most one** potential
    failure point, and more than one draws a **Warning** suggesting the step
    be split.

    `send`, `tell`, `yield` and `put` can fail, and so can each embedded
    `call` or `get` — `let x = call F(get from input I)` counts as two.

## A Saga Is Not a Processor

A Saga extends the [vital definition](vital.md) base rather than
[Processor](processor.md), so it takes no [version](version.md) and no
[copyright](copyright.md).

It **does** bear [inlets](inlet.md) and [outlets](outlet.md) — a coordinator
has messages to receive and emit — so "not a processor" is about the version and
copyright scopes, not about ports. Its contents are exactly: steps, ports,
functions and includes.

## Occurs In
* [Contexts](context.md)
* [Domains](domain.md)
* [Modules](module.md)

## Contains
* [SagaStep](sagastep.md)
