---
title: "Statement"
draft: false
---

A Statement is an action that can be taken in response to a message. Statements
form the body of an [on clause](onclause.md) which is what
[handlers](handler.md) are composed of. Statements express the business logic
of your system in a structured but abstract way.

## Statement Types

RIDDL provides the following statement types:

| Statement | Description | Example |
|-----------|-------------|---------|
| `when` | Conditional logic with optional else | `when "condition" then { ... } end` |
| `match` | Pattern matching for multiple cases | `match "status" { case "x" { ... } }` |
| `send` | Send a message to an outlet or inlet | `send event X to outlet Events` |
| `tell` | Send a message directly to a processor | `tell command X to entity Y` |
| `set` | Assign a value to a field | `set field status to "Active"` |
| `let` | Create a local variable binding | `let total = "price * quantity"` |
| `prompt` | Natural language action description | `prompt "Calculate the total"` |
| `error` | Produce an error with a message | `error "Invalid state"` |
| `code` | Embed implementation code | `` ```scala ... ``` `` |

### Entity-Specific Statements

These statements are only valid within Entity handlers:

| Statement | Description | Example |
|-----------|-------------|---------|
| `morph` | Change entity to a different state | `morph entity X to state Y with command Z` |
| `become` | Switch entity to a different handler | `become entity X to handler Y` |

## Statement Details

### When Statement

The `when` statement provides conditional logic:

```riddl
when "user is authenticated" then {
  send event LoginSucceeded to outlet Events
} else {
  error "Authentication failed"
} end
```

The `end` keyword is required. Conditions can be:

- Literal strings: `when "condition description" then`
- Identifier references: `when authorized then` (using a `let` binding)
- Negated identifiers: `when !authorized then`

### Match Statement

Pattern matching for multiple conditions:

```riddl
match "orderStatus" {
  case "pending" {
    tell command ProcessOrder to entity OrderProcessor
  }
  case "shipped" {
    send event OrderShipped to outlet Events
  }
  default {
    error "Unknown order status"
  }
}
```

### Send vs Tell

- **send**: Routes messages through outlets/inlets (streaming, pub/sub)
- **tell**: Sends messages directly to a specific processor (point-to-point)

```riddl
// Send to an outlet (for streaming/events)
send event ItemAdded to outlet CartEvents

// Tell a specific entity (direct command)
tell command ProcessPayment to entity PaymentService
```

### Prompt Statement

Use `prompt` to describe complex business logic in natural language that will
be implemented in target code:

```riddl
prompt "Calculate the total price including all applicable taxes, discounts,
        and shipping based on the customer's location and membership tier"
```

### Code Statement

Embed actual implementation code when necessary:

```riddl
```scala
val total = items.map(_.price).sum * (1 - discountRate)
```
```

Supported languages: `scala`, `java`, `python`, `mojo`

### Morph and Become (Entity Only)

- **morph**: Transitions an entity to a new state
- **become**: Switches which handler processes messages

```riddl
// Transition to a new state
morph entity Order to state Shipped with command ShipOrder

// Switch to a different handler
become entity Order to handler ShippedHandler
```

## Level of Detail

Statements express pseudocode in a structured but abstract way. RIDDL does not
require the system model to contain implementation code. The objectives are:

- Converting specifications to executable code should be done by humans or AI
- Statements capture interactions between model definitions
- Statements are intentionally **not** Turing complete
- Natural language descriptions (via `prompt`) suffice for complex logic

## Applicability

Not all statements can be used everywhere. Statement availability depends on
the containing definition:

| Context | Available Statements |
|---------|---------------------|
| All handlers | when, match, send, tell, set, let, prompt, error, code |
| Entity handlers | All above + morph, become |
| Functions | when, match, set, let, prompt, error, code |
| Saga steps | send, tell, prompt, error |

## Occurs In

- [On Clause](onclause.md)
- [Function](function.md) (body)
- [Saga Step](sagastep.md)

## Contains

Statements may contain:

- Conditionals (in `when` and `match`)
- Literal values
- Field references
- Path identifiers to reference definitions

None of these are definitions themselves.
