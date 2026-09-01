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
  requires record PricingInput returns record PricingInput
  function CalculateTotal is { requires record PricingInput returns record PricingInput ??? }
}
entity Order is {
  state Started of record DoneData is { handler StartedHandler is { ??? } }
  state Done of record DoneData is { handler DoneHandler is { ??? } }
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

## The Eleven Forms

| Form | Syntax | Meaning |
|------|--------|---------|
| Literal | `"some text"` | Opaque pseudo-code, or a literal constant |
| Empty | `empty`, `none`, `empty String*` | The minimum-cardinality inhabitant of a type — the absence of a value |
| Value reference | `order.total` | A field, state field, function input, or `let` local |
| Constructor | `OrderPlaced(id, total = x)` | Builds a message or record |
| Get | `get from input SignupForm` | Reads a UI input or an entity state |
| Call | `call function Pricing.Total(a, b)` | Invokes a pure function for its result |
| Prompt | `prompt("compute the discount") [as <type>]` | A value computed by AI at generation time; the ascription states its type |
| Boolean | `a > b and not c` | A structured boolean expression |
| Ask | `ask query GetInfo of entity Catalog` | A query paired with the reply that answers it |
| Initiate | `initiate entity Order` | Brings an instance into being; **yields its `Id`** |
| Self | `self`, `self.id` | The instance executing right now |

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

<!-- riddl: in-yielding-handler -->
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

### Multi-line prompts

Guidance long enough to need more than one line goes in **braces**, as a
sequence of strings with no commas or other separator between them:

<!-- riddl: in-handler -->
```riddl
let sentiment = prompt({
  "rate the customer's sentiment from the note on the order,"
  "returning a value between 0.0 and 1.0"
}) as Real
```

The braces are the only multi-line form — a bare `prompt("…")` takes **exactly
one** string. That restriction is deliberate: RIDDL statements have no
terminator, so allowing two juxtaposed strings would leave nothing but the next
keyword to mark where the statement ended.

## Typed holes: `prompt("…") as <type>`

`prompt(...)` may carry an optional type ascription:

<!-- riddl: in-handler -->
```riddl
let price = prompt("a plausible price for this item") as Real
```

<!-- riddl: in-context -->
```riddl
constant Greeting: String = prompt("a friendly greeting")
```

That is a **typed hole**, and it is the seam between RIDDL's two tiers: the
**type is known and checkable at compile time**, while the computation that
produces a value of that type is prose an AI fills in at generation time. The
deterministic tier parses, validates and type-checks; the AI tier is the string
inside the parentheses.

The ascription **restates the position's type; it never overrides it.** A
`let` takes its type from the ascription, but in a position that already
determines the type — a constructor argument, a field — the ascription must
agree with it. Writing one is opt-in: unascribed `prompt(...)` is unchanged and
still valid, and is the right form wherever the position already says enough.

## Empty and None

`empty` denotes the **minimum-cardinality inhabitant** of a type: no value at
all, written where a value is expected.

<!-- riddl: in-handler -->
```riddl
set field nickname to empty
set field tags to none
```

`none` is a **synonym**, not a second construct. Both spellings produce the
identical AST, and `prettify` converges them on `empty`. Use whichever reads
better where it appears — `none` often suits an optional scalar and `empty` a
collection — but expect formatted output to say `empty`.

### Only where the minimum cardinality is zero

`empty` is meaningful only for a type that admits having no value: an optional
`T?`, a sequence `T*`, or an explicit range starting at zero, `T{0,n}`. A bare
`T` or a `T+` requires at least one value, so `empty` is not an inhabitant of
it, and asking for one is the `value-empty-needs-zero-cardinality` Error.

### The type ascription

`empty` may carry a type, which is what lets it be written in a position that
does not itself supply one — most often a constructor argument:

<!-- riddl: in-handler -->
```riddl
let noTags = empty String*
let unset  = none String?
```

The ascription is where the cardinality rule is checked, so `empty String` —
a bare, one-or-more type — is the Error above, while `empty String*` is fine.

!!! note "Why the ascription cannot be followed by just anything"
    A type expression is a bare path, and RIDDL statements are separated by
    whitespace with no terminator. Without a guard, `set x to empty` followed
    by `set y to …` would read the second statement's `set` as the first's
    ascription. Every statement begins with a reserved keyword, so the parser
    refuses those in the ascription position — a complete fix rather than a
    heuristic, since no type can be named `set`.

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

## Initiate

`initiate` brings a new instance of an entity into being, and its **value is
that instance's identity**:

<!-- riddl: in-handler -->
```riddl
let fresh = initiate entity ExampleEntity
tell command ExampleWelcome(target = fresh) to fresh
```

It is not a second way to exist — construction still completes only when
`on init` finishes. But without it no `Id` value could ever come into being,
so nothing could be addressed.

`initiate` and [`terminate`](statement.md) are **entity-only** and are both
**effects**: banned in a function body, in `on activate`/`on passivate`, and
in a correlation fold; legal in a saga step.

!!! warning "Discarding the id is a warning"
    The id is the only thing `initiate` produces, so binding it and never
    using it means the instance was created and immediately made unreachable.

## Self

`self` is the instance executing right now. Its type is a **synthesized
record** carrying `id` and `version`:

<!-- riddl: in-handler -->
```riddl
let me  = self
let who = self.id
```

Because that type is an ordinary record, `self.id` resolves by the same path
walk as any other value — which is why no resolution rule has to know `self`
exists.

The type is not user-nameable, though: `self.id` is `Id(Order)` in an Order
handler and `Id(Shipping)` in a Shipping one. So `let me: T = self` has no `T`
to write, and **`self` cannot be assigned into a message field — pass
`self.id`.** The field set is closed; adding to it is a language change.

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
