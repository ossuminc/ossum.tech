---
title: "Adaptor"
draft: false
---

An adaptor's purpose is to _adapt_ one [Context](context.md)
to another [Context](context.md).  In Domain-Driven Design, 
this concept is known as an _anti-corruption layer_ that keeps the
ubiquitous language of one context from "corrupting" the language of another 
context.  The authors of RIDDL didn't like that term for a variety of reasons
so we have renamed the concept as _adaptor_ in RIDDL. Same idea, different name.

## Message Translation
Adaptors do their work at the level of messages sent between 
[Contexts](context.md). This is done using one or
more [Handlers](handler.md). Each handler specifies 
how messages are translated into other messages and forwarded to the target
[context](context.md).

## Target Context
Adaptors are only definable within a containing 
[Context](context.md) which provides one participant of the 
translation. The other [Context](context.md), known as the 
*target* context, is specified within the definition of the adaptor. 

## Adaptation Directionality
Adaptors only translate in one direction, between the containing context and 
the target context. However, multiple Adaptors can be defined 
to achieve bidirectional adaptation between
[Contexts](context.md). 
The directionality of an Adaptor is specified in the definition of the adaptor.
This leads to two kinds of adaptors: inbound and outbound.

## Inbound Adaptors
Inbound adaptors provide an adaptation that occurs from the 
[Context](context.md) referenced in the adaptor to the
[Context](context.md) containing the adaptor. 

## Outbound Adaptors
Outbound adaptors provide an adaptation that occurs from the
[Context](context.md) containing the adaptor to the
[Context](context.md) referenced in the adaptor.

## Syntax

```riddl
context Orders is {
  adaptor PaymentAdapter from context Payments is {
    |Translates payment-related messages between Orders and Payments contexts.

    handler InboundPayments is {
      on event Payments.PaymentCompleted {
        tell entity Order to MarkAsPaid
      }
      on event Payments.PaymentFailed {
        tell entity Order to HandlePaymentFailure
      }
    }
  }

  adaptor InventoryAdapter to context Inventory is {
    |Translates inventory requests from Orders to Inventory context.

    handler OutboundInventory is {
      on command ReserveItems {
        tell context Inventory to Inventory.ReserveStock
      }
    }
  }
}
```

## When to Use Adaptors

Use an adaptor when:

- **Contexts have different vocabularies**: The same concept has different
  names or structures in each context
- **You need to protect domain integrity**: Prevent external concepts from
  leaking into your bounded context
- **Contexts evolve independently**: Changes in one context shouldn't force
  changes in another
- **Integration with external systems**: Translate between your domain model
  and external APIs

**Example scenario**: Your Orders context tracks "line items" while the
Inventory context uses "stock reservations". An adaptor translates between
these models so neither context needs to know about the other's terminology.

## Adaptor vs. Direct References

| Approach | When to Use |
|----------|-------------|
| **Adaptor** | Contexts have different models, need translation |
| **Direct reference** | Contexts share the same model, tightly coupled by design |

## Occurs In
* [Contexts](context.md)

## Contains
* [Handlers](handler.md)
