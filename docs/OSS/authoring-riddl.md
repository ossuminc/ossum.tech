# Authoring RIDDL Sources

This guide provides helpful tips and techniques for writing RIDDL source files
effectively, regardless of which IDE or editor you use.

## File Organization

### File Extension

All RIDDL source files use the `.riddl` extension. Both the IntelliJ plugin
and VS Code extension recognize this extension automatically.

### Structuring Your Model

RIDDL models typically follow a hierarchical structure:

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

```riddl
domain Ordering is {
  // domain contents
} with {
  author Reid is {
    name: "Reid Spencer"
    email: "reid@ossuminc.com"
  }
}
```

### Multiple Authors

For collaborative definitions, list all contributors:

```riddl
context Payments is {
  // context contents
} with {
  author Reid is {
    name: "Reid Spencer"
    email: "reid@ossuminc.com"
  }
  author James is {
    name: "James Lovett"
    email: "james@ossuminc.com"
  }
}
```

### Terms (Glossary)

Define domain-specific terminology:

```riddl
domain ECommerce is {
  // domain contents
} with {
  term "SKU" is described as "Stock Keeping Unit - unique product identifier"
  term "Cart" is described as "Collection of items a customer intends to purchase"
}
```

### Brief Descriptions

Add a one-line description to any definition:

```riddl
entity Cart is {
  // entity contents
} with {
  brief "Shopping cart holding items for purchase"
}
```

### Full Documentation

For detailed documentation, use the `described by` clause with markdown:

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
| **Text** | `String`, `Id`, `UUID`, `Pattern` |
| **Numbers** | `Integer`, `Number`, `Decimal`, `Natural`, `Whole`, `Real` |
| **Temporal** | `Date`, `Time`, `DateTime`, `Timestamp`, `Duration` |
| **Logical** | `Boolean`, `Nothing`, `Abstract` |
| **Collections** | `List`, `Set`, `Map`, `Sequence`, `Mapping` |
| **Ranges** | `Range` |
| **Binary** | `Blob`, `Length`, `Location` |
| **Currency** | `Currency`, `Money` |
| **Identity** | `UserId`, `UUID`, `URL` |

### Custom Types

Define domain-specific types:

```riddl
// Simple type alias
type OrderId is Id(Order)

// Enumeration
type OrderStatus is one of { Pending, Confirmed, Shipped, Delivered, Cancelled }

// Aggregation (record)
type Address is {
  street: String,
  city: String,
  state: String,
  postalCode: Pattern("\\d{5}(-\\d{4})?"),
  country: String
}

// Alternation (union)
type PaymentMethod is one of {
  CreditCard, DebitCard, BankTransfer, DigitalWallet
}
```

### Type References

Reference types defined elsewhere:

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

```riddl
command AddItemToCart is {
  cartId: Id(Cart),
  productId: Id(Product),
  quantity: Natural
}
```

### Events (Facts That Occurred)

Events record things that happened:

```riddl
event ItemAddedToCart is {
  cartId: Id(Cart),
  productId: Id(Product),
  quantity: Natural,
  addedAt: Timestamp
}
```

### Queries (Information Requests)

Queries request data without side effects:

```riddl
query GetCartContents is {
  cartId: Id(Cart)
}
```

### Results (Query Responses)

Results return data from queries:

```riddl
result CartContents is {
  cartId: Id(Cart),
  items: List of CartItem,
  total: Money
}
```

---

## Entity Design

### Basic Entity Structure

```riddl
entity Cart is {
  option aggregate
  option event-sourced

  // Identity
  type CartId is Id(Cart)

  // State
  record State is {
    id: CartId,
    customerId: Id(Customer),
    items: List of CartItem,
    createdAt: Timestamp,
    updatedAt: Timestamp
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

### Entity Options

Common entity options:

| Option | Description |
|--------|-------------|
| `aggregate` | This entity is an aggregate root |
| `event-sourced` | State is reconstructed from event history |
| `transient` | Entity state is not persisted |
| `finite-state-machine` | Entity follows FSM pattern |

---

## Handler Statements

Handlers use pseudocode statements to describe behavior:

### Common Statements

```riddl
handler OrderCommands is {
  on command PlaceOrder {
    // Create a local value
    let orderId = "new OrderId"

    // Validate with conditional
    if "inventory is available" then {
      // Produce an event
      send event OrderPlaced to outlet Events
      // Update state
      set field State.status to OrderStatus.Confirmed
    } else {
      // Return an error
      error "Insufficient inventory for order"
    }

    // Log information
    tell "Order {orderId} processed"
  }
}
```

### Statement Reference

| Statement | Purpose | Example |
|-----------|---------|---------|
| `let` | Create local value | `let x = "expression"` |
| `set` | Update state field | `set field State.name to "value"` |
| `send` | Emit message | `send event X to outlet Y` |
| `tell` | Log/output info | `tell "message"` |
| `error` | Signal error | `error "error message"` |
| `if/then/else` | Conditional | `if "condition" then { } else { }` |
| `morph` | Transform state | `morph entity X to state Y` |
| `become` | Change handler | `become handler NewHandler` |
| `return` | Return value | `return "result expression"` |

---

## Comments and Documentation

### Line Comments

```riddl
// This is a single-line comment
domain Example is {
  // Comments can appear anywhere
}
```

### Block Comments

```riddl
/* This is a block comment
   that spans multiple lines */
```

### Documentation Strings

Use markdown lines for rich documentation:

```riddl
entity Order is {
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

  // entity definition continues
}
```

---

## Common Patterns

### Aggregate with Event Sourcing

```riddl
entity Account is {
  option aggregate
  option event-sourced

  type AccountId is Id(Account)

  record State is {
    id: AccountId,
    balance: Money,
    transactions: List of Transaction
  }

  handler Commands is {
    on command Deposit {
      if "amount is positive" then {
        send event MoneyDeposited to outlet Events
      }
    }
    on command Withdraw {
      if "balance >= amount" then {
        send event MoneyWithdrawn to outlet Events
      } else {
        error "Insufficient funds"
      }
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

```riddl
saga OrderSaga is {
  input command PlaceOrder
  output event OrderCompleted
  output event OrderFailed

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

- [IntelliJ Plugin Shortcuts](./intellij-plugin/index.md#tool-window-actions)
- [VS Code Extension Shortcuts](./vscode-extension/index.md#keyboard-shortcuts)

---

## Further Reading

- [RIDDL Language Reference](../riddl/references/language-reference.md)
- [EBNF Grammar](../riddl/references/ebnf-grammar.md)
- [Concept Guide](../riddl/concepts/index.md)