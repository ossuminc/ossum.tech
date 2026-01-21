---
title: "Value"
draft: false
---

A value is an expression, in the context of a statement, that provides a
value to a statement. There are a variety of value expressions but they are
intentionally vague or abstract. The idea is that statements, values, and
conditions work together to express business logic at an appropriate level
of abstraction—detailed enough to be meaningful, but not so specific as to
constrain implementation.

## Value Types

- **Literals**: Direct values like strings, numbers, or booleans
- **Field references**: References to fields in state or message types
- **Path identifiers**: References to definitions elsewhere in the model
- **Expressions**: Combinations of values using operators

## Occurs In

* [Statements](statement.md)

## Contains

Values are self-contained and only contain other values.
