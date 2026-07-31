---
title: "Processors"
draft: false
---

A Processor is an abstract [vital definition](vital.md) with several concrete
manifestations (see below) that represents any definition capable of processing
messages. Processors have [handlers](handler.md) to process messages sent to
them, and can have [inlets](inlet.md) and [outlets](outlet.md) for receiving
and sending messages in streams.

## Concrete Processor Types

The following definitions are all processors:

* [Adaptor](adaptor.md) — translates messages between contexts
* [Context](context.md) — a bounded context (has exactly one handler)
* [Entity](entity.md) — stateful business object (can have multiple handlers per state)
* [Projector](projector.md) — projects events into queryable data
* [Repository](repository.md) — persistent storage abstraction
* [Streamlet](streamlet.md) — stream processing component
* [Saga](saga.md) — distributed transaction coordinator

## Message Delivery

Messages can be delivered to a processor in two ways:

1. **To an inlet** — for stream-based message flow
2. **Directly to the handler** — via the `tell` statement for point-to-point messaging

## Inlets

An [inlet](inlet.md) provides the name and data type for an input to the
processor. There can be multiple inlets or none. A processor with no inlets
is called a _source_ since it originates data by itself.

## Outlets

An [outlet](outlet.md) provides the name and data type for an output from
the processor. There can be multiple outlets or none. A processor with no
outlets is called a _sink_ since it terminates data flow.

## Kinds Of Processors

The kind of processor depends on the number of inlets and outlets defined:

| # Inlets | # Outlets | Kind   | Description                                            |
|----------|-----------|--------|--------------------------------------------------------|
| 0        | any       | Source | Originates data and publishes it to outlets            |
| any      | 0         | Sink   | Terminates data flow by consuming from inlets          |
| 1        | 1         | Flow   | Transforms data from one inlet to one outlet           |
| 1        | any       | Split  | Routes data from one inlet to multiple outlets         |
| any      | 1         | Merge  | Combines data from multiple inlets to a single outlet  |
| any      | any       | Multi  | Any other combination is a many-to-many flow           |

## Handlers

A processor contains handlers that specify how the business logic should
proceed. For sources, sinks, and flows, this is straightforward. For splits,
merges, and multis, the handler specifies how messages received on inlets
are transformed and routed to outlets.

## Occurs In

* [Contexts](context.md)

## Contains

* [Inlets](inlet.md)
* [Outlets](outlet.md)
* [Handlers](handler.md)