---
title: "Inlets"
draft: false
description: >-
  A typed input port. In RIDDL 2.0 any processor may declare one.
---

<!-- riddl-prelude
event TemperatureReading is { value is Natural }
-->

An Inlet is a component of a [Processor](processor.md) that specifies a named
input through which data of a particular [type](type.md) streams into the
processor.

<!-- riddl: in-entity -->
```riddl
inlet readings is type TemperatureReading

// An inlet is only half of it: something must RECEIVE what arrives, or
// nothing happens when it does. RIDDL says so as a CompletenessWarning.
handler ReadingsHandler is {
  on event TemperatureReading is {
    do "record the reading"
  }
}
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
| `error-sink` | This inlet receives the hard errors a generator reports |

### `error-sink`

When a generated system hits an unrecoverable failure it reports a
`GeneratorError` — a record in RIDDL's standard module. Somewhere has to
receive one, and RIDDL does not presume where: what a system does with an
operational alert is a modelling decision, no different from handling any other
message. So the model names the destination itself.

The mark goes on the **inlet** rather than the processor, because an inlet names
the receiver, the port and the message type in one place; a processor may have
several inlets and a generator would be left guessing which.

Three rules come with it:

- The inlet **must accept `GeneratorError`** — typed by it directly, or by an
  alternation that includes it, so a model may route its own error messages to
  the same place and give the operator one thing to watch. An inlet typed only
  by the model's own command is a destination a generator cannot deliver to,
  so this is an **Error**.
- **At most one per domain**, an Error for the same reason duplicate adaptors
  are: two leave a generator no way to choose. Several across *different*
  domains is correct and intended — unrelated concerns need not share an alert
  stream.
- A **leaf** domain with no error-sink in scope draws a `[missing]` warning.
  Declaring one on an ancestor domain satisfies every leaf beneath it, so a
  single destination for a whole model is one declaration. Grouping domains are
  not asked, because the work that can fail lives in the leaves.

An error-sink inlet does not count against the processor's shape, so a `flow`
or a dedicated `sink` may host one without changing what it is.

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
