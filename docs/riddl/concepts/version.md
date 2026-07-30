---
title: "Version"
draft: false
description: >-
  A leaf definition contributing one component to a scope's composed version
  coordinate.
---

# Version

Facts that apply across a *scope* are definitions in RIDDL, not metadata
options — the same principle that makes [author](author.md) a definition. A
`version` is one of those.

A version's component is **either a name or a natural number**, never both:

<!-- riddl: skip reason="illustrative fragment; references vocabulary this page does not define" -->
```riddl
version Garibaldi
version 4
```

Organizations routinely name their releases — Ubuntu's "Jammy Jellyfish", the
Android desserts — so both forms are first class and may be mixed freely across
scopes. The name uses the ordinary identifier production rather than a quoted
string, so a composed coordinate can never contain characters a generator would
have to sanitize.

## Composition

A definition's precise version is **composed** from the versions its ancestors
declare, root to leaf, joined with `.`:

<!-- riddl: skip reason="illustrative fragment; references vocabulary this page does not define" -->
```riddl
domain Garibaldi is {
  version Garibaldi
  context Ordering is {
    version 4
    entity Order is {
      version 3
    }
  }
}
```

The `Order` entity's composed version is `Garibaldi.4.3`.

A [type](type.md), a [message](message.md) or a [handler](handler.md) declares
no version scope of its own, so it simply reports its container's coordinate.
That is deliberate: types are notoriously hard to attach metadata to, and some
have no body at all.

### The missing-level rule

Only scopes that actually **bear** a version contribute a component. The same
model with an unversioned context composes to `Garibaldi.3`.

This is what makes adoption incremental: version the domain first, refine
inward later, and nothing breaks in between.

## Where Versions May Be Declared

Nine scopes: [Root](root.md), [Module](module.md), [Domain](domain.md), and all
six [processors](processor.md) — [Adaptor](adaptor.md), [Context](context.md),
[Entity](entity.md), [Projector](projector.md), [Repository](repository.md) and
[Streamlet](streamlet.md).

A processor's messages form an API and therefore a contract, so a version has
to be expressible per component. [Saga](saga.md) and [Function](function.md)
are vital definitions rather than processors, and are deliberately excluded.

!!! warning "Validation"
    A scope declaring more than one version is an **Error**, reported at the
    second declaration.

!!! info "`version` as an identifier still works"
    Making `version` a keyword does not break models that use it as a field or
    type name. Keywords are not excluded from the identifier production.

## A Coordinate, Not a Semantic Version

The composed form *looks* like a semantic version but is a **hierarchical
coordinate**. Do not read compatibility into it:

- `3.1.6` → `3.2.1` says nothing whatever about breakage
- `Garibaldi.4.3` is not orderable against `Jellyfish.1.1` at all
- The coordinate's length varies with nesting depth, so comparison must be
  component-wise

A generator targeting an ecosystem that demands semver needs an **explicit
mapping rule**; it cannot simply pass the coordinate through.

## Compared with Copyright

[Copyright](copyright.md) is the other scope-wide leaf definition, and it
behaves deliberately differently: a version **composes** a coordinate from
every versioned ancestor, whereas a copyright does not accumulate at all — the
applicable notice is simply the nearest one.

## Occurs In

* [Root](root.md), [Module](module.md), [Domain](domain.md)
* All six [processors](processor.md)

## Contains

Nothing — it is a leaf definition.
