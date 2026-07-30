---
title: "Condition"
draft: false
---

A condition is a logical (boolean) expression resulting in true or false.
Conditions are used in `when` statements to control flow and in `match`
statements for pattern matching.

## Arbitrary Conditional

The simplest form is a string that describes the condition in natural language:

```riddl
when "user is authenticated" then {
  // actions when condition is true
} end
```

This allows authors to express conditions at the appropriate level of
abstraction. The actual implementation of the condition check is left to
code generation or manual implementation.

## Identifier Conditions

Conditions can reference identifiers defined with `let`:

```riddl
let isValid = "order.items.count > 0"
when isValid then {
  // actions when valid
} end
```

Identifiers can be negated:

```riddl
when !isValid then {
  error "Order must have at least one item"
} end
```

## Numeric Expressions

Numeric expressions involve comparisons and arithmetic:

- **Comparison operators**: `>`, `<`, `>=`, `<=`, `==`, `!=`
- **Arithmetic operators**: `+`, `-`, `*`, `/`

```riddl
when "order.total > 100" then {
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

```riddl
when "user.isVerified AND order.total > 0" then {
  // process order
} end
```

## Match Expressions

The `match` statement provides pattern matching:

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
