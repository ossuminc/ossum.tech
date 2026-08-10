---
title: "Command-Event Patterns"
description: "Alternatives and recommendations for command handler messages"
---

<!-- riddl-prelude
    type OrganizationId is UUID
    type OrgId is UUID
    type MemberId is UUID
    type Address is String
    record Info is {
      name: String,
      address: Address?,
      isPrivate: Boolean
    }
    record Contacts is {
      primaryContacts: MemberId+,
      billingContacts: MemberId*,
      distributionContacts: MemberId*
    }
    event MemberAdded is { orgId: OrgId, memberId: MemberId }
    command AddMember yields event MemberAdded is {
      orgId: OrgId,
      memberId: MemberId
    }
-->


# Command-Event Patterns

This guide covers design patterns for structuring commands and their
corresponding events in RIDDL. Choosing the right pattern affects
traceability, message size, and system maintainability.

## Overview

In event-driven systems, commands request actions and events record what
happened. The relationship between command parameters and event parameters
requires careful design.

For background on messages, see the [Message concept](../../../concepts/message.md).

## Declaring the Pairing

Whichever pattern you choose below, RIDDL 2.0 lets you state the
command→event pairing **declaratively** with a `yields` clause:

<!-- riddl: in-context no-prelude=AddMember -->
```riddl
command AddMember yields event MemberAdded is {
  orgId: OrgId,
  memberId: MemberId
}
```

This does two things a comment cannot. Generators get a precise
request/response signature rather than having to infer one, and the validator
checks conformance: a handler for a `yields`-declaring command must
`yield` exactly that event, and one that never yields is an **Error**.

A command's `yields` must name an **event** and a query's must name a
**result**; anything else is an Error.

`yields` is optional and adoptable one message at a time. A handler in a model
that declares none may still yield whatever it likes, so adding the clause to
an existing model never breaks the parts you have not annotated yet.

The corresponding statement is `yield`:

<!-- riddl: in-clauses -->
```riddl
on cmd: command AddMember {
  yield event MemberAdded(orgId = cmd.orgId, memberId = cmd.memberId)
}
```

!!! info "`yield` is for commands; queries use `reply`"
    A command handler `yield`s the **event** the command declares with
    `yields`. A query handler `reply`s the **result** the query declares with
    `replies`. Crossing them is an Error.

    Before RIDDL 2.0 both were spelled `yield` and `reply` was a deprecated
    synonym; that was reversed, and `reply` is now a statement in its own
    right.

## Type Cardinality Notation

RIDDL uses suffixes to indicate how many values a field can hold:

| Suffix | Meaning | Example | Description |
|--------|---------|---------|-------------|
| *(none)* | Exactly one | `name: String` | Required, single value |
| `?` | Zero or one | `nickname: String?` | Optional field |
| `*` | Zero or more | `tags: Tag*` | Optional list (may be empty) |
| `+` | One or more | `contacts: Contact+` | Required list (at least one) |

These suffixes appear throughout the examples below. Understanding them is
essential for designing message types that accurately represent your domain
constraints.

## Example Entity

Throughout this guide, we'll use this Organization entity:

<!-- riddl: in-context no-prelude=Info,Contacts -->
```riddl
entity Organization is {
  state Active of record OrganizationState is {
    handler OrganizationHandler is {
      on command AddMembers { ??? }
    }
  }
}

record OrganizationState is {
  info: Info,
  members: MemberId*,
  contacts: Contacts
}

type Info is {
  name: String,
  address: Address?,
  isPrivate: Boolean
}

type Contacts is {
  primaryContacts: MemberId+,
  billingContacts: MemberId*,
  distributionContacts: MemberId*
}

command EstablishOrganization is { info: Info, contacts: Contacts }
command ModifyOrganizationInfo is { id: OrganizationId, info: Info }
command AddMembers is { orgId: OrganizationId, members: MemberId* }
command ModifyContacts is { orgId: OrganizationId, contacts: Contacts }
```

## Pattern 1: Same Event for All Commands

**Question:** Should all commands on an entity yield the same event?

<!-- riddl: in-context -->
```riddl
event OrganizationModified is {
  id: OrganizationId,
  info: Info,
  members: MemberId*,
  contacts: Contacts
}
```

### Assessment

!!! warning "Generally Not Recommended"
    In an event-driven system, distinct events for each operation are important
    for traceability and understanding system behavior.

**Problems:**

- No way to distinguish what changed by looking at the event
- Event consumers must diff current and previous state
- Poor audit trail

**When it might work:**

- Very simple entities with few modifications
- Systems where change tracking isn't important

## Pattern 2: Distinct Events, Full Entity Data

**Question:** Should each command have its own event containing the full entity?

<!-- riddl: in-context -->
```riddl
event OrganizationEstablished is {
  id: OrganizationId,
  info: Info,
  members: MemberId*,
  contacts: Contacts
}

event OrganizationInfoModified is {
  id: OrganizationId,
  info: Info,
  members: MemberId*,
  contacts: Contacts
}

event OrganizationMembersModified is {
  id: OrganizationId,
  info: Info,
  members: MemberId*,
  contacts: Contacts
}
```

### Assessment

!!! note "Better Traceability, But Verbose"
    Event names tell you what changed, but events carry unnecessary data.

**Advantages:**

- Clear what operation occurred
- Event consumers always have full context

**Disadvantages:**

- Extraneous data in modification events
- Larger message sizes
- Potential for confusion about what actually changed

**Recommendation:** Use for establishment events; consider other patterns for
modification events.

## Pattern 3: Optional Parameters

**Question:** Should modification events use optional versions of types?

<!-- riddl: in-context -->
```riddl
type InfoUpdate is {
  name: String?,
  address: Address?,
  isPrivate: Boolean?
}

event OrganizationEstablished is {
  id: OrganizationId,
  info: Info,
  contacts: Contacts
}

event OrganizationInfoModified is {
  id: OrganizationId,
  info: InfoUpdate
}

event OrganizationContactsModified is {
  id: OrganizationId,
  contacts: Contacts
}
```

### Assessment

!!! tip "Recommended for Complex Types"
    Good balance between clarity and payload size.

**Advantages:**

- Clear what changed (non-None fields)
- Reduced message size
- Type safety maintained

**Disadvantages:**

- Requires maintaining "Update" versions of types
- Event consumers must handle optional fields

**When to use:**

- Types with many fields where partial updates are common
- When message size matters (high-frequency events)

## Pattern 4: Surfaced Parameters

**Question:** Should events contain only the changed fields directly?

<!-- riddl: in-context -->
```riddl
event OrganizationMembersModified is {
  id: OrganizationId,
  members: MemberId*
}

command AddPrimaryContacts is {
  orgId: OrganizationId,
  contacts: MemberId*
}

event PrimaryContactsAdded is {
  id: OrganizationId,
  addedContacts: MemberId+
}

event PrimaryContactsRemoved is {
  id: OrganizationId,
  removedContacts: MemberId*
}
```

### Assessment

!!! tip "Recommended for High-Frequency Changes"
    Most direct access to changed data; minimal overhead.

**Advantages:**

- Minimal message size
- Clear exactly what changed
- Fine-grained operations

**Disadvantages:**

- More event types to manage
- Event consumers may need to maintain state

**Key decision:** For collection changes, decide whether the event contains:

- The items added/removed (delta), or
- The new complete collection (full state)

Document this decision clearly:

<!-- riddl: in-context -->
```riddl
event MembersAdded is {
  id: OrganizationId,
  addedMembers: MemberId+ // Only newly added members, not full list
} with { briefly "Contains only the members that were added in this operation" }
```

## Pattern Selection Guide

| Scenario | Recommended Pattern |
|----------|---------------------|
| Entity creation | Full entity data (#2) |
| Infrequent updates, simple types | Full entity data (#2) |
| Frequent updates, complex types | Optional parameters (#3) |
| High-frequency, specific field updates | Surfaced parameters (#4) |
| Audit/compliance requirements | Surfaced parameters (#4) |

## Best Practices

1. **Document conventions** - Use `briefly` or `description` to clarify what
   events contain

2. **Consistency within context** - Use the same pattern for similar operations

3. **Consider consumers** - How will event processors use this data?

4. **Size vs. simplicity** - Larger events are simpler but may impact performance

5. **Separate creation from modification** - Creation events should always
   contain complete initial state

## Related Concepts

- [Message](../../../concepts/message.md) - Message fundamentals
- [Handler](../../../concepts/handler.md) - Processing commands and events
- [Entity](../../../concepts/entity.md) - Stateful business objects
