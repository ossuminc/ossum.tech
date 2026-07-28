---
title: "Interaction"
draft: false
description: >-
  A single typed step within a use case, describing how one participant
  communicates with or acts upon another.
---

An interaction defines a single step within a [Use Case](use-case.md),
describing how one participant communicates with or acts upon another.
Interactions are the building blocks of use cases, capturing the flow of
actions between users, entities, and other system components.

## Purpose

Interactions serve to:

- **Document step-by-step flows**: Show exactly what happens at each point
- **Enable sequence diagram generation**: Provide data for visual documentation
- **Define acceptance criteria**: Each interaction can be verified in testing
- **Clarify responsibilities**: Make explicit which component handles each action

## Syntax

Every interaction is introduced by the `step` keyword, followed by one of the
ten step forms:

```riddl
case PlaceOrder is {
  user Customer wants to "check out" so that "the order is placed"

  step focus user Customer on page Storefront.Cart
  step take form Storefront.PaymentDetails from user Customer
  step send command ProcessPayment from user Customer to entity PaymentService
  step for entity OrderService is "create the order record"
  step show document Storefront.Confirmation to user Customer
}
```

## Step Kinds

| Kind | Syntax | Participants |
|------|--------|--------------|
| **Focus** | `step focus <user> on <group>` | User → Group |
| **Direct** | `step direct <user> to <url>` | User → URL |
| **Select** | `step <user> selects <input>` | User → Input |
| **Take input** | `step take <input> from <user>` | Input ← User |
| **Show output** | `step show <output> to <user>` | Output → User |
| **Refusal** | `step <source> refuses <user> "<reason>"` | Any → User |
| **Send message** | `step send <message> from <source> to <target>` | Any → Processor |
| **Self-processing** | `step for <ref> is "<description>"` | Any, alone |
| **Arbitrary** | `step from <source> "<relationship>" to <target>` | Any → Any |
| **Vague** | `step is "<subject>" "<verb>" "<object>"` | Prose only |

### Typed vs. Free-Text Steps

Eight of the ten steps name **real definitions**. That is what lets RIDDL check
them: it can ask whether the receiver of a `send` actually has a matching `on`
clause, whether a `show output` is ever written to by a `put` statement, and
whether the whole ordered sequence is admissible through the entities'
state machines.

The **arbitrary** and **vague** steps carry free prose instead. They remain
available because not every interaction is worth typing, but nothing can be
verified about them — so RIDDL instead predicts whether their prose is likely
to be AI-translatable into a test, and warns when it is not. See
[Use Case validation](use-case.md#validation).

### Refusal

New in RIDDL 2.0. A refusal models a system element declining a user's
request:

```riddl
step entity Cart refuses user Customer "the item is out of stock"
```

Before it existed, the error branch of a use case — often the most interesting
one — could only be written as free prose, which meant it was also the least
checkable part of the model.

## Grouping

Interactions may be grouped to express ordering semantics:

- `sequence { … }` — steps occur in the order written
- `parallel { … }` — steps occur in any order
- `optional { … }` — steps may be skipped entirely

These affect analysis, not just documentation: an `optional` block's steps are
neither checked for admissibility nor treated as changing entity state, and a
`parallel` block's deliveries are checked across every order they could occur
in.

## Participants

Interactions can involve:

- **[Users](user.md)**: Human or system actors defined at the domain level
- **[Entities](entity.md)**: Stateful business objects that process commands
- **[Groups](group.md), [Inputs](input.md), [Outputs](output.md)**: UI
  components in an [application](application.md) context
- **[Sagas](saga.md)**: Multi-step processes that coordinate across components
- Any other [processor](processor.md)

!!! warning "Users interact only at the application boundary"
    For the arbitrary and send-message steps — the two that admit a user
    opposite an arbitrary referent — when exactly one side is a User, the
    other must be a UI element or a definition inside an `application`
    [context](context.md#intention). Otherwise it is an **Error**.

    The five dedicated user-interaction steps hard-type their non-user side
    already, so they cannot violate this.

## Occurs In

* [Use Case](use-case.md)

## Contains

Nothing — an interaction is a leaf element within a use case.
