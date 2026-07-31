---
title: "Streamlet"
draft: false
---

A Streamlet is a [processor](processor.md) that handles streaming data flows.
Streamlets are the building blocks for data pipelines, connecting sources of
data to consumers through transformations.

## Streamlet Types

The type of a streamlet is determined by its inlets (inputs) and outlets
(outputs):

| Type | Inlets | Outlets | Description |
|------|--------|---------|-------------|
| Source | 0 | 1+ | Generates data (e.g., from external systems, timers) |
| Sink | 1+ | 0 | Consumes data (e.g., writes to database, sends notifications) |
| Flow | 1 | 1 | Transforms data from input to output |
| Split | 1 | 2+ | Routes data from one input to multiple outputs |
| Merge | 2+ | 1 | Combines data from multiple inputs to one output |
| Router | 1+ | 1+ | Routes data based on content or rules |
| Void | 0 | 0 | No data flow (placeholder or utility) |

## Syntax

```riddl
streamlet TemperatureProcessor is {
  inlet readings of type TemperatureReading
  outlet alerts of type TemperatureAlert
  outlet metrics of type TemperatureMetric

  handler ProcessReading is {
    on event TemperatureReading {
      when "reading.value > threshold" then {
        send event TemperatureAlert to outlet alerts
      } end
      send event TemperatureMetric to outlet metrics
    }
  }
}
```

## Source Streamlets

Sources generate data without receiving input. They might:

- Poll external systems
- Listen for external events
- Generate data on timers
- Read from files or databases

```riddl
streamlet OrderEventSource is {
  outlet orders of type OrderEvent

  handler GenerateEvents is {
    on init {
      prompt "Subscribe to order queue and emit events"
    }
  }
}
```

## Sink Streamlets

Sinks consume data without producing output. They might:

- Write to databases
- Send notifications
- Update external systems
- Log or archive data

```riddl
streamlet NotificationSink is {
  inlet notifications of type UserNotification

  handler SendNotifications is {
    on event UserNotification {
      prompt "Send notification via email or push"
    }
  }
}
```

## Flow Streamlets

Flows transform data from one format to another:

```riddl
streamlet OrderEnricher is {
  inlet rawOrders of type RawOrder
  outlet enrichedOrders of type EnrichedOrder

  handler EnrichOrder is {
    on event RawOrder {
      prompt "Look up customer details and product info"
      send event EnrichedOrder to outlet enrichedOrders
    }
  }
}
```

## Connecting Streamlets

Streamlets are connected using [Connectors](connector.md) that link outlets
to inlets:

```riddl
context DataPipeline is {
  streamlet source is { ... }
  streamlet transform is { ... }
  streamlet sink is { ... }

  connector SourceToTransform is {
    from outlet source.events to inlet transform.input
  }
  connector TransformToSink is {
    from outlet transform.output to inlet sink.data
  }
}
```

## Use Cases

- **Event Processing**: React to events in real-time
- **Data Integration**: Move data between systems
- **ETL Pipelines**: Extract, transform, and load data
- **Monitoring**: Collect and process metrics
- **Notifications**: Route alerts to appropriate channels

## When to Use Streamlets vs. Entities

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
use a Streamlet.

## Occurs In

* [Contexts](context.md)

## Contains

* [Inlets](inlet.md)
* [Outlets](outlet.md)
* [Handlers](handler.md)
