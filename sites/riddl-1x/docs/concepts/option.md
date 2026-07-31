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

```riddl
entity Order is {
  ???
} with {
  option is event-sourced
  option is technology("Akka")
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

## Known Options By Definition

| Definition | Supported Options |
|------------|-------------------|
| [Adaptor](adaptor.md) | `css`, `faicon`, `kind`, `technology` |
| [Application](application.md) | `css`, `faicon`, `kind`, `technology` |
| [Connector](connector.md) | `kind`, `persistent`, `technology` |
| [Context](context.md) | `css`, `faicon`, `gateway`, `kind`, `namespace`, `package`, `service`, `technology`, `wrapper` |
| [Domain](domain.md) | `css`, `external`, `faicon`, `kind`, `namespace`, `package`, `technology` |
| [Entity](entity.md) | `aggregate`, `available`, `consistent`, `css`, `event-sourced`, `faicon`, `finite-state-machine`, `kind`, `message-queue`, `technology`, `transient`, `value` |
| [Epic](epic.md) | `css`, `faicon`, `kind`, `sync`, `technology` |
| [Projector](projector.md) | `css`, `faicon`, `kind`, `technology` |
| [Repository](repository.md) | `css`, `faicon`, `kind`, `technology` |
| [Saga](saga.md) | `css`, `faicon`, `kind`, `parallel`, `sequential`, `technology` |
| [Streamlet](streamlet.md) | `css`, `kind`, `technology` |

### Common Options

These options are available on most definitions:

- **`technology`** — Names the implementation technologies,
  adapted from
  [Simon Brown's](https://www.linkedin.com/in/simonbrownjersey/)
  [C4 Model](https://c4model.com/#Notation). Takes string
  arguments: `option is technology("Kafka")`
- **`kind`** — A semantic categorization of the definition.
  Takes a string argument: `option is kind("device")`
- **`css`** — A CSS class name for visual rendering
- **`faicon`** — A Font Awesome icon name for visual rendering

### Notable Definition-Specific Options

- **Entity**: `event-sourced`, `value`, `aggregate`,
  `transient`, `consistent`, `available`,
  `finite-state-machine`, `message-queue`
- **Context**: `gateway`, `service`, `wrapper`
- **Domain**: `external`
- **Connector**: `persistent`
- **Saga**: `parallel`, `sequential`
- **Epic**: `sync`

## Occurs In

[Metadata](metadata.md) blocks (`with { }`) on any
[vital definition](vital.md).

## Contains

Option values which are simple identifiers with an optional set of
string arguments.
