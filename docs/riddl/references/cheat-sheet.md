---
title: "RIDDL Cheat Sheet"
description: >-
  A dense, scannable reference for every RIDDL definition type—what it
  means, when to use it, where it lives, and what it contains.
---

# RIDDL Cheat Sheet

This page is a quick-lookup reference for every definition type in the
RIDDL language. Each entry distills the semantic purpose from the full
[Concepts](../concepts/index.md) documentation. For formal syntax, see
the [EBNF Grammar](ebnf-grammar.md). For narrative explanations, see
the [Language Reference](language-reference.md).

---

## Decision Guide

| I need to... | Use |
|---|---|
| Organize a knowledge area | [Domain](#domain) |
| Define a bounded context with services | [Context](#context) |
| Model a stateful business object | [Entity](#entity) |
| Persist data for later retrieval | [Repository](#repository) |
| Build a read-model / CQRS projection | [Projector](#projector) |
| Coordinate a multi-step atomic process | [Saga](#saga) |
| Translate messages between contexts | [Adaptor](#adaptor) |
| Process streaming data | [Processor](#processor-generic) |
| Connect two stream endpoints | [Connector](#connector) |
| Describe a user-facing interface | [`application` context](#application) |
| Capture a user journey | [Epic](#epic) / [Use Case](#use-case-case) |
| Define a data structure | [Type](#type) |
| Define a request, response, or notification | [Message](#message) |
| Declare what a command or query produces | [`yields` clause](#message) |
| React to incoming messages | [Handler](#handler) / [On Clause](#on-clause) |
| Create a reusable computation | [Function](#function) |
| Assert a precondition in a handler | [`require` statement](#concrete-statements) |
| Produce a query's result | [`yield` statement](#concrete-statements) |
| Iterate a collection | [`foreach` statement](#concrete-statements) |
| Show a value to a user | [`put` statement](#concrete-statements) |
| Refuse a user's request in a use case | [refusal step](#use-case-case) |
| Package definitions for reuse | [Module](#module) / [Import](#import) |
| Stamp a release coordinate | [Version](#version) |
| Attribute a legal notice | [Copyright](#copyright) |
| Link a UI element to its design | [Figma reference](#figma-reference) |
| Discard an unused stream | [Standard Module](#standard-module) |
| Split a model across files | [Include](#include) |

---

## Containment Hierarchy

```
Root
├── Domain
│   ├── Context                       (processor)
│   │   ├── Entity                    (processor)
│   │   │   ├── State
│   │   │   │   ├── Handler → On Clause → Statements
│   │   │   │   └── Invariant
│   │   │   ├── Handler → On Clause → Statements
│   │   │   ├── Inlet, Outlet
│   │   │   ├── Function
│   │   │   ├── Type, Constant, Invariant
│   │   │   ├── Version, Copyright
│   │   │   └── Include
│   │   ├── Repository                (processor)
│   │   ├── Projector                 (processor)
│   │   ├── Adaptor                   (processor)
│   │   ├── Processor                 (generic streaming processor)
│   │   │   ├── Inlet, Outlet
│   │   │   └── Handler
│   │   ├── Saga → Saga Step
│   │   ├── Connector
│   │   ├── Group (application contexts only)
│   │   │   ├── Input, Output
│   │   │   └── Group (nested)
│   │   ├── Handler, Function
│   │   ├── Inlet, Outlet
│   │   ├── Type, Constant, Invariant
│   │   ├── Version, Copyright
│   │   └── Include
│   ├── User
│   ├── Epic → Use Case
│   ├── Saga
│   ├── Repository                    (when it spans contexts)
│   ├── Connector                     (when it spans contexts)
│   ├── Type
│   ├── Author
│   ├── Version, Copyright
│   └── Include
└── Module (a flat bag of ANY top-level definition)
```

**Every** processor may declare Inlets and Outlets, a Version, and a
Copyright — not just streamlets. A Saga and a Function are *not* processors:
they are vital definitions, so they bear none of those.

| Level | Body definitions | Metadata (`with { }`) |
|---|---|---|
| **Root** | Domain, Module, Author, Version, Copyright, Include, Import | briefly, described by |
| **Module** | *any* top-level definition, flat and unordered | term, option, by author, briefly, described by, attachment |
| **Domain** | Context, User, Epic, Saga, Repository, Connector, Type, Author, Version, Copyright, Include, Import | term, option, by author, briefly, described by, attachment |
| **Context** | Entity, Repository, Projector, Saga, Adaptor, Processor, Connector, Group, + *processor contents* | term, option, by author, briefly, described by, attachment, figma (if `application`) |
| **Entity** | State, + *processor contents* | term, option, by author, briefly, described by, attachment |
| **Repository / Projector / Adaptor / Processor** | *processor contents* | term, option, by author, briefly, described by, attachment |
| **State** | Handler, Invariant | term, option, by author, briefly, described by, attachment |
| **Epic** | Use Case | term, option, by author, briefly, described by, attachment |
| **Saga** | Saga Step | term, option, by author, briefly, described by, attachment |

*Processor contents* = Handler, Function, Type, Constant, Invariant, Inlet,
Outlet, nested Processor, Connector, Relationship, Version, Copyright,
Comment, Include.

---

## Structural Definitions

### Root

**Purpose**: The implicit top-level container for an entire RIDDL model.

**When to use**: Every model has exactly one root—it is not explicitly
declared. It is simply the outermost scope of a `.riddl` file.

**Contains**: Domain, Module, Author.

> *[For more details →](../concepts/root.md)*

### Domain

**Purpose**: A knowledge-domain boundary that groups related bounded
contexts, types, users, and epics.

**When to use**: When you need to delineate a business area (e.g.,
"Sales", "Shipping", "Inventory"). Domains may nest sub-domains.

**Lives in**: Root, Module, or another Domain.
**Contains**: Context, User, Epic, Saga, Repository, Connector, Type,
Author, Version, Copyright, Include, Import.

**Key details**:

- Maps to a DDD Domain
- Nesting domains creates sub-domain hierarchies
- Types defined here are visible to all contained contexts
- A Repository or Connector may live here when it genuinely spans
  several contexts
- A domain that identifies no author draws a MissingWarning

> *[For more details →](../concepts/domain.md)*

### Module

**Purpose**: A named, **flat** collection of any top-level definition — the
unit of reuse and of compiled (`.bast`) output.

**When to use**: To package a group of definitions for import by other
models, or to organize a large root.

**Lives in**: Root or another Module.
**Contains**: Anything that can appear at top level, in any order, with no
hierarchy enforced at the module's own level. Each contained definition's
own rules still apply.

**Syntax**: `module Commerce is { ... }`

!!! warning "Nebula is deprecated"
    An anonymous whole-file sequence of definitions (a *nebula*) still parses
    but emits one `[deprecated]` message and yields a Module named `nebula`.
    Wrap definitions in `module <Name> is { … }` instead.

---

## Processors

A **processor** is any definition that can receive messages and declare
ports. All processors can contain Handlers, Functions, Types, Constants,
Invariants, Inlets, Outlets, Versions, Copyrights, and Includes.

### Streaming Shapes

A processor's shape is **derived** from its port arity and may optionally be
**ascribed** with `as <shape>`:

| Shape | Inlets | Outlets | Purpose | Synonym |
|---|---|---|---|---|
| `source` | 0 | 1+ | Produce data | |
| `sink` | 1+ | 0 | Consume data | |
| `flow` | 1 | 1 | Transform data | `cascade` |
| `merge` | 2+ | 1 | Combine streams | `fanin` |
| `split` | 1 | 2+ | Divide a stream | `broadcast`, `fanout` |
| `router` | 1 | 2+ | Route by content | |
| `void` | 0 | 0 | No ports at all | |

An ascription that contradicts the arity is an **Error**. Ports with no
ascription draw a suppressible **StyleWarning**.

### Context

**Purpose**: A bounded context—an autonomous service boundary with its
own ubiquitous language, types, and processors.

**When to use**: When you need an isolated area of the system with its
own data models and message contracts. Contexts are also how you model
applications (by adding Groups).

**Lives in**: Domain or Module.
**Contains**: Entity, Repository, Projector, Saga, Adaptor, Processor,
Connector, Group, plus all processor contents.

**Key details**:

- Maps to a DDD Bounded Context
- Context-level handlers act as the context's external API
- A Context is itself a processor, so it may hold ports of its own
- An optional **intention** prefix declares what kind of context it is

| Intention | Meaning |
|---|---|
| `application` | Presents a user interface — the only place UI may be modeled |
| `external` | A third-party system the model does not own |
| `gateway` | An entry point adapting the outside world to the inside |
| `service` | An internal service with no user interface |

**Syntax**: `application context Storefront is { ... }`

!!! warning "The `gateway`, `service`, `external` and `wrapper` options are deprecated"
    Use the intention prefix. The options still parse and emit a
    `[deprecated]` message.

> *[For more details →](../concepts/context.md)*

### Entity

**Purpose**: A stateful business object that responds to commands, emits
events, and manages its own lifecycle through state transitions.

**When to use**: When you need a uniquely identifiable object with
mutable state and business rules (e.g., Order, Customer, Account).

**Lives in**: Context.
**Contains**: State, Handler, Function, Type, Constant, Invariant,
Include. *(Note: options like `event-sourced` and `aggregate` go
in the `with { }` metadata block, not in the body.)*

**Key details**:

- Entities have one or more named States, each backed by a **record**
- An optional `initial` marker names the starting state and the handler
  live after a `morph`; without it, the first declared wins
- Supports `morph` (change state) and `become` (change handler)
- `on activate` / `on passivate` handle rehydration and eviction, and must
  be side-effect free
- Options: `event-sourced`, `aggregate`, `transient`, `available`,
  `consistent`, `message-queue`, `value`, `auto-id` (auto-assign ULID at
  instantiation)
- The primary unit of consistency in a reactive system

**Syntax**: `entity Order is { initial state Active of record OrderData ... }`

> *[For more details →](../concepts/entity.md)*

### Repository

**Purpose**: Persistent storage for entity or projection data—the
abstraction for a database, cache, or file store.

**When to use**: When a context needs to persist data beyond the
lifetime of individual messages.

**Lives in**: Context, or **Domain** when it synthesizes data across several
contexts.
**Contains**: Schema, plus all processor contents.

**Key details**:

- Defines a `schema` (flat, relational, time-series, graphical,
  hierarchical, star, document, columnar, vector, other)
- Handlers typically react to events and persist data
- Usually paired with a Projector for CQRS read-side writes
- A repository's **reach** is the set of contexts owning the messages its
  `on` clauses handle. A domain-scoped repository reaching only one context
  is an **Error**; a context-scoped one reaching another context draws a
  **CompletenessWarning** suggesting promotion.

> *[For more details →](../concepts/repository.md)*

### Projector

**Purpose**: Transforms and aggregates events into denormalized read
models—the write side of CQRS's read side.

**When to use**: When you need a materialized view optimized for queries
that differs from the entity's write model.

**Lives in**: Context.
**Contains**: `updates`, plus all processor contents.

**Key details**:

- Declares `updates repository X` to link to its target store
- **Event-only**: `on command`, `on query` and `on record` are rejected at
  parse time. Only `on event` and `on result` are valid.
- Handlers subscribe to events (often cross-context) and update the
  repository
- Multiple projectors can write to the same repository

> *[For more details →](../concepts/projector.md)*

### Saga

**Purpose**: Orchestrates a multi-step atomic process with compensation
logic for rollback on failure.

**When to use**: When a business process spans multiple processors or
contexts and must either complete entirely or be undone.

**Lives in**: Context or Domain.
**Contains**: Saga Step, plus `requires` and `returns` type signatures.

**Key details**:

- Each step has a forward action and a `reverted by` compensation block
- Steps execute sequentially; failure triggers compensation in reverse
- A Saga is a **vital definition, not a processor** — it bears no ports, no
  version and no copyright
- Options: `compensate` (run undo blocks in reverse on failure),
  `parallel` (start all steps at once). Sequential is the default, so there
  is no `sequential` option.
- A step referencing a definition owned by a **different domain** is an
  **Error** — a saga orchestrates within one bounded domain
- A step whose do-block has more than one potential failure point draws a
  **Warning**; split the step

> *[For more details →](../concepts/saga.md)*

#### Saga Step

**Purpose**: One step within a Saga—a unit of work with its own
compensation action.

**When to use**: Automatically, as part of defining a Saga.

**Lives in**: Saga.
**Contains**: Statements (forward action) and a `reverted by` block
(compensation action).

> *[For more details →](../concepts/sagastep.md)*

### Adaptor

**Purpose**: Translates messages between bounded contexts, bridging
differences in terminology and data formats.

**When to use**: When one context needs to communicate with another that
uses different message types or naming conventions.

**Lives in**: Context.
**Contains**: All processor contents.

**Key details**:

- Direction: `from context X` (inbound) or `to context X` (outbound)
- Handlers map foreign messages to/from the local context's types
- Implements the DDD Anti-Corruption Layer pattern
- **The isolation seam**: an adaptor bridges exactly two contexts — its
  parent and its referent. Trafficking in a **third** context's messages is
  an **Error**. Types defined at domain or root level are shared vocabulary
  and are never flagged.
- Every adaptor handler must have an `on other` clause, or it is an
  **Error** — an adaptor must say what it does with what it does not
  recognize

> *[For more details →](../concepts/adaptor.md)*

### Processor (generic) {#processor-generic}

**Purpose**: A stream-processing component with typed input/output ports for
building data pipelines.

**When to use**: When data needs to flow continuously through
transformation, filtering, merging, or routing stages.

**Lives in**: Context, or any other processor body.
**Contains**: Inlet, Outlet, plus all processor contents.

**Syntax**: `processor OrderEnricher as flow is { ... }`

See [Streaming Shapes](#streaming-shapes) for the arity table.

!!! warning "Deprecated shape keywords"
    `source`, `sink`, `flow`, `merge`, `split` and `router` as standalone
    keywords still parse but emit a `[deprecated]` message. Write
    `processor <id> as <shape>` instead.

> *[For more details →](../concepts/streamlet.md)*

---

## Data Definitions

### Type

**Purpose**: Defines a named data structure—the building block for all
messages, states, and parameters in RIDDL.

**When to use**: Whenever you need to name a data shape.

**Lives in**: Domain, Context, Entity, or any processor.

**Key details**:

- **Aggregation** (record): `type X is { field1: T1, field2: T2 }`
- **Alternation** (union): `type X is one of { T1, T2, T3 }` — zero
  alternatives is an Error, one draws a deprecation, `one of { ??? }` is
  undecided
- **Enumeration**: `type X is any of { A, B, C }`
- **Aggregate use cases**: `graph`, `table`
- **Collection**: `many T`, `set of T`, `mapping from K to V`, `T?`
- **Simple predefined types** — use the name alone, no parameters:
  `Anything`, `Nothing`, `Boolean`, `Current`, `Date`, `DateTime`,
  `Duration`, `Length`, `Luminosity`, `Mass`, `Mole`, `Number`,
  `String`, `Temperature`, `Time`, `TimeStamp`, `UUID`
- **Parameterized predefined types** — **require parenthesized
  arguments**; using these without parameters is invalid:
    - `String(min, max, enc)` — constrained string
    - `Id(entity)` — unique identifier for an entity type
    - `URL(scheme)` — URL with a specific scheme
    - `Range(min, max)` — bounded integer range
    - `LatLong(lat, long)` — geographic coordinates
    - `Currency(country-code)` — monetary amount
      (e.g., `Currency(USD)`)
    - `Pattern(regex)` — string matching a regular expression

`Anything` is the dual of `Nothing`: assignment-compatible with every type in
both directions. A port typed `Anything` is compatible with any port it joins.

!!! warning "`Abstract` is deprecated"
    Renamed to `Anything`. The old spelling parses to the same node and emits
    a `[deprecated]` message.

> *[For more details →](../concepts/type.md)*

### Field

**Purpose**: A named, typed member within an aggregation (record type)
or a message.

**When to use**: Inside type definitions and message definitions to
declare individual data elements.

**Lives in**: Type (aggregation), Message, State record.

> *[For more details →](../concepts/field.md)*

### State

**Purpose**: A named snapshot of an Entity's data at a point in time,
backed by a record type and optionally paired with state-specific
handlers.

**When to use**: Every Entity needs at least one State. Use multiple
states to model lifecycle stages (e.g., Draft, Active, Archived).

**Lives in**: Entity.
**Contains**: Handler (state-specific message handling), Invariant.

**Key details**:

- Syntax: `[initial] state X of record RecordName`
- The data type must be a **record** — a state is record-shaped data
- A state body may hold Invariants constraining that state's data
- The entity transitions between states via `morph`
- Each state can have its own handlers that override entity defaults
- More than one `initial` state in an entity is an **Error**

> *[For more details →](../concepts/state.md)*

### Message

**Purpose**: A typed data envelope for communication between processors.
RIDDL has four message kinds.

**When to use**: To define the contracts for inter-processor
communication.

**Lives in**: Context, Entity, or any processor.

| Kind | Keyword | Semantics |
|---|---|---|
| **Command** | `command` | Request to change state |
| **Event** | `event` | Notification that something happened |
| **Query** | `query` | Request for information |
| **Result** | `result` | Response to a query |

**Key details**:

- Commands should produce events (reactive principle)
- Events are past-tense facts; commands are imperative requests
- Queries and results form request-response pairs
- A command or query may declare its response with an optional `yields`
  clause: `command PlaceOrder yields event OrderPlaced is { ... }`.
  A command's must resolve to an event, a query's to a result.
  When declared, the handler must `yield` exactly that message.

!!! warning "A `record` is NOT a message"
    A record is **data**. It can never be sent, told, yielded, or handled.
    `send`, `tell`, `yield` and `on <ref>` take the four messages only;
    `state … of` and `morph … with` take a record. In RIDDL 1.x a record
    reference was accepted wherever a message reference was — it no longer is.

> *[For more details →](../concepts/message.md)*

### Constant

**Purpose**: A named, unchanging value.

**When to use**: For domain constants like thresholds, magic numbers, or
configuration values embedded in the model.

**Lives in**: Any vital definition (Domain, Context, Entity, etc.).

> *[For more details →](../concepts/constant.md)*

### Invariant

**Purpose**: A boolean condition that must always hold true for an
Entity's state.

**When to use**: To express business rules that the entity must never
violate (e.g., "balance >= 0").

**Lives in**: Any processor, or an Entity **State** body.

**Key details**:

- The condition may be a structured boolean expression, not just an opaque
  string: `invariant InStock is quantity >= Zero`
- A state-scoped invariant constrains that state's record data
- Reference one from a handler with `require invariant Name`
- An invariant never referenced by a `require invariant` draws a
  **UsageWarning**

> *[For more details →](../concepts/invariant.md)*

---

## Behavioral Definitions

### Handler

**Purpose**: Defines how a processor responds to incoming messages. A
handler is a collection of On Clauses, each matching a specific message
type.

**When to use**: In any processor that needs to react to commands,
events, queries, or lifecycle signals.

**Lives in**: Entity, Context, Repository, Projector, Adaptor,
Streamlet, State.

**Contains**: On Clause.

**Key details**:

- Entity handlers are the default; State handlers override them
- Context-level handlers act as the bounded context's API
- Multiple handlers per processor allow grouping by concern

> *[For more details →](../concepts/handler.md)*

### On Clause

**Purpose**: A single message-reaction rule within a Handler—"when this
message arrives, do these statements."

**When to use**: Inside a Handler to define behavior for each message
type.

**Lives in**: Handler.
**Contains**: Statements.

| Clause | Matches |
|---|---|
| `on command X` | A specific command message |
| `on event X` | A specific event message |
| `on query X` | A specific query message (use `yield` to produce the result) |
| `on result X` | A specific result message |
| `on init` | Processor initialization (once ever) |
| `on term` | Processor termination (once ever) |
| `on activate` | Entity rehydration (every time) |
| `on passivate` | Entity eviction (every time) |
| `on other` | Any unmatched message (catch-all) |

**Key details**:

- An `on` clause may bind a local name to the handled message using type
  ascription: `on ord: command PlaceOrder { when ord.total > Min then ... }`.
  Within the body the name denotes the whole message.
- It may also name the origin: `on command X from context Other { ... }`
- `on activate` / `on passivate` are **entity-only** and must be
  side-effect free — `send`, `tell`, `yield`, `morph` and `become` are
  rejected at parse time
- `require` and `error` are forbidden in `on event` — an event has already
  happened and must always be accepted
- Two clauses in one handler handling the same message draw a
  **StyleWarning**; the later one is unreachable

> *[For more details →](../concepts/onclause.md)*

### Function

**Purpose**: A reusable, named computation with typed inputs (`requires`)
and outputs (`returns`).

**When to use**: When logic needs to be shared across handlers or
extracted for clarity.

**Lives in**: Context, Entity, or any processor.
**Contains**: Statements.

**Key details**:

- Functions are **not** Turing complete—they express structured
  pseudocode
- Functions must be **pure**. A body may not `set`, `morph`, `become`,
  `send`, `tell` or `yield`. This is enforced at *parse* time, so an effect
  statement can never enter a function's AST. Refusals (`require`, `error`)
  and pure computation stay legal.
- `requires` and `returns` take a **named type reference** —
  `requires Age`, `requires record Args`, `returns Price` — which makes
  unary and nullary functions natural
- Use `return <value>` to produce the result, and `do "..."` to describe
  logic for later implementation
- Invoke one with the `call` value expression:
  `let total = call function Pricing.Total(subtotal)`

!!! warning "The inline `requires { … }` form is deprecated"
    It still works but emits a `[deprecated]` message. Name a type instead.

> *[For more details →](../concepts/function.md)*

### Concrete Statements

Statements are the actions inside On Clauses, Functions, and Saga Steps.
RIDDL is intentionally **not** Turing complete—statements capture
interactions between definitions, not full implementations.

#### Value Expressions

Wherever a statement needs a value, any of these is accepted:

| Form | Syntax | Meaning |
|---|---|---|
| Literal | `"some text"` | Opaque pseudo-code or a literal constant |
| Value reference | `order.total` | A field, state field, function input, or `let` local |
| Constructor | `OrderPlaced(id, total = x)` | Builds a message or record; positional args first, then named |
| Get | `get from input SignupForm` | Reads a UI input or an entity state |
| Call | `call function Pricing.Total(a, b)` | Invokes a pure function for its result |
| Prompt | `prompt("compute the discount")` | A value computed by AI at generation time |
| Boolean | `a > b and not c` | A structured boolean expression |

!!! warning "Comparisons are type-safe and ref-only"
    Both operands must be a value reference, a `get from`, or a named
    `constant` — never a literal. `count > 5`, `count > "5"` and
    `count > true` all fail at **parse** time. Name the threshold instead:

    ```riddl
    constant MaxItems is Natural = "100"
    when cart.itemCount > MaxItems then error "too many" end
    ```

    `==`/`!=` need operands of the same category; `<`/`>`/`<=`/`>=` need an
    ordered (numeric) type on both sides.

`and`, `or`, `not`, `true` and `false` are context-sensitive: recognized only
inside a boolean expression, so they remain legal identifiers elsewhere.

#### Control Flow

| Statement | Syntax | Description |
|---|---|---|
| `when` | `when <cond> then { ... } else { ... } end` | Conditional; `end` required. Condition may be a boolean expression, a bare boolean-typed reference (`order.isPaid`), a `let` binding or `!binding`, or a literal string. |
| `match` | `match <subject> { case <pattern> [when <bool>] { ... } default { ... } }` | Multi-way branch over a typed subject; closed by `}`. |
| `foreach` | `foreach x in field order.lines { ... }` | RIDDL's only loop — bounded iteration over a collection field or `let` local. |

A `match` pattern is a **type case** (`case Pending`), a **comparison**
(`case >= Threshold`, with the subject as implicit left operand), or a legacy
**literal** (`case "pending"`). An unknown type-case name is an **Error**; a
non-exhaustive match over a closed subject without `default` draws a
**StyleWarning**.

#### Messaging

| Statement | Syntax | Description |
|---|---|---|
| `send` | `send event X to outlet Y` | Emit on one of *this* processor's own outlets; a connector routes it onward. |
| `tell` | `tell command X to entity Y` | Deliver a message directly to a processor (point-to-point). |
| `yield` | `yield result ProductInfo(id, name)` | Produce a command's or query's declared response, without knowing the sender. |

The message operand may be a bare reference or an inline constructor.

#### Data

| Statement | Syntax | Description |
|---|---|---|
| `set` | `set field status to <value>` | Assign to a state field. Also accepts a state ref: `set state X to <value>`. |
| `let` | `let total = <value>` | Create a local binding. Optional annotation: `let total: Decimal = ...`; otherwise inferred. Lexically scoped and statement-ordered. |
| `put` | `put order.number to output Panel` | Publish a value to a UI output. Application and context handlers only. |
| `return` | `return <value>` | Return a function's result. Function bodies only. |

#### Preconditions

| Statement | Syntax | Description |
|---|---|---|
| `require` | `require amount > Zero` | Assert a precondition as a boolean expression. |
| `require` | `require "the customer is in good standing"` | Assert a precondition as a literal string. |
| `require` | `require invariant BalanceNonNegative` | Assert a precondition by referencing a named invariant. |

!!! warning "Refusals before effects"
    Within any single linear statement list, every refusal (`require`,
    `error`) must precede every effect (`set`, `morph`, `become`, `send`,
    `tell`, `yield`, `put`). Acting and then refusing would leave partial
    changes behind. Each branch of a `when`, `match` or `foreach` body is its
    own list. A refusal after an effect is an **Error**.

#### Description / Implementation

| Statement | Syntax | Description |
|---|---|---|
| `do` | `do "Calculate the total"` | Natural-language action description for implementation. |
| `error` | `error "Invalid state"` | Refuse to proceed, with a reason. |
| `code` | `` ```scala ... ``` `` | Embed implementation code (scala, java, python, mojo). |

Do not confuse the `do` statement with the `prompt(...)` **value** — the
parentheses distinguish them. The statement describes an action for a human;
the value denotes something AI computes.

#### Entity-Only

| Statement | Syntax | Description |
|---|---|---|
| `morph` | `morph entity X to state Y with record Z(...)` | Transition entity to a different State. The payload is a **record**. |
| `become` | `become entity X to handler Y` | Switch entity to a different Handler. |

#### Statement Applicability

| Context | Available Statements |
|---|---|
| All handlers | when, match, foreach, send, tell, yield, require, set, let, do, error, code |
| Entity handlers | All above + morph, become |
| Application / context handlers | All above + put |
| Functions | when, match, foreach, require, let, return, do, error, code |
| `on activate` / `on passivate` | Side-effect free only — no send, tell, yield, morph, become |
| `on event` | No require or error — an event must always be accepted |
| Saga steps | send, tell, yield, put, do, error |

#### Deprecated Statements

| Deprecated | Replacement |
|---|---|
| `reply <msg>` | `yield <msg>` |
| `prompt "..."` | `do "..."` |
| `send … to inlet X` | `send … to outlet Y`, or `tell` |

> *[For more details →](../concepts/statement.md)*

---

## Streaming Components

### Inlet

**Purpose**: A typed input port that receives messages.

**When to use**: On any processor that consumes data.

**Lives in**: **Any** processor — Context, Entity, Adaptor, Projector,
Repository, or a generic Processor. Ports are no longer streamlet-only.

**Syntax**: `inlet Name is type MessageType`

**Options**: `async` (a deliberate codegen async boundary), `ordered`,
`unordered`.

> *[For more details →](../concepts/inlet.md)*

### Outlet

**Purpose**: A typed output port that sends messages.

**When to use**: On any processor that produces data.

**Lives in**: **Any** processor. An entity may own an outlet.

**Syntax**: `outlet Name is type MessageType`

**Options**: `async`.

> *[For more details →](../concepts/outlet.md)*

### Connector

**Purpose**: Wires an Outlet to an Inlet, defining how data flows
between Streamlets (or between processors and Streamlets).

**When to use**: After defining Streamlets with Inlets/Outlets, to
assemble them into a data pipeline.

**Lives in**: Context, or **Domain** when the two ends are in different
contexts.

**Syntax**: `connector Name is from outlet X.Y to inlet A.B`

**Key details**:

- The outlet's type and the inlet's type must be compatible. A port typed
  `Anything` is compatible with everything.
- **Exactly one connector per port.** Fan-in and fan-out are modeled by
  declaring multiple *ports* — arity derives the `merge` or `split` shape —
  never by attaching several connectors to one port. More than one is an
  **Error**.
- Placement is validated: ends in different **domains** is an **Error**;
  a domain-scoped connector whose ends share one context is over-scoped
  (**Error**); a context-scoped connector whose ends cross contexts is
  under-scoped (**Error**).
- A domain-scoped cross-context connector without the `persistent` option
  draws a **CompletenessWarning**.

**Options**: `persistent`, `ordered`, `unordered`.

> *[For more details →](../concepts/connector.md)*

### Standard Module

**Purpose**: A predefined module named `Riddl`, available to every model with
no import and no author declaration, providing the stream terminators that
one-connector-per-port makes structurally necessary.

| Definition | Kind | Purpose |
|---|---|---|
| `BottomlessPit` | sink | Consumes everything on its inlet `hole`, emits nothing |
| `ForeverEmpty` | source | Never produces anything on its outlet `void` |
| `Drain` | type | `Anything`, so one drain absorbs every message type |

**Syntax**: `connector Discard is from outlet X.Unused to inlet BottomlessPit.hole`

Reaching `BottomlessPit` terminates a pipeline exactly as a modeled sink does;
`ForeverEmpty` originates one. Neither draws reachability warnings, and the
port-cardinality rule is waived for them. A model that ignores the standard
module is completely unaffected by it.

---

## User Interaction Definitions

### Epic

**Purpose**: A collection of related Use Cases that together describe a
user's journey or feature set.

**When to use**: To capture high-level user stories and the scenarios
that fulfill them.

**Lives in**: Domain.
**Contains**: Use Case.

**Key details**:

- Declares a User and their goal: `user X wants to "..." so that "..."`
- The verb may be any of `wants`, `must`, `shall`, `should`, `may`, `will`,
  `can`. All parse to the same structure — the modality is vocabulary, not
  captured data.
- Epics group related Use Cases under a single narrative

> *[For more details →](../concepts/epic.md)*

### Use Case (Case)

**Purpose**: A specific interaction flow between a User and the system,
describing a sequence of steps.

**When to use**: Inside an Epic, to detail one scenario of user-system
interaction.

**Lives in**: Epic.
**Contains**: Interaction steps.

**Key details**:

| Step | Syntax |
|---|---|
| Focus | `step focus <user> on <group>` |
| Direct | `step direct <user> to <url>` |
| Select | `step <user> selects <input>` |
| Take input | `step take <input> from <user>` |
| Show output | `step show <output> to <user>` |
| Refusal | `step <source> refuses <user> "<reason>"` |
| Send message | `step send <message> from <source> to <target>` |
| Self-processing | `step for <ref> is "<description>"` |
| Arbitrary | `step from <source> "<relationship>" to <target>` |
| Vague | `step is "<subject>" "<verb>" "<object>"` |

- The **refusal** step is new in 2.0 — a system element declining a user's
  request, which previously had no way to be expressed except as free text
- Group steps with `sequence { }`, `parallel { }`, `optional { }`
- Multiple cases per epic cover alternate paths (happy, error, edge)

!!! warning "Users interact only at the application boundary"
    For the two untyped step kinds (arbitrary and send-message), when exactly
    one side is a User, the other must be a UI element or a definition inside
    an `application` context. Otherwise it is an **Error**.

!!! warning "Use-case completeness"
    RIDDL checks that each step is **witnessed** by the model's structure and
    that the step sequence is an **admissible trace** through the state
    machines it drives, emitting **CompletenessWarnings** for unwitnessed
    steps, unhandled deliveries, and free-text steps whose prose is grounded
    in no in-scope vocabulary. Adding `term` definitions quiets the last one.

> *[For more details →](../concepts/use-case.md)*

### User

**Purpose**: An external actor who participates in Epics and Use
Cases—a persona rather than a specific individual.

**When to use**: To identify each distinct role that interacts with the
system (Customer, Administrator, Webhook, BatchJob).

**Lives in**: Domain.
**Contains**: Nothing (leaf definition).

**Key details**:

- Named by role, not by person: `user Buyer`, not `user John`
- System integrations (webhooks, batch jobs) are users too
- Uses the term "User" (not "Actor") per Use Cases 2.0

> *[For more details →](../concepts/user.md)*

### Application

**Purpose**: Not a separate definition type. An Application is a
[Context](#context) declared with the `application` **intention**, which is
the only place [Groups](#group) — and therefore UI — may be modeled.

**When to use**: When you need to describe the data-flow structure of a
user interface without prescribing technology.

**Lives in**: Domain (as a Context).
**Contains**: Group, Handler, plus all normal Context contents.

**Syntax**: `application context Storefront is { page Home is { ??? } }`

!!! warning "UI outside an application context is an Error"
    A context holding a `group` (or any of its aliases) without the
    `application` intention is a hard **Error** in 2.0. In earlier releases
    any context could hold UI.

> *[For more details →](../concepts/application.md)*

### Group

**Purpose**: An abstract structural unit for organizing UI
elements—pages, forms, panes, dialogs, screens.

**When to use**: Inside an `application` context to define the hierarchy
of UI containers.

**Lives in**: An `application` Context, or another Group (nesting).
**Contains**: Group, Input, Output, Type.

**Aliases**: `group`, `page`, `pane`, `dialog`, `menu`, `popup`, `frame`,
`column`, `window`, `section`, `tab`, `flow`, `block`.

**Key details**:

- Groups can nest, forming a UI hierarchy
- Contains Inputs (data from user) and Outputs (data to user)
- May carry a [Figma reference](#figma-reference)

> *[For more details →](../concepts/group.md)*

#### Input

**Purpose**: An abstract data-entry point—the net result of a user
providing information (form submission, button tap, voice response, etc.).

**Lives in**: Group.
**Contains**: Type, Message (command).

**Aliases**: `input`, `form`, `text`, `button`, `picklist`, `selector`,
`item`.

**Acquisition verbs**: `acquires`, `reads`, `takes`, `accepts`, `admits`,
`enters`, `provides`, `selects`, `chooses`, `picks`, `initiates`, `submits`,
`triggers`, `activates`, `starts`.

**Syntax**: `button Checkout activates type Boolean`

!!! warning "Selection verbs expect a choice type"
    An input using `selects`, `chooses` or `picks` whose type is not an
    Enumeration or Alternation draws a **StyleWarning** — a selection widget
    should choose among options.

**Reads**: A handler reads an input's value with `get from input <Name>`.

> *[For more details →](../concepts/input.md)*

#### Output

**Purpose**: An abstract data-display point—the net result of showing
information to a user (text, chart, audio, etc.).

**Lives in**: Group.
**Contains**: Type, Message (result).

**Aliases**: `output`, `document`, `list`, `table`, `graph`, `animation`,
`picture`.

**Presentation verbs**: `presents`, `shows`, `displays`, `writes`, `emits`.

**Writes**: A handler publishes to an output with `put <value> to output
<Name>`.

> *[For more details →](../concepts/output.md)*

---

## Metadata & Documentation

These elements provide supplementary information about definitions
without affecting core semantics.

### Author

**Purpose**: Attribution metadata—who created or maintains a
definition.

**When to use**: At the domain level to identify the model
author(s). Reference them from any definition's `with { }` block
using `by author Name`.

**Defined in**: Module, Domain (body definitions only).
**Referenced in**: Any definition's `with { }` metadata block via
`by author Name`.
**Contains**: `name`, `email` fields only.

**Syntax**: `author Name is { name is "..." email is "..." }`

> *[For more details →](../concepts/author.md)*

### Term

**Purpose**: A glossary entry—defines domain-specific terminology
within the model itself.

**When to use**: When your domain uses jargon that readers (human
or AI) might not know.

**Lives in**: Metadata blocks (`with { }`) on any definition.
**Contains**: A doc block (description).

**Syntax**: `term SKU is { |Stock Keeping Unit... }`

> *[For more details →](../concepts/term.md)*

### Option

**Purpose**: An instruction to translators about how a definition
should be implemented or interpreted.

**When to use**: To annotate definitions with technology hints,
behavioral flags, or classification metadata.

**Lives in**: Metadata blocks (`with { }`) on any vital definition.

**Key details**:

- `option is technology("Kafka")` — implementation hint
- `option is kind("core")` — classification
- Boolean if no arguments: `option is event-sourced`

| Applies to | Options |
|---|---|
| Entity | `event-sourced`, `aggregate`, `transient`, `available`, `consistent`, `message-queue`, `value`, `auto-id` |
| Saga | `compensate`, `parallel` |
| Inlet / Outlet | `async` |
| Connector / Inlet | `ordered`, `unordered`, `persistent` |
| Any processor | `protocol` |
| Epic | `sync` |
| Any definition | `css`, `technology`, `kind`, `faicon` |

!!! warning "Deprecated context options"
    `gateway`, `service`, `external` and `wrapper` are superseded by the
    context intention prefix and emit a `[deprecated]` message.

> *[For more details →](../concepts/option.md)*

### Naming Rules

Two rules constrain every identifier, both **Errors** as of RIDDL 2.0:

- **Sibling names are unique regardless of kind.** `type Thing` beside
  `entity Thing` in one container is an Error; uniqueness used to be checked
  per kind, so this previously passed.
- **A definition-introducing keyword may not be a bare identifier** —
  `domain`, `context`, `entity`, `adaptor`, `saga`, `epic`, `projector`,
  `repository`, `streamlet`, `handler`, `function`. Use a quoted identifier
  (`handler 'projector' is { ??? }`) or different case (`Projector`); the
  check is case-sensitive.

`version` and `copyright` are deliberately *not* in that list and remain
usable as field and type names.

### Version

**Purpose**: One component of a scope's version coordinate — either a name or
a natural number, never both.

**When to use**: To stamp releases onto a model, incrementally from the
outside in.

**Lives in**: Root, Module, Domain, and all six processor kinds.
**Contains**: Nothing (leaf definition).

**Syntax**: `version Garibaldi` or `version 4`

**Key details**:

- A definition's precise version is **composed** from every versioned
  ancestor, root to leaf, joined with `.` — a domain `Garibaldi` over a
  context `4` over an entity `3` gives `Garibaldi.4.3`
- Only scopes that actually bear a version contribute a component, so an
  unversioned context gives `Garibaldi.3`. That is what makes adoption
  incremental.
- More than one version in a single scope is an **Error**

!!! warning "Not a semantic version"
    The composed form *looks* like semver but is a **hierarchical
    coordinate**. `3.1.6` → `3.2.1` says nothing about breakage, and
    `Garibaldi.4.3` is not orderable against `Jellyfish.1.1` at all. Its
    length varies with nesting depth, so comparison must be component-wise.

### Copyright

**Purpose**: A named legal notice carried verbatim.

**When to use**: To attribute ownership, especially where an inner scope's
notice differs from its parent's.

**Lives in**: Root, Module, Domain, and all six processor kinds.
**Contains**: Nothing (leaf definition).

**Syntax**: `copyright House is "© 2026 Ossum Inc."`

**Key details**:

- The literal string is the notice **in its entirety** — symbol, year and
  holder — because notices vary by jurisdiction, holder and license
- Unlike `version`, a copyright does **not** compose. The applicable notice
  is **nearest-wins**: the one declared by the definition itself, or failing
  that by the nearest ancestor that declares one. A vendored `external`
  context bearing a third party's notice *overrides* its enclosing domain's.
- It is **named** so a documentation generator can gather a model's distinct
  notices and attribute each properly
- More than one copyright in a single scope is an **Error**

### Import

**Purpose**: Loads compiled definitions from a binary `.bast` module.

**When to use**: To reuse definitions across models without re-parsing
source.

**Lives in**: Root, Module, Domain, Context.

**Syntax**:

- Full: `import "commerce.bast"` — takes everything the file's root module
  holds
- Selective: `import domain Shopping from "commerce.bast"` — takes one named
  definition
- Renaming: `import type Money from "commerce.bast" as Currency`

**Importable kinds**: `domain`, `context`, `entity`, `type`, `epic`, `saga`,
`adaptor`, `function`, `projector`, `repository`, `streamlet`, `author`,
`module`, `user`, `connector`, `constant`, `invariant`.

**Key details**:

- `include` splices **source**; `import` loads **compiled** definitions
- An imported definition must be structurally legal *where the directive
  sits*, exactly as if written there by hand. An illegal placement is an
  **Error**.

### Figma Reference {#figma-reference}

**Purpose**: Connects a model element to the exact Figma frame that depicts
it.

**When to use**: On UI definitions, so a design and its model stay
verifiably linked.

**Lives in**: Metadata (`with { }`) of an Input, Output, Group, or an
`application` Context.

**Syntax**: `figma "aBcD1234" node "42:1337"`

**Key details**:

- The two strings are the file key and node id — exactly the arguments the
  Figma REST API takes — so it resolves to **one frame**, not a document to
  search
- It is metadata, not a definition: no identifier, nothing can
  path-reference it, and it adds nothing to the symbol table
- Drift validation is **opt-in and off by default**. With
  `--check-figma-drift` and a `FIGMA_TOKEN`, an unknown node is an **Error**
  and a mismatched frame name a **Warning**. Names compare on letters and
  digits only, so `Payment Screen`, `PaymentScreen` and `payment_screen` all
  correspond. An offline build cannot be affected — only a successful API
  answer can produce a message.

### Include

**Purpose**: Inserts the contents of another `.riddl` file at the
current location, enabling multi-file model organization.

**When to use**: To split large models across files for readability and
team collaboration.

**Lives in**: Any vital definition.

**Syntax**: `include "path/to/file.riddl"`

**Key details**:

- Path is relative to the including file
- Included content must be valid for its insertion point (containment
  rules still apply)

> *[For more details →](../concepts/include.md)*

### Description

**Purpose**: User-facing documentation attached to a definition, written
in Markdown.

**When to use**: On every definition—`briefly` for a one-liner,
`described by` for extended documentation.

**Lives in**: Any definition (via `with { ... }` metadata block).

**Key details**:

- `briefly "short text"` — one-line summary
- `described by { |Markdown lines... }` — extended docs
- Can reference external files or public URLs
- Supports Mermaid diagrams and Markdown formatting

> *[For more details →](../concepts/description.md)*

### Comment

**Purpose**: Semantic annotations captured by the parser—unlike most
languages, RIDDL comments are not discarded.

**When to use**: For implementation notes, TODOs, and technical
decisions. Use Descriptions for user-facing documentation.

**Syntax**: `// line comment` or `/* block comment */`

**Key details**:

- Comments are associated with nearby definitions by the parser
- Valid only at file scope and around definitions—not arbitrary
  whitespace positions

> *[For more details →](../concepts/comment.md)*

### Attachment

**Purpose**: Associates an external file (diagram, spreadsheet, image)
with a definition.

**When to use**: When a definition needs supplementary material that
cannot be expressed in Markdown descriptions.

**Lives in**: Any vital definition.

**Syntax** — the MIME type comes **before** the content, in all three forms:

```riddl
attachment StateChart is image/png in file "diagrams/states.png"
attachment Note      is text/plain as "reviewed 2026-07-29"
attachment ULID      is "01ARZ3NDEKTSV4RRFFQ69G5FAV"
```

`attachment X is "path" as "image/png"` — content first — does not parse.

---

## Validation Severity Levels

| Severity | Kind | Meaning |
|:---:|---|---|
| 0 | Info | Informational note |
| 1 | StyleWarning | Naming/style convention issue |
| 2 | MissingWarning | Missing optional content |
| 3 | UsageWarning | Unused or unreferenced definition |
| 3 | **Deprecation** | Use of a construct slated for removal |
| 4 | **CompletenessWarning** | Valid but incomplete for implementation |
| 5 | Warning | Likely mistake or problematic pattern |
| 6 | Error | Invalid — prevents compilation |
| 7 | SevereError | Fatal — halts processing |

Severity ≥ 4 is **actionable**. CompletenessWarnings flag models that
validate but lack detail for code generation. Toggle with `-c` /
`--show-completeness-warnings`.

**Deprecations** are rendered with their own `[deprecated]` label rather than
folded in with ordinary warnings, so a model can be checked for zero
deprecations independently of zero warnings. They surface under every command
— `parse`, `validate`, `stats`, `bastify`, prettify and generation — not only
`validate`.

---

## Abstract / Meta Concepts

These concepts appear in the documentation hierarchy but are not
directly instantiated in RIDDL models:

- **[Definition](../concepts/definition.md)** — The base concept:
  anything with a name and optional metadata.
- **[Vital](../concepts/vital.md)** — A definition that supports
  metadata (options, terms, author references, descriptions, and
  attachments in `with { }` blocks), plus includes. All processors,
  Domain, and Context are vital.
- **[Processor](../concepts/processor.md)** — The abstract parent of
  Context, Entity, Repository, Projector, Adaptor, and Streamlet. All of
  them bear ports, a version and a copyright. Saga and Function extend the
  vital-definition base instead, so they bear none of those.
- **[Element](../concepts/element.md)** — Any named thing in a RIDDL
  model (broader than Definition).
- **[Value](../concepts/value.md)** — A definition that carries a type
  expression (Fields, Constants, States).
- **[Interaction](../concepts/interaction.md)** — A step within a Use
  Case.
- **[Conditional](../concepts/conditional.md)** — A `when`/`match`
  branch within a Use Case (not the same as the `when` statement).
