---
title: "Interaction"
draft: false
---

An interaction defines a single step within a [Use Case](use-case.md), describing
how one participant communicates with or acts upon another. Interactions are the
building blocks of use cases, capturing the flow of actions between users,
entities, and other system components.

## Purpose

Interactions serve to:

- **Document step-by-step flows**: Show exactly what happens at each point
- **Enable sequence diagram generation**: Provide data for visual documentation
- **Define acceptance criteria**: Each interaction can be verified in testing
- **Clarify responsibilities**: Make explicit which component handles each action

## Syntax

Interactions use a natural language-like syntax within use cases:

```riddl
case PlaceOrder is {
  user Customer "selects items and clicks checkout"
  then entity ShoppingCart "validates item availability"
  then entity PaymentService "processes payment"
  then entity OrderService "creates order record"
  then user Customer "receives confirmation"
}
```

## Interaction Keywords

| Keyword | Description | Example |
|---------|-------------|---------|
| `user ... then` | User initiates an action | `user Customer "clicks submit"` |
| `then` | Continues the flow to next step | `then entity Service "processes request"` |
| `tell` | Send a command to an entity | `tell entity Order to CreateOrder` |
| `publish` | Send a message to a pipe | `publish event OrderCreated to OrderEvents` |
| `saga` | Initiate a saga process | `saga PaymentSaga "processes distributed transaction"` |

## Participants

Interactions can involve:

- **Users**: Human or system actors defined at the domain level
- **Entities**: Stateful business objects that process commands
- **Applications**: UI components that present information
- **Sagas**: Multi-step processes that coordinate across components

## Example: Complete Flow

```riddl
epic UserRegistration is {
  user NewUser wants to "create an account"
  so that "they can access the platform"

  case SuccessfulRegistration is {
    user NewUser "enters email and password on signup form"
    then application SignupForm "validates input format"
    then entity UserService "checks email availability"
    then entity UserService "creates new user record"
    then entity EmailService "sends verification email"
    then user NewUser "sees success message"
  }

  case EmailAlreadyExists is {
    user NewUser "enters existing email"
    then application SignupForm "validates input format"
    then entity UserService "finds email already registered"
    then user NewUser "sees error suggesting login instead"
  }
}
```

## Occurs In

* [Use Case](use-case.md)

## Contains

Nothing (leaf element within use cases)