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

<!-- riddl: standalone -->
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
      items: Integer
    }

    // Entities, handlers, etc.
  }

  context Kitchen is {
    // Terms specific to kitchen
    type Station is any of { Grill, Fryer, Salad, Dessert }

    // Messages in kitchen's language
    command PrepareItem is {
      station: Station,
      item: String,
      specialInstructions: String?
    }
  }

}
```

An adaptor is declared **inside** the context it protects, and names the one
peer it translates for — outbound (`to`) or inbound (`from`), never both:

<!-- riddl: standalone -->
```riddl
domain Restaurant is {
  context FrontOfHouse is {
    type Table is Integer
    command PlaceOrder is { table: Table }
    event OrderPlaced is { table: Table }
  }
  context Kitchen is {
    type Station is any of { Grill, Fryer, Salad, Dessert }
    command PrepareItem is { station: Station }

    // INBOUND adaptors handle the peer's OUTPUT -- its events and results.
    // Outbound (`to`) adaptors handle the target's input, its commands.
    // This is the only thing in Kitchen that knows FrontOfHouse's shapes.
    adaptor OrderToKitchen from context FrontOfHouse is {
      handler OrderIntake is {
        on event FrontOfHouse.OrderPlaced is {
          do "translate a placed order into a PrepareItem for the station"
        }
        on other is { error "Unexpected message from FrontOfHouse" }
      }
    }
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

## Where Do the Boundaries Come From?

There are no formal rules, and that is deliberate — domains are *fuzzy*
concepts, because they describe how people actually think and talk about a
business rather than how a system is built. Two heuristics do most of the work:

- **Follow the organisation.** Teams that talk constantly converge on a shared
  language; teams that rarely speak do not. That correspondence between
  communication structure and system structure is
  [Conway's Law](https://en.wikipedia.org/wiki/Conway%27s_law), and it is
  usually a better first guess at a boundary than any diagram.

- **Look for the seams in the vocabulary.** Wherever one word starts meaning
  two different things — as "order" does in the table above — you have found an
  edge worth drawing a context around.

If the DDD vocabulary itself is new to you, this
[glossary of domain-driven design terms](https://xenovation.com/blog/patterns/domain-driven-design-glossary/ddd-domain-definition)
is a compact reference for the words used throughout this guide.

## Related Concepts

- [Domain](../../../concepts/domain.md) - The containing structure for contexts
- [Adaptor](../../../concepts/adaptor.md) - Translates between contexts
- [Context](../../../concepts/context.md) - Full context reference
