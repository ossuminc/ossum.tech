---
title: "Standard Module"
draft: false
description: >-
  The predefined `Riddl` module, providing the stream terminators every model
  can use without importing anything.
---

# The Standard Module

Every model has access to a predefined [module](module.md) named `Riddl`. It
requires no `import` and no author declaration — it is simply always in scope.

It exists because of the [one-connector-per-port](connector.md#port-cardinality)
rule. Under that rule every [outlet](outlet.md) must terminate somewhere and
every [inlet](inlet.md) must be fed, which makes terminators structurally
necessary rather than merely convenient. Without them, a model with genuinely
unconsumed output has to invent a placeholder consumer — modelling something
that isn't true.

## Contents

| Definition | Kind | Purpose |
|------------|------|---------|
| `BottomlessPit` | sink | Consumes everything delivered to its inlet `hole` and emits nothing — `/dev/null` for a stream |
| `ForeverEmpty` | source | Never produces anything on its outlet `void` |
| `Drain` | type | `Anything`, so one drain absorbs every message type |

## Usage

Route output you genuinely do not consume into the pit:

```riddl
connector DiscardDiagnostics is
  from outlet MyProcessor.Diagnostics
  to inlet BottomlessPit.hole
```

Feed an inlet that has no upstream yet:

```riddl
connector NoInputYet is
  from outlet ForeverEmpty.void
  to inlet MyProcessor.incoming
```

## Exemptions

The terminators are exempt from the rules that would otherwise make them
awkward, and the exemptions are matched by **identity** against the predefined
definitions — never by name, so your own definition called `BottomlessPit` gets
no special treatment:

- **Port cardinality** — many connectors may share the universal drain
- **Unattached port** and **isolated processor** completeness checks
- **Reachability**, in both directions. Reaching `BottomlessPit` terminates a
  pipeline exactly as a modelled sink does, and `ForeverEmpty` originates one.
- **Handler completeness** — consuming everything and producing nothing are
  runtime behaviours, not modelled ones

## Name Collisions

Lookups consult your model's own definitions first and fall back to the
predefined ones. A definition of your own that shares a name therefore wins,
structurally, with no ambiguity and no message. It is then ordinary model
content, subject to every normal rule.

## Invisibility

The standard module is never added to your model's contents. A model that
ignores it is byte-for-byte unchanged: identical prettified output, identical
BAST bytes, identical JSON, and an AST scan finds no predefined definition. It
is seeded into the symbol table only, and into a table kept deliberately
separate from your model's, so "all the contexts in the model" never
accidentally includes the standard library.

## See Also

* [Connector](connector.md) — the cardinality rule that makes terminators
  necessary
* [Module](module.md) — the reuse unit the standard module is an instance of
* [Type](type.md) — `Anything`, which `Drain` aliases
