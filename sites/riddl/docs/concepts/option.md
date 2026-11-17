---
title: "Options"
draft: false
---

Options are instructions to translators on how a particular
definition should be regarded. Any translator can make use of any
option. Options can take a list of string arguments much like the
options and arguments to a program. If none are specified, the
option is considered to be a Boolean value that is `true` if
specified.

Options appear in `with { }` metadata blocks, not inside a
definition's body. The syntax is `option is` *option_name* with
optional string arguments:

<!-- riddl: in-context -->
```riddl
entity Order is {
  ???
} with {
  option is technology("Akka")
  option is kind("core")
}
```

Every [vital definition](vital.md) in RIDDL allows a `technology`
option that takes any number of string arguments. These can specify
the technologies intended for the implementation. This idea was
adapted from a similar idea in
[Simon Brown's](https://www.linkedin.com/in/simonbrownjersey/)
[C4 Model For Software Architecture](https://c4model.com/#Notation).

Other options are specific to the kind of vital definition.
Non-vital definitions do not allow options.

## The Option Registry

RIDDL keeps a single registry of recognized option names, their valid parent
kinds, and their argument counts. An option not in the registry is not an
error — it draws a **StyleWarning**, so the system stays extensible — but an
option used on the wrong kind of definition draws a nudge.

!!! info "One table, not two"
    Before RIDDL 2.0 the option relation was described twice, in two
    hand-maintained lists that had to be kept in step. They drifted three
    times, and each drift produced a spurious *"not a recognized RIDDL
    option"* warning on a perfectly valid option. In 2.0 the per-kind lists
    are **derived** from the registry, so they cannot disagree with it.

    Consolidating them also exposed eight options RIDDL advertised but never
    registered — including six entity markers — every use of which had been
    drawing that spurious warning.

### Options Valid on Any Definition

| Option | Arguments | Meaning |
|--------|:---------:|---------|
| `technology` | 1 | Names the implementation technology |
| `kind` | 1 | A semantic categorization |
| `css` | 1 | A CSS fragment for rendering |
| `color` | 1 | A color for rendering |
| `faicon` | 1 | A Font Awesome icon name |
| `event_catalog_version` | 1 | Version pinning for EventCatalog generation |
| `sql_dialect`, `sql_table` | 1 | SQL DDL generation hints |
| `backstage_owner`, `backstage_lifecycle`, `backstage_type` | 1 | Backstage catalog generation hints |
| `message_envelope` | 1 | Names the envelope a generator wraps messages in |

### Options By Definition Kind

| Definition | Options |
|------------|---------|
| [Entity](entity.md) | `auto-id`, `bulkhead`, `finite-state-machine`, `message-queue`, `microservice`, `protocol`, `rate-limit`, `snapshots` |
| [Context](context.md) | `bulkhead`, `clustered`, `microservice`, `namespace`, `protocol` |
| [Domain](domain.md) | `namespace`, `confluence_space`, `confluence_parent` |
| [Connector](connector.md) | `ordered`, `unordered`, `partitioned`, `circuit-breaker` |
| [Inlet](inlet.md) | `async`, `ordered`, `unordered`, `error-sink` |
| [Outlet](outlet.md) | `async`, `lowering` |
| [Saga](saga.md) | `parallel`, `timeout`, `retry`, `undo-retry`, `failure-message`, `microservice`, `protocol` |
| Saga Step | `timeout`, `retry`, `delay` |
| [Handler](handler.md) | `timeout`, `retry`, `idempotent`, `cacheable`, `rate-limit` |
| [On Clause](onclause.md) | `timeout`, `idempotent` |
| [Adaptor](adaptor.md) | `circuit-breaker`, `clustered`, `protocol` |
| [Projector](projector.md) | `cacheable`, `batch`, `clustered`, `microservice`, `protocol` |
| [Repository](repository.md) | `transient`, `available`, `consistent`, `batch`, `clustered`, `microservice`, `protocol` |
| [Streamlet](streamlet.md) | `clustered`, `lowering`, `protocol` |
| [Epic](epic.md) | `sync` |

Every definition also takes the options in the table above. Both tables were
checked against riddl 2.7.0's option registry.

!!! warning "Deprecated options"
    These still parse, emit `[deprecated]`, and are slated for removal in 3.0.
    See [Deprecated Constructs](../references/language-reference.md#deprecated-constructs)
    for each one's replacement:

    - on an **entity**: `aggregate`, `available`, `consistent`,
      `event-sourced`, `transient`, `value`. Write them as
      [intentions](entity.md#intentions) before `entity`.
    - on a **connector**: `persistent`, `at-least-once`, `at-most-once`,
      `exactly-once`. Write them before `connector`.
    - on a **context**: `external`, `gateway`, `service`, `wrapper`.
    - on a **domain** or **context**: `external`, and `package` (use
      `namespace`).

### Notable Options

- **`technology`** — Names the implementation technologies, adapted from
  [Simon Brown's](https://www.linkedin.com/in/simonbrownjersey/)
  [C4 Model](https://c4model.com/#Notation): `option is technology("Kafka")`
- **`auto-id`** — An entity is assigned a ULID at instantiation
- **`parallel`** — A saga's steps all start at once, rather than in sequence.
  A saga is sequential by definition, so `parallel` declares the exception.
- **`async`** — Marks a port as a deliberate codegen async boundary, so the
  generator inserts a real boundary there instead of fusing the stream
- **`persistent`** — Messages crossing a connector are durably stored

!!! warning "Deprecated options"
    | Deprecated | Replacement | Since |
    |------------|-------------|-------|
    | `gateway`, `service`, `external` on a Context | the [context intention prefix](context.md#intention) | 2.0.0 |
    | `wrapper` | an [adaptor](adaptor.md) | 2.0.0 |
    | `package` | `namespace` | 1.15.0 |

    Each is still *recognized* — deliberately, so that using one draws only
    the `[deprecated]` message rather than an additional and contradictory
    "unrecognized option" warning.

    `sequential` on a saga was dropped outright: it requested the default
    behavior, so it said nothing.

## Occurs In

[Metadata](metadata.md) blocks (`with { }`) on any
[vital definition](vital.md).

## Contains

Option values which are simple identifiers with an optional set of
string arguments.
