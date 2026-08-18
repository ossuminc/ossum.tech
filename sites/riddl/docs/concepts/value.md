---
title: "Value"
draft: false
description: >-
  Value expressions: the seven forms a statement operand may take, including
  constructors, calls, gets and boolean expressions.
---

<!-- riddl-prelude
constant MaxItems is Natural = 100
record DoneData is { note is String }
record SignupData is { email is String }
event OrderPlaced is { orderId is String, total is Natural, currency is String }
record PricingInput is { subtotal is Natural, taxRate is Natural }
function Pricing is {
  requires PricingInput returns PricingInput
  function CalculateTotal is { requires PricingInput returns PricingInput ??? }
}
entity Order is {
  state Done of record DoneData is { handler H is { ??? } }
}
-->

A value is an expression, in the context of a [statement](statement.md), that
provides a value to that statement. Values, statements and conditions work
together to express business logic at an appropriate level of abstraction —
detailed enough to be meaningful, but not so specific as to constrain
implementation.

RIDDL 2.0 replaced what had been a mostly-opaque quoted string with a real
value-expression system. A literal string is still accepted everywhere, so
pseudo-code remains available where structure would be false precision.

## The Seven Forms

| Form | Syntax | Meaning |
|------|--------|---------|
| Literal | `"some text"` | Opaque pseudo-code, or a literal constant |
| Value reference | `order.total` | A field, state field, function input, or `let` local |
| Constructor | `OrderPlaced(id, total = x)` | Builds a message or record |
| Get | `get from input SignupForm` | Reads a UI input or an entity state |
| Call | `call function Pricing.Total(a, b)` | Invokes a pure function for its result |
| Prompt | `prompt("compute the discount")` | A value computed by AI at generation time |
| Boolean | `a > b and not c` | A structured boolean expression |

## Value References

A value reference names something in scope. Four sources are consulted, in
order:

1. the [on clause](onclause.md)'s message binding — bare `ord` is the whole
   message, `ord.field` reaches into it
2. a field of the handled message, the entity [state](state.md), or a
   [function](function.md)'s `requires` input
3. a definition reached by a qualified path, such as `GState.active`
4. a named [constant](constant.md)

A `let` local is also a value reference, but resolves **lexically** rather than
through the symbol table: it is visible only after its declaration and is
shadowed inside nested blocks.

## Constructors

A constructor builds a [message](message.md) or record inline, rather than
requiring it be assembled elsewhere first:

<!-- riddl: in-handler -->
```riddl
yield event OrderPlaced(orderId, total = cart.total, currency = "USD")
morph entity Order to state Done with record DoneData(note = "fulfilled")
```

Arguments are **positional first, then named**. Count, names, ordering and
(best effort) types are all checked against the target's fields.

## Get

`get from` reads a value from a UI [input](input.md) or an entity
[state](state.md):

<!-- riddl: in-application -->
```riddl
let email = get from input SignupForm
```

<!-- riddl: in-context -->
```riddl
record BasketData is { total is Natural }
command AddItem is { sku is String }

entity Basket is {
  state Filling of record BasketData is {
    handler BasketHandler is {
      on command AddItem {
        let current = get from state Filling
      }
    }
  }
}
```

The two forms cannot appear in the same clause. An `input` exists only inside
an `application` context, and **state may be read only inside the entity that
owns it** — reading another definition's state is an Error as of RIDDL 2.0.

## Call

`call` invokes a [function](function.md) — and only a function, since
functions are the only definitions guaranteed pure — and produces its result:

<!-- riddl: in-handler -->
```riddl
let total = call function Pricing.CalculateTotal(subtotal, taxRate = rate)
```

A call is value-producing rather than a bare statement, so it composes with
`let`, `set`, `return` and constructor arguments. Calling something that
declares no `returns` is an **Error**.

## Prompt

`prompt("...")` denotes a value computed by AI at generation time:

<!-- riddl: in-handler -->
```riddl
set field recommendation to prompt("suggest a complementary product")
```

It is distinguished from the `do` **statement** by its parentheses. The
statement describes an action for a human to implement; the value denotes
something AI computes.

## Boolean Expressions

Precedence runs `or` < `and` < `not` < comparison < atom, with parentheses to
group:

<!-- riddl: in-handler -->
```riddl
when order.isPaid and not (order.isCancelled or order.isRefunded) then ??? end
```

`and`, `or`, `not`, `true` and `false` are **context-sensitive**: they are
recognized only inside a boolean expression, so they remain legal identifiers
everywhere else in the language.

!!! warning "Comparisons are type-safe and reference-only"
    Both operands of a comparison must be a **typed reference** — a value
    reference, a `get from`, or a named [constant](constant.md) — never a
    literal. This is enforced at **parse** time, so `count > 5`,
    `count > "5"`, `count > true` and `count > R(1)` all fail to parse.

    To compare against a fixed value, name it. The constant is a definition,
    declared alongside the other definitions of its context:

    <!-- riddl: in-context no-prelude=MaxItems -->
    ```riddl
    constant MaxItems is Natural = 100
    ```

    and the comparison is a statement, written inside an on-clause:

    <!-- riddl: in-handler -->
    ```riddl
    when cart.itemCount > MaxItems then error "too many items" end
    ```

    The point is to remove magic constants from models and to make every
    comparison check the types on both sides. `==` and `!=` require operands
    of the same category; `<`, `>`, `<=` and `>=` require an ordered numeric
    type on both sides.

    `true` and `false` remain valid boolean *atoms* — usable with `and`, `or`,
    `not`, and standalone — just not as comparison operands.

## Where Values Are Used

| Statement | Operand |
|-----------|---------|
| `set` | the assigned value |
| `let` | the bound expression |
| `put` | the published value |
| `return` | the returned value |
| `send`, `tell`, `yield` | a message reference or constructor |
| `morph` | a record reference or constructor |
| `when`, `require`, `invariant` | a condition |
| `match` | the subject, and each comparison pattern's comparand |

## Occurs In

* [Statements](statement.md)
* [Invariants](invariant.md)

## Contains

Values may contain other values — a constructor's arguments, a call's
arguments, and a boolean expression's operands are all themselves values.
