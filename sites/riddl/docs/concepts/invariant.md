---
title: "Invariants"
draft: false
description: >-
  A named business rule that must always hold — checked implicitly as a
  precondition before every effect in its declaring scope.
---

<!-- riddl-domain-prelude
command PlaceOrder is { note is String }
-->
<!-- riddl-prelude
constant Zero is Whole = 0
constant minimumFee is Natural = 5
record OpenData is { balance is Natural, quantity is Natural,
  holdAmount is Natural }
record ClosedData is { balance is Natural }
record AvailIn is { held is Natural, total is Natural }
command Withdraw is { amount is Natural }
command PlaceOrder is { note is String }
event PaymentReversed is { note is String }
command FlagForReview is { reason is String }
entity Review is { ??? }
function Available is { requires AvailIn returns AvailIn ??? }
-->

An invariant is a named business rule: a boolean condition that must always be
true. Naming it is what promotes the rule from a comment in somebody's code to a
citizen of the model — something a domain expert can review and the tooling can
enforce.

## Invariants Apply Implicitly

**An invariant applies to every clause of the scope that declares it**, checked
as a *precondition* before any effect in that clause. Nothing at the point of
use turns it on:

<!-- riddl: in-context -->
```riddl
entity Account is {
  invariant BalanceNonNegative is balance >= Zero

  state Open of record OpenData is {
    handler Transacting is {
      on command Withdraw {
        // BalanceNonNegative is checked here, before anything below runs
        ???
      }
    }
  }
}
```

!!! warning "Changed in RIDDL 2.0"
    Previously an invariant did nothing unless some clause named it in a
    `require invariant X` statement. That made it easy — and common — to carry a
    constraint that *read* as enforced and was inert: an unreferenced invariant
    generated no code, so the rule existed only as prose. Implicit application
    closes that gap.

    If you have models written against the old rule, they get **stronger**, not
    broken: constraints you declared now actually hold.

Every invariant applies, including ones you also `require` explicitly. The
alternative — "only unreferenced invariants apply everywhere" — would mean that
adding one `require invariant X` to a single clause silently narrowed X from
enforced-everywhere to enforced-there, weakening every other clause with an edit
that reads like it strengthens the model.

## The Condition Has Three Forms

<!-- riddl: in-entity -->
```riddl
invariant Legacy      is "the account must be in good standing"   // 1
invariant InStock     is quantity >= Zero                          // 2
invariant CanCoverFee is {                                         // 3
  let available = call function Available(held = holdAmount, total = balance)
  available >= minimumFee
}
```

1. A **literal string** — natural language. This is an AI-fill site: the
   generator emits a marker and an AI assistant writes the predicate from the
   description, with the state's type structure as context.
2. A **[boolean expression](value.md#boolean-expressions)** — the structured
   sub-language. Not an AI-fill site; it already *is* the predicate.
3. A **block** — pure statements followed by the boolean expression that is the
   predicate.

The block form earns its place by giving you `let` bindings and calls to pure
[functions](function.md), which is the difference between a condition you can
express and one you must write as English and hope is read the same way twice.
It also lowers cleanly: a block-form invariant becomes a private boolean method,
exactly the shape a call site wants.

Because comparisons are reference-only, a threshold is named rather than written
inline:

<!-- riddl: in-entity no-prelude=Zero -->
```riddl
constant Zero is Whole = 0
invariant BalanceNonNegative is balance >= Zero
```

!!! warning "No numeric literals, and no arithmetic"
    The boolean sub-language has no numeric literal atom, so `amount >= 0` does
    not parse. Nor is arithmetic available inside a block: a `let` binds a
    reference or a `call`, never an expression such as `balance - holdAmount`.
    Both limitations predate the 2.0 invariant work.

## Scope: Where It Applies, and What It May Read

These are the same question, and the answer is in the declaration — never at the
call site. An invariant may declare `requires <state-ref | type-ref>` to narrow
or redirect that scope. There is no `returns`: the condition ends in a boolean,
so the result type is fixed by construction.

| Declaration | Applies to | May read |
|---|---|---|
| in an **[entity](entity.md)**, no `requires` | every clause of that entity, including its states' handlers | fields present in **every** state record |
| inside a **[state](state.md) S** | that state's handlers only | S's record fields |
| in an entity, `requires state S` | that entity's clauses **while in state S** | S's record fields |
| `requires <type T>` | nothing implicitly — **explicit only** | the value handed to it |
| on a **[context](context.md)** or other stateless processor | nothing implicitly — **explicit only** | the value handed to it |

State scoping is what lets different states carry different rules — an open
account may hold any non-negative balance, while a closed one must hold exactly
nothing:

<!-- riddl: in-context -->
```riddl
entity Account is {
  initial state Open of record OpenData is {
    invariant BalanceNonNegative is balance >= Zero

    handler Transacting is { ??? }
  }

  state Closed of record ClosedData is {
    invariant BalanceIsZero is balance == Zero

    handler Settling is { ??? }
  }
}
```

The same narrowing can be written from the entity level instead, which keeps
related rules together where an author would rather read them side by side:

<!-- riddl: in-context -->
```riddl
entity Account is {
  invariant BalanceNonNegative requires state Open   is balance >= Zero
  invariant BalanceIsZero      requires state Closed is balance == Zero

  initial state Open   of record OpenData   is { handler Transacting is { ??? } }
  state         Closed of record ClosedData is { handler Settling    is { ??? } }
}
```

### The Intersection Rule

An entity-level invariant reading `balance` forces **every** state record of that
entity to have a `balance` field. Referencing a field that any state record
lacks is an **Error** — the invariant would otherwise be unevaluable in some
states while claiming to hold in all of them, which is exactly the
inert-constraint problem implicit application exists to remove.

An entity with no states cannot carry an entity-level invariant that reads fields
at all.

## Stateless Processors Are Explicit-Only

A [context](context.md), [adaptor](adaptor.md), [projector](projector.md),
[streamlet](streamlet.md) or [repository](repository.md) has no state, so there
is no ambient data for an implicit predicate to read. An invariant declared there
must name what it needs with `requires <type T>` and be invoked explicitly, with
the clause supplying the value:

<!-- riddl: in-domain -->
```riddl
context Ordering is {
  record Limits is { ceiling: Integer, used: Integer }

  invariant UnderLimit requires record Limits is used <= ceiling

  handler Intake is {
    on command PlaceOrder {
      require invariant UnderLimit with record Limits(ceiling = "10", used = "1")
    }
  }
}
```

The division of labour is the point: **the clause gathers, the invariant
receives.**

## Restating a Check with `require`

A [handler](handler.md) may still name an invariant explicitly:

<!-- riddl: in-clauses -->
```riddl
on command Withdraw {
  require invariant BalanceNonNegative
  do "apply the withdrawal"
}
```

This is a **restatement**, not a restriction. The invariant was already going to
run. Write it when you want the check called out at a particular point — or when
the invariant declares `requires <type T>` and the value has to be handed in,
which is the one case where the `require` is doing work nothing else can do.

## An Invariant Never Acquires — It Only Receives

An invariant block may contain only the statements a pure
[function](function.md) may contain: **no state writes, no `send` or `tell`, no
`morph`, `become`, `yield` or `reply`.** With the no-loops rule that makes the
block structurally terminating.

The prohibition on `send` catches people out, because a read-only query looks
harmless. It is not, and the reason is not mutation — it is that a send would
break four properties a precondition depends on:

- it becomes **asynchronous**, so the whole refusal window goes async and every
  mutating command acquires a `Future`-shaped signature;
- it becomes **fallible** — a timeout gives the predicate a third outcome
  besides true and false;
- it becomes **non-deterministic and TOCTOU-prone** — remote state can change
  between the check and the effect, so the invariant is *sampled* rather than
  enforced, and the model claims a guarantee it does not have;
- it stops being **structurally terminating**, because an unbounded wait removes
  the termination guarantee.

Gathering belongs in the clause, where sending is already legal and already
modeled.

!!! note "How this differs from a function's purity"
    The *effect* prohibitions are identical, but a [function](function.md) may
    read no entity state at all — everything arrives through its `requires`
    message. An invariant **may** read state, bounded by the table above. That
    asymmetry is sound because an invariant is by definition a predicate over
    state, is evaluated inside the entity's single-writer window, and has its
    readable fields fixed by its declaration, so the reads stay statically
    checkable.

## When an Invariant Fails

The same predicate means two different things depending on how it was applied,
and the distinction matters because it decides whether the failure is part of
your clause's contract:

| Applied | Failure is a | Meaning |
|---|---|---|
| explicitly, at `require invariant X` | **refusal** | a modeled, expected outcome — comes back as an error result naming the rule |
| implicitly | **fault** | the model never asserted this mutation preserves X, so the violation is a defect: exception plus rollback |

A fault does **not** widen the clause's result type. That is deliberate: making
every implicit check a modeled outcome would force every mutating command into
an `Outcome<…>` signature for something that a validated model cannot produce.

Multiple invariants in scope are checked in declaration order, and the first
failure is the one reported.

### Lifecycle and Event Clauses

- **`on init` is skipped.** That clause is where state comes into existence, so
  a precondition over it is ill-defined and would fail on every entity creation.
- **`on term` applies** — state still exists there.
- **`on event` clauses apply**, which is not a contradiction of the rule that
  *authored* `require` and `error` statements are forbidden there. That rule
  bars **refusing** an event, because an event is a fact already accepted
  elsewhere. An implicit violation faults and rolls back; it does not refuse,
  and the event remains a fact. Excluding event clauses would have been worse —
  state changes in event clauses, so an invariant unchecked there would mean
  "always true except where the state actually moves".

### Reacting Instead of Faulting

When an event handler should *respond* to a rule being false rather than fault,
name the invariant in a [`when`](statement.md#when-statement) and take action:

<!-- riddl: in-clauses -->
```riddl
on event PaymentReversed {
  when not invariant BalanceNonNegative then
    tell command FlagForReview(reason = "balance went negative") to entity Review
  end
}
```

The `invariant` keyword is optional here — bare `when not BalanceNonNegative
then` is identical — but spelling it out matches `require invariant X` and
reads as what it is. Either form composes like any other boolean (`when
invariant BalanceNonNegative and order.isPaid then`), and both are resolved
and checked: naming an invariant that does not exist is an Error.

!!! note "A condition asks; a `require` applies"
    A condition never has to hand an invariant its data — even one declaring
    `requires <type>`, where `with <expr>` is optional. `require invariant X`
    is the asymmetric one: it *applies* the rule, so it must be given what the
    rule reads. Asking whether something holds and enforcing it are different
    acts. Verified against `2.0.0-rc.9-54`.

## Diagnostics

An invariant that can never run is precisely the defect implicit application
exists to remove, so riddlc says so rather than passing silently:

- an invariant declaring `requires <type T>` that no `require invariant X with
  <expr>` ever invokes draws a **warning** — it is inert;
- an entity-level invariant referencing a field absent from any state record is
  an **Error** (the intersection rule above).

## Occurs In

* Any [processor](processor.md) — [entities](entity.md),
  [contexts](context.md), [repositories](repository.md),
  [projectors](projector.md), [adaptors](adaptor.md),
  [streamlets](streamlet.md)
* An entity [state](state.md) body
* [Modules](module.md)

## Contains

Nothing — but its condition is a [value](value.md), and its block form contains
[statements](statement.md).
