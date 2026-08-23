---
title: "Adaptor"
draft: false
---

<!-- riddl-domain-prelude
context Payments is {
  event PaymentCompleted is { orderId is String }
  event PaymentFailed is { orderId is String }
}
context Inventory is {
  record StockData is { orderId is String }
  command ReserveStock is { orderId is String }
  // The tell addresses the CONTEXT, so the context is the sink and needs its
  // own clause -- a contained entity's handler does not receive on its behalf.
  handler InventoryBoundary is {
    on command ReserveStock { ??? }
    on other { error "Unexpected message at the Inventory boundary" }
  }
  entity Stock is {
    state Held of record StockData is {
      handler StockHandler is { on command ReserveStock { ??? } }
    }
  }
}
-->

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

!!! warning "One adaptor per direction, per pair of contexts"
    A context may adapt both **to** and **from** another context, but only
    **once in each direction**. Two adaptors with the same direction to the
    same foreign context split that context's translation across two places,
    with nothing to say which one handles a given message — an **Error**,
    because the ambiguity has no defensible resolution.

    Direction is part of the rule. Inbound *plus* outbound between the same
    pair is the sanctioned way to say "both ways", not duplication. And
    adaptors owned by *different* contexts are equally fine: A adapting from B
    while B adapts from A is two contexts each defending its own model.

## Inbound Adaptors
Inbound adaptors provide an adaptation that occurs from the 
[Context](context.md) referenced in the adaptor to the
[Context](context.md) containing the adaptor. 

## Outbound Adaptors
Outbound adaptors provide an adaptation that occurs from the
[Context](context.md) containing the adaptor to the
[Context](context.md) referenced in the adaptor.

## Syntax

<!-- riddl: in-domain -->
```riddl
context Orders is {
  record OrderData is { orderId is String, isPaid is Boolean }
  command MarkAsPaid is { orderId is String }
  command HandlePaymentFailure is { orderId is String }
  command ReserveItems is { orderId is String }

  entity Order is {
    state Active of record OrderData is {
      handler OrderHandler is {
        on command MarkAsPaid { ??? }
        // A `tell` needs a clause at the far end, or nothing receives it.
        on command HandlePaymentFailure { ??? }
      }
    }
  }

  adaptor PaymentAdapter from context Payments is {
    handler InboundPayments is {
      on paid: event Payments.PaymentCompleted {
        tell command MarkAsPaid(paid.orderId) to entity Order
      }
      on failed: event Payments.PaymentFailed {
        tell command HandlePaymentFailure(failed.orderId) to entity Order
      }
      on other {
        error "Unrecognized message from the Payments context"
      }
    }
  } with {
    briefly as "Translates payment messages between Orders and Payments"
  }

  // Declared so the outbound `tell` below has somewhere to land.
  adaptor InventoryAdapter to context Inventory is {
    handler OutboundInventory is {
      on req: command ReserveItems {
        tell command Inventory.ReserveStock(req.orderId) to context Inventory
      }
      on other {
        error "Unrecognized outbound message"
      }
    }
  } with {
    briefly as "Translates inventory requests from Orders to Inventory"
  }
}
```

Note the operand order: `tell <message> to <processor>`, not the reverse.

## The Isolation Seam

An adaptor bridges **exactly two** contexts: the context that contains it, and
the `referent` context named in its declaration. It is the only sanctioned
crossing point between contexts, so it must not traffic in a **third**
context's messages.

!!! warning "Validation"
    **Errors:**

    - A message whose owning context is neither the parent nor the referent.
      This applies both to the message an `on` clause consumes and to every
      `send`/`tell` target it emits, including those nested inside `when`,
      `match` and `foreach` bodies.
    - A handler with no `on other` clause. An adaptor must say explicitly what
      it does with messages it does not recognize, rather than discarding them
      silently.

    Types defined at [domain](domain.md) or [root](root.md) level are shared
    vocabulary common to both sides and are never flagged.

!!! info "Why only adaptors are held to `on other`"
    `on other` is a fall-through, not a duty: for most processors the general
    rule is *"nothing to do, omit the clause"*, and a proposal to require it
    everywhere was **declined** in 2026-08-14. About two thirds of the handlers
    in `riddl-models` carry one, which is a healthy majority rather than a
    universal.

    An adaptor is the exception because for a translator there is never
    nothing to do. It exists to translate **everything** crossing the seam —
    including messages it was not designed for, where the translation is
    "I cannot translate that". Doing nothing with an unrecognized message is
    to drop a turn in a conversation between two contexts, silently, with the
    far side still waiting. So the adaptor rule is an *application* of the
    general one, not an exception to it.

## Options

`circuit-breaker` (0–2 arguments) is valid on an adaptor, tripping the
adaptation when the far side is failing.

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
* [Modules](module.md)

## Contains

```mermaid
flowchart TD
    Adaptor(["Adaptor"]) --> Handler
    Adaptor --> PC["Processor contents"]
```

* [Handler](handler.md) — the translation rules
* Everything a [processor](processor.md) may contain: [Type](type.md), [Constant](constant.md), [Invariant](invariant.md), [Function](function.md), [Handler](handler.md), [Streamlet](streamlet.md), nested [Processor](processor.md), [Connector](connector.md), Relationship, [Inlet](inlet.md), [Outlet](outlet.md), [Version](version.md), [Copyright](copyright.md), [Comment](comment.md)
* [Include](include.md)

