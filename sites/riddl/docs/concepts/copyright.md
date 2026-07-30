---
title: "Copyright"
draft: false
description: >-
  A named legal notice carried verbatim, inherited by nearest declaring scope
  rather than composed.
---

# Copyright

Facts that apply across a *scope* are definitions in RIDDL, not metadata
options — the same principle that makes [author](author.md) and
[version](version.md) definitions. A `copyright` completes the set, after which
the rule "metadata options apply to the bearing definition only" holds without
exception.

A copyright is a **named** leaf carrying the notice verbatim:

```riddl
copyright House is "© 2026 Ossum Inc."
```

## The Notice Is the Whole String

The quoted string is the notice **in its entirety** — symbol, year and holder.
RIDDL does not decompose it into parts, because notices vary by jurisdiction,
by holder and by license, and any decomposition RIDDL imposed would be wrong
somewhere.

## Why It Is Named

Copyrights at lower scopes routinely **differ** — a vendored `external`
[context](context.md) bears a third party's notice — and vary in detail. The
name lets a documentation generator gather a model's distinct notices and
attribute each one properly in front matter, rather than emitting the same
string many times or guessing at identity.

## Nearest Wins

The copyright that **applies** to a definition is the one declared by the
definition itself or, failing that, by the **nearest ancestor** that declares
one.

```riddl
domain Shopping is {
  copyright House is "© 2026 Ossum Inc."

  context Ordering is {
    // applies: House
  }

  external context StripePayments is {
    copyright Stripe is "© 2026 Stripe, Inc."
    // applies: Stripe -- it OVERRIDES House, it is not appended to it
  }
}
```

This is the deliberate semantic difference from [version](version.md). A
version **composes** a coordinate out of every versioned ancestor; a copyright
does not accumulate at all. That is the whole point of allowing it at inner
scopes: an `external` context bearing a third party's notice must *override*
its enclosing domain's for everything inside it.

## Where Copyrights May Be Declared

The same nine scopes as [version](version.md): [Root](root.md),
[Module](module.md), [Domain](domain.md), and all six
[processors](processor.md) — [Adaptor](adaptor.md), [Context](context.md),
[Entity](entity.md), [Projector](projector.md), [Repository](repository.md) and
[Streamlet](streamlet.md).

A processor's messages form an API and therefore a contract, so attribution has
to be expressible per component. [Saga](saga.md) and [Function](function.md)
extend the vital-definition base rather than Processor, and are deliberately
excluded.

!!! warning "Validation"
    A scope declaring more than one copyright is an **Error**, reported at the
    second declaration.

!!! info "`copyright` as an identifier still works"
    Making `copyright` a keyword does not break models that use it as a field
    or type name. Keywords are not excluded from the identifier production.

## Occurs In

* [Root](root.md), [Module](module.md), [Domain](domain.md)
* All six [processors](processor.md)

## Contains

Nothing — it is a leaf definition.
