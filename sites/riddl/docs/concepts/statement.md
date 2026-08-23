---
title: "Statement"
draft: false
description: >-
  The actions available inside an on clause, function body, or saga step,
  and the value expressions they operate on.
---

<!-- riddl-prelude
constant MaxItems is Natural = 100
constant Zero is Whole = 0
constant HighValueThreshold is Natural = 1000
type OrderStatus is any of { Pending, InTransit, Delivered }
record ShippedData is { trackingNumber is String }
event OrderPlaced is { orderId is String, total is Natural, currency is String }
event ItemAdded is { sku is String }
event LineShipped is { sku is String }
event LoginSucceeded is { who is String }
event OrderShipped is { orderId is String }
event Withdrawn is { amount is Natural }
command Withdraw yields event Withdrawn is { amount is Natural }
command AddItem yields event ItemAdded is { sku is String }
query GetCart replies result CartInfo is { id is String }
command ProcessOrder is { orderId is String }
command ProcessPayment is { orderId is String }
command EscalateReview is { orderId is String }
result CartInfo is { id is String, total is Natural }
outlet CartEvents is event ItemAdded
type StatementEvent is LoginSucceeded | OrderShipped
outlet Events is type StatementEvent
outlet Shipments is event LineShipped
entity OrderProcessor is { ??? }
entity Review is { ??? }
entity PaymentService is { ??? }
entity Order is {
  state Shipped of record ShippedData is {
    handler ShippedHandler is { ??? }
  }
}
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
| `foreach` | Bounded iteration over a collection | `foreach line in field lines { ... }` |
| `send` | Emit a message on one of this processor's outlets | `send event X to outlet Events` |
| `tell` | Deliver a message directly to a processor, or to one **instance** | `tell command X to entity Y` · `tell command X to order.id` |
| `forward` | Pass the handled message on, **discharging** its response obligation | `forward ord to entity Payments` |
| `yield` | Produce a command's declared **event** | `yield event Placed(id)` |
| `reply` | Answer a query with its declared **result** | `reply result Info(id)` |
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
| `terminate` | End this instance's life | `terminate self.id` |

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
| Ask | `ask query GetInfo of entity Catalog` | A query paired with the reply that answers it |
| Prompt | `prompt("compute the discount")` | A value computed by AI at generation time |
| Boolean | `a > b and not c` | A structured boolean expression |

### Constructors

A constructor builds a [message](message.md) or record inline. Arguments are
positional first, then named, and are checked against the target's fields for
count, name, order and (best effort) type:

<!-- riddl: in-yielding-handler -->
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
    constant MaxItems is Natural = 100
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

<!-- riddl: in-handler -->
```riddl
when order.isPaid and not order.isCancelled then {
  send event LoginSucceeded(who = "the signed-in user") to outlet Events
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

<!-- riddl: in-handler -->
```riddl
match order.status {
  case Pending {
    tell command ProcessOrder(orderId) to entity OrderProcessor
  }
  case InTransit when order.isPaid {
    send event OrderShipped(orderId) to outlet Events
  }
  default {
    error "Unknown order status"
  }
}
```

A **comparison** case compares the subject against a constant, so it needs a
subject the operator accepts — an ordered numeric type for `>=`, not the status
above:

<!-- riddl: in-handler -->
```riddl
match order.total {
  case >= HighValueThreshold {
    tell command EscalateReview(orderId) to entity Review
  }
  default {
    do "handle an ordinary order"
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

<!-- riddl: in-handler -->
```riddl
foreach line in field order.lines {
  send event LineShipped(sku = line.sku) to outlet Shipments
}
```

The collection is a `field` reference or a `let`-bound local whose type
resolves to a collection: Sequence, Set, Graph, Table, Replica, Mapping, or a
cardinality wrapper such as `many` or `optional`. Any path that lands on a
collection will do — the field need not be a direct field of the state, as
`order.lines` above shows.

**The element is bound over the loop body**, and it carries the element's
*type*, not merely its name: `line.sku` resolves, while `line.nosuch` is an
Error. The binding ends at the closing brace, so referring to it after the
loop is an Error too.

#### Destructuring a mapping

A mapping has two halves, so iterating one binds **two** names — a key and a
value:

<!-- riddl: in-handler -->
```riddl
foreach sku, price in field order.prices {
  send event LineShipped(sku = sku) to outlet Shipments
}
```

The arity is checked both ways, and each mistake has its own message:

- one name over a mapping — *"binds a key AND a value, so it needs two names"*
- two names over anything else — *"binds a second name only over a mapping"*

### Send, Tell, Yield and Reply

- **send** — emit on one of *this* processor's own [outlets](outlet.md); a
  [connector](connector.md) routes it onward
- **tell** — deliver directly to a specific processor (point-to-point)
- **yield** — produce a **command's** declared event, without needing to know
  the sender's identity
- **reply** — answer a **query** with its declared result

<!-- riddl: in-clauses -->
```riddl
on add: command AddItem {
  send event ItemAdded(sku = add.sku) to outlet CartEvents
  tell command ProcessPayment(orderId = add.sku) to entity PaymentService
  yield event ItemAdded(sku = add.sku)   // AddItem's declared event
}
```

`reply` is the query half of the same idea:

<!-- riddl: in-clauses -->
```riddl
on cart: query GetCart {
  reply result CartInfo(id = cart.id, total = 1)   // GetCart's declared result
}
```

#### Forward

- **forward** — hand the handled message onward and **discharge** its response
  obligation, because whatever handles it downstream produces the answer

A command declaring `yields event E` obliges *every* handler of it to produce an
`E`. A boundary handler that only passes the command along produces nothing, and
before `forward` existed it had no way to say so:

<!-- riddl: in-clauses -->
```riddl
on add: command AddItem {
  forward add to entity PaymentService
}
```

It takes both transmission shapes — `to outlet ...` like `send`, or
`to entity ...` like `tell`. It is legal only in a clause handling a command
that declares `yields` or a query that declares `replies`; an **event** or a
**result** answers nothing, so neither can be forwarded. Because the response
has been delegated, a `yield` or `reply` after a `forward` is an **Error**.

!!! info "What settles a path"
    Only `yield`/`reply`, `error`/`require`, and `forward` discharge a response
    obligation. A `send` of the handled message does **not**, even to an outlet
    that admits it.

!!! warning "`send … to inlet` is deprecated"
    Sending directly into another processor's inlet bypasses the streaming
    model — that is `tell`'s job. The inlet form still parses and emits a
    `[deprecated]` message.

!!! warning "Changed in RIDDL 2.0: `reply` is no longer deprecated"
    `reply` used to be a deprecated synonym for `yield`. It is now a statement
    in its own right: a command handler `yield`s its declared **event**, and a
    query handler `reply`s its declared **result**. The wrong pairing —
    `yield result` or `reply event` — is an Error.

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

<!-- riddl: in-handler -->
```riddl
require amount > Zero
require invariant BalanceNonNegative
require invariant UnderLimit with limits
error "Price must be greater than zero"
```

`error` **ends its statement list.** It refuses unconditionally, so anything
after it is unreachable and is an **Error**. `require` is deliberately *not*
terminal — it refuses only when its condition fails, so later statements are
ordinary. `terminate` ends a list for the other reason: the instance is gone.
An `on term` clause is unaffected; it runs *because* of the termination.

A `require invariant` is an explicit **restatement** — an
[invariant](invariant.md) already applies implicitly across its declaring
scope. The `with <value>` form is the exception that does real work: it hands a
value to an invariant declaring `requires <type>`, which is the one form
ambient scope cannot supply.

!!! warning "Refusals before effects"
    Within any single linear statement list, every **refusal** (`require`,
    `error`) must appear before every **effect** — and an "effect" here is a
    change to **this definition's own state**: `set`, `morph` and `terminate`.
    Acting and then refusing would leave a partial change behind.

    `send`, `tell` and `yield` are **transmissions**, not local changes: any
    state they cause is elsewhere and later. `become` changes behaviour rather
    than state, and `put` writes to an [output](output.md). None of them can
    leave this definition half-changed, so none has to wait for the refusals —
    which is what makes "refuse **and** publish a rejection event" expressible.

    Each statement list is checked independently, so each branch of a `when`,
    `match` or `foreach` body is its own list. A refusal after an effect in the
    same list is an **Error**.

    <!-- riddl: in-clauses -->
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

<!-- riddl: in-handler -->
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
| All handlers | when, match, foreach, send, tell, yield, reply, require, set, let, do, error, code |
| Entity handlers | All above + morph, become |
| Application-context handlers | All above + put |
| Functions | when, match, foreach, require, let, return, do, error, code |
| `on activate` / `on passivate` | Side-effect free only — no send, tell, yield, reply, morph, become |
| `on event` | No require or error — an event has happened and must be accepted |
| Saga steps | when, match, foreach, send, tell, require, let, do, error, code |

The function and lifecycle bans are enforced at **parse** time, so a banned
statement can never enter the AST at all.

!!! warning "A saga step is not a handler"
    `yield` and `reply` are **not** available in a saga step — a step is not
    answering a message, so it has no sender to answer. Neither are `morph` and
    `become`, which belong to an entity, nor `put`, which is rejected in a step
    even inside an `application` context because it is handler-only.

    A step *may* use `call` inside a `let` — which is what the
    [one-failure-point rule](saga.md) counts when it says
    `let x = call F(get from input I)` is two failure points.

## Deprecated Statements

| Deprecated | Replacement |
|------------|-------------|
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
