---
description: >-
  Complete reference for the RIDDL 2.0 language: structure, containment
  rules, the type system, statements, value expressions, and validation.
---

<!-- riddl-prelude
    type Price is Decimal(10, 2)
    type OrderId is UUID
    type ProductId is UUID
    type CartId is UUID
    type OrderEvent is String
    type EnrichedOrderEvent is String
    result ProductInfo is { id is ProductId, price is Price }
    record OrderData is { id is OrderId, total is Price }
    record TotalInputs is { subtotal is Price, taxRate is Price }
    record CartItem is { sku is String, quantity is Integer }
    record ShippedData is { trackingNumber is String }
    constant Zero is Whole = 0
    constant MinimumOrder is Natural = 1
    constant MinimumPrice is Natural = 1
    constant AlertThreshold is Natural = 10
    constant HighValueThreshold is Natural = 1000
    constant MaxItems is Natural = 100
    event PriceUpdated is { productId is ProductId, newPrice is Price }
    event OrderPlaced is { id is OrderId, total is Price }
    result OrderInfo is { id is OrderId, total is Price }
    command UpdatePrice yields event PriceUpdated is { productId is ProductId, newPrice is Price }
    command PlaceOrder yields event OrderPlaced is { id is OrderId, total is Price }
    query GetProduct replies result ProductInfo is { id is ProductId }
    record CheckoutInputs is { orderId is OrderId }
    record CheckoutOutcome is { ok is Boolean }
    command ProcessPayment is { orderId is OrderId }
    command RefundPayment is { orderId is OrderId }
    command ReserveItems is { orderId is OrderId }
    command ReleaseItems is { orderId is OrderId }
    entity PaymentService is { ??? }
    entity Inventory is { ??? }

    // --- added for the statement and definition fences below ---
    type RawEvent is String
    type ValidatedEvent is String
    record Item is { sku is String, quantity is Integer }
    record ProductRecord is { id is ProductId, price is Price, status is String }
    record PendingData is { note is String }
    record ActiveData is { note is String }
    record PendingOrderData is { note is String }
    record ActiveOrderData is { note is String }
    record ShippedOrderData is { trackingNumber is String }
    record CartData is { id is CartId, total is Price, items is many CartItem }
    record Product is { id is ProductId, price is Price }
    record AvailIn is { held is Natural, total is Natural }
    constant minimumFee is Natural = 5
    function Available is { requires AvailIn returns AvailIn ??? }
    record PricingInput is { subtotal is Price, taxRate is Price,
      tax is Price, shipping is Price }
    function Pricing is {
      requires PricingInput returns PricingInput
      function CalculateTotal is { requires PricingInput returns PricingInput ??? }
      function Total is { requires PricingInput returns PricingInput ??? }
    }
    // NOTE: do NOT define `Tax` here. The in-function wrapper supplies a
    // sibling `context Tax`, and a prelude entry of that name makes every
    // `Tax.…` path ambiguous, breaking the in-function fences on this page.
    event ItemAdded is { sku is String }
    event ActionCompleted is { note is String }
    event LineShipped is { sku is String }
    event OrderPending is { id is OrderId }
    event OrderShipped is { id is OrderId }
    event Withdrawn is { amount is Natural }
    event CartCreated is { id is CartId }
    event OrderPaymentReceived is { id is OrderId }
    command ConfirmOrder is { id is OrderId }
    type OrderRef is Id(entity Order)
    command Reprice is { orderId: OrderRef, newTotal: Price }
    command ShipOrder is { trackingNumber is String }
    command EscalateReview is { id is OrderId }
    command Withdraw yields event Withdrawn is { amount is Natural }
    type ExampleEvent is PriceUpdated | ActionCompleted
    outlet Events is type ExampleEvent
    outlet CartEvents is type ItemAdded
    outlet PaymentRequests is type ProcessPayment
    outlet Shipments is type LineShipped
    type OrderLifecycle is OrderPlaced | OrderPaymentReceived
    outlet OrderEvents is type OrderLifecycle
    entity Cart is {
      state Filling of record CartData is {
        handler CartHandler is { on event ItemAdded { ??? } }
      }
    }
    entity Catalog is {
      state Listed of record ProductRecord is {
        handler CatalogHandler is {
          on query GetProduct { reply result ProductInfo(ProductRecord.id, ProductRecord.price) }
        }
      }
    }
    entity Review is {
      state Reviewing of record OrderData is {
        handler ReviewHandler is { on command EscalateReview { ??? } }
      }
    }
    // `become` names an ENTITY-level handler, so ShippedHandler sits beside
    // the state rather than inside it. A fence that declares its own
    // `entity Order` must say no-prelude=Order.
    entity Order is {
      state Placed of record OrderData is {
        handler PlacedHandler is { on command ConfirmOrder { ??? } }
      }
      handler ShippedHandler is { on command ShipOrder { ??? } }
    }
    // The match statement needs a CLOSED subject for its type-cases. This
    // lives here, not in the shared wrapper: an enumeration's enumerators
    // join the enclosing namespace, so a wrapper-level `Shipped` collides
    // with any page that names a state `Shipped` -- statement.md does.
    type ShipmentState is any of { Pending, Shipped, Delivered }
    constant orderStatus is ShipmentState = "Pending"

    // Endpoints for the `connector` fence that discards an unused outlet.
    processor MyProcessor as source is { outlet Unused is type OrderEvent }
    processor BottomlessPit as sink is { inlet hole is type OrderEvent }
-->

<!-- riddl-domain-prelude
    // Domain-level vocabulary for the fences that declare a whole `context`.
    // Streams carry these across context boundaries, so they cannot live in
    // any one context; a domain may hold type definitions.
    // These are EVENTS, not plain types: an `on event X` clause rejects a
    // String-typed X with "should reference one of these types: Event".
    event OrderEvent is { orderId is UUID, amount is Decimal(10, 2) }
    event EnrichedOrderEvent is { orderId is UUID, region is String }
    event RawEvent is { note is String }
    event ValidatedEvent is { note is String }

    user Customer is "a shopper buying from the store"

    // The sibling contexts that whole-context fences name by dotted path. A
    // fence declaring its own `context OrderContext` must say
    // no-prelude=OrderContext.
    context PaymentContext is {
      event PaymentCompleted is { reference is UUID, amount is Decimal(10, 2) }
    }
    context OrderContext is {
      event OrderCompleted is { orderId is UUID, amount is Decimal(10, 2) }
      event OrderRefunded is { orderId is UUID, amount is Decimal(10, 2) }
    }
    application context Storefront is {
      record StorefrontData is { sku is String }
      page ProductDetails is {
        form AddToCartForm submits type StorefrontData
      }
      page ShoppingCart is {
        list CartSummary shows type StorefrontData
      }
    }
    // Self-contained on purpose: a fence may strip Storefront with
    // no-prelude, so nothing outside it may depend on StorefrontData.
    context Shopping is {
      record ShoppingCartData is { sku is String }
      command AddToCart is { sku is String }
      entity Cart is {
        state Filling of record ShoppingCartData is {
          handler CartHandler is { on command AddToCart { ??? } }
        }
      }
    }
    // A projector `updates` a repository, and a domain body may hold one.
    repository SalesData is { ??? }
-->


# RIDDL Language Guide

## Overview

RIDDL (Reactive Interface to Domain Definition Language) is a domain-specific
language designed for modeling reactive systems using Domain-Driven Design (DDD)
principles. It bridges the gap between business domain experts and software
engineers by providing a language that's both expressive for domain modeling and
precise enough for implementation. This language was also designed to provide
an AI model with sufficient context to generate code accurately from the
specification.

## Language Design Emphasis

RIDDL emphasizes:

- Declarative syntax with natural language readability
- Hierarchical structure with domains, (bounded) contexts, entities, processors,
  repositories, projectors, adaptors, and other definitions that specify the
  behavior of a system
- Event-driven and reactive design patterns
- State-based entity modeling with explicit state transitions
- Streaming of data between components from outlet to inlet via connectors
- Clear separation of commands, events, queries and results
- Saga-based coordination of complex atomic processes, possibly distributed
- Comprehensive domain modeling through DDD concepts
- Asynchronous, non-blocking communications (implied)

## Language Structure

### Definitions

Everything that has a name and can have metadata is known as a Definition in
RIDDL.

### Branches

Branch definitions are containers that hold other definitions. They form the
hierarchical structure of a RIDDL model:

- **Root**: The implicit top-level container (not explicitly defined)
- **Module**: A flat, named collection of any top-level definition
- **Domain**: Contains bounded contexts and domain-wide definitions
- **Context**: Contains entities, repositories, sagas, and other processors
- **Entity**: Contains states, handlers, functions, and message types
- **Epic**: Contains use cases describing user interactions
- **Saga**: Contains steps for multi-step processes with compensation

### Processors

A **processor** is any definition that can receive and process messages, and
that may declare ports. Processors are the active components of a RIDDL model.

RIDDL has one unified processor model. Every processor kind — Context, Entity,
Adaptor, Projector, Repository, and the generic `processor` — may declare
inlets and outlets, and may carry an ascribed streaming shape:

- **Entity**: Stateful processor with commands, events, states, and handlers.
  Entities are the primary business objects that maintain state and respond to
  commands.
- **Adaptor**: Translates messages between two contexts. Defined with a
  direction (`from` or `to`) relative to a context.
- **Repository**: Handles persistence of data. Contains schemas and handlers
  for storage operations.
- **Projector**: Projects events to a repository, often transforming or
  aggregating data for read models (CQRS pattern). Projectors handle events
  only, and may declare [correlations](#correlations) that join several events
  into one command.
- **Processor**: The generic streaming processor, declared with the `processor`
  keyword and an optional `as <shape>` ascription.
- **Context**: A bounded context is itself a processor, so it may hold handlers
  and ports of its own.

A **Saga** orchestrates multi-step processes with compensation logic for
failure recovery. A **Function** defines a pure, reusable computation. Neither
is a processor — both extend the vital-definition base — so neither takes a
version or a copyright. A Saga does nonetheless bear inlets and outlets, being
a coordinator with messages to receive and emit; a Function does not.

All processors can contain handlers, functions, types, constants, invariants,
ports, and other processor-specific definitions.

### Streaming Shapes

A processor's **shape** describes its streaming arity. It is normally *derived*
from the number of ports the processor declares, and may optionally be
*ascribed* with `as <shape>` to state the intent explicitly:

| Shape | Description | Inlets | Outlets | Synonym |
|-------|-------------|--------|---------|---------|
| `source` | Produces data from external sources | 0 | 1+ | |
| `sink` | Consumes data to external destinations | 1+ | 0 | |
| `flow` | Transforms data passing through | 1 | 1 | `cascade` |
| `merge` | Combines multiple streams into one | 2+ | 1 | `fanin` |
| `split` | Divides one stream into multiple | 1 | 2+ | `broadcast`, `fanout` |
| `router` | Routes messages based on content | 1 | 2+ | |
| `void` | Declares no ports at all | 0 | 0 | |

<!-- riddl: in-context -->
```riddl
processor OrderEnricher as flow is {
  inlet RawOrders is type OrderEvent
  outlet EnrichedOrders is type EnrichedOrderEvent
}
```

If an ascribed shape contradicts the declared arity, that is an **Error**. If a
processor declares at least one port but ascribes no shape, that is a
suppressible **StyleWarning** nudging you to say what you meant.

!!! warning "Deprecated shape keywords"
    The dedicated keywords `source`, `sink`, `flow`, `merge`, `split` and
    `router` still parse but emit a `[deprecated]` message. Write
    `processor <id> as <shape>` instead. They are slated for removal in 3.0.

### Domain Hierarchy

RIDDL models are organized hierarchically:

- **Root**: The top-level container for the entire system. Roots are not
  declared; they consist of the top-level definitions in a file. A Root may
  contain Modules, Domains, Authors, Versions, Copyrights and Comments.
- **Module**: A named, *flat* collection of any top-level definition, in any
  order, with no hierarchy enforced at its own top level. The internal rules of
  each contained definition still apply. Modules are the unit of reuse and of
  compiled (`.bast`) output.
- **Domain**: A container for the specification of some knowledge domain.
- **Context**: Bounded context containing related entities and components.
- **Entity**: Stateful business objects with commands, events, and handlers.
- **Repository**: Persistent storage. May live in a Context or, when it
  synthesizes data across several contexts, directly in a Domain.
- **Projector**: A component that projects events to a repository for later
  retrieval, possibly transforming the data or merging multiple event streams.
- **Saga**: The orchestration of a multi-step atomic process with compensating
  actions to undo the process when errors arise.
- **Epic**: A collection of use cases showing an expected usage pattern.
- **Case**: A specific user interaction flow.

!!! warning "Nebula is deprecated"
    Earlier releases had an anonymous top-level scratch pad called a *nebula*.
    A Module now does everything a nebula did and has a name. An anonymous
    whole-file sequence of definitions still parses, but emits one
    `[deprecated]` message and yields a Module with the synthetic id `nebula`.
    Wrap your definitions in `module <Name> is { … }` instead.

### Data Types

RIDDL has a rich type system supporting both simple and complex data structures.

**Predefined Types:**

- **Strings**: `String`, `String(min,max)` with length constraints
- **Numbers**: `Integer`, `Natural`, `Whole`, `Real`, `Number`, `Decimal(w,f)`
- **Boolean**: `Boolean`
- **Temporal**: `Date`, `Time`, `DateTime`, `TimeStamp`, `Duration`,
  `ZonedDateTime(zone)`
- **Identifiers**: `UUID`, `UserId`, `Id(entity path)`
- **Other**: `URL`, `URL(scheme)`, `Currency(code)`, `Location`, `Nothing`,
  `Anything`
- **Physical**: `Length`, `Mass`, `Current`, `Temperature`, `Luminosity`, `Mole`

`Anything` is the dual of `Nothing`: a type assignment-compatible with every
other type in both directions. A port typed `Anything` is compatible with any
port it is connected to.

!!! warning "`Abstract` is deprecated"
    `Abstract` was renamed to `Anything`. The old spelling still parses to the
    same node and emits a `[deprecated]` message.

**Pattern Types:**

- `Pattern("regex")` — String matching a regular expression

**Compound Types:**

- **Aggregation**: `{ field1 is Type1, field2 is Type2 }` — Named field
  collections
- **Alternation**: `one of { TypeA, TypeB, TypeC }` — Union/sum types. An
  alternation must offer a **real choice**: zero alternatives is an **Error**,
  exactly one draws a `[deprecated]` message, two or more is clean, and
  `one of { ??? }` remains the way to say "not decided yet".
  May also be written with bars: `TypeA | TypeB | TypeC` is the identical
  type. `prettify` rewrites bars back to `one of { ... }`, which stays the
  canonical spelling. Predefined types are not valid alternatives either way.
- **Enumeration**: `any of { Value1, Value2, Value3 }` — Enumerated values

**Aggregate Use Cases:**

The keyword that introduces an aggregate says what kind of thing it is:
`type`, `command`, `query`, `event`, `result`, `record`, `graph`, `table`.

- **Graph**: `graph` — models graph-structured data
- **Table**: `table` — models tabular data

**Collection Types:**

- **Sequence**: `sequence of Type` or `many Type`
- **Set**: `set of Type`
- **Mapping**: `mapping from KeyType to ValueType`
- **Optional**: `optional Type` or `Type?`

**Special Types:**

- **Entity Reference**: `reference to entity Path`
- **Unique ID**: `Id(<kind> Path)` — runtime identity of one *instance* of a
  processor. Not entity-only; see [Instance Identity](#instance-identity)

### Messages and Records

There are exactly four **messages**: `command`, `query`, `event` and `result`.
Only a message can be sent, told, yielded, or handled by an `on` clause.

A `record` is **data**, not a message. A record can never be sent or handled. It
types an entity's state and supplies the payload of a `morph`.

!!! warning "Record is no longer a message"
    In RIDDL 1.x a `record` reference was accepted wherever a message reference
    was. It no longer is. `send`, `tell`, `yield` and `on <ref>` accept the four
    real messages only; `state … of` and `morph … with` accept a record.

### Basic Syntax Elements

1. **Readability Words**: Optional words that improve human readability of a
   model.
     - The complete list is: `and`, `are`, `as`, `at`, `by`, `for`, `from`,
       `in`, `is`, `of`, `so`, `that`, `to`.
     - A synonym for `is` is `:`, `=`, or `are`.
     - These words are accepted by the grammar but not required.

2. **Definition Structure**:
   ```
   [kind] [name] is {
     // definition contents
   } with {
     // metadata
   }
   ```
     - The `[kind]` indicates the kind of definition (domain, context, entity,
       etc.).
     - The `[name]` is the identifier for this definition, which must be unique
       amongst its peers.
     - The "definition contents" depend on the `[kind]` of definition.
     - The metadata section must always come **after** the closing brace of the
       definition, not within it.

3. **Type References**: Always specify the kind of reference.
     - `entity Product`
     - `command CreateCart`
     - `event OrderCreated`
     - `record ProductData`
     - `user Customer`

## Naming Rules

### How a path identifier resolves

Every reference names its target with a **path identifier**: one or more
identifiers separated by dots, such as `Tax.TaxIn` or `Outer.Deep.Leaf`. A
single name and a dotted path resolve by different rules, so they are worth
taking separately.

#### A single name searches the whole model

One identifier with no dots is looked up in the **symbol table** — a dictionary
of every name defined anywhere in the model. If exactly one definition carries
that name, that is the answer, wherever it lives. If more than one does, the
reference is an **ambiguity error** listing the candidates; if none does, it is
a not-found error.

This is why a bare name can reach a definition in a *sibling* context without
naming it, and why adding a definition elsewhere in the model can turn a
working bare reference into an ambiguous one. To make a reference immune to
that, qualify it.

#### A dotted path anchors, then walks down

A path of two or more names is resolved in two phases.

**Phase 1 — anchor on the first name**, tried in this order:

1. The literal name `Root` anchors at the root of the model, which makes the
   rest of the path absolute.
2. Otherwise, if the name matches one of the **ancestors** of the place the
   reference is written, that ancestor is the anchor. The ancestor **closest**
   to the reference wins.
3. Otherwise the name is looked up in the symbol table, exactly as a single
   name is: unique anchors the path, ambiguous is an error, absent is an error.

Steps 1 and 2 are the guaranteed forms — they depend only on where the
reference is written, so they cannot be broken by a definition added elsewhere.
Step 3 is the convenient one, and carries the same ambiguity risk as any bare
name.

**Phase 2 — walk down, one name at a time.** Each remaining name must be found
among the contents of the definition named before it. There is no scope-popping
after the anchor: `Tax.TaxIn` means "anchor `Tax`, then look for `TaxIn` inside
it", and if `Tax` has no `TaxIn` the path fails there, even when a `TaxIn`
exists elsewhere in the model.

<!-- riddl: in-domain -->
```riddl
context Tax is {
  record TaxIn is { subtotal is Natural }
}
context Billing is {
  // `Tax` anchors via the symbol table, then `TaxIn` is
  // sought among Tax's own contents.
  record Invoice is { amount is Tax.TaxIn }
}
```

#### What counts as "inside" depends on the kind

For most definitions the contents are just the definitions written inside the
braces. Several kinds contribute something else, so that paths follow the model
rather than the syntax:

| Anchoring definition | What the next name may match |
|---|---|
| **State** | its own contents (handlers, invariants) **first**, then the fields of the record it is `of` — so a handler shadows a same-named field |
| **on-clause** | the fields of the message being handled |
| **Field**, **Constant**, **Type** | the members of its type expression |
| **Inlet**, **Outlet** | the members of the type it carries |
| **Function** | its own definitions, plus the fields of a deprecated inline `requires`/`returns` aggregation |
| **Include** | the definitions the included file contributes, as though written in place |

Because a State's own contents are searched before the record's fields, a
handler named the same as a field is reached by a path, and the field is not.
The nearer declaration wins.

### Sibling names must be unique, regardless of kind

This rule exists **because** of how paths resolve. Each step of a dotted path
picks a definition out of a container by name alone — the kind is never part of
the choice — so two definitions sharing a name in one container would leave the
step with nothing to decide on.

Uniqueness among siblings is what makes that step well-defined. It does **not**
make a *bare* name unambiguous, since a bare name is looked up across the whole
model: two definitions of the same name in different containers are perfectly
legal, and a bare reference to that name is then an ambiguity error at the
point of use rather than at either definition.

Two definitions in the same container may not share a name, even when they are
different kinds of thing:

<!-- riddl: skip reason="deliberate counter-example; shows what does NOT work" -->
```riddl
context Catalog is {
  type   Thing is String
  entity Thing is { ??? }     // Error: 'Thing' is already taken
}
```

!!! warning "Changed in RIDDL 2.0"
    Uniqueness used to be checked per *kind*, so `type Thing` beside
    `entity Thing` passed with zero errors. It is now an **Error**.

    This is the rule behind a class of confusing failures: with both defined,
    a reference such as `Id(Thing)` had two plausible referents, and which one
    it found was not something the model stated.

### A definition keyword may not be a bare identifier

Eleven keywords **introduce** a definition, and none may be used as a bare
name:

`domain`, `context`, `entity`, `adaptor`, `saga`, `epic`, `projector`,
`repository`, `streamlet`, `handler`, `function`

<!-- riddl: skip reason="deliberate counter-example; shows what does NOT work" -->
```riddl
handler projector is { ??? }     // Error: two introducing keywords in a row
```

Two escapes, both legal:

<!-- riddl: in-context -->
```riddl
handler 'projector' is { ??? }   // quoted identifier
handler Projector  is { ??? }    // the check is case-sensitive
```

Nothing is wrong with the *names* — the point is that two introducing keywords
in a row leave a reader, and any tool, guessing which word is the keyword. The
quoted form says which.

This is deliberately **not** all 156 keywords. `version` and `copyright`, in
particular, remain usable as field and type names; that was a compatibility
decision when they were added, and it stands. The ambiguity only bites where a
word would otherwise start a definition, so that is where the rule bites.

## Containment Rules

RIDDL follows strict containment rules that define what elements can be defined
within other elements.

### Root

A **Root** can contain Domains, Modules, Authors, Versions, Copyrights,
Comments, `include` directives, and `import` directives.

### Module

A **Module** is flat: it can contain *any* top-level definition, in any order —
types and the four message kinds, constants, invariants, users, contexts,
entities, adaptors, functions, projectors, repositories, streamlets, sagas,
epics, connectors, relationships, authors, versions, copyrights, nested
modules, `include` and `import`.

### Domain

A **Domain** can contain:

- Types
- Authors
- Contexts (bounded contexts)
- Domains (nested subdomains)
- Users (actors who interact with the system)
- Epics (user stories with use cases)
- Sagas (multi-step processes)
- Repositories (when they synthesize across several contexts)
- Connectors (when they join ports across contexts)
- Versions and Copyrights
- Imports (from `.bast` files)
- Includes (file inclusion)

### Context

A **Context** (bounded context) can contain:

- Everything in *processor definition contents* (below)
- Entities
- Repositories
- Projectors
- Sagas
- Adaptors (message translation between contexts)
- Streamlets and generic processors
- Connectors (linking outlets and inlets)
- Groups (UI components, also called page, pane, dialog, etc.)
- Imports and Includes

### Entity

An **Entity** can contain:

- Everything in *processor definition contents*
- States (with their own handlers and invariants)
- Includes

### Processor Definition Contents

Every processor — Context, Entity, Adaptor, Projector, Repository, Streamlet —
can contain:

- Types
- Constants
- Invariants
- Functions
- Handlers
- Inlets and Outlets
- Nested processors, streamlets, connectors and relationships
- Versions and Copyrights
- Comments and Includes

### Leaf Definitions

**Authors**, **Users**, **Terms**, **Constants**, **Versions** and
**Copyrights** contain only their metadata and cannot contain other RIDDL
definitions.

## Type System

### Basic Types

- `UUID`, `String(min, max)`, `Integer`, `Decimal(whole, fractional)`
- `Boolean`, `Pattern("regex")`, `Real`, `Natural`, etc.

Numeric arguments accept a sign: `range(-5, 5)` and `Decimal(-3, 2)` mean what
they say.

### Complex Types

- **Record Types**: Named collections of fields
  <!-- riddl: in-domain -->
  ```riddl
  record Address is {
    street1 is String
    city is String
    state is String
    zipCode is String
    country is String
  } with {
    briefly as "Physical mailing address"
    described by {
      | Represents a physical address with standard components
      | used for shipping and billing purposes.
    }
  }
  ```

- **Enumerations**:
  <!-- riddl: in-domain -->
  ```riddl
  type Status is any of {
    Active
    Inactive
    Suspended
  } with {
    briefly as "Possible entity statuses"
  }
  ```

- **Collections**:
  <!-- riddl: in-record -->
  ```riddl
  items is many Item
  ```

### The `yields` and `replies` Clauses

A command or query may declare the response it produces. This makes the
request/response pairing declarative, so generators can emit precise
signatures. RIDDL has **two** such pairings, and each has its own keyword:

<!-- riddl: in-function -->
```riddl
command PlaceOrder yields event OrderPlaced is {
  cartId is CartId
}

query GetOrder replies result OrderInfo is {
  orderId is OrderId
}
```

A **command `yields` an event**; a **query `replies` a result**. The two are
genuinely different acts — emitting an event as a consequence of a command is
not the same thing as answering a question — and a generator lowers them
differently. Crossing them is an Error: `yields` on a query, `replies` on a
command, or either naming a type of the wrong kind.

!!! warning "Changed in RIDDL 2.0"
    Before 2.0 both were spelled `yields`, and the `reply` statement was a
    deprecated synonym for `yield` that parsed to the same node. They are now
    distinct, and the switch is **hard**: `yields result` is an Error
    immediately, with no transitional period.

    The declaration side was effectively empty in practice — commands widely
    declared `yields event`, while almost no query declared its result — so
    `replies` fills a gap rather than breaking established models.

Both are **optional**. When declared, the handler for that message must respond
with exactly that message; when not declared, a handler may respond as it
likes. The one place `replies` is **required** is a query that something
[`ask`s](#ask) — an ask takes the answer's type from the query's `replies`, so
there is nothing to read without it.

!!! warning "Type Validation"
    **Errors:**

    - Defining a type whose name exactly matches a predefined type name
      (e.g., `type Currency is Decimal(10,2)`) — this shadows the built-in
      type and is not allowed
    - `yields` or `replies` on a type that is not a command or query
    - A command whose `yields` names a non-event, or a query whose `replies`
      names a non-result
    - Pairing the wrong keyword with the use case: `yields` on a query, or
      `replies` on a command

    **Style Warnings:**

    - Defining a type whose name is a case-variant of a predefined type
      (e.g., `type timestamp is TimeStamp`)

    **Completeness Warnings:**

    - Command types with no fields (excluding `???` placeholders)
    - Event types not produced by any handler
    - Query types without corresponding result types (and vice versa)

## Contexts and Intentions

A context may declare its **intention** — what kind of bounded context it is —
with a keyword prefix:

<!-- riddl: in-domain no-prelude=Storefront -->
```riddl
type Request is String

application context Storefront    is { ??? }
external    context StripePayments is { ??? }

// gateway and service carry SHAPE requirements -- see below
gateway context PublicApi is {
  inlet fromWeb    is type Request
  inlet fromMobile is type Request
  outlet inbound   is type Request
}
service context Pricing is {
  inlet  request  is type Request
  outlet response is type Request
}
```

| Intention | Meaning |
|-----------|---------|
| `application` | Presents a user interface. The only place UI may be modeled. |
| `external` | A third-party system the model does not own. |
| `gateway` | An entry point that adapts the outside world to the inside. |
| `service` | An internal service with no user interface. |

The intention is optional; a plain `context` declares no intention and is
subject to no intention rules.

!!! warning "Intention Validation"
    **Errors:**

    - A context that contains a `group` (or any of its UI aliases) but is not
      an `application` context. UI belongs at the application boundary.
    - A `gateway` context that is not a **merge** — it must have 2 or more
      inlets and exactly 1 outlet. A gateway funnels several outside channels
      into one inside path, so a portless `gateway context G is { ??? }` is an
      Error: *"Gateway context 'G' must have a merge shape (>=2 inlets, 1
      outlet) but is void"*.
    - A `service` context that is not a **flow** — exactly 1 inlet and 1
      outlet. A service takes a request and returns a response.
    - An `external` context modeling persistence it cannot own

    `application` and `external` carry **no** shape requirement, so a
    placeholder `application context A is { ??? }` is fine. `gateway` and
    `service` cannot be stubbed that way: declaring the intention commits you
    to the ports.

!!! warning "The `gateway`, `service`, `external` and `wrapper` options are deprecated"
    These were previously spelled as options in the `with { }` block. Use the
    intention prefix instead. The options still parse and emit a
    `[deprecated]` message.

## Entities and States

Entities are stateful objects with explicit states. Each state references a
**record** that defines its data structure, and can optionally contain handlers
and invariants that apply while the entity is in that state:

<!-- riddl: in-context no-prelude=Product -->
```riddl
entity Product is {
  initial state ProductData of record ProductRecord is {
    invariant PriceIsPositive is price > MinimumPrice

    handler ProductHandler is {
      on cmd: command UpdatePrice {
        set field ProductRecord.price to cmd.newPrice
        yield event PriceUpdated(productId = cmd.productId,
                                 newPrice = cmd.newPrice)
      }
    }
  } with {
    briefly as "Product state with update handling"
  }
} with {
  briefly as "Represents a purchasable item"
}
```

States can also be defined without a body when handlers are defined at the
entity level instead:

<!-- riddl: in-context -->
```riddl
entity SimpleProduct is {
  state ProductData of record ProductRecord
  handler ProductHandler is { ??? }
}
```

### The `initial` Marker

An optional `initial` keyword before `state` or `handler` marks the entity's
starting state, and the handler that is live after a `morph`:

<!-- riddl: skip reason="its `state Active` is elided to `???`, and RIDDL 2.0 requires every state to have a handler" -->
```riddl
entity Order is {
  initial state Pending of record PendingData is {
    initial handler PendingHandler is { ??? }
  }
  state Active of record ActiveData is { ??? }
}
```

Unmarked models keep the previous "first one declared wins" behavior, so this
is fully backward compatible. Marking it explicitly makes the model safe to
reorder.

Declaring more than one `initial` state in an entity, or more than one
`initial` handler in a state, is an **Error**.

### Finite State Machines

When an entity has multiple states with their own handlers, it models a finite
state machine — each state responds to messages differently, and the `morph`
statement transitions between states:

<!-- riddl: skip reason="`record ActiveOrderData()` is an empty constructor for a record that must have at least one field; the fence elides the arguments" -->
```riddl
entity Order is {
  initial state PendingOrder of record PendingOrderData is {
    handler PendingHandler is {
      on command ConfirmOrder {
        morph entity Order to state Order.ActiveOrder
          with record ActiveOrderData()
      }
    }
  }
  state ActiveOrder of record ActiveOrderData is {
    handler ActiveHandler is {
      on command ShipOrder {
        morph entity Order to state Order.ShippedOrder
          with record ShippedOrderData()
      }
    }
  }
  state ShippedOrder of record ShippedOrderData is {
    handler ShippedHandler is { ??? }
  }
} with {
  option is finite-state-machine
}
```

!!! warning "Entity Validation"
    **Errors:**

    - More than one `initial` state, or more than one `initial` handler in a
      state
    - Defining a type whose name exactly matches a predefined type

    **Warnings:**

    - Entity Id type defined inside the entity body instead of the containing
      context (move it to the context level)
    - Entity Id type defined at domain level or beyond (scope too broad)
    - Entity Id type not defined at all

    **Completeness Warnings:**

    - States without an `on init` clause
    - `on init` without a `set` statement
    - Command handlers that neither `send` nor `yield` an event, **and do
      not refuse**. A clause that refuses with `error` or `require` has
      processed the command — it decided, it declined, and there is nothing
      to record — so it discharges the obligation. Previously this flagged the
      honest refusal-only clause, and was silenced by adding a `send` *after*
      the refusal, which the refusals-before-effects rule makes unreachable:
      it rewarded exactly the dead code a modeller should avoid.
    - Query handlers that don't `yield` or `send` a result
    - Entities without any `on query` clause
    - Entities with no handlers at all
    - FSM entities (2+ states) without `morph` or `become` statements
    - Empty handlers (no statements or only `???`)
    - Handlers containing only `do` statements
    - Empty `on other` clauses (silently discards messages)

## Commands and Events

Commands represent requests to change state:

<!-- riddl: in-function -->
```riddl
command UpdatePrice yields event PriceUpdated is {
  productId is ProductId
  newPrice is Price
} with {
  briefly as "Command to change a product's price"
}
```

Events represent state changes that have occurred:

<!-- riddl: in-record -->
```riddl
event PriceUpdated is {
  productId is ProductId
  oldPrice is Price
  newPrice is Price
} with {
  briefly as "Event indicating a product price change"
}
```

### Command-Event Relationship

Commands should always result in one or more events being emitted. This follows
the reactive principles of RIDDL:

<!-- riddl: in-entity -->
```riddl
handler ProductCommandHandler is {
  on cmd: command UpdatePrice {
    when cmd.newPrice > MinimumPrice then
      yield event PriceUpdated(productId = cmd.productId,
                               newPrice = cmd.newPrice)
    else
      error "Price must exceed the minimum"
    end
  }
}
```

## Handlers

Handlers define how processors respond to messages. They contain `on` clauses
that match specific message kinds and execute statements.

### On Clause Types

| Clause | Purpose | Example |
|--------|---------|---------|
| `on command X` | Handle a specific command | `on command CreateOrder { ... }` |
| `on event X` | Handle a specific event | `on event OrderCreated { ... }` |
| `on query X` | Handle a query and yield a result | `on query GetOrder { ... }` |
| `on result X` | Handle a result | `on result OrderInfo { ... }` |
| `on init` | Execute when the processor initializes | `on init { ... }` |
| `on term` | Execute when the processor terminates | `on term { ... }` |
| `on activate` | Execute when an entity is rehydrated | `on activate { ... }` |
| `on passivate` | Execute when an entity is evicted | `on passivate { ... }` |
| `on other` | Handle any unmatched message | `on other { ... }` |

`on init` and `on term` are once-ever lifecycle events. `on activate` and
`on passivate` fire on every rehydration and eviction, are **entity-only**, and
must be side-effect free: `send`, `tell`, `yield`, `morph` and `become` are
rejected inside them at parse time.

### Naming the Handled Message

An `on` clause may bind a local name to the message it is handling, using
ordinary type ascription. Within the body the name denotes the whole message:

<!-- riddl: in-context -->
```riddl
handler H is {
  on ord: command PlaceOrder {
    yield event OrderPlaced(id = ord.id, total = ord.total)
  }
}
```

The binding is optional, so every existing model parses unchanged. A local name
that shadows an outer definition is legal but draws a Warning; a name that does
not begin with a lowercase letter draws a StyleWarning.

### Message Origins

An `on` clause may name where the message came from:

<!-- riddl: skip reason="two spellings of the SAME on-clause, which cannot share one handler -- same shape as onclause.md" -->
```riddl
on command DoIt from context Other { ??? }
on command DoIt from di: context Other { ??? }
```

### Basic Handler Example

<!-- riddl: in-entity -->
```riddl
handler ProductCommandHandler is {
  on upd: command UpdatePrice {
    when upd.newPrice > Zero then
      set field ProductRecord.price to upd.newPrice
      yield event PriceUpdated(productId = upd.productId, newPrice = upd.newPrice)
    else
      error "Price must be greater than zero"
    end
  }

  on query GetProduct {
    reply result ProductInfo(ProductRecord.id, ProductRecord.price)
  }
} with {
  briefly as "Processes commands for product management"
}
```

### Handler Locations

Handlers can be defined at multiple levels:

- **Entity handlers**: Default message handling for the entity
- **State handlers**: Message handling specific to a state
- **Context handlers**: API-level handlers for the bounded context
- **Processor handlers**: Handlers in Repository, Projector, Adaptor, etc.

An entity-scope handler may be marked `initial`, which makes it the initial
handler for **every state that does not define one of its own** — a default
across the whole state machine rather than a per-state choice. Where no marker
appears, an entity-scope handler is defaulted to `initial` only when the entity
has exactly one state.

Declaring more than one `initial` handler at entity scope is an **Error**,
regardless of how many states the entity has. Verified against
`2.0.0-rc.9-54`.

!!! warning "Handler Kind Rules"
    **Errors, enforced at parse time where possible:**

    - A projector is **event-only**: `on command`, `on query` and `on record`
      are rejected. `on event` and `on result` are valid.
    - `require` and `error` are forbidden in `on event` — an event has already
      happened and must always be accepted.
    - `on activate` / `on passivate` outside an entity, or containing an
      effect statement.
    - An adaptor handler with no `on other` clause. An adaptor must say
      explicitly what it does with messages it does not recognize.

    **Style Warnings:**

    - Two `on` clauses in one handler that handle the same message. The later
      clause is unreachable.

## Invariants

An invariant is a named boolean rule. Its full form is:

```
invariant <identifier> [requires (state <ref> | <type-ref>)] is <condition>
```

### Implicit Application

**An invariant applies to every clause of its declaring scope**, checked as a
precondition before any effect in that clause. No statement at the point of use
is needed.

!!! warning "Changed in RIDDL 2.0"
    Previously an invariant did nothing unless a clause named it in `require
    invariant X`, which made it easy to carry a constraint that read as enforced
    and was inert. Every invariant now applies — including ones you also
    `require` explicitly, because otherwise adding a single `require` would
    silently narrow a rule from enforced-everywhere to enforced-there.

### Condition Forms

<!-- riddl: in-entity -->
```riddl
invariant Legacy      is "the account must be in good standing"
invariant InStock     is quantity >= Zero
invariant CanCoverFee is {
  let available = call function Available(held = holdAmount, total = balance)
  available >= minimumFee
}
```

!!! warning "No numeric literals in a condition"
    The boolean sub-language has no numeric literal atom, so `amount >= 0` does
    not parse — compare against another named value instead (`amount >= floor`).
    Arithmetic is not available either: a `let` binds a reference or a `call`,
    not an expression such as `balance - holdAmount`.

A literal string is an AI-fill site. A
[boolean expression](#boolean-expressions) or a block already *is* the
predicate. The block form admits the statements a pure function may contain,
ending in the boolean that is the predicate.

### Scope and Readable Fields

The declaration decides both — never the call site:

| Declaration | Applies to | May read |
|---|---|---|
| in an entity, no `requires` | every clause of that entity, including its states' handlers | fields present in **every** state record |
| inside a state S | that state's handlers only | S's record fields |
| in an entity, `requires state S` | that entity's clauses while in state S | S's record fields |
| `requires <type T>` | nothing implicitly — explicit only | the value handed to it |
| on a context or other stateless processor | nothing implicitly — explicit only | the value handed to it |

**The intersection rule.** An entity-level invariant reading `balance` forces
every state record of that entity to have a `balance` field. Referencing a field
absent from any state record is an **Error**.

A stateless processor has no ambient data for an implicit predicate to read, so
an invariant declared on one must name what it needs and be invoked explicitly:

<!-- riddl: in-context -->
```riddl
record Limits is { ceiling: Integer, used: Integer }

invariant UnderLimit requires record Limits is used <= ceiling
```

The clause then hands it the value:

<!-- riddl: in-handler -->
```riddl
require invariant UnderLimit with record Limits(ceiling = "10", used = "1")
```

### Purity

An invariant block may contain only the statements a pure function may contain:
no state writes, no `send`/`tell`, no `morph`/`become`/`yield`/`reply`. An
invariant may **not** send even a read-only query — doing so would make the
predicate asynchronous, fallible, non-deterministic and no longer structurally
terminating. The clause gathers; the invariant receives.

A [function](#functions) may read no entity state at all; an invariant may read
the state its declaration names. That asymmetry is deliberate — an invariant is
a predicate over state, evaluated inside the entity's single-writer window, with
its readable fields bounded by its declaration.

### Failure Modes

| Applied | Failure is a | Result |
|---|---|---|
| explicitly, at `require invariant X` | **refusal** | modeled outcome — an error result naming the rule |
| implicitly | **fault** | exception plus rollback; does **not** widen the clause's result type |

Invariants in scope are checked in declaration order; the first failure is
reported.

Implicit invariants are **skipped in `on init`** — that clause is where state
comes into existence. They **apply in `on term`**, and they **apply in `on
event`** clauses. The last is not a contradiction of the rule forbidding
authored `require`/`error` in `on event`: that rule bars *refusing* an event,
and an implicit violation faults and rolls back rather than refusing, so the
event remains a fact.

### Diagnostics

- An invariant declaring `requires <type T>` that no `require invariant X with
  <expr>` ever invokes draws a **warning** — it is inert.
- An entity-level invariant referencing a field absent from any state record is
  an **Error**.

See the [Invariant concept page](../concepts/invariant.md) for the reasoning
behind these rules.

## Value Expressions

RIDDL 2.0 introduces a real value-expression system. Wherever a statement
needs a value, it accepts any of these forms:

| Form | Syntax | Meaning |
|------|--------|---------|
| Literal | `"some text"` | Opaque pseudo-code or a literal constant |
| Value reference | `order.total` | A named field, state field, function input, or `let` local |
| Constructor | `OrderPlaced(total, id = x)` | Builds a message or record |
| Get | `get from input SignupForm` | Reads a UI input or an entity state |
| Call | `call function Pricing.Total(a, b)` | Invokes a pure function for its result |
| Prompt | `prompt("compute the discount")` | A value computed by AI at generation time |
| Boolean | `a > b and not c` | A structured boolean expression |

### Constructors

A constructor builds a message or a record inline. Arguments are positional
first, then named:

<!-- riddl: in-yielding-handler -->
```riddl
yield event OrderPlaced(orderId, total = cart.total)
```

An **empty** argument list is an arity of zero and must match like any other,
so `OrderPlaced()` against a message that has fields is an Error.

Argument count, names, ordering and (best effort) types are all checked against
the target's fields.

!!! info "An operand may name a VALUE, not only a type"
    `send`, `tell`, `yield`, `reply` and `morph` all take an operand saying
    **which** message or record is being delivered. That operand may be a bare
    name already in hand — an on-clause binding, a state field, a `let` local,
    or a function input:

    <!-- riddl: in-clauses -->
    ```riddl
    on evt: event ItemAdded is {
      send evt to outlet CartEvents      // the VALUE, not the type
    }
    ```

    Naming a message **type** says nothing about where the value comes from,
    which is most of what a generator needs to know. A bare type reference
    still parses and still means "some value of this type", but it draws a
    **CompletenessWarning** — and the intended end state is an Error, deferred
    only because the reference corpus holds over fourteen thousand of them.

    `morph` gets the same freedom with a different rule: its operand is checked
    for type-conformance against the target state's record, since the
    message-operand test would reject every correct use.

!!! warning "Duplicates are Errors"
    A **repeated field name** in an aggregate — `command C is { x is String, x
    is Integer }` — is an **Error**. A repeated name makes the aggregate's
    shape ambiguous, so every consumer would have to pick one silently. Both
    locations are named in the diagnostic, because the author is looking at one
    and needs the other.

    A **repeated constructor argument** — `C(x = 1, x = 2)` — is the same
    mistake at the call site, and is likewise an Error.

### Correlations

A `correlation` accumulates several events, keyed by one or more fields, into a
single command the repository handles. It is legal only inside a
[projector](../concepts/projector.md#correlations).

```
correlation <Id> by <field> {, <field>} yields command <CmdRef> is {
  handler <Id> is { <on-event clauses that set the command's fields> }
} times out after "<duration>" { <statements> }
```

<!-- riddl: skip reason="syntax template with placeholders, not a model" -->
```riddl
correlation FulfillmentJoin by customerId, orderId
  yields command RecordFulfillment is {
  handler Collect is {
    on event OrderPlaced  { set field RecordFulfillment.total to "the total" }
    on event PaymentTaken { set field RecordFulfillment.paidAmount to "paid" }
  }
} times out after "30 days" {
  tell command ReportStalled to entity Monitor
}
```

Four rules carry the meaning:

- **Identity is the full key tuple**, ordered as written and never
  canonicalized.
- **Completion is derived from the target command's type** — every *required*
  field set by some fold. Key fields are exempt, being filled from the key.
- **`times out after` is mandatory**, so an unbounded correlation cannot be
  written. Its duration is an ordinary string.
- **The target must be a command**, because a repository is changed by handling
  one; `yields record R` is deliberately not derivable.

!!! warning "Errors"
    - A required non-key field of the target that **no fold sets** — the
      correlation could never complete.
    - **Two folds setting the same field** — the completed value would depend
      on arrival order, which across sources is not guaranteed.

### Get

`get from` reads a value from a UI input or an entity state:

<!-- riddl: in-application -->
```riddl
let email = get from input SignupForm
```

<!-- riddl: in-context -->
```riddl
record HamperData is { total is Natural }
command AddItem is { sku is String }

entity Hamper is {
  state Collecting of record HamperData is {
    handler HamperHandler is {
      on command AddItem {
        let current = get from state Collecting
      }
    }
  }
}
```

The two forms cannot share a clause. An `input` exists only inside an
`application` context, and **state may be read only inside the entity that
owns it** — reading another definition's state is an Error.

### Call

`call` invokes a **function** — and only a function, because functions are the
only pure definitions — and produces its result:

<!-- riddl: in-handler -->
```riddl
let total = call function Pricing.CalculateTotal(subtotal, taxRate = rate)
```

Calling something with no declared `returns` is an Error.

### Boolean Expressions

Boolean expressions have the usual precedence: `or` < `and` < `not` <
comparison < atom. Parentheses group.

<!-- riddl: in-handler -->
```riddl
when order.isPaid and not order.isCancelled then ??? end
require count == total
```

An [invariant](../concepts/invariant.md) takes one too, though it is a
definition rather than a statement:

<!-- riddl: in-entity -->
```riddl
invariant InStock is quantity >= Zero
```

`and`, `or`, `not`, `true` and `false` are **context-sensitive**: they are
recognized only inside a boolean expression, so they remain legal identifiers
everywhere else.

!!! warning "Comparisons are type-safe"
    Both operands of a comparison must be **typed references** — a value
    reference, a `get from`, or a named `constant`. A literal is not permitted:
    `count > "5"`, `count > 5`, `count > true` and `count > R(1)` all fail at
    parse time.

    To compare against a fixed value, name it:

    <!-- riddl: skip reason="elided template; a context-level constant beside a statement" -->
    ```riddl
    constant MaxItems is Natural = 100
    // ...
    when cart.itemCount > MaxItems then error "too many items" end
    ```

    This is deliberate. It removes magic constants from models and makes every
    comparison check the types on both sides. `==` and `!=` require operands of
    the same category; `<`, `>`, `<=` and `>=` require an ordered (numeric)
    type on both sides.

## Statement Syntax

### Morph Statement

Changes entity state. The payload is a **record** — a bare record reference or
an inline constructor:

<!-- riddl: skip reason="`ProductRecord(price)` passes one positional argument to a three-field record, and `price` is not in scope; the fence elides the rest" -->
```riddl
morph entity Product to state ProductData with record ProductRecord(price)
```

### Send Statement

Emits a message on one of *this* processor's own outlets. A connector then
routes it to a downstream inlet:

<!-- riddl: in-handler -->
```riddl
send event ItemAdded(sku = "the item") to outlet CartEvents
send command ProcessPayment(orderId) to outlet PaymentRequests
```

!!! warning "`send … to inlet` is deprecated"
    Sending directly into another processor's inlet bypasses the streaming
    model — that is `tell`'s job. `outlet` is the canonical `send` target. The
    inlet form still parses and emits a `[deprecated]` message; it is slated
    for removal in 3.0.

!!! warning "The portlet's type is a contract"
    A `send` naming a message the portlet's declared type does **not** admit is
    an **Error**. The portlet's type is what the connector and every downstream
    consumer are built on, so a consumer typed by it simply cannot receive the
    value.

    Both portlet kinds are checked, and both sides expand through alias chains.
    To carry more than one message on an outlet, declare its type as an
    **alternation** of everything that may travel on it:

    <!-- riddl: in-context -->
    ```riddl
    type CartTraffic is ItemAdded | LineShipped
    outlet MixedCartEvents is type CartTraffic
    ```

    The same rule applies to [`forward`](#forward-statement) on its portlet
    shape. `tell` is not checked this way — it names a processor, which has no
    single declared type.

### Tell Statement

Delivers a message directly to a processor:

<!-- riddl: in-handler -->
```riddl
tell event ItemAdded(sku = "the item") to entity Cart
tell command ProcessPayment(orderId) to entity PaymentService
```

!!! warning "Validation"
    A `tell` whose target is not reachable through any modeled connector draws
    a **Warning**.

#### Addressing is structural

A `tell` names a processor *type* — but an entity has many instances, so
something must say **which one**. RIDDL takes that from the message itself:
the address is the message's field typed [`Id(target)`](#instance-identity),
found without annotation.

<!-- riddl: in-context no-prelude=OrderRef,Reprice -->
```riddl
type OrderRef is Id(entity Order)

// `orderId` is typed Id(entity Order), so it IS the address. Nothing
// needs to be declared, and nothing needs to be written at the call site.
command Reprice is { orderId: OrderRef, newTotal: Price }
```

`tell … by <field>` exists only to **disambiguate** when more than one field
qualifies:

<!-- riddl: in-handler -->
```riddl
tell command Reprice(orderId = prompt("the order to reprice"),
  newTotal = cart.total) to entity Order by orderId
```

Two rules make this predictable:

- Candidates match by **resolved identity**, never by the path's last segment,
  so two entities named `Order` in different contexts cannot collide.
- The search **follows alias chains but never nesting**. A field typed
  `OrderId`, where `type OrderId is Id(Order)`, is an address — that alias is
  ordinary house style. A field whose *nested record* carries the id is not,
  because descending into an aggregate is an unbounded search with no
  principled place to stop. **Renaming is followed; containment is not.**

**Zero candidates is a CompletenessWarning, and only when the target is an
entity** — an entity is the only multiply-instantiated processor. It is not an
Error for a measured reason: the reference corpus held 7,556 `tell`s against
7 `Id`-typed fields, so an Error would have condemned essentially every model
in existence. **Ambiguity, by contrast, *is* an Error** — it is a
contradiction rather than an omission.

### Forward Statement

Passes the handled message on to somewhere else **and discharges this clause's
response obligation**, because whatever handles it downstream is what produces
the declared `yields` event or `replies` result.

It takes both transmission shapes — a portlet like [`send`](#send-statement),
a processor like [`tell`](#tell-statement):

<!-- riddl: in-clauses -->
```riddl
on ord: command PlaceOrder {
  forward ord to entity PaymentService     // processor shape
}
```

Without it, a boundary handler that merely passes a command along had **nothing
it could say**. `yields` is declared on the message, so every handler of a
command declaring `yields event E` owes an `E` — even one whose entire job is
delegation and which produces nothing itself.

!!! warning "Validation"
    `forward` is legal **only** in a clause handling a command that declares
    [`yields`](#the-yields-and-replies-clauses) or a query that declares
    `replies`. You cannot forward an **event** or a **result**: those record
    what happened and owe no answer, so there is no obligation to pass on.

    The operand's **type** must match the handled message. Values are not
    compared, so a handler may adjust field contents and still be forwarding
    the same message.

    It is **not terminal**, but the response has been delegated — so a `yield`
    or `reply` after it is an **Error**, since this clause cannot also produce
    what it just handed away. A `send` or `tell` after it is legal and draws a
    style warning.

    On the portlet shape the [outlet's declared type](#inlets-and-outlets) must
    admit the message, exactly as for `send`.

!!! info "What settles a path"
    Only `yield`/`reply`, `error`/`require`, and `forward` discharge a
    response obligation. A `send` of the handled message does **not** — not
    even to an outlet that admits it. Emitting some *other* message does not
    either.

### Yield and Reply Statements

These are the statement halves of the two pairings described under
[`yields` and `replies`](#the-yields-and-replies-clauses). Both produce a
declared response without the handler needing to know the sender's identity:

<!-- riddl: in-clauses -->
```riddl
on ord: command PlaceOrder {
  yield event OrderPlaced(ord.id, ord.total)
}
```

<!-- riddl: in-clauses -->
```riddl
on query GetProduct {
  reply result ProductInfo(id, price = 9.99)
}
```

`yield` emits a **command's** declared event. `reply` answers a **query** with
its declared result. Each satisfies the completeness check for its own kind of
handler, and the wrong pairing — `yield result` or `reply event` — is an Error.

!!! warning "Changed in RIDDL 2.0"
    Until 2.0 `reply` was a *deprecated synonym* for `yield`, parsing to the
    same node. That is now reversed: `reply` is a first-class statement with
    its own meaning, and `yield result` no longer parses as valid. If you are
    migrating a 1.x model, `reply` is a destination rather than something to
    rewrite away.

### Set Statement

Assigns a value to a field or a state:

<!-- riddl: skip reason="`set state ActiveOrder to record ActiveOrderData()` is an empty constructor for a one-field record, and `call function Pricing.Total(subtotal, tax)` passes two of four inputs" -->
```riddl
set field status to "Active"
set field total to call function Pricing.Total(subtotal, tax)
set state ActiveOrder to record ActiveOrderData()
```

!!! warning "`set` requires something that OWNS state"
    `set` — and `get from state` — are legal only where the container actually
    owns state: an **Entity**, which owns its `State`, or a **Projector**,
    which owns the read-model record its folds build.

    Everywhere else it is an **Error**: a **Context** (state lives in the
    entities, repositories and projectors it contains, never in the context
    itself), a **Saga** (whose state is housekeeping with no domain meaning), a
    **Repository**, an **Adaptor**, and the streamlets. A **Function** is
    rejected at the keyword — functions are pure, so the caller passes state in
    through `requires`.

    State is also readable only inside the entity that owns it. Reaching into
    another entity's state is not a scoping inconvenience; it is the thing
    entity boundaries exist to prevent.

### Let Statement

Creates a local variable binding, with an optional type annotation. When no
annotation is given, the type is inferred from the bound expression:

<!-- riddl: skip reason="calls `Cart.Total`, a function this page never defines, and annotates a `let` with the predefined `Decimal`, which does not resolve as a type path" -->
```riddl
let totalPrice = call function Cart.Total(subtotal, tax, shipping)
let discount: Decimal = "totalPrice * 0.1"
let ready = order.isPaid and not order.isCancelled
```

A `let` is lexically scoped and statement-ordered: it is visible only after its
declaration and is shadowed inside nested blocks.

### Ask

`ask` states that two messages are two halves of **one** interaction: a query
sent to a processor, and the reply that answers it. It is a **value**, not a
statement, so it is used through `let`:

<!-- riddl: in-handler -->
```riddl
let answer = ask query GetProduct of entity Catalog
```

Before `ask`, a model could say a message was sent (`tell`) and what handling
one produces (`yields`/`replies`), but not that a caller awaits a particular
answer. `yield` names no destination and `tell` says nothing about a reply, so
a generator could not tell fire-and-forget from request/response.

**`ask` declares that correlation and nothing else.** It deliberately implies
no mechanism — not a future, a temporary actor, a correlation-id field, or a
blocking call. All four are lowerings a generator may choose, on the same
principle as `message_envelope`: RIDDL specifies meaning, generators choose
representation. Timeouts are likewise a generated-code concern, not language.

**Queries only, structurally.** The operand is a query reference, not a general
message reference — a command, event, result or record is not answerable, so
the restriction is in the shape of the syntax rather than in a validation rule.

**The answer's type is always known:** it is the query's declared
[`replies result X`](#the-yields-and-replies-clauses). This is the one place
`replies` is mandatory, which is why the requirement sits at the `ask` site
rather than on every query.

!!! warning "Errors"
    - Asking a query that declares no `replies` — there is no type to give the
      answer.
    - Asking a processor that has no clause handling the query. An `on other`
      clause counts as handling everything, and an entity's handlers may live
      under a state.
    - Asking **anywhere inside a saga step**, including as a value nested in a
      larger expression. See below.

    An ask whose callee **refuses** is expected, not an error: recording a
    rejection settles the obligation, consistent with the discharge rule.

!!! warning "A saga may not `ask`"
    A saga must not depend on dynamic state, or the same inputs could yield
    different transaction results at different times. Compensation makes this
    sharper: if the forward action read a value that has since changed, the
    undo would be reversing something other than what happened.

    The remedy is to acquire the value in a handler and pass it into the saga
    through the saga's `requires`, so the saga is closed over its inputs and
    compensation sees the same data the forward action saw.

    The prohibition reaches **every `ask` embedded in a value expression, at
    any depth** — it is not enough to keep `ask` off the right-hand side of a
    `let`.

### Instance Identity

RIDDL could describe processors but not **instances** of them. A model could
say what an `Order` entity does, and could not say *which* Order, could not
bring one into being, and could not name the one it is currently running as.
Four constructs close that gap.

#### `Id(P)` — the identity of one instance

`Id` names any **processor**, not only an entity: adaptor, context, entity,
projector, repository or streamlet. The keyword form is canonical and a bare
path is shorthand:

<!-- riddl: in-context no-prelude=OrderRef -->
```riddl
type OrderRef   is Id(entity Order)      // canonical
type PlainRef   is Id(Order)             // shorthand for the same thing
type CatalogRef is Id(entity Catalog)
```

The keyword is stored **as written**, so `prettify` is byte-exact — and
validation makes it tell the truth. A keyword contradicting the referent's
actual kind is an **Error**, because a wrong keyword is worse than none: a
reader believes it.

<!-- riddl: skip reason="a deliberate counter-example: the keyword contradicts the referent" -->
```riddl
type WrongRef is Id(entity Ordering)   // fails: Ordering is a context
```

!!! info "Why `Id` covers a singleton too"
    A context or repository has exactly one instance, so its `Id` may look
    pointless. It is not: an `Id` is **how you address something**. For a
    singleton it denotes the deployment, and addressing it means "select the
    right shard and forward". Only entities may be created and ended, but
    every processor may be named.

This is **runtime** identity, and it is not the definition's model-time
identity. Two `Order` instances share one definition but never share an
`Id(Order)`. The value is opaque and system-generated, so a **business** key —
an order number, an email — belongs in state, supplied through `on init`.

#### `self` — the instance running right now

<!-- riddl: in-handler -->
```riddl
let me  = self
let who = self.id
```

`self`'s type is a **synthesized record** with `id` and `version`. That it is
an ordinary record is load-bearing: `self.id` resolves through the same path
walk as every other value, so no resolution rule anywhere has to know `self`
exists.

Two consequences follow from the type not being user-nameable — `self.id` is
`Id(Order)` inside an Order handler and `Id(Shipping)` inside a Shipping one:

- `let me: T = self` has no `T` you could write.
- `self` is not assignable into a message field. **Pass `self.id`.**

The field set is **closed**. Adding to it is a language change, and the test is
*runtime-only*: anything a generator can know statically it should inline,
which is why `version` qualifies and, say, cluster placement does not.

#### `initiate` — bring an instance into being

`initiate` is a **value**: it yields the new instance's `Id`, so it is used
through `let`.

<!-- riddl: in-handler -->
```riddl
let fresh = initiate entity ExampleEntity
```

It does **not** add a second way for an instance to exist — construction still
completes only when [`on init`](#on-clause-types) finishes. Without it, no
`Id(P)` value could ever come into being and the whole addressing story would
be inert.

`initiate` and [`terminate`](#terminate-statement) are **entity-only**, by an
explicit check rather than as a side effect of the type system. Both are
**effects**, so both are banned in a function body, in `on activate` /
`on passivate`, and in a correlation fold. Both are legal in a saga step.

!!! note "The asymmetry is the design"
    `initiate` names a **type** and yields an id; `terminate` consumes an
    **id** and yields nothing. So `initiate` is a value and `terminate` is a
    statement, and `on term` needs no parameter naming the instance — `self`
    is in scope for the whole body and stays live to its very end, so
    `self.id` already says which one is ending.

### Put Statement

Publishes a value to a UI output. Valid only in application and context
handlers:

<!-- riddl: in-application -->
```riddl
put order.confirmationNumber to output ConfirmationPanel
```

### Return Statement

Returns a function's result. Valid only in a function body:

<!-- riddl: in-function -->
```riddl
return call function Tax.Compute(subtotal)
```

### When Statement

Conditional logic. The `end` keyword is required:

<!-- riddl: skip reason="syntax template with placeholders, not a model" -->
```riddl
when <condition> then {
  // actions
} end
```

A condition may be any of:

- A boolean expression: `when a > b and not c then`
- A bare boolean-typed reference, including a dotted path:
  `when order.isPaid then`
- A `let` binding, optionally negated: `when authorized then`,
  `when !authorized then`
- An AI-evaluated prompt: `when prompt("the user is authenticated") then`

A bare reference is resolved and checked to be Boolean-typed; a clearly
non-Boolean condition is an Error.

!!! warning "A bare string condition is deprecated"
    `when prompt("the user is authenticated") then` still parses but draws a
    `[deprecated]` message. Write `when prompt("…")` instead.

    The reason is consistency: everywhere else in RIDDL a bare quoted string
    denotes a **literal value**, while `prompt(…)` marks something an AI
    decides. A natural-language condition is plainly the latter, so it should
    say so rather than borrow the literal's spelling.

An `else` clause handles the false case:

<!-- riddl: in-handler -->
```riddl
let authorized = user.hasPermission
when authorized then {
  send event ActionCompleted(note = "done") to outlet Events
} else {
  error "User not authorized"
} end
```

### Match Statement

Pattern matching over a typed subject. The subject is a value reference, a
`get from`, or a legacy pseudo-code literal:

<!-- riddl: in-handler -->
```riddl
match orderStatus {
  case Pending {
    tell event OrderPending(orderId) to entity Order
  }
  case Shipped when order.isPaid {
    tell event OrderShipped(orderId) to entity Order
  }
  default {
    error "Unknown order state"
  }
}
```

A comparison case needs a **numeric** subject, so it belongs to a different
match than the one above — the subject's type decides which case forms are
legal on it:

<!-- riddl: in-handler -->
```riddl
match order.total {
  case >= HighValueThreshold {
    tell command EscalateReview(orderId) to entity Review
  }
  default { do "no escalation needed" }
}
```

A case pattern is one of:

- **Type case** — a bare type reference matching an alternant, enumerator or
  message subtype: `case Pending`
- **Comparison** — an operator and a comparand, with the subject as the
  implicit left operand: `case >= HighValueThreshold`
- **Literal** — a legacy pseudo-code label: `case "pending"`

Each case may carry an optional `when <boolean>` guard.

Naming an unknown type-case is an **Error**. For a *closed* subject — an
Enumeration or Alternation — a non-exhaustive match without a `default` draws a
**StyleWarning**.

### Foreach Statement

RIDDL's safe, bounded loop. There is no unbounded iteration in the language:

<!-- riddl: skip reason="`myLocalCollection` must be a `let`-bound local, and the fence elides the binding" -->
```riddl
foreach line in field order.lines {
  send event LineShipped(sku = line.sku) to outlet Shipments
}

foreach item in myLocalCollection {
  do "record the item"
}
```

The collection is a `field` reference or a `let`-bound local whose type resolves
to a collection — Sequence, Set, Graph, Table, Replica, Mapping, or a
cardinality wrapper such as `many` or `optional`. **Any resolvable path that
lands on a collection is accepted**; it need not be a direct field of the
enclosing state, which is why `order.lines` above works.

The element name is **bound over the loop body** and carries the element's
type, so `line.sku` resolves and `line.nosuch` is an Error. The binding ends at
the closing brace.

#### Destructuring a mapping

A mapping yields a key and a value, so iterating one binds **two** names:

<!-- riddl: in-handler -->
```riddl
foreach sku, price in field order.prices {
  send event LineShipped(sku = sku) to outlet Shipments
}
```

Arity is a validation rule rather than a grammatical one — both shapes parse —
and it is checked in both directions:

| Mistake | Message |
|---|---|
| one name over a mapping | *binds a key AND a value, so it needs two names* |
| two names over a non-mapping | *binds a second name only over a mapping* |

### Require Statement

Asserts a precondition that must hold before proceeding:

<!-- riddl: in-handler -->
```riddl
require amount > Zero
require "the customer is in good standing"
require invariant BalanceNonNegative
require invariant UnderLimit with limits
```

The `with <value>` form hands a value to an invariant that declares
`requires <type>` — the one invariant form ambient scope cannot supply. See
[Invariants](#invariants).

In a `when` or `match` **condition** the same invariant needs no argument, and
the `invariant` keyword itself is optional there. The asymmetry is deliberate:
a condition *asks* whether the rule holds, while a `require` *applies* it and
so must be handed what the rule reads.

!!! warning "Naming an invariant does not switch it on"
    As of RIDDL 2.0 an invariant applies **implicitly** across its declaring
    scope, whether or not any clause names it. A `require invariant X` is an
    explicit restatement at a point you want the check called out — never what
    activates it. The rule that an unreferenced invariant draws a UsageWarning
    is **withdrawn**; the only inert form left is an invariant declaring
    `requires <type>` that nothing ever invokes, and that still warns.

### Error Statement

Refuses to proceed, with a reason:

<!-- riddl: in-handler -->
```riddl
error "Price must be greater than zero"
```

`error` **ends its statement list.** It refuses unconditionally, so anything
written after it can never run, and a following statement is an **Error**. Use
[`require`](#require-statement) instead when the refusal is conditional —
`require` refuses only when its condition fails, so statements after it are
ordinary and reachable.

[`terminate`](#terminate-statement) ends a list the same way, for a different
reason: the instance is gone, so a later statement has nothing to act on. An
`on term` clause is unaffected — it is a separate statement list that runs
*because* of the termination, never after it.

### Terminate Statement

Ends the life of the entity instance handling the message. It names the
identity being terminated, and may carry closing values the way a constructor
does:

<!-- riddl: in-clauses -->
```riddl
on cmd: command ExampleCommand {
  require cmd.amount > ExampleZero   // refusals first
  terminate self.id
}
```

Like [`error`](#error-statement), `terminate` **ends its statement list**: the
instance no longer exists, so a statement written after it can never run and is
an **Error**. Unlike `error`, the way to react to it is not a conditional
refusal but an [`on term`](#on-clause-types) clause, which is a separate list
that runs *because* the instance ended.

`terminate` **is** an effect for the [refusals-before-effects](#refusals-before-effects)
rule — ending the instance is the most complete local state change there is.

### Refusals Before Effects

Within any single linear statement list, every **refusal** (`require`, `error`)
must come before every **effect** — and for this rule an "effect" is a change to
**this definition's own state**: `set`, `morph` and `terminate`. Performing one
and then refusing would leave a partial change behind.

Each statement list is checked independently, so each branch of a `when`,
`match` or `foreach` body is its own list. A refusal after an effect in the same
list is an **Error**.

!!! note "Why `send`, `tell`, `yield`, `become` and `put` are not effects here"
    This rule asks *"would refusing now leave a partial change?"*, which is a
    narrower question than *"is this pure?"* — the one asked of
    [functions](#purity).

    `send`, `tell` and `yield` are **transmissions**: any state they cause is
    somewhere else and later, which is a remote "maybe" a locally-refusing
    statement can live with. `become` changes *behaviour*, not state. `put`
    delivers to an [output](#put-statement). None of them can leave this
    definition half-changed, so none of them has to come after the refusals.

    This matters in practice: "refuse **and** publish a rejection event" is a
    common idiom, and it is expressible precisely because a `send` may sit
    before an `error`.

<!-- riddl: in-clauses -->
```riddl
on cmd: command Withdraw {
  require cmd.amount > Zero        // refusals first
  require balance >= cmd.amount
  set field balance to "balance - amount"   // then effects
  yield event Withdrawn(amount = cmd.amount)
}
```

### Do Statement

Describes an action in natural language for later implementation:

<!-- riddl: in-handler -->
```riddl
do "Calculate the total price including all applicable taxes and discounts"
```

This is useful for describing business logic that will be implemented in
target code.

!!! warning "The `prompt` statement is deprecated"
    `do` is canonical. `prompt "..."` still builds the same node and emits a
    `[deprecated]` message; prettified output normalizes it to `do`.

    Do not confuse it with the `prompt(...)` **value**, which is a different
    construct distinguished by its parentheses — it denotes a value computed by
    AI rather than an action described for a human.

### Code Statement

The `code` statement is RIDDL's deliberate **escape hatch**: an opaque
pass-through of raw target-language source, handed to the code generator
untouched.

It is written as a fenced block with a language tag:

<!-- riddl: in-context -->
````riddl
```scala
val total = items.map(_.price).sum * (1 - discountRate)
```
````

The language tag must be one of exactly four: **`scala`**, **`java`**,
**`python`**, **`mojo`**.

RIDDL does not parse, check, or understand the contents. Everything between
the fences is carried through verbatim.

#### Where it is allowed

Everywhere. Unlike every other statement, `code` is subject to none of the
scope rules:

| Rule | Applies to `code`? |
|------|--------------------|
| [Functions must be pure](#functions) | **No** — `code` is legal in a function body |
| `on activate` / `on passivate` must be side-effect free | **No** — `code` is legal there |
| [Refusals must precede effects](#refusals-before-effects) | **No** — `code` is neither, so it never trips the check |

That is not an oversight. RIDDL cannot classify opaque source: it has no way
to know whether a block of Scala writes state, sends a message, or computes a
number, so it declines to guess rather than guessing wrong.

!!! warning "Using it opts out of the guarantees"
    Every rule above exists to give a model a property worth having — a
    function that is provably pure, a lifecycle clause that provably does not
    emit, a handler that provably refuses before it acts. A `code` block
    suspends those guarantees for as long as it lasts, and it makes the model
    specific to one target language.

    That is a real trade and worth making deliberately. Prefer
    [`do "..."`](#do-statement) to describe intent and let the generator
    implement it; reach for `code` when a generator genuinely cannot express
    what you need.

!!! info "The tag is matched by prefix"
    The parser matches the four tags as prefixes, so `javafoo` and `pythonic`
    are currently accepted, with the surplus text treated as part of the code
    body. Do not rely on this — only the four tags above are supported, and
    the leniency may be tightened.

### Become Statement

Switches the live handler of an entity:

<!-- riddl: in-handler -->
```riddl
become entity Order to handler ShippedHandler
```

## Functions

Functions define reusable, **pure** operations. A function's `requires` and
`returns` may name an existing type rather than spelling out an aggregation,
which makes unary and nullary functions natural:

<!-- riddl: skip reason="calls `Tax.Apply`, which this page never defines; the prelude cannot supply a `Tax` because the in-function wrapper already owns that name" -->
```riddl
function CalculateTotal is {
  requires record TotalInputs
  returns Price

  return call function Tax.Apply(subtotal)
} with {
  briefly as "Calculates the final cart total"
}
```

The inline aggregation form still works:

<!-- riddl: skip reason="declares its inputs and outputs as inline anonymous aggregates, which 2.0 marks deprecated in favour of a named record" -->
```riddl
function CalculateTotal is {
  requires { subtotal is Price, taxes is Price, shipping is Price }
  returns { total is Price }
  do "Add subtotal, taxes and shipping"
}
```

!!! warning "Functions must be pure"
    A function body may not write entity state (`set`, `morph`, `become`), nor
    `send`, `tell` or `yield`. This is enforced **at parse time**, so an effect
    statement can never enter a function's AST.

    Refusals (`require`, `error`) and pure computation (`let`, `when`, `match`,
    `foreach`, `do`, `return`, code blocks) remain legal.

!!! warning "The inline `requires { … }` form is deprecated"
    Naming a type is preferred. The inline aggregation emits a `[deprecated]`
    message but continues to work.

## Sagas

Sagas coordinate multi-step processes with compensation:

<!-- riddl: in-context -->
```riddl
saga CheckoutProcess is {
  requires record CheckoutInputs
  returns record CheckoutOutcome

  step TakePayment is {
    tell command ProcessPayment(CheckoutInputs.orderId) to entity PaymentService
  } reverted by {
    tell command RefundPayment(CheckoutInputs.orderId) to entity PaymentService
  } with {
    briefly as "Processes payment for the order"
  }

  step ReserveStock is {
    tell command ReserveItems(CheckoutInputs.orderId) to entity Inventory
  } reverted by {
    tell command ReleaseItems(CheckoutInputs.orderId) to entity Inventory
  } with {
    briefly as "Holds the items until payment settles"
  }
} with {
  option is compensate
  briefly as "Orchestrates the checkout process steps"
}
```

### Saga Options

| Option | Meaning |
|--------|---------|
| `compensate` | On failure, run the accumulated steps' undo blocks in reverse |
| `parallel` | Start all steps at once; the coordinator gathers results asynchronously. Any one failure compensates in reverse order of the original sends. |

A saga is sequential by default, so there is no `sequential` option.

!!! warning "Saga Validation"
    **Errors:**

    - A saga step that references a definition owned by a **different domain**.
      A saga orchestrates a transaction within one bounded domain.

    **Warnings:**

    - A step's do-block containing more than one potential failure point.
      A step's do/undo is all-or-nothing, so it should have at most one place
      it can fail — split the step. `send`, `tell`, `yield` and `put` can fail,
      as can each embedded `call` or `get`.

    **Completeness Warnings:**

    - Saga step do-statements that drive no command

## Repositories

Repositories define persistence:

<!-- riddl: in-context no-prelude=Cart -->
```riddl
// `record Cart` here, not the page's `entity Cart`: a schema stores DATA.
record CartLine is { id: ProductId, quantity: Natural }
record Cart is { items: many CartLine }

repository CartRepository is {
  schema CartData is relational of
    cart as record Cart
    link cartItems as field Cart.items.id to field Product.id

  handler CartRepositoryHandler is {
    on event CartCreated {
      do "Persist the new cart record to the database"
    }
    on other { error "Unrecognized message" }
  }
} with {
  briefly as "Persistent storage for shopping cart data"
}
```

### Repositories at Domain Scope

A repository that synthesizes messages from entities across several contexts,
and is queried by several contexts, may be declared directly in a Domain rather
than in a Context.

!!! warning "Repository Scope Validation"
    A repository's **reach** is the set of contexts owning the messages its
    `on` clauses handle.

    - **Error**: a domain-scoped repository reaching only ONE context. It is
      provably unnecessary at domain scope — move it into that context.
    - **CompletenessWarning**: a context-scoped repository reaching another
      context. Consider promoting it to domain scope.

## Adaptors

Adaptors translate messages between bounded contexts. They handle the
transformation needed when one context communicates with another that uses
different message formats or terminology.

### Direction

Adaptors specify a direction relative to a context:

- `from context X`: Receives messages from context X, translates for local use
- `to context X`: Sends messages to context X, translating from local format

### Example

<!-- riddl: in-domain no-prelude=OrderContext -->
```riddl
context OrderContext is {
  event OrderPaymentReceived is { orderId is UUID }
  outlet OrderEvents is type OrderPaymentReceived

  adaptor PaymentIntegration from context PaymentContext is {
    handler InboundPayments is {
      on evt: event PaymentContext.PaymentCompleted {
        let orderId = evt.reference
        send event OrderPaymentReceived(orderId) to outlet OrderEvents
      }
      on other {
        error "Unrecognized payment event"
      }
    }
  } with {
    briefly as "Translates payment events for order processing"
  }
}
```

!!! warning "The Isolation Seam"
    An adaptor bridges exactly **two** contexts: its parent context and its
    referent context. It is the only sanctioned crossing point between
    contexts, so it must not traffic in a **third** context's messages.

    A message whose owning context is neither the parent nor the referent is an
    **Error**. Types defined at domain or root level are shared vocabulary
    common to both sides and are never flagged.

    Every adaptor handler must also have an `on other` clause.

## Projectors

Projectors transform and aggregate events into read models. They are key to
implementing CQRS, where the write model (entities) is separate from the read
model (projections).

### Purpose

- Project (transform) events from multiple sources into denormalized views
- Aggregate data for efficient querying
- Maintain materialized views updated by event streams

### Example

<!-- riddl: in-domain -->
```riddl
context ReportingContext is {
  projector SalesDashboard is {
    record DailySales is { day is Date, total is Decimal(10, 2) }
    updates repository SalesData

    handler SalesEventHandler is {
      on event OrderContext.OrderCompleted {
        do "Update daily sales totals with order amount"
      }
      on event OrderContext.OrderRefunded {
        do "Subtract refund amount from daily totals"
      }
    }
  } with {
    briefly as "Projects order events to sales dashboard"
  }
}
```

!!! warning "Projectors are event-only"
    `on command`, `on query` and `on record` are rejected **at parse time**
    inside a projector. Only `on event` and `on result` are valid.

    **Completeness Warnings:**

    - Projectors not referencing any repository
    - Projector handlers not `tell`ing to a repository
    - Declared repository references never used in `tell`

## Streaming Processors

Streaming processors define components for building data pipelines with typed
input ports (inlets) and output ports (outlets).

### Inlets and Outlets

- **Inlet**: A typed input port that receives messages
- **Outlet**: A typed output port that sends messages

Every processor kind may declare ports — not just streamlets. An entity may
own an outlet; a projector may own an inlet.

<!-- riddl: in-domain -->
```riddl
context DataPipeline is {
  processor OrderEventSource as source is {
    outlet OrderEvents is type OrderEvent
  } with {
    briefly as "Streams order events from the event store"
  }

  processor OrderEnricher as flow is {
    inlet RawOrders is type OrderEvent
    outlet EnrichedOrders is type EnrichedOrderEvent

    handler EnrichmentHandler is {
      on event OrderEvent {
        do "Look up customer details and product information"
        send event EnrichedOrderEvent(OrderEvent.orderId, region = "EU") to outlet EnrichedOrders
      }
    }
  }

  processor AnalyticsSink as sink is {
    inlet AnalyticsEvents is type EnrichedOrderEvent

    handler AnalyticsHandler is {
      on event EnrichedOrderEvent {
        do "Send event to analytics platform"
      }
    }
  }
}
```

### Portlet Options

| Option | Applies to | Meaning |
|--------|-----------|---------|
| `async` | Inlet, Outlet | A deliberate codegen async boundary; the generator inserts a real boundary here rather than fusing the stream |
| `ordered` | Connector, Inlet | Delivery preserves order |
| `unordered` | Connector, Inlet | Delivery order is not significant |

!!! warning "Streaming Validation"
    **Errors:**

    - An ascribed shape that contradicts the declared port arity
    - A port referenced by more than one connector (see below)

    **Style Warnings:**

    - A processor with at least one port and no `as <shape>` ascription
    - A connected pipeline in which **every** portlet is `async`. Nothing can
      be fused, so the stream pays message-passing overhead at every boundary
      and typically runs slower than a fused one.

    **Completeness Warnings:**

    - Isolated processors not connected to any connector
    - Sources without a downstream path to a sink
    - Sinks without an upstream path from a source
    - Unattached inlets and outlets
    - Flow/Split/Router handlers that don't send to outlets

## Connectors

Connectors link an outlet to an inlet, defining how data flows between
processors.

### Syntax

```
connector [name] is from outlet [source.outlet] to inlet [target.inlet]
```

### Example

<!-- riddl: skip reason="continuation of the pipeline fence above; the processors it connects are declared there" -->
```riddl
context DataPipeline is {
  connector OrderFlow is
    from outlet OrderEventSource.OrderEvents
    to inlet OrderEnricher.RawOrders
  with {
    briefly as "Connects order source to enrichment"
  }
}
```

### Port Cardinality

**Exactly one connector may attach to any given port.** Fan-in and fan-out are
modeled by declaring multiple *ports* — a `merge` or `split` shape derives from
its arity — never by attaching several connectors to a single port.

More than one connector on a port is an **Error**.

### Connector Scope

A connector may be declared in a Context or, when it joins ports in two
different contexts, in the enclosing Domain.

!!! warning "Connector Placement Validation"
    - **Error**: the two ends resolve to different **domains**. A stream edge
      across a domain boundary is a failure of domain analysis.
    - **Error**: a domain-scoped connector whose ends share one context
      (over-scoped) — move it into that context.
    - **Error**: a context-scoped connector whose ends cross contexts
      (under-scoped) — promote it to domain scope.
    - **CompletenessWarning**: a domain-scoped connector that **crosses**
      between two different contexts without the `persistent` option.
      Durability at a context boundary can be model correctness, not merely
      deployment. A connector with both ends inside the *same* external context
      does not cross anything and is not asked for it.
    - **Error**: a cross-context connector that reaches **past** a context
      boundary. Each end must land on the context's **own** portlet — the
      source context's outlet, the target context's inlet — never on a portlet
      declared by something the context contains.

!!! info "Why the boundary rule is an Error"
    A context publishes a public API — its message set — while its
    representations stay private. Wiring a cross-context connector to a
    contained entity's inlet binds a peer to that entity's existence and to its
    current command set, so the entity can no longer change without breaking a
    stranger. That contradicts the bounded context rather than under-stating
    it.

    **Inside** one context the rule does not engage at all: any processor,
    streamlet or connector may talk to any other, and a connector may drive a
    contained entity's inlet directly.

### Pipeline Pattern

<!-- riddl: in-domain -->
```riddl
context EventProcessing is {
  processor Events as source is { outlet Raw is type RawEvent }
  processor Validate as flow is {
    inlet In is type RawEvent
    outlet Out is type ValidatedEvent
  }
  processor Store as sink is { inlet In is type ValidatedEvent }

  connector Step1 is from outlet Events.Raw to inlet Validate.In
  connector Step2 is from outlet Validate.Out to inlet Store.In
}
```

## The Standard Module

Every model has access to a predefined module named `Riddl`, with no import and
no author declaration required. It provides the two stream terminators that the
one-connector-per-port rule makes structurally necessary:

| Definition | Kind | Purpose |
|------------|------|---------|
| `BottomlessPit` | sink | Consumes everything delivered to its inlet `hole` and emits nothing |
| `ForeverEmpty` | source | Never produces anything on its outlet `void` |
| `Drain` | type | `Anything`, so one drain absorbs every message type |

<!-- riddl: in-context -->
```riddl
connector DiscardUnused is
  from outlet MyProcessor.Unused
  to inlet BottomlessPit.hole
```

Reaching `BottomlessPit` terminates a pipeline exactly as a modeled sink does,
and `ForeverEmpty` originates one, so neither draws reachability warnings. The
port-cardinality rule is waived for them: many connectors may share the
universal drain.

A model that ignores the standard module is completely unaffected by it — the
module is never added to your model's contents.

## UI Components

RIDDL supports UI modeling. **UI may only be modeled inside an `application`
context.**

<!-- riddl: in-domain no-prelude=Storefront -->
```riddl
application context Storefront is {
  command PlaceOrder is { cartId is UUID }
  record PaymentDetails is { cardToken is String, amount is Decimal(10, 2) }

  page ProductDetails is { ??? } with {
    briefly as "Page showing product information"
  }

  page ShoppingCart is {
    button Checkout activates command PlaceOrder with {
      briefly as "Checkout button to proceed to payment"
    }
  }

  page Payment is {
    form PaymentEntry submits record PaymentDetails
  }
} with {
  briefly as "User interface components for the system"
}
```

An input element always names a **defined** type — a command it triggers, or a
record it submits. A predefined type such as `Boolean` will not do: the
reference is resolved against the model, and predefined types are not
definitions in it.

### Element Aliases

| Role | Keyword and aliases |
|------|---------------------|
| Group | `group`, `page`, `pane`, `dialog`, `menu`, `popup`, `frame`, `column`, `window`, `section`, `tab`, `flow`, `block`, `scene`, `space`, `zone` |
| Output | `output`, `document`, `list`, `table`, `graph`, `animation`, `picture`, `sound`, `speech`, `haptic` |
| Input | `input`, `form`, `text`, `button`, `picklist`, `selector`, `item`, `voice`, `gesture`, `gaze` |

### Interaction Verbs

- **Presentation** (outputs): `presents`, `shows`, `displays`, `writes`,
  `emits`
- **Acquisition** (inputs): `acquires`, `reads`, `takes`, `accepts`, `admits`,
  `enters`, `provides`, `selects`, `chooses`, `picks`, `initiates`, `submits`,
  `triggers`, `activates`, `starts`

!!! warning "UI Validation"
    **Errors:**

    - A `group` (or alias) in a context that is not an `application` context

    **Style Warnings:**

    - An input using a **selection** verb (`selects`, `chooses`, `picks`)
      whose type is not a choice among options — that is, not an Enumeration
      or Alternation

## Epics and Use Cases

Epics model user stories:

<!-- riddl: in-domain -->
```riddl
epic ShoppingCartEpic is {
  user Customer wants to "add items to a shopping cart"
  so that "they can purchase multiple items at once"

  case AddingToCart is {
    user Customer must "add products to cart"
    so that "they can purchase them later"

    step focus user Customer on page Storefront.ProductDetails
    step take input Storefront.ProductDetails.AddToCartForm from user Customer
    step send command AddToCart from context Storefront to entity Cart
    step show output Storefront.ShoppingCart.CartSummary to user Customer
    step entity Cart refuses user Customer "the item is out of stock"
  } with {
    briefly as "Adding products to the shopping cart"
  }
}
```

Two rules shape those steps. Inputs and outputs are **group** contents, so a
step names the page that holds them, not the context directly. And a user may
only interact at the **application boundary**: the command travels from
`context Storefront` to the entity, not from the user to the entity. Routing a
user's command straight at an entity is an Error.

### User Story Verbs

The user-story verb may be any of `wants`, `must`, `shall`, `should`, `may`,
`will`, `can`. All variants parse to the same structure — the modality is
vocabulary, not captured data.

### Interaction Step Kinds

| Step | Syntax |
|------|--------|
| Focus | `step focus <user> on <group>` |
| Direct | `step direct <user> to <url>` |
| Select | `step <user> selects <input>` |
| Take input | `step take <input> from <user>` |
| Show output | `step show <output> to <user>` |
| Refusal | `step <source> refuses <user> "<reason>"` or `… invariant <ref>` — the invariant form ties the step to the `require` that enforces it |
| Send message | `step send <message> from <source> to <target>` |
| Self-processing | `step for <ref> is "<description>"` |
| Arbitrary | `step from <source> "<relationship>" to <target>` |
| Vague | `step is "<subject>" "<verb>" "<object>"` |

The **refusal** step is new in 2.0. It models a system element declining a
user's request, which previously had no way to be expressed except as free
text:

<!-- riddl: in-usecase no-prelude -->
```riddl
step entity Cart refuses user Customer "the item is out of stock"
```

The **arbitrary** and **vague** steps carry free prose rather than typed
references, so they are the two that the AI-translatability check examines.

Steps may be grouped with `sequence { … }`, `parallel { … }` and
`optional { … }`.

!!! warning "Users interact only at the application boundary"
    A User may not reach past the application straight into the domain. For the
    two untyped step kinds — arbitrary and send-message — when exactly one side
    resolves to a User, the other side must be a UI element or a definition
    whose enclosing context has the `application` intention. Otherwise it is an
    **Error**.

!!! warning "Use Case Completeness"
    RIDDL analyzes whether each use-case step is **witnessed** by the model's
    structure, and whether the ordered sequence of steps is an **admissible
    trace** through the state machines of the entities it drives. Both emit
    **CompletenessWarnings**:

    - A `send` step whose receiver has no matching `on` clause, or no reachable
      wiring from sender to receiver
    - A `show output` step with no handler doing `put … to <output>`
    - A `take`/`select input` step whose input type nothing consumes
    - A message delivered to an entity in a state that does not handle it
    - A step whose free-text prose contains no word found in the in-scope
      vocabulary, so it is unlikely to be AI-translatable into a test. Adding
      `term` definitions and descriptions enlarges the vocabulary and quiets
      this.

## Modules and Imports

A **module** is a named, flat collection of any top-level definition:

```riddl
module Commerce is {
  domain Shopping is { ??? }
  type Money is Decimal(12, 2)
  author Reid is { name is "Reid Spencer" email is "reid@ossuminc.com" }
}
```

Modules can be compiled to a binary `.bast` file and imported by other models.

### Importing

The **full** form takes everything the file's root module holds:

<!-- riddl: skip reason="loads a BAST file that does not exist; nothing on disk can satisfy it" -->
```riddl
import "commerce.bast"
```

The **selective** form takes exactly one named definition, optionally renamed:

<!-- riddl: skip reason="loads a BAST file that does not exist; nothing on disk can satisfy it" -->
```riddl
import domain Shopping from "commerce.bast"
import type Money from "commerce.bast" as Currency
```

An importable kind may be any of `domain`, `context`, `entity`, `type`, `epic`,
`saga`, `adaptor`, `function`, `projector`, `repository`, `streamlet`,
`author`, `module`, `user`, `connector`, `constant`, `invariant`.

An imported definition must be structurally legal **where the directive sits**,
exactly as if it had been written there by hand. An illegal placement is an
**Error**.

### Import vs Include

- `include "file.riddl"` splices **source** text; the parser rules are
  determined by the enclosing container.
- `import "file.bast"` loads **compiled** definitions from a binary module.

!!! warning "Include Hygiene"
    - **StyleWarning**: an included file whose path does not end in `.riddl`
    - **MissingWarning**: an include that parsed but contributed no definitions

## Version

A `version` declares a component of a scope's version coordinate. It is either a
name or a natural number, never both:

```riddl
domain Garibaldi is {
  version Garibaldi
  context Ordering is {
    version 4
    command Reorder is { orderId is UUID }
    record OrderState is { status is String }
    entity Order is {
      version 3
      state Open of record OrderState is {
        handler OrderHandler is { on command Reorder { ??? } }
      }
    }
  }
}
```

A definition's precise version is **composed** from every versioned ancestor,
root to leaf, joined with `.`. The `Order` entity above is `Garibaldi.4.3`. Only
scopes that actually bear a version contribute a component, so an unversioned
context would give `Garibaldi.3` — which is what makes adoption incremental.

Versions may be declared at Root, Module, Domain, and all six processor kinds.
Declaring more than one version in a single scope is an **Error**.

!!! warning "A version coordinate is not a semantic version"
    The composed form *looks* like semver but is a **hierarchical coordinate**.
    Do not read compatibility into it: `3.1.6` → `3.2.1` says nothing about
    breakage, and `Garibaldi.4.3` is not orderable against `Jellyfish.1.1` at
    all. Its length varies with nesting depth, so comparison must be
    component-wise. A generator targeting a semver-demanding ecosystem needs an
    explicit mapping rule.

## Copyright

A `copyright` is a **named** notice carried verbatim:

```riddl
domain Shopping is {
  copyright House is "© 2026 Ossum Inc."

  external context StripePayments is {
    copyright Stripe is "© 2026 Stripe, Inc."
  }
}
```

The literal string is the notice **in its entirety** — symbol, year and holder —
because notices vary by jurisdiction, holder and license.

Unlike `version`, a copyright does **not** compose. The applicable notice is the
one declared by the definition itself or, failing that, by the **nearest**
ancestor that declares one. That is the point of allowing it at inner scopes: a
vendored `external context` bearing a third party's notice must *override* its
enclosing domain's, not be appended to it.

Copyrights may be declared at the same nine scopes as versions. Declaring more
than one in a single scope is an **Error**.

## Metadata

Metadata goes in a `with { }` block **after** the closing brace of the
definition:

<!-- riddl: in-context no-prelude=Product -->
```riddl
event-sourced entity Product is {
  // Entity definition content
  ???
} with {
  briefly as "Product available for purchase"
  described by {
    | Represents a product in the catalog that customers can purchase.
  }
  by author Reid
  term SKU is {
    | Stock Keeping Unit, the unique identifier for a variant
  }
}
```

The available metadata kinds are `briefly`, `described by`/`described at`/
`described in file`, `term`, `option`, `by author`, `figma`, `attachment` and
comments.

!!! warning "Metadata Validation"
    **Style Warnings:**

    - Repeating a single-valued metadata kind (`briefly`, `ulid`). Only the
      first is used. `author`, `see`, `term`, `option`, `comment` and
      `described` may be repeated freely.
    - The same `term` name defined at two scopes with **different** definition
      text. Identical redefinitions are fine.

    **Missing Warnings:**

    - A Domain that identifies no author, considering its own author
      references and defined authors as well as those of any enclosing domain

### Figma References

A `figma` reference connects a model element to the exact frame in a Figma file
that depicts it:

<!-- riddl: in-domain no-prelude=Storefront -->
```riddl
application context Storefront is {
  page Checkout is { ??? } with {
    figma "aBcD1234" node "42:1337"
  }
}
```

The two literal strings are the file key and the node id — exactly the two
arguments the Figma REST API takes — so the reference resolves to **one frame**
rather than a document a human must search.

It is metadata, not a definition: it has no identifier, nothing can
path-reference it, and it contributes nothing to the symbol table. It is
permitted on `Input`, `Output`, `Group`, and an `application` context — the
definitions that describe user interface.

!!! warning "Drift validation is opt-in and off by default"
    With `--check-figma-drift` and a `FIGMA_TOKEN` in the environment, a node
    the API does not know about is an **Error**, and a frame whose name does not
    correspond to the annotated definition's name is a **Warning**. Names are
    compared on letters and digits only, so `Payment Screen`, `PaymentScreen`
    and `payment_screen` all correspond.

    An offline build cannot be affected: the flag is off by default, no token
    means no client, and every failure to reach or understand the API produces
    nothing at all. Only a successful API answer can produce a message.

## Validation Message Severity

RIDDL's validator produces messages at the following severity levels (from
lowest to highest):

| Severity | Kind | Description |
|:---:|---|---|
| 0 | Info | Informational notes |
| 1 | StyleWarning | Naming and style conventions |
| 2 | MissingWarning | Missing optional content |
| 3 | UsageWarning | Unused definitions or unreferenced declarations |
| 3 | **Deprecation** | Use of a construct slated for removal |
| 4 | **CompletenessWarning** | Model is valid but incomplete for implementation |
| 5 | Warning | Likely mistakes or problematic patterns |
| 6 | Error | Invalid constructs that prevent compilation |
| 7 | SevereError | Fatal errors that halt processing |

**Deprecation** messages are rendered with their own `[deprecated]` label rather
than being folded in with ordinary warnings, so a model can be checked for zero
deprecations independently of zero warnings. They surface under every command —
`parse`, `validate`, `stats`, `bastify` and the prettify and generation
commands — not only `validate`.

**CompletenessWarning** (severity 4) identifies models that parse and validate
correctly but are missing details needed for a complete, implementable
specification. They can be toggled with the `-c` /
`--show-completeness-warnings` CLI flag (default: `true`).

Messages at severity 4 and above are considered **actionable** — they should be
addressed before considering a model ready for translation or code generation.

## Best Practices

1. **Include Metadata**: Add descriptions to all definitions in `with` clauses
   after their closing braces.
2. **Be Explicit**: Always specify reference kinds (entity, command, event…).
3. **Ascribe Shapes**: Write `as <shape>` on any processor with ports, so the
   intent is stated rather than inferred.
4. **Name Constants**: Comparisons require typed references, so give thresholds
   names — `constant MaxItems is Natural = 100` — rather than embedding
   magic numbers.
5. **Declare `yields`**: A command or query that declares its response gives
   generators a precise signature and lets the validator check conformance.
6. **Mark `initial`**: Marking the starting state and handler explicitly makes
   a model safe to reorder.
7. **Refuse First**: Put every `require` and `error` ahead of every effect.
8. **End When Statements**: Always terminate `when` with `end`.
9. **Use Match for Multiple Conditions**: Prefer `match` over a chain of `when`
   statements.
10. **Model Complete Flows**: Include UI components and user interactions, and
    keep all UI inside an `application` context.
11. **Follow Containment Rules**: Only define elements within their appropriate
    containers.
12. **Terminate Every Stream**: Every outlet needs a connector; route genuinely
    unused output to `BottomlessPit`.

## Common Parse Errors

Some mistakes produce an error that does not point at the thing that is
wrong. These are the ones worth recognising by their symptom.

### `Expected ("(")` at a field, far from any obvious cause

You have named one of your own types after a **parameterized predefined
type**. The parser reaches the reference, recognises the built-in name, and
demands its argument list — so the error is reported at the *use*, which may be
hundreds of lines from the declaration that caused it.

<!-- riddl: skip reason="deliberate counter-example; shows what does NOT work" -->
```riddl
type Currency is any of { USD, EUR, GBP, JPY }   // the actual cause
// ...
record Payment is {
  amount: Currency                                // Expected ("(") reported HERE
}
```

The fix is to rename your type — `CurrencyCode`, say.

Predefined names whose parentheses are **required** produce this misleading
form: `Currency`, `Decimal`, `Pattern`, `Id`. Naming a type after a **bare**
predefined instead gives a clear, well-located error at the declaration —
*"Type 'Location' redefines built-in type 'Location'"* — so those are easy.

The full set of reserved type names:

| Group | Names |
|-------|-------|
| Text | `String`, `Pattern`, `URL` |
| Numeric | `Boolean`, `Integer`, `Natural`, `Whole`, `Number`, `Real`, `Decimal` |
| Physical | `Current`, `Length`, `Luminosity`, `Mass`, `Mole`, `Temperature` |
| Temporal | `Date`, `Time`, `DateTime`, `TimeStamp`, `Duration`, `ZonedDate`, `ZonedDateTime` |
| Identity | `UUID`, `UserId`, `Id` |
| Other | `Currency`, `Location`, `Nothing`, `Anything`, `Abstract` |

Grep a model for these before you start if you are hunting an error of this
shape.

### `Expected one of ("*" | "+" | "," | …)` after a collection field

You have written `many of X`. The collection prefix is **`many`** with no
`of`:

<!-- riddl: skip reason="deliberate counter-example; shows what does NOT work" -->
```riddl
items: many ProductInfo     // correct
items: ProductInfo*         // equivalent
items: many of ProductInfo  // does not parse
```

`of` does belong to the *other* collection forms — `sequence of X`, `set of X`,
`graph of X`, `mapping from K to V` — which is what makes `many of` such an
easy slip.

### `Expected one of ("(" | "yields")` at the `is` of a message

The body is empty. RIDDL has no empty body; use the `???` placeholder:

<!-- riddl: skip reason="deliberate counter-example; shows what does NOT work" -->
```riddl
command Checkout is { ??? }   // correct
command Checkout is {}        // does not parse
```

The error lands on `is` rather than on the braces, because the parser is still
looking for what may follow the identifier.

### A comment after `???`

`???` **ends** the body, so nothing may follow it inside the braces. A comment
may, however, come *before* it — that is the whole point of the
`undefined = {comment} "???"` production:

<!-- riddl: skip reason="deliberate counter-example; shows what does NOT work" -->
```riddl
domain MyDomain is {
  // Start building your domain model here
  ???                       // fine -- the comment introduces the stub
}

domain MyDomain is {
  ???
  // Start building your domain model here
                            // does not parse -- ??? already closed the body
}
```

Both parts survive a prettify round trip. The comment is **kept** as part of
the container's contents, and the `???` is re-emitted for a body that holds
nothing but comments — because the marker records deliberate intent ("not
specified yet") that a bare comment does not.

## Undefined Bodies

`???` is available wherever a body may be left unspecified, and the same rule
applies at each: an optional run of comments, then the marker. That covers
container bodies (domain, context, entity, processor, repository, adaptor,
projector, group, handler, author), type bodies (`aggregate_definitions`,
`enumerators`, `alternation_contents`), statement blocks, `with { }` metadata
blocks and doc blocks.

## Common Syntax Issues

1. Don't use `=` to assign fields; use `set field x to <value>`. `let x = …` is
   valid for local bindings.
2. Don't forget `end` after `when` statements.
3. Always include reference kinds before identifiers.
4. `state … of` and `morph … with` take a **record**, not a message.
5. `send` targets an **outlet**; use `tell` for direct delivery to a processor.
6. A comparison operand must be a reference or a named constant, never a
   literal.
7. Place comments only where definitions are allowed, not within clauses.
8. Metadata blocks follow their definitions rather than being nested within
   them.
9. Never place entity, type, or repository definitions directly within a
   domain — they belong in a context. (A repository is the exception, when it
   genuinely spans contexts.)
10. Never place definitions inside an author — authors only contain metadata.
11. Use `when` for conditionals; `if` is not supported.
12. Use `do` for describing implementation logic, not bare quoted strings.
13. Every adaptor handler needs an `on other` clause.
14. Attach at most one connector to any port.

## Incomplete Definitions

Use `???` as a placeholder for incomplete definitions:

<!-- riddl: in-app-context -->
```riddl
record PaymentDetails is { ??? } with {
  briefly as "Record for payment information details"
}

page Checkout is { ??? } with {
  briefly as "Checkout page for completing purchase"
}
```

## Author Inheritance

Authors are defined once and inherited throughout the model hierarchy, but
cannot contain any definitions. An `author` **definition** may only appear in a
Module or a Domain body; everywhere else, reference one with `by author Name` in
the `with { }` block:

```riddl
domain ShopifyCart is {
  author Claude is {
    name is "Anthropic Claude"
    email is "support@anthropic.com"
  } with {
    briefly as "Model creator and maintainer"
  }

  context ShoppingContext is {
    ???
  } with {
    by author Claude
    briefly as "Main shopping context containing commerce entities"
  }
} with {
  briefly as "Shopping cart domain model"
}
```

## Deprecated Constructs

Everything below still parses in 2.x and emits a `[deprecated]` message. All of
it is slated for removal in 3.0.

| Deprecated | Replacement |
|------------|-------------|
| `source`/`sink`/`flow`/`merge`/`split`/`router` keywords | `processor <id> as <shape>` |
| `prompt "..."` statement | `do "..."` |
| `Abstract` type | `Anything` |
| `state X is record R`, or no introducer at all | `state X of record R` |
| `when "a natural-language condition"` | `when prompt("…")` |
| `send … to inlet X` | `send … to outlet Y`, or `tell` |
| anonymous nebula (top-level definitions with no wrapper) | `module <Name> is { … }` |
| `option is gateway`/`service`/`external`/`wrapper` | the context intention prefix |
| `requires { … }` inline aggregation | `requires <TypeRef>` |
