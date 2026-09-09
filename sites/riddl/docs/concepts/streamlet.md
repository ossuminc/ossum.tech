---
title: "Streamlet"
draft: false
description: >-
  The generic streaming processor, declared with the `streamlet` keyword and
  an optional `as <shape>` ascription.
---

<!-- riddl-domain-prelude
event RawOrder is { id is Natural }
event EnrichedOrder is { id is Natural }
-->
<!-- riddl-prelude
constant AlertThreshold is Natural = 100
event TemperatureReading is { value is Natural }
event TemperatureAlert is { value is Natural }
event TemperatureMetric is { value is Natural }
event OrderEvent is { id is Natural }
event UserNotification is { note is String }
event RawOrder is { id is Natural }
event EnrichedOrder is { id is Natural }
-->

A Streamlet is a [processor](processor.md) that handles streaming data flows.
Streamlets are the building blocks for data pipelines, connecting sources of
data to consumers through transformations.

A streamlet is declared with the `streamlet` keyword and an optional shape
ascription. The shape is otherwise **derived** from how many
[inlets](inlet.md) and [outlets](outlet.md) the processor declares.

!!! note "This keyword was `processor` until recently"
    `processor X is { … }` still parses and means exactly the same thing, but
    is deprecated (`stream-processor-keyword`) and `prettify` emits
    `streamlet`. `riddlc validate --fix --fix-rule stream-processor-keyword`
    rewrites it. See [Processor](processor.md#the-streamlet-keyword) for why
    the abstraction kept the older name while the keyword changed.

<!-- riddl: in-context -->
```riddl
streamlet TemperatureProcessor as split is {
  inlet readings is event TemperatureReading
  outlet alerts is event TemperatureAlert
  outlet metrics is event TemperatureMetric

  handler ProcessReading is {
    on reading: event TemperatureReading {
      when reading.value > AlertThreshold then
        send event TemperatureAlert(reading.value) to outlet alerts
      end
      send event TemperatureMetric(reading.value) to outlet metrics
    }
  }
}
```

## Shapes

| Shape | Inlets | Outlets | Description | Synonym |
|-------|--------|---------|-------------|---------|
| `source` | 0 | 1+ | Generates data (external systems, timers) | |
| `sink` | 1+ | 0 | Consumes data (database writes, notifications) | |
| `flow` | 1 | 1 | Transforms data from input to output | `cascade` |
| `merge` | 2+ | 1 | Combines data from several inputs into one | `fanin` |
| `split` | 1 | 2+ | Routes data from one input to several outputs | `broadcast`, `fanout` |
| `router` | 1 | 2+ | Routes data based on content or rules | |
| `void` | 0 | 0 | No ports (placeholder or utility) | |

!!! warning "The dedicated shape keywords are deprecated"
    `source`, `sink`, `flow`, `merge`, `split` and `router` still parse as
    standalone keywords, but each emits a `[deprecated]` message telling you to
    write `processor <id> as <keyword>` instead. They are slated for removal in
    3.0. Prettified output normalizes them, so running `riddlc prettify` over a
    1.x model migrates them for you.

## Sources

Sources generate data without receiving input. They might poll external
systems, listen for external events, generate data on timers, or read from
files and databases.

<!-- riddl: in-context -->
```riddl
streamlet OrderEventSource as source is {
  outlet orders is event OrderEvent

  handler GenerateEvents is {
    on init {
      do "Subscribe to order queue and emit events"
    }
  }
}
```

## Sinks

Sinks consume data without producing output. They might write to databases,
send notifications, update external systems, or log and archive data.

<!-- riddl: in-context -->
```riddl
streamlet NotificationSink as sink is {
  inlet notifications is event UserNotification

  handler SendNotifications is {
    on event UserNotification {
      do "Send notification via email or push"
    }
  }
}
```

## Flows

Flows transform data from one shape to another:

<!-- riddl: in-context -->
```riddl
streamlet OrderEnricher as flow is {
  inlet rawOrders is event RawOrder
  outlet enrichedOrders is event EnrichedOrder

  handler EnrichOrder is {
    on raw: event RawOrder {
      do "Look up customer details and product info"
      send event EnrichedOrder(raw.id) to outlet enrichedOrders
    }
  }
}
```

## Connecting Processors

Processors are wired together with [Connectors](connector.md), which link an
outlet to an inlet:

<!-- riddl: in-domain -->
```riddl
context DataPipeline is {
  streamlet Ingest    as source is { outlet events is event RawOrder }
  streamlet Transform as flow   is {
    inlet input is event RawOrder
    outlet output is event EnrichedOrder
  }
  streamlet Store     as sink   is { inlet data is event EnrichedOrder }

  connector IngestToTransform is
    from outlet Ingest.events to inlet Transform.input
  connector TransformToStore is
    from outlet Transform.output to inlet Store.data
}
```

Exactly one connector may attach to any given port. To fan out, declare more
outlets rather than more connectors. To discard output you genuinely do not
need, route it to the [standard module's](standard-module.md) `BottomlessPit`.

## Where a Chain Ends

A stream chain ends where its message is **consumed** — not at a processor
whose shape happens to be `sink`. A processor is a **tail** for a message type
when it has an inlet, handles every type its inlets admit, and no clause
handling type `T` sends, tells or forwards a message of *that* type onward.

**Sending a different type is a write, not a continuation.** An event log that
receives an event and sends a `Persist` command has *consumed* the event, even
though it owns an outlet and its arity therefore reads as a `flow`. Its shape
says nothing about whether the chain stopped there; what its clauses do with
the type does.

A processor with **no handlers at all** is a tail whatever its shape. An opaque
processor lets no rule assert what it does with a message, so nothing can claim
the chain continues through it.

## Cycles

`stream-graph-cycle` forbids an infinite **message** loop, not a ring of
connectors. A cycle is an `on X` clause that transmits `X`, whose message can
travel the network back round to an `on X` clause that transmits `X` again.

A ring of connectors is therefore **not** by itself a cycle: a request/response
pair is two chains that happen to point at each other. It is also why the
schedule-to-yourself idiom is legal — in

<!-- riddl: skip reason="illustrates the shape of a legal self-schedule; the whole model is on the send-at page" -->
```riddl
on command Book  { send event ReminderDue(...) to outlet Out at b.startsAt }
on event ReminderDue { … }
```

the emitting clause handles `Book` and sends `ReminderDue`, so the event it
sends can never re-enter it.

## Use Cases

- **Event Processing**: React to events in real time
- **Data Integration**: Move data between systems
- **ETL Pipelines**: Extract, transform and load data
- **Monitoring**: Collect and process metrics
- **Notifications**: Route alerts to appropriate channels

## Streamlets vs. Entities

| Use Case | Streamlet | Entity |
|----------|-----------|--------|
| **Stateless transformation** | Yes | No |
| **Long-lived business state** | No | Yes |
| **High-throughput data flow** | Yes | Maybe |
| **Complex business rules with state** | No | Yes |
| **Data enrichment/filtering** | Yes | No |
| **Order processing with lifecycle** | No | Yes |

**Rule of thumb**: If you need to remember something between messages, use an
Entity. If you're transforming or routing messages without persistent state,
use a streaming processor.

This is a question of *purpose*, not of capability: an entity may declare ports
too, and often does — that is how it publishes its events into a stream.

## Occurs In

* [Contexts](context.md)
* Any other processor body

## Contains

```mermaid
flowchart TD
    Streamlet(["Streamlet"]) --> Inlet
    Streamlet --> Outlet
    Streamlet --> PC["Processor contents"]
```

* [Inlet](inlet.md) and [Outlet](outlet.md) — its stream ports, in the number its shape requires
* Everything a [processor](processor.md) may contain: [Type](type.md), [Constant](constant.md), [Invariant](invariant.md), [Function](function.md), [Handler](handler.md), [Streamlet](streamlet.md), nested [Processor](processor.md), [Connector](connector.md), Relationship, [Inlet](inlet.md), [Outlet](outlet.md), [Version](version.md), [Copyright](copyright.md), [Comment](comment.md)
* [Include](include.md)

