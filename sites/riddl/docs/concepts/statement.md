---
title: "Statement"
draft: false
description: >-
  The actions available inside an on clause, function body, or saga step,
  and the value expressions they operate on.
---

<!-- riddl-prelude
constant MaxItems is Natural = "100"
-->

A Statement is an action that can be taken in response to a message. Statements
form the body of an [on clause](onclause.md) which is what
[handlers](handler.md) are composed of. Statements express the business logic
of your system in a structured but abstract way.

## Statement Types

| Statement | Description | Example |
|-----------|-------------|---------|
| `when` | Conditional logic with optional else | `when total > Minimum then { ... } end` |
| `match` | Pattern matching over a typed subject | `match status { case Pending { ... } }` |
| `foreach` | Bounded iteration over a collection | `foreach line in field order.lines { ... }` |
| `send` | Emit a message on one of this processor's outlets | `send event X to outlet Events` |
| `tell` | Deliver a message directly to a processor | `tell command X to entity Y` |
| `yield` | Produce a command's or query's declared response | `yield result Info(id)` |
| `set` | Assign a value to a field or state | `set field status to "Active"` |
| `let` | Create a local variable binding | `let total = call function Cart.Total(items)` |
| `put` | Publish a value to a UI output | `put order.number to output Panel` |
| `return` | Return a function's result | `return call function Tax.Compute(sub)` |
| `require` | Assert a precondition | `require amount > Zero` |
| `do` | Natural language action description | `do "Calculate the total"` |
| `error` | Refuse to proceed, with a reason | `error "Invalid state"` |
| `code` | Embed implementation code | `` ```scala ... ``` `` |

### Entity-Specific Statements

These statements are only valid within Entity handlers:

| Statement | Description | Example |
|-----------|-------------|---------|
| `morph` | Change entity to a different state | `morph entity X to state Y with record Z()` |
| `become` | Switch entity to a different handler | `become entity X to handler Y` |

## Value Expressions

RIDDL 2.0 introduces a real value-expression system beneath the statements.
Wherever a statement needs a value, any of these forms is accepted:

| Form | Syntax | Meaning |
|------|--------|---------|
| Literal | `"some text"` | Opaque pseudo-code, or a literal constant |
| Value reference | `order.total` | A field, state field, function input, or `let` local |
| Constructor | `OrderPlaced(id, total = x)` | Builds a message or record |
| Get | `get from input SignupForm` | Reads a UI input or an entity state |
| Call | `call function Pricing.Total(a, b)` | Invokes a pure function for its result |
| Prompt | `prompt("compute the discount")` | A value computed by AI at generation time |
| Boolean | `a > b and not c` | A structured boolean expression |

### Constructors

A constructor builds a [message](message.md) or record inline. Arguments are
positional first, then named, and are checked against the target's fields for
count, name, order and (best effort) type:

<!-- riddl: skip reason="illustrative fragment; references vocabulary this page does not define" -->
```riddl
yield event OrderPlaced(orderId, total = cart.total, currency = "USD")
```

### Boolean Expressions

Precedence runs `or` < `and` < `not` < comparison < atom, with parentheses to
group. `and`, `or`, `not`, `true` and `false` are **context-sensitive**: they
are recognized only inside a boolean expression, so they stay legal identifiers
everywhere else.

!!! warning "Comparisons are type-safe and reference-only"
    Both operands of a comparison must be a **typed reference** — a value
    reference, a `get from`, or a named [constant](constant.md). A literal is
    not permitted, and this is enforced at **parse** time:

    <!-- riddl: skip reason="deliberate counter-example; shows what does NOT work" -->
    ```riddl
    when count > 5 then ??? end        // fails to parse
    when count > "5" then ??? end      // fails to parse
    ```

    Name the threshold instead. The constant is a definition, declared
    alongside the other definitions of its context:

    <!-- riddl: in-context no-prelude=MaxItems -->
    ```riddl
    constant MaxItems is Natural = "100"
    ```

    and the comparison is a statement, written inside an on-clause:

    <!-- riddl: in-handler -->
    ```riddl
    when cart.itemCount > MaxItems then error "too many items" end
    ```

    This removes magic constants from models and makes every comparison check
    the types on both sides. `==` and `!=` require operands of the same
    category; `<`, `>`, `<=` and `>=` require an ordered numeric type.

## Statement Details

### When Statement

<!-- riddl: skip reason="illustrative fragment; references vocabulary this page does not define" -->
```riddl
when order.isPaid and not order.isCancelled then {
  send event LoginSucceeded to outlet Events
} else {
  error "Authentication failed"
} end
```

The `end` keyword is required. A condition may be:

- a boolean expression: `when a > b and not c then`
- a bare boolean-typed reference, including a dotted path:
  `when order.isPaid then`
- a `let` binding, optionally negated: `when authorized then`,
  `when !authorized then`
- an AI-evaluated prompt: `when prompt("the user is authenticated") then`

!!! warning "A bare string condition is deprecated"
    `when prompt("the user is authenticated") then` parses but draws a `[deprecated]`
    message; write `when prompt("…")`. Everywhere else a bare string is a
    **literal**, while `prompt(…)` marks a value an AI decides — and a
    natural-language condition is the latter.

A bare reference is resolved and checked to be Boolean-typed; a clearly
non-Boolean condition is an **Error**.

### Match Statement

<!-- riddl: skip reason="illustrative fragment; references vocabulary this page does not define" -->
```riddl
match order.status {
  case Pending {
    tell command ProcessOrder to entity OrderProcessor
  }
  case Shipped when order.isPaid {
    send event OrderShipped to outlet Events
  }
  case >= HighValueThreshold {
    tell command EscalateReview to entity Review
  }
  default {
    error "Unknown order status"
  }
}
```

The subject is a value reference, a `get from`, or a legacy pseudo-code
literal. A case pattern is one of:

- **Type case** — a bare type reference matching an alternant, enumerator or
  message subtype: `case Pending`
- **Comparison** — an operator and a comparand, with the subject as the
  implicit left operand: `case >= HighValueThreshold`
- **Literal** — a legacy pseudo-code label: `case "pending"`

Each case may carry an optional `when <boolean>` guard. Naming an unknown
type-case is an **Error**. For a *closed* subject — an Enumeration or
Alternation — a non-exhaustive match without `default` draws a
**StyleWarning**.

### Foreach Statement

RIDDL's only loop, and deliberately bounded — there is no unbounded iteration
in the language:

<!-- riddl: skip reason="illustrative fragment; references vocabulary this page does not define" -->
```riddl
foreach line in field order.lines {
  send event LineShipped(sku = line.sku) to outlet Shipments
}
```

The collection is a `field` reference or a `let`-bound local whose type
resolves to a collection: Sequence, Set, Graph, Table, Replica, Mapping, or a
cardinality wrapper such as `many` or `optional`.

### Send, Tell and Yield

- **send** — emit on one of *this* processor's own [outlets](outlet.md); a
  [connector](connector.md) routes it onward
- **tell** — deliver directly to a specific processor (point-to-point)
- **yield** — produce a command's or query's declared response, without
  needing to know the sender's identity

<!-- riddl: skip reason="illustrative fragment; references vocabulary this page does not define" -->
```riddl
send event ItemAdded to outlet CartEvents
tell command ProcessPayment(orderId) to entity PaymentService
yield result CartInfo(cart.id, cart.total)
```

!!! warning "`send … to inlet` is deprecated"
    Sending directly into another processor's inlet bypasses the streaming
    model — that is `tell`'s job. The inlet form still parses and emits a
    `[deprecated]` message.

!!! warning "`reply` is deprecated"
    `reply` is a deprecated synonym for `yield`, parsing to the same node.

### Put and Return

`put` publishes a value to a UI [output](output.md) and is valid only in
application and context handlers. `return` produces a
[function](function.md)'s result and is valid only in a function body.

They can never appear together — the two scopes are disjoint. `put`, in an
application or context handler:

<!-- riddl: in-application -->
```riddl
put order.confirmationNumber to output ConfirmationPanel
```

and `return`, in a function body:

<!-- riddl: in-function -->
```riddl
return call function Tax.Compute(subtotal)
```

### Require and Error

<!-- riddl: skip reason="illustrative fragment; references vocabulary this page does not define" -->
```riddl
require amount > Zero
require invariant BalanceNonNegative
require invariant UnderLimit with limits
error "Price must be greater than zero"
```

A `require invariant` is an explicit **restatement** — an
[invariant](invariant.md) already applies implicitly across its declaring
scope. The `with <value>` form is the exception that does real work: it hands a
value to an invariant declaring `requires <type>`, which is the one form
ambient scope cannot supply.

!!! warning "Refusals before effects"
    Within any single linear statement list, every **refusal** (`require`,
    `error`) must appear before every **effect** (`set`, `morph`, `become`,
    `send`, `tell`, `yield`, `put`). Acting and then refusing would leave
    partial changes behind.

    Each statement list is checked independently, so each branch of a `when`,
    `match` or `foreach` body is its own list. A refusal after an effect in the
    same list is an **Error**.

    <!-- riddl: skip reason="illustrative fragment; references vocabulary this page does not define" -->
    ```riddl
    on cmd: command Withdraw {
      require cmd.amount > Zero          // refusals first
      require balance >= cmd.amount
      set field balance to "balance - amount"    // then effects
      yield event Withdrawn(amount = cmd.amount)
    }
    ```

### Do Statement

Use `do` to describe business logic in natural language that will be
implemented in target code:

<!-- riddl: in-handler -->
```riddl
do "Calculate the total price including all applicable taxes, discounts,
    and shipping based on the customer's location and membership tier"
```

!!! warning "The `prompt` statement is deprecated"
    `do` is canonical; `prompt "..."` emits a `[deprecated]` message and
    prettify normalizes it.

    Do not confuse it with the `prompt(...)` **value**, distinguished by its
    parentheses. The statement describes an action for a human to implement;
    the value denotes something AI computes.

### Code Statement

RIDDL's deliberate **escape hatch**: an opaque pass-through of raw
target-language source, handed to the code generator untouched.

<!-- riddl: in-function -->
````riddl
```scala
val total = items.map(_.price).sum * (1 - discountRate)
```
````

Supported languages: `scala`, `java`, `python`, `mojo`. RIDDL does not parse
or check the contents — everything between the fences is carried through
verbatim.

`code` is allowed in **every** statement scope, including pure
[function](function.md) bodies and `on activate` / `on passivate`. It is also
exempt from the [refusals-before-effects](#require-and-error) rule, being
neither a refusal nor an effect.

!!! warning "Using it opts out of the guarantees"
    Those exemptions are not oversights: RIDDL cannot classify opaque source,
    so it declines to guess rather than guessing wrong. But the rules exist to
    buy something — a provably pure function, a lifecycle clause that provably
    does not emit — and a `code` block suspends that for as long as it lasts,
    while tying the model to one target language.

    Prefer [`do "..."`](#do-statement) to describe intent and let the
    generator implement it. Reach for `code` when a generator genuinely cannot
    express what you need.

### Morph and Become (Entity Only)

<!-- riddl: skip reason="illustrative fragment; references vocabulary this page does not define" -->
```riddl
morph entity Order to state Shipped with record ShippedData(trackingNumber)
become entity Order to handler ShippedHandler
```

The `morph` payload is a **record** — a bare record reference or an inline
constructor. It is not a message; a message cannot type a [state](state.md).

## Level of Detail

Statements express pseudocode in a structured but abstract way. RIDDL does not
require the system model to contain implementation code. The objectives are:

- Converting specifications to executable code should be done by humans or AI
- Statements capture interactions between model definitions
- Statements are intentionally **not** Turing complete — `foreach` is bounded
  by its collection, so it does not change this
- Natural language descriptions (via `do`) suffice for complex logic

## Applicability

Not all statements can be used everywhere. Availability depends on the
containing definition — and, as of 2.0, several places actively *ban*
statements:

| Context | Available Statements |
|---------|---------------------|
| All handlers | when, match, foreach, send, tell, yield, require, set, let, do, error, code |
| Entity handlers | All above + morph, become |
| Application / context handlers | All above + put |
| Functions | when, match, foreach, require, let, return, do, error, code |
| `on activate` / `on passivate` | Side-effect free only — no send, tell, yield, morph, become |
| `on event` | No require or error — an event has happened and must be accepted |
| Saga steps | send, tell, yield, put, do, error |

The function and lifecycle bans are enforced at **parse** time, so a banned
statement can never enter the AST at all.

## Deprecated Statements

| Deprecated | Replacement |
|------------|-------------|
| `reply <msg>` | `yield <msg>` |
| `prompt "..."` | `do "..."` |
| `send … to inlet X` | `send … to outlet Y`, or `tell` |

## Occurs In

- [On Clause](onclause.md)
- [Function](function.md) (body)
- [Saga Step](sagastep.md)

## Contains

Statements may contain:

- Value expressions (constructors, calls, gets, references, boolean
  expressions)
- Conditionals (in `when`, `match` guards, and `require`)
- Literal values
- Field references
- Path identifiers to reference definitions

None of these are definitions themselves.
