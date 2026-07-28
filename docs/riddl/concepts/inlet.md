---
title: "Inlets"
draft: false
description: >-
  A typed input port. In RIDDL 2.0 any processor may declare one.
---

An Inlet is a component of a [Processor](processor.md) that specifies a named
input through which data of a particular [type](type.md) streams into the
processor.

```riddl
inlet readings is type TemperatureReading
```

## Where Inlets May Be Declared

In RIDDL 2.0, **every** processor kind may declare inlets — not only
streamlets. A [Context](context.md), [Entity](entity.md),
[Adaptor](adaptor.md), [Projector](projector.md), [Repository](repository.md)
or generic `processor` may all own one.

Declaring an inlet does not make a definition something other than what it is.
An entity with an inlet is still an entity; the inlet simply says that messages
also reach it through a stream rather than only through `tell`.

## Effect on Shape

The number of inlets a processor declares contributes to its derived
[shape](processor.md#shape). A processor with one inlet and one outlet is a
`flow`; with several inlets and one outlet it is a `merge`. An `as <shape>`
ascription that disagrees with the arity is an **Error**.

## Cardinality

**Exactly one [connector](connector.md) may attach to an inlet.** Fan-in is
modeled by declaring several inlets — which is what makes the processor a
`merge` — never by attaching several connectors to one inlet. More than one is
an **Error**.

An inlet that no connector feeds draws a **CompletenessWarning**.

## Options

| Option | Meaning |
|--------|---------|
| `async` | Marks this port as a deliberate codegen async boundary, so the generator inserts a real boundary here instead of fusing the stream |
| `ordered` | Delivery preserves order |
| `unordered` | Delivery order is not significant, enabling partitioning and parallelism |

!!! warning "Over-parallelization"
    If **every** portlet along a connected pipeline is `async`, the stream
    cannot be fused anywhere, so it pays message-passing overhead at every
    boundary and typically runs slower than a fused stream. That draws one
    **StyleWarning** for the pipeline.

## Occurs In

* [Processors](processor.md) — all kinds
* [Entity](entity.md)

## Contains

* [Type](type.md)
