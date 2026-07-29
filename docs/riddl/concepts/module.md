---
title: "Module"
draft: false
description: >-
  A named, flat collection of any top-level definition -- RIDDL's unit of
  reuse and of compiled output.
---

# Module

A Module is a **named, flat collection** of any top-level definition. It is
RIDDL's unit of reuse and the root of compiled (`.bast`) output.

```riddl
module Commerce is {
  domain Shopping is { ??? }
  type Money is Decimal(12, 2)
  author Reid is {
    name is "Reid Spencer"
    email is "reid@ossuminc.com"
  }
}
```

## Flat, Not Hierarchical

A module enforces **no hierarchy at its own top level**. Any top-level
definition may appear, in any order: types and the four
[message](message.md) kinds, [constants](constant.md),
[invariants](invariant.md), [users](user.md), [contexts](context.md),
[entities](entity.md), [adaptors](adaptor.md), [functions](function.md),
[projectors](projector.md), [repositories](repository.md),
[streamlets](streamlet.md), [sagas](saga.md), [epics](epic.md),
[connectors](connector.md), relationships, [authors](author.md),
[versions](version.md), [copyrights](copyright.md), nested modules,
`include` and `import`.

The internal rules of each contained definition still apply. Flatness is about
what a module will *hold*, not a licence to write invalid definitions.

## Module vs. Root

A [Root](root.md) is the parse root of a file and stays deliberately narrow: it
holds domains, modules, authors, versions, copyrights, comments, and the
`include` and `import` directives. A module is the wide, flat container.

!!! warning "Nebula is deprecated"
    RIDDL 1.x had two overlapping top-level containers: the Root, and an
    anonymous flat bag called a *nebula*. A module is the same idea with a
    name, so it absorbed the nebula in 2.0.

    An anonymous whole-file sequence of definitions still parses, but emits one
    `[deprecated]` message and yields a Module with the synthetic id `nebula`.
    Wrap your definitions in `module <Name> is { … }` instead.

## Compilation and Reuse

A module can be compiled to a binary `.bast` file with `riddlc bastify`, and
imported by another model. Loading a compiled module is roughly six to ten
times faster than reparsing the source, and the file is typically two thirds
the size.

### Importing

The **full** form takes everything the file's root module holds:

```riddl
import "commerce.bast"
```

The **selective** form takes exactly one named definition, optionally renamed:

```riddl
import domain Shopping from "commerce.bast"
import type Money from "commerce.bast" as Currency
```

An importable kind may be any of `domain`, `context`, `entity`, `type`, `epic`,
`saga`, `adaptor`, `function`, `projector`, `repository`, `streamlet`,
`author`, `module`, `user`, `connector`, `constant`, `invariant`.

!!! warning "Placement is validated"
    An imported definition must be structurally legal **where the directive
    sits**, exactly as if it had been written there by hand. Importing a
    `context` at root level, or a domain-bearing library inside a context,
    would build a tree the parser itself would have rejected. That is an
    **Error**, one per offending definition.

### Import versus Include

[`include`](include.md) brings in **source** text, with the parser rules
determined by the enclosing container. `import` brings in **compiled**
definitions from a binary module.

### Both Are Nodes in the Model

An `include` and an `import` each become a **node** in the model, with the
definitions they bring in as that node's children. Nothing is copied or
spliced: traversal simply descends through the node, so the definitions
inside participate exactly as if written in place. References to them resolve,
validation covers them, and generators see them.

The node also records where the content **came from**, which is what lets a
diagnostic point at the right file and lets tooling tell your model apart from
what it imported.

!!! warning "Flattening is lossy — you rarely want it"
    `riddlc flatten` removes those nodes, promoting their children into the
    enclosing container. The definitions survive; the **origin does not**.
    After flattening, nothing records that a definition came from another file
    or another module.

    Flattening is not a step in making a model work — it already works — and
    it is not something to do routinely. Reach for it only when a single
    self-contained file is the actual goal, such as handing one file to a tool
    that cannot follow includes.

## Occurs In

* [Root](root.md)
* Another Module

## Contains

Any top-level definition, plus [versions](version.md),
[copyrights](copyright.md), `include` and `import`.
