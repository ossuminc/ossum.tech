---
title: "Use Case"
draft: false
---

A use case is a definition found in an [epic](epic.md) that defines one way
a user might interact with the system. Use cases capture the step-by-step
interactions between users and system components.

## Purpose

Use cases in RIDDL serve several purposes:

- **Document user journeys**: Show how users accomplish goals
- **Define acceptance criteria**: Establish what "done" looks like
- **Generate sequence diagrams**: Visualize component interactions
- **Guide implementation**: Provide clear requirements for developers

## Syntax

```riddl
epic UserAuthentication is {
  user Customer wants to "securely access their account"
  so that "they can view orders and manage settings"

  case SuccessfulLogin is {
    user Customer "enters credentials on login page"
    then entity AuthService "validates credentials"
    then entity AuthService "creates session token"
    then user Customer "is redirected to dashboard"
  }

  case FailedLogin is {
    user Customer "enters invalid credentials"
    then entity AuthService "rejects authentication"
    then user Customer "sees error message"
  }
}
```

## Interaction Types

Use cases support various interaction patterns:

| Keyword | From | To | Description |
|---------|------|-----|-------------|
| `user ... then` | User | Any | User initiates an action |
| `tell` | Any | Entity | Send command to entity |
| `publish` | Any | Pipe | Publish message to pipe |
| `subscribe` | Any | Pipe | Subscribe to messages |
| `saga` | Any | Saga | Initiate a saga |
| `select` | User | Element | Select from UI element |
| `provide` | User | Element | Provide input to UI |
| `present` | Element | User | Display info to user |

## Happy Path vs. Alternatives

A complete epic typically includes:

- **Happy path**: The ideal scenario where everything works
- **Alternative paths**: Variations that still succeed
- **Error paths**: Handling of failures and edge cases

```riddl
epic PlaceOrder is {
  user Customer wants to "purchase items in cart"
  so that "they receive products they need"

  case HappyPath is {
    // Normal successful order
  }

  case OutOfStock is {
    // Item unavailable handling
  }

  case PaymentFailed is {
    // Payment rejection handling
  }
}
```

## Relationship to Testing

Use cases directly inform acceptance tests. Each case can be translated into
a test scenario that verifies the system behaves as specified.

## Occurs In

* [Epics](epic.md)

## Contains

* [Steps/Interactions](case.md) - the individual steps in the use case
