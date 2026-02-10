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
| Process streaming data | [Streamlet](#streamlet) |
| Connect two stream endpoints | [Connector](#connector) |
| Describe a user-facing interface | [Context with Groups](#application) |
| Capture a user journey | [Epic](#epic) / [Use Case](#use-case-case) |
| Define a data structure | [Type](#type) |
| Define a request, response, or notification | [Message](#message) |
| React to incoming messages | [Handler](#handler) / [On Clause](#on-clause) |
| Create a reusable computation | [Function](#function) |
| Split a model across files | [Include](#include) |

---

## Containment Hierarchy

```
Root
├── Domain
│   ├── Context                       (processor)
│   │   ├── Entity                    (processor)
│   │   │   ├── State
│   │   │   │   └── Handler → On Clause → Statements
│   │   │   ├── Handler → On Clause → Statements
│   │   │   ├── Function
│   │   │   ├── Type, Constant, Invariant
│   │   │   └── Include
│   │   ├── Repository                (processor)
│   │   ├── Projector                 (processor)
│   │   ├── Saga → Saga Step          (processor)
│   │   ├── Adaptor                   (processor)
│   │   ├── Streamlet                 (processor)
│   │   │   ├── Inlet, Outlet
│   │   │   └── Handler
│   │   ├── Connector
│   │   ├── Group (Application UI)
│   │   │   ├── Input, Output
│   │   │   └── Group (nested)
│   │   ├── Handler, Function
│   │   ├── Type, Constant
│   │   └── Include
│   ├── User
│   ├── Epic → Use Case
│   ├── Saga
│   ├── Type
│   ├── Author
│   └── Include
└── Module (for organizing large roots)
```

| Level | Body definitions | Metadata (`with { }`) |
|---|---|---|
| **Root** | Domain, Module, Author | briefly, described by |
| **Domain** | Context, User, Epic, Saga, Type, Author, Include | term, option, by author, briefly, described by, attachment |
| **Context** | Entity, Repository, Projector, Saga, Adaptor, Streamlet, Connector, Group, Handler, Function, Type, Constant, Include | term, option, by author, briefly, described by, attachment |
| **Entity** | State, Handler, Function, Type, Constant, Invariant, Include | term, option, by author, briefly, described by, attachment |
| **Repository / Projector / Adaptor** | Handler, Function, Type, Constant, Include | term, option, by author, briefly, described by, attachment |
| **Streamlet** | Inlet, Outlet, Handler, Function, Type, Constant, Include | term, option, by author, briefly, described by, attachment |
| **Epic** | Use Case | term, option, by author, briefly, described by, attachment |
| **Saga** | Saga Step | term, option, by author, briefly, described by, attachment |

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

**Lives in**: Root or another Domain.
**Contains**: Context, User, Epic, Saga, Type, Author, Include.
Metadata (in `with { }`): term, option, by author, briefly,
described by, attachment.

**Key details**:

- Maps to a DDD Domain
- Nesting domains creates sub-domain hierarchies
- Types defined here are visible to all contained contexts

> *[For more details →](../concepts/domain.md)*

---

## Processors

Processors are definitions that can receive and process messages. They
are the active components of a RIDDL model. All processors can contain
Handlers, Functions, Types, Constants, and Includes.

### Context

**Purpose**: A bounded context—an autonomous service boundary with its
own ubiquitous language, types, and processors.

**When to use**: When you need an isolated area of the system with its
own data models and message contracts. Contexts are also how you model
applications (by adding Groups).

**Lives in**: Domain.
**Contains**: Entity, Repository, Projector, Saga, Adaptor,
Streamlet, Connector, Group, Handler, Function, Type, Constant,
Include.

**Key details**:

- Maps to a DDD Bounded Context
- Context-level handlers act as the context's external API
- Adding Groups makes the context an Application (UI model)
- Options: `service`, `gateway`, `package`

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

- Entities have one or more named States, each backed by a record type
- Supports `morph` (change state) and `become` (change handler)
- Options: `event-sourced`, `aggregate`, `transient`, `available`
- The primary unit of consistency in a reactive system

> *[For more details →](../concepts/entity.md)*

### Repository

**Purpose**: Persistent storage for entity or projection data—the
abstraction for a database, cache, or file store.

**When to use**: When a context needs to persist data beyond the
lifetime of individual messages.

**Lives in**: Context.
**Contains**: Handler, Function, Type, Constant, Include.

**Key details**:

- Defines a `schema` (relational, document, graph, etc.)
- Handlers typically react to events and persist data
- Usually paired with a Projector for CQRS read-side writes

> *[For more details →](../concepts/repository.md)*

### Projector

**Purpose**: Transforms and aggregates events into denormalized read
models—the write side of CQRS's read side.

**When to use**: When you need a materialized view optimized for queries
that differs from the entity's write model.

**Lives in**: Context.
**Contains**: Handler, Function, Type, Constant, Include.

**Key details**:

- Declares `updates repository X` to link to its target store
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
- Sagas are themselves processors and can have handlers

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
**Contains**: Handler, Function, Type, Constant, Include.

**Key details**:

- Direction: `from context X` (inbound) or `to context X` (outbound)
- Handlers map foreign messages to/from the local context's types
- Implements the DDD Anti-Corruption Layer pattern

> *[For more details →](../concepts/adaptor.md)*

### Streamlet

**Purpose**: A stream-processing component with typed input/output ports
for building data pipelines.

**When to use**: When data needs to flow continuously through
transformation, filtering, merging, or routing stages.

**Lives in**: Context.
**Contains**: Inlet, Outlet, Handler, Function, Type, Constant, Include.

**Key details**:

- Subtypes determine port configuration:

| Subtype | Inlets | Outlets | Purpose |
|---|---|---|---|
| `source` | 0 | 1+ | Produce data |
| `sink` | 1+ | 0 | Consume data |
| `flow` | 1 | 1 | Transform data |
| `merge` | 2+ | 1 | Combine streams |
| `split` | 1 | 2+ | Divide a stream |
| `router` | 1 | 2+ | Route by content |
| `void` | 1 | 0 | Discard (testing) |

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
- **Alternation** (union): `type X is one of { T1, T2, T3 }`
- **Enumeration**: `type X is any of { A, B, C }`
- **Collection**: `many T`, `set of T`, `mapping from K to V`, `T?`
- **Pattern**: `Pattern("regex")`
- **Predefined**: `String`, `Integer`, `Boolean`, `UUID`, `Date`,
  `DateTime`, `Duration`, `URL`, `Currency`, `Decimal`, etc.

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
**Contains**: Handler (state-specific message handling).

**Key details**:

- Syntax: `state X of TypeName`
- The entity transitions between states via `morph`
- Each state can have its own handlers that override entity defaults

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

**Lives in**: Entity.

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
| `on query X` | A specific query message |
| `on init` | Processor initialization |
| `on term` | Processor termination |
| `on other` | Any unmatched message (catch-all) |

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
- Use `prompt` for complex business logic descriptions
- `requires { ... }` defines input parameters
- `returns { ... }` defines output parameters

> *[For more details →](../concepts/function.md)*

### Concrete Statements

Statements are the actions inside On Clauses, Functions, and Saga Steps.
RIDDL is intentionally **not** Turing complete—statements capture
interactions between definitions, not full implementations.

#### Control Flow

| Statement | Syntax | Description |
|---|---|---|
| `when` | `when "condition" then { ... } else { ... } end` | Conditional; `end` keyword required. Condition can be a string literal, identifier, or `!identifier`. |
| `match` | `match "expr" { case "val" { ... } default { ... } }` | Multi-way branch; closed by `}`. |

#### Messaging

| Statement | Syntax | Description |
|---|---|---|
| `send` | `send event X to outlet Y` | Route a message through an outlet or inlet (pub/sub, streaming). |
| `tell` | `tell command X to entity Y` | Send a message directly to a specific processor (point-to-point). |

#### Data

| Statement | Syntax | Description |
|---|---|---|
| `set` | `set field status to "Active"` | Assign a value to a state field. |
| `let` | `let total = "price * qty"` | Create a local variable binding. |

#### Description / Implementation

| Statement | Syntax | Description |
|---|---|---|
| `prompt` | `prompt "Calculate the total"` | Natural-language action description for implementation. |
| `error` | `error "Invalid state"` | Produce a named error. |
| `code` | `` ```scala ... ``` `` | Embed implementation code (scala, java, python, mojo). |

#### Entity-Only

| Statement | Syntax | Description |
|---|---|---|
| `morph` | `morph entity X to state Y with command Z` | Transition entity to a different State. |
| `become` | `become entity X to handler Y` | Switch entity to a different Handler. |

#### Statement Applicability

| Context | Available Statements |
|---|---|
| All handlers | when, match, send, tell, set, let, prompt, error, code |
| Entity handlers | All above + morph, become |
| Functions | when, match, set, let, prompt, error, code |
| Saga steps | send, tell, prompt, error |

> *[For more details →](../concepts/statement.md)*

---

## Streaming Components

### Inlet

**Purpose**: A typed input port on a Streamlet that receives messages.

**When to use**: On any Streamlet that consumes data (sink, flow, merge,
split, router, void).

**Lives in**: Streamlet.

**Syntax**: `inlet Name is type MessageType`

> *[For more details →](../concepts/inlet.md)*

### Outlet

**Purpose**: A typed output port on a Streamlet that sends messages.

**When to use**: On any Streamlet that produces data (source, flow,
merge, split, router).

**Lives in**: Streamlet.

**Syntax**: `outlet Name is type MessageType`

> *[For more details →](../concepts/outlet.md)*

### Connector

**Purpose**: Wires an Outlet to an Inlet, defining how data flows
between Streamlets (or between processors and Streamlets).

**When to use**: After defining Streamlets with Inlets/Outlets, to
assemble them into a data pipeline.

**Lives in**: Context.

**Syntax**: `connector Name is from outlet X.Y to inlet A.B`

**Key details**:

- The outlet's type and the inlet's type must be compatible
- Connectors enable building multi-stage pipelines declaratively

> *[For more details →](../concepts/connector.md)*

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

- Steps use: `user X "action"`, `then entity Y "action"`,
  `step send command Z from user X to entity Y`
- Multiple cases per epic cover alternate paths (happy, error, edge)

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

**Purpose**: Not a separate definition type. An Application is simply a
[Context](#context) that contains [Groups](#group). It models a user
interface abstractly.

**When to use**: When you need to describe the data-flow structure of a
user interface without prescribing technology.

**Lives in**: Domain (as a Context).
**Contains**: Group, Handler, plus all normal Context contents.

> *[For more details →](../concepts/application.md)*

### Group

**Purpose**: An abstract structural unit for organizing UI
elements—pages, forms, panes, dialogs, screens.

**When to use**: Inside an Application context to define the hierarchy
of UI containers.

**Lives in**: Context (Application) or another Group (nesting).
**Contains**: Group, Input, Output, Type.

**Key details**:

- Groups can nest, forming a UI hierarchy
- Concrete names are implementation-dependent (page, form, etc.)
- Contains Inputs (data from user) and Outputs (data to user)

> *[For more details →](../concepts/group.md)*

#### Input

**Purpose**: An abstract data-entry point—the net result of a user
providing information (form submission, button tap, voice response, etc.).

**Lives in**: Group.
**Contains**: Type, Message (command).

> *[For more details →](../concepts/input.md)*

#### Output

**Purpose**: An abstract data-display point—the net result of showing
information to a user (text, chart, audio, etc.).

**Lives in**: Group.
**Contains**: Type, Message (result).

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
- Entity options: `event-sourced`, `aggregate`, `transient`,
  `available`
- Context options: `service`, `gateway`, `package`

> *[For more details →](../concepts/option.md)*

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

**Syntax**: `attachment Name is "path/to/file" as "mime/type"`

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
  Context, Entity, Repository, Projector, Saga, Adaptor, and Streamlet.
- **[Element](../concepts/element.md)** — Any named thing in a RIDDL
  model (broader than Definition).
- **[Value](../concepts/value.md)** — A definition that carries a type
  expression (Fields, Constants, States).
- **[Interaction](../concepts/interaction.md)** — A step within a Use
  Case.
- **[Conditional](../concepts/conditional.md)** — A `when`/`match`
  branch within a Use Case (not the same as the `when` statement).
