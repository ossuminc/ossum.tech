---
title: "Outlets"
draft: false
description: >-
  A typed output port. In RIDDL 2.0 any processor may declare one, and it is
  the canonical target of `send`.
---

An Outlet is a component of a [Processor](processor.md) that specifies a named
output through which data of a particular [type](type.md) streams out of the
processor.

<!-- riddl: skip reason="illustrative fragment; references vocabulary this page does not define" -->
```riddl
outlet alerts is type TemperatureAlert
```

## Where Outlets May Be Declared

In RIDDL 2.0, **every** processor kind may declare outlets — not only
streamlets. An [Entity](entity.md) commonly owns one: that is how it publishes
its events into a stream.

## The Canonical `send` Target

A processor emits on its **own** outlet, and a [connector](connector.md) routes
the message to a downstream inlet:

<!-- riddl: skip reason="illustrative fragment; references vocabulary this page does not define" -->
```riddl
send event TemperatureAlert(reading.value) to outlet alerts
```

!!! warning "`send … to inlet` is deprecated"
    Sending directly into another processor's inlet bypasses the streaming
    model — that is what `tell` is for. `outlet` is the canonical `send`
    target. The inlet form still parses and emits a `[deprecated]` message; it
    is slated for removal in 3.0.

## Effect on Shape

The number of outlets contributes to the processor's derived
[shape](processor.md#shape). No inlets and one or more outlets makes a
`source`; one inlet and several outlets makes a `split`.

## Cardinality

**Exactly one [connector](connector.md) may attach to an outlet.** Fan-out is
modeled by declaring several outlets — which is what makes the processor a
`split` — never by attaching several connectors to one outlet. More than one is
an **Error**.

An outlet that no connector drains draws a **CompletenessWarning**. When output
genuinely has no consumer, route it to the
[standard module's](standard-module.md) `BottomlessPit` rather than leaving it
dangling:

<!-- riddl: skip reason="illustrative fragment; references vocabulary this page does not define" -->
```riddl
connector DiscardDiagnostics is
  from outlet MyProcessor.Diagnostics
  to inlet BottomlessPit.hole
```

## Options

| Option | Meaning |
|--------|---------|
| `async` | Marks this port as a deliberate codegen async boundary |

## Occurs In

* [Processors](processor.md) — all kinds
* [Entity](entity.md)

## Contains

* [Type](type.md)
