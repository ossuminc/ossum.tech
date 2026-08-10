---
title: "Condition"
draft: false
---

A condition is a logical (boolean) expression resulting in true or false.
Conditions are used in `when` statements to control flow and in `match`
statements for pattern matching.

## Natural-Language Conditions

The simplest form describes the condition in natural language, wrapped in
`prompt(…)` so it is clear an AI decides it:

<!-- riddl: in-handler -->
```riddl
when prompt("the user is authenticated") then {
  // actions when the condition holds
} end
```

This lets authors express conditions at the appropriate level of abstraction.
Evaluating the condition is left to code generation.

!!! warning "The bare-string form is deprecated"
    <!-- riddl: skip reason="deliberate counter-example: it emits [deprecated], which the gate treats as failure" -->
    ```riddl
    when "user is authenticated" then { ??? } end   // deprecated
    ```

    It still parses, but draws a `[deprecated]` message. Everywhere else in
    RIDDL a bare quoted string denotes a **literal value**, while `prompt(…)`
    marks something an AI decides — so a natural-language condition should say
    which of the two it is rather than borrowing the literal's spelling.

## Identifier Conditions

Conditions can reference identifiers defined with `let`:

<!-- riddl: in-handler -->
```riddl
let isValid = "order.items.count > 0"
when isValid then {
  // actions when valid
} end
```

Identifiers can be negated:

<!-- riddl: in-handler -->
```riddl
when !isValid then {
  error "Order must have at least one item"
} end
```

## Numeric Expressions

Numeric expressions involve comparisons and arithmetic:

- **Comparison operators**: `>`, `<`, `>=`, `<=`, `==`, `!=`
- **Arithmetic operators**: `+`, `-`, `*`, `/`

<!-- riddl: in-handler -->
```riddl
when prompt("order.total > 100") then {
  // apply discount
} end
```

Note: In RIDDL, these expressions are typically written as strings that
describe the intended logic. The actual parsing and evaluation happens
during code generation.

## Boolean Expressions

Boolean expressions combine conditions using logical operators:

- **AND**: Both conditions must be true
- **OR**: Either condition must be true
- **NOT**: Negates a condition

<!-- riddl: in-handler -->
```riddl
when prompt("user.isVerified AND order.total > 0") then {
  // process order
} end
```

## Match Expressions

The `match` statement provides pattern matching:

<!-- riddl: in-handler -->
```riddl
match "orderStatus" {
  case "pending" {
    // handle pending
  }
  case "processing" {
    // handle processing
  }
  case "shipped" {
    // handle shipped
  }
  default {
    // handle unknown status
  }
}
```

## Occurs In

* [Statements](statement.md) - specifically `when` and `match` statements

## Contains

Conditions are leaf elements containing:

* String literals describing the condition
* Identifier references
* Logical operators combining sub-conditions
