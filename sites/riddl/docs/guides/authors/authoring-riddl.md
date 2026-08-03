# Authoring RIDDL Sources

<!-- riddl-prelude
  entity Cart is { ??? }
  entity Order is { ??? }
  entity Account is { ??? }
  entity Product is { ??? }
  entity Customer is { ??? }
  type ProductId is Id(Product)
  type Money is Currency(USD)
  record CartItem is { product: ProductId, quantity: Natural }
  record Transaction is { amount: Money, at: TimeStamp }
  command PlaceOrder is { cartId: Id(Cart) }
  command AddItemToCart is { cartId: Id(Cart), quantity: Natural }
  command RemoveItemFromCart is { cartId: Id(Cart) }
  command Deposit is { amount: Money }
  command Withdraw is { amount: Money }
  event ItemAddedToCart is { cartId: Id(Cart), quantity: Natural }
  event MoneyDeposited is { amount: Money }
  event MoneyWithdrawn is { amount: Money }
  event OrderCompleted is { orderId: Id(Order) }
  event OrderFailed is { orderId: Id(Order), reason: String }
-->


This guide provides helpful tips and techniques for writing RIDDL source files
effectively, regardless of which IDE or editor you use.

## File Organization

### File Extension

All RIDDL source files use the `.riddl` extension. Both the IntelliJ plugin
and VS Code extension recognize this extension automatically.

### Structuring Your Model

RIDDL models typically follow a hierarchical structure:

<!-- riddl: skip reason="illustrates file organisation; the included paths do not exist" -->
```riddl
// Main domain file: myproject.riddl
domain MyProject is {
  include "contexts/orders.riddl"
  include "contexts/inventory.riddl"
  include "types/common-types.riddl"
}
```

**Best Practices:**

- Use a single top-level `.riddl` file as the entry point
- Organize contexts into separate files using `include` directives
- Keep shared types in a common types file
- Use descriptive file names that match the definitions they contain

### Include Directives

The `include` directive brings in content from other files:

<!-- riddl: skip reason="illustrates file organisation; the included paths do not exist" -->
```riddl
include "path/to/file.riddl"       // Relative path
include "types/*.riddl"            // Glob pattern for multiple files
```

!!! tip "Relative Paths"
    Paths in `include` directives are relative to the file containing the
    include statement, not the project root.

---

## Adding Metadata with `with`

Every RIDDL definition can have metadata attached using the `with` clause.
This metadata provides important context about the definition.

### Author Information

Always identify who created or maintains a definition:

<!-- riddl: standalone -->
```riddl
domain Ordering is {
  author Reid is {
    name is "Reid Spencer"
    email is "reid@ossuminc.com"
  }
  // domain contents
}
```

### Multiple Authors

For collaborative definitions, list all contributors:

<!-- riddl: standalone -->
```riddl
domain Ordering is {
  author Reid is {
    name is "Reid Spencer"
    email is "reid@ossuminc.com"
  }
  author James is {
    name is "James Lovett"
    email is "james@ossuminc.com"
  }

  context Payments is {
    // context contents
  } with {
    by author Reid
    by author James
  }
}
```

### Terms (Glossary)

Define domain-specific terminology:

<!-- riddl: standalone -->
```riddl
domain ECommerce is {
  // domain contents
} with {
  term SKU is {
    |Stock Keeping Unit - unique product identifier
  }
  term Cart is {
    |Collection of items a customer intends to purchase
  }
}
```

### Brief Descriptions

Add a one-line description to any definition:

<!-- riddl: in-context no-prelude=Cart -->
```riddl
entity Cart is {
  // entity contents
} with {
  brief "Shopping cart holding items for purchase"
}
```

### Full Documentation

For detailed documentation, use the `described by` clause with markdown:

<!-- riddl: in-domain -->
```riddl
context OrderFulfillment is {
  // context contents
} with {
  brief "Handles order processing and fulfillment"
  described by {
    |## Order Fulfillment Context
    |
    |This bounded context manages the complete order lifecycle:
    |
    |* Order validation and acceptance
    |* Payment processing coordination
    |* Inventory reservation
    |* Shipping coordination
    |
    |### Key Workflows
    |
    |1. **Order Placement** - Customer submits order
    |2. **Payment Capture** - Funds are secured
    |3. **Fulfillment** - Items are picked and shipped
  }
}
```

!!! note "Markdown Lines"
    Lines starting with `|` are treated as markdown documentation.
    The pipe character is stripped, and the remaining content is processed
    as markdown when generating documentation.

---

## Type Definitions

### Predefined Types

RIDDL provides many built-in types:

| Category | Types |
|----------|-------|
| **Text** | `String`, `String(min,max)`, `Pattern("regex")` |
| **Numbers** | `Integer`, `Natural`, `Whole`, `Number`, `Real`, `Decimal(w,f)` |
| **Measures** | `Current`, `Length`, `Luminosity`, `Mass`, `Mole`, `Temperature` |
| **Temporal** | `Date`, `Time`, `DateTime`, `TimeStamp`, `Duration` |
| **Zoned** | `ZonedDate(zone)`, `ZonedDateTime(zone)` |
| **Logical** | `Boolean`, `Nothing`, `Anything` |
| **Identity** | `Id(Entity)`, `UUID`, `UserId`, `URL` |
| **Currency** | `Currency(USD)` |
| **Other** | `Location` |

!!! warning "`TimeStamp` has a capital S"
    It is the one predefined type whose spelling regularly catches people
    out. `Timestamp` does not resolve.

Collections are **not** predefined type names — they are type *expressions*
built with keywords, so there is no `List`, `Set` or `Map` to reference:

| Form | Meaning |
|------|---------|
| `many CartItem` | one or more |
| `many optional CartItem` | zero or more |
| `optional CartItem` | zero or one |
| `sequence of CartItem` | an ordered sequence |
| `set of CartItem` | an unordered set with no duplicates |
| `mapping from ProductId to CartItem` | a key-to-value mapping |
| `range(1,10)` | a bounded integer range |

!!! note "`Abstract` is deprecated"
    It still parses, but as the old spelling of `Anything`, and the compiler
    emits a `[deprecated]` message. Use `Anything`.

### Custom Types

Define domain-specific types:

<!-- riddl: in-context -->
```riddl
// Simple type alias
type OrderId is Id(Order)

// Enumeration
type OrderStatus is any of { Pending, Confirmed, Shipped, Delivered, Cancelled }

// Aggregation (record)
type Address is {
  street: String,
  city: String,
  state: String,
  postalCode: Pattern("\\d{5}(-\\d{4})?"),
  country: String
}

// Enumeration
type PaymentMethod is any of {
  CreditCard, DebitCard, BankTransfer, DigitalWallet
}
```

### Type References

Reference types defined elsewhere:

<!-- riddl: in-context -->
```riddl
type LineItem is {
  product: ProductId,          // Reference to Id type
  quantity: Natural,           // Positive integer
  unitPrice: Money             // Currency amount
}
```

---

## Messages: Commands, Events, Queries, and Results

### Commands (Requests for Action)

Commands represent requests that may change state:

<!-- riddl: in-context no-prelude=AddItemToCart -->
```riddl
command AddItemToCart is {
  cartId: Id(Cart),
  productId: Id(Product),
  quantity: Natural
}
```

### Events (Facts That Occurred)

Events record things that happened:

<!-- riddl: in-context no-prelude=ItemAddedToCart -->
```riddl
event ItemAddedToCart is {
  cartId: Id(Cart),
  productId: Id(Product),
  quantity: Natural,
  addedAt: TimeStamp
}
```

### Queries (Information Requests)

Queries request data without side effects:

<!-- riddl: in-context -->
```riddl
query GetCartContents is {
  cartId: Id(Cart)
}
```

### Results (Query Responses)

Results return data from queries:

<!-- riddl: in-context -->
```riddl
result CartContents is {
  cartId: Id(Cart),
  items: sequence of CartItem,
  total: Money
}
```

---

## Entity Design

### Basic Entity Structure

<!-- riddl: in-context no-prelude=Cart -->
```riddl
aggregate entity Cart is {
  // Identity
  type CartId is Id(Cart)

  // State
  record State is {
    id: CartId,
    customerId: Id(Customer),
    items: sequence of CartItem,
    createdAt: TimeStamp,
    updatedAt: TimeStamp
  }

  // Commands it handles
  handler Commands is {
    on command AddItemToCart {
      // implementation pseudocode
    }
    on command RemoveItemFromCart {
      // implementation pseudocode
    }
  }

  // Events it produces
  handler Events is {
    on event ItemAddedToCart {
      // state update logic
    }
  }
}
```

### Entity Intentions

An entity's semantics are declared as keywords **before** `entity`, not as
options in `with { }`. They change what the model *means*, and one of them —
`event-sourced` — decides whether it is even legal, so they are part of the
declaration rather than advice to a generator.

<!-- riddl: in-context no-prelude=Order -->
```riddl
aggregate consistent event-sourced entity Order is { ??? }
```

There are three independent groups. Within a group the keywords are mutually
exclusive; across groups you may take one of each, in any order.

| Group | Keywords | Meaning |
|---|---|---|
| Role | `aggregate` | The entity is an aggregate root |
| Consistency | `consistent` / `available` | Which side of CAP the entity favours |
| Persistence | `event-sourced` / `persistent` / `transient` | How its state survives |

`event-sourced` implies `persistent`, so the two are never written together.
`transient` means the state is not persisted at all.

!!! warning "These used to be options"
    `option is event-sourced` and friends still parse, but emit a
    `[deprecated]` message and will be removed in RIDDL 3.0. Note also that
    `persistent` was previously spelled `value`.

Choosing `event-sourced` brings four rules with it — see
[Event Sourcing Rules](#event-sourcing-rules) below.

`finite-state-machine` is a genuine option and stays in `with { }`; it is not
an intention.

### Event Sourcing Rules

Replay rebuilds an entity's state by re-applying its recorded events in order,
so the *same* state changes must happen again. That is only possible if the
model is shaped for it, and RIDDL now checks four things. All four are Errors,
and all four apply only when the entity is `event-sourced`.

1. **Every handled command declares what it yields.** Write it on the command's
   type, between the name and `is` — otherwise there is nothing to record.

    <!-- riddl: in-context -->
    ```riddl
    event Placed is { total: Integer }
    command Place yields event Placed is { total: Integer }
    ```

2. **Every event named by such a `yields` has an `on event` clause**, so replay
   has something to apply.

3. **`set`, `morph` and `become` appear only in `on event` clauses.** There is
   no exemption for `on init`: an initial state must come from an event like
   any other change. Commands *decide*; events *apply*.

4. **A foreign event may not change state.** An event declared outside the
   entity must first be turned into one of the entity's own:

    <!-- riddl: skip reason="two clauses from different handlers, shown to contrast rule 4" -->
    ```riddl
    on event Sales.PaymentTaken { yield event Order.Placed }
    on event Order.Placed { set field Main.total to "1" }
    ```

Together these give the shape every event-sourced entity takes: the command
handler validates and yields, and the event handler performs the change.

<!-- riddl: in-context no-prelude=Order -->
```riddl
event-sourced entity Order is {
  record Fields is { total: Integer }
  command Place yields event Placed is { total: Integer }
  event Placed is { total: Integer }

  state Main of record Order.Fields is {
    handler Behavior is {
      on command Order.Place { yield event Order.Placed }
      on event Order.Placed { set field Main.total to "1" }
    }
  }
}
```

!!! tip "Declare the events inside the entity"
    Rule 4 makes ownership matter: only the entity's *own* events may change
    its state. Declaring commands and events inside the entity that uses them
    is the simplest way to satisfy it.

#### Refusing a command

`yields` says what a command records **when it succeeds** — not that every
clause mentioning it must record something. A clause that *refuses* the command
discharges the contract by declining, so it need not yield:

<!-- riddl: in-context no-prelude=Account,Withdraw -->
```riddl
event-sourced entity Account is {
  record Fields is { balance: Integer }
  command Withdraw yields event Withdrawn is { amount: Integer }
  event Withdrawn is { amount: Integer }

  state Main of record Account.Fields is {
    handler H is {
      on command Account.Withdraw {
        when prompt("sufficient funds") then {
          yield event Account.Withdrawn
        } else {
          error "Insufficient funds"
        } end
      }
      on event Account.Withdrawn {
        set field Main.balance to "balance - amount"
      }
    }
  }
}
```

This is the ordinary shape of a command accepted in one state and refused in
others, and without the exemption it would be inexpressible: every refusing
clause would have to yield the success event, recording a state change it had
just declined to make.

Both `error` and `require` count as refusals. A refusing clause that yields the
*wrong* event is still an error — the exemption excuses silence, not a
mismatch.

---

## Handler Statements

Handlers use pseudocode statements to describe behavior:

### Common Statements

<!-- riddl: in-context -->
```riddl
handler OrderCommands is {
  on command PlaceOrder {
    // Create a local value
    let orderId = "new OrderId"

    // Validate with conditional
    when prompt("inventory is available") then {
      // Produce an event
      send event OrderPlaced to outlet Events
      // Update state
      set field State.status to "Confirmed"
    } else {
      // Return an error
      error "Insufficient inventory for order"
    } end

    // Describe an action the implementation must perform
    do "Record that order {orderId} was processed"
  }
}
```

### Statement Reference

| Statement | Purpose | Example |
|-----------|---------|---------|
| `let` | Create local value | `let x = "expression"` |
| `set` | Update state field | `set field State.name to "value"` |
| `send` | Emit message | `send event X to outlet Y` |
| `tell` | Send a message to a processor | `tell command X to context Y` |
| `do` | Describe an action in prose | `do "recompute the totals"` |
| `error` | Signal error | `error "error message"` |
| `when/then/else/end` | Conditional | `when prompt("condition") then { } else { } end` |
| `morph` | Transform state | `morph entity X to state Y` |
| `become` | Change handler | `become handler NewHandler` |
| `return` | Return value | `return "result expression"` |

---

## Comments and Documentation

### Line Comments

<!-- riddl: standalone -->
```riddl
// This is a single-line comment
domain Example is {
  // Comments can appear anywhere
}
```

### Block Comments

<!-- riddl: standalone -->
```riddl
/* This is a block comment
   that spans multiple lines */
```

### Documentation Strings

Use markdown lines for rich documentation:

<!-- riddl: in-context no-prelude=Order -->
```riddl
entity Order is {
  // entity definition continues
} with {
  described by {
    |## Order Entity
    |
    |Represents a customer order in the system.
    |
    |### Lifecycle
    |
    |1. Created when customer checks out
    |2. Confirmed after payment
    |3. Shipped when inventory allocated
    |4. Completed on delivery
  }
}
```

---

## Common Patterns

### Aggregate with Event Sourcing

<!-- riddl: in-context no-prelude=Account -->
```riddl
aggregate entity Account is {
  type AccountId is Id(Account)

  record State is {
    id: AccountId,
    balance: Money,
    transactions: sequence of Transaction
  }

  handler Commands is {
    on command Deposit {
      when prompt("amount is positive") then {
        send event MoneyDeposited to outlet Events
      } end
    }
    on command Withdraw {
      when prompt("balance >= amount") then {
        send event MoneyWithdrawn to outlet Events
      } else {
        error "Insufficient funds"
      } end
    }
  }

  handler Projections is {
    on event MoneyDeposited {
      set field State.balance to "balance + amount"
    }
    on event MoneyWithdrawn {
      set field State.balance to "balance - amount"
    }
  }
}
```

### Saga for Distributed Transactions

<!-- riddl: in-context -->
```riddl
saga OrderSaga is {
  requires command PlaceOrder
  returns event OrderCompleted

  step ReserveInventory is {
    // reserve inventory
  } reverted by {
    // release inventory on failure
  }

  step ProcessPayment is {
    // charge payment
  } reverted by {
    // refund payment on failure
  }

  step ConfirmOrder is {
    // finalize order
  } reverted by {
    // mark the order cancelled
  }
}
```

---

## Validation Tips

Both IDE tools validate your RIDDL as you type. Common validation messages:

| Message | Cause | Fix |
|---------|-------|-----|
| "Undefined reference" | Referenced type/entity not defined | Add definition or check spelling |
| "Empty handler" | Handler has no `on` clauses | Add message handlers |
| "Missing brief" | Definition lacks description | Add `brief "description"` in `with` |
| "Unused definition" | Definition never referenced | Remove or add references |

!!! tip "Incremental Development"
    When building models incrementally, use the "Validate Partial" feature
    (available via MCP tools) to ignore undefined references temporarily.

---

## Keyboard Shortcuts Summary

See the specific IDE documentation for shortcuts:

- [IntelliJ Plugin Shortcuts](/ide-help/intellij-plugin/#tool-window-actions)
- [VS Code Extension Shortcuts](/ide-help/vscode-extension/#keyboard-shortcuts)

---

## Further Reading

- [RIDDL Language Reference](../../references/language-reference.md)
- [EBNF Grammar](../../references/ebnf-grammar.md)
- [Concept Guide](../../concepts/index.md)