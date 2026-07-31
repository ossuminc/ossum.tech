---
title: "Bounded Contexts"
description: "Using contexts to isolate language and define boundaries"
---

# Bounded Contexts in RIDDL

DDD defines the notion of a *bounded context* which is a portion of a domain
that has a well-defined and finite boundary. RIDDL uses bounded contexts to
divide complexity in large knowledge domains into manageable portions.

## Why Bounded Contexts?

When the knowledge domain is large enough to exceed a single human's
comprehension, bounded contexts become a primary model structuring principle.

A bounded context defines its boundary via *ubiquitous language* which
facilitates common comprehension of the bounded context amongst team members.
This helps eliminate the confusion and miscommunication that imprecise
conceptualizations in human languages produce.

### The Problem of Ambiguous Terms

Consider the word "order" in various contexts:

| Context | Meaning |
|---------|---------|
| Restaurant | A list of food items to be made and delivered to a table |
| BackOffice | A list of things to be received from a shipper |
| Politics | A state of peace, freedom from unruly behavior |
| Mathematics | A sequence or arrangement of successive things |
| Sociology | A group of people united in a formal way |
| Economics | A written direction to pay money to someone |
| Military | A directive or command from a superior |

And that's just one common business word! Within your domain, the same term
might have different meanings in different contexts.

## Ubiquitous Language

The notion of *ubiquitous language* means concise and specific words used with
precision by the subject matter experts of a given bounded context.

When modeling a system with RIDDL, the ubiquitous language consists of:

- **Named data types** - The vocabulary of information
- **Named messages** - Commands, events, queries, and results
- **Handlers** - How those messages are processed

## Context Boundaries

Bounded contexts are not isolated from other parts of a system model, but they
do isolate the content (state, business logic, processes) behind their
ubiquitous language. Think of the ubiquitous language as the interface to the
bounded context, much as an API is the interface to a program.

## Adaptation Between Contexts

When language confusion exists between contexts, DDD provides the Anti-Corruption
Layer (ACL) pattern. RIDDL calls these **Adaptors** because they adapt one
bounded context to another without corrupting either context's ubiquitous
language.

Adaptors translate messages coming from (or going to) a bounded context,
limiting the surface area of system design that must know about multiple
bounded contexts simultaneously.

### Example: Restaurant Order Adaptation

Consider what an "order" looks like in various restaurant contexts:

| Context | Relevant Order Aspects |
|---------|------------------------|
| Server | Food/Drink Items, Table #, Seat #, Name |
| Customer | Price of items and total cost |
| Kitchen | Food items to prepare (no prices needed) |
| Bar | Drink items to prepare (no prices needed) |
| Accounting | Total price, Loyalty points, Payment form |

An Adaptor from the Server context to the Kitchen context might:
- Remove drink items (those go to the Bar)
- Drop price information (kitchen doesn't need it)
- Add cooking instructions

## RIDDL Contexts

In RIDDL, we use a `context` definition to implement bounded contexts:

```riddl
domain Restaurant is {
  context FrontOfHouse is {
    // Terms specific to front-of-house
    type Table is Integer
    type Seat is Integer

    // Messages in this context's language
    command PlaceOrder is {
      table: Table,
      seat: Seat,
      items: OrderItem*
    }

    // Entities, handlers, etc.
  }

  context Kitchen is {
    // Terms specific to kitchen
    type Station is any of { Grill, Fryer, Salad, Dessert }

    // Messages in kitchen's language
    command PrepareItem is {
      station: Station,
      item: FoodItem,
      specialInstructions: String?
    }
  }

  // Adaptor between contexts
  adaptor OrderToKitchen from context FrontOfHouse to context Kitchen is {
    // Transform FrontOfHouse.PlaceOrder to Kitchen.PrepareItem
  }
}
```

A `context` can:

- Define terms/words precisely
- Define an API through messages and handlers
- Define entities with their state and behavior
- Define adaptors to/from other contexts
- Define sagas of interaction with other contexts

## Design Guidelines

1. **One team per context** - Each bounded context should be owned by a
   single team that maintains its ubiquitous language

2. **Clear boundaries** - If you find yourself constantly needing to understand
   another context's internals, the boundary may be wrong

3. **Explicit translation** - Never leak internal concepts across context
   boundaries; always use adaptors

4. **Size appropriately** - Too large and it becomes unwieldy; too small and
   you have excessive translation overhead

## Related Concepts

- [Domain](../../../concepts/domain.md) - The containing structure for contexts
- [Adaptor](../../../concepts/adaptor.md) - Translates between contexts
- [Context](../../../concepts/context.md) - Full context reference
