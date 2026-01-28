---
title: "Author's Guide"
description: "A comprehensive guide for authoring RIDDL models"
draft: false
weight: 5
---

# Author's Guide

This guide is for those who author RIDDL models. Authors are typically domain
experts who understand the business domain being modeled and collaborate with
AI assistants to express that understanding in RIDDL syntax. You don't need to
be a programmer to author RIDDL models, but you do need to understand your
domain deeply and be willing to learn RIDDL's concepts and conventions. A 
familiarity with Domain-Driven Design (DDD) and distributed system architecture
is helpful. 

## What is an Author?

An author in the RIDDL ecosystem is someone who:

- **Understands the domain**: You have deep knowledge of the business area,
  processes, and terminology being modeled
- **Expresses intent**: You describe what the system should do, not how it
  should be implemented
- **Collaborates with AI**: You work with AI assistants (like the Ossum MCP
  Service) that help translate your domain knowledge into valid RIDDL syntax
- **Iterates on models**: You refine the model based on validation feedback
  and stakeholder input
- **Defines Simulation Models**: You define scenarios for the simulator to
  specify scenarios to simulate for testing and validation

Authors bridge the gap between domain expertise and formal specification.

## Prerequisites

Before you begin authoring RIDDL models, ensure you have:

1. **Domain Knowledge**: Expertise in the business area you're modeling
2. **Access to Tools**:
   - An IDE with RIDDL support (VS Code, IntelliJ IDEA), or Synapify
   - An AI assistant configured with the Ossum MCP Service
3. **Conceptual Understanding**: Familiarity with the RIDDL
   [concepts](../../concepts/index.md) section

## The Authoring Workflow

### Step 1: Define Your Domain

Start by identifying the knowledge domain you're modeling. A domain in RIDDL
represents a bounded area of knowledge or business function. Ask yourself:

- What is the scope of this system?
- What major business capabilities does it support?
- What terminology do experts in this area use?

```riddl
domain OnlineRetail is {
  // This domain covers e-commerce operations including
  // product catalog, shopping cart, and order fulfillment
} with {
  briefly "E-commerce operations for retail sales"
  described as {
    |The OnlineRetail domain encompasses all aspects of selling
    |products to consumers through digital channels. This includes
    |browsing products, managing shopping carts, placing orders,
    |and tracking fulfillment.
  }
}
```

!!! tip "Start with Description"
    Always begin with clear descriptions. The `briefly` and `described as`
    clauses help both humans and AI understand what you're modeling.

### Step 2: Identify Bounded Contexts

Within your domain, identify distinct bounded contexts. A context in RIDDL
corresponds to the Domain-Driven Design concept of a
[bounded context](https://martinfowler.com/bliki/BoundedContext.html)—a
self-contained area with its own ubiquitous language.

Consider these questions:
- What are the major subsystems or capabilities?
- Where do terms have different meanings?
- What could be developed or deployed independently?

```riddl
domain OnlineRetail is {
  context Catalog is {
    // Product information and browsing
  } with {
    briefly "Product catalog and browsing experience"
  }

  context Shopping is {
    // Cart management and checkout
  } with {
    briefly "Shopping cart and checkout process"
  }

  context Fulfillment is {
    // Order processing and delivery
  } with {
    briefly "Order fulfillment and shipping"
  }
}
```

### Step 3: Define Your Types

Types define the shape of information in your model. Start with the core
concepts in your domain—the "nouns" of your ubiquitous language.

```riddl
context Catalog is {
  type ProductId is Id(Product) with {
    briefly "Unique identifier for a product"
  }

  type Money is {
    amount is Decimal(10,2),
    currency is Currency("USD")
  } with {
    briefly "Monetary amount with currency"
  }

  type Product is {
    id is ProductId,
    name is String(1,200),
    description is String,
    price is Money,
    category is CategoryId,
    images is URL+
  } with {
    briefly "A product available for purchase"
  }
}
```

### Step 4: Define Entities

Entities are the heart of your model. They represent things with identity
that persist over time and respond to messages. Each entity should model
a single business concept.

```riddl
context Catalog is {
  entity Product is {
    option aggregate
    option event-sourced

    // Commands - requests to change state
    command CreateProduct is {
      name is String,
      description is String,
      price is Money,
      category is CategoryId
    }

    command UpdatePrice is {
      productId is ProductId,
      newPrice is Money
    }

    // Events - things that happened
    event ProductCreated is {
      id is ProductId,
      name is String,
      price is Money,
      at is TimeStamp
    }

    event PriceUpdated is {
      productId is ProductId,
      oldPrice is Money,
      newPrice is Money,
      at is TimeStamp
    }

    // State - what the entity remembers
    state Active is {
      fields {
        info is Product
      }
      handler ActiveHandler is {
        on command UpdatePrice {
          if "price is different from current" then {
            set field info.price to @UpdatePrice.newPrice
            send event PriceUpdated to outlet Events
          }
        }
      }
    }
  } with {
    briefly "A product in the catalog"
  }
}
```

### Step 5: Define Handlers and Behavior

Handlers specify what happens when messages are received. They contain
on clauses that match message types and execute statements.

```riddl
handler CartHandler is {
  on command AddItem {
    if "item not already in cart" then {
      "add the item to the cart with quantity 1"
    } else {
      "increment the quantity of the existing item"
    }
    send event ItemAdded to outlet Events
  }

  on command RemoveItem {
    if "item exists in cart" then {
      "remove the item from the cart"
      send event ItemRemoved to outlet Events
    } else {
      error "Item not found in cart"
    }
  }

  on query GetCartContents {
    reply result CartContents with { items: @fields.items }
  }
} with {
  briefly "Handles shopping cart operations"
}
```

!!! note "Pseudocode in Handlers"
    RIDDL handlers use pseudocode (text in quotes) for logic that will be
    implemented later. Focus on expressing *what* should happen, not *how*
    to implement it. The goal is clarity for human readers and AI code
    generators. There is even a `prompt` pseudocode keyword that allows you
    to ask AI for help.

### Step 6: Define User Stories with Epics

Epics describe how users interact with your system. They help validate that
your model supports required use cases.

```riddl
domain OnlineRetail is {
  user Customer is {
    briefly "A person shopping on the website"
  }

  epic BrowseAndPurchase is {
    user Customer wants to "find and buy products"
    so that "they can receive goods they need"

    case BrowseProducts is {
      user Customer "opens the product catalog"
      then user Customer "searches for a product"
      then Catalog.Product "returns matching products"
      then user Customer "views product details"
    }

    case AddToCart is {
      user Customer "selects a product to purchase"
      then Shopping.Cart "adds the item"
      then Shopping.Cart "confirms item added"
    }
  } with {
    briefly "Customer browses catalog and makes purchases"
  }
}
```

## Working with AI Assistants

The Ossum MCP Service provides AI assistants with RIDDL language
intelligence. Here's how to work effectively with AI assistance:

### Describe Your Intent Clearly

When asking AI for help, describe:
- What business concept you're modeling
- What behavior you expect
- Any constraints or requirements

**Example prompt:**
> "I need to model a shopping cart entity that tracks items a customer wants
> to purchase. Items can be added, removed, or have their quantities changed.
> The cart should calculate totals and apply any discount codes."

### Review and Refine

AI-generated RIDDL should be reviewed for:
- **Correctness**: Does it match your domain understanding?
- **Completeness**: Are all necessary commands, events, and states present?
- **Consistency**: Does it follow conventions used elsewhere in your model?

### Iterate Based on Validation

Use `riddlc` to validate your model after each change:

```bash
riddlc validate mymodel.riddl
```

Address any warnings or errors, and ask AI for help understanding
validation messages.

## Best Practices

### Naming Conventions

- **Domains**: PascalCase nouns (`OnlineRetail`, `HealthcareManagement`)
- **Contexts**: PascalCase nouns (`Catalog`, `Shopping`, `Fulfillment`)
- **Entities**: PascalCase singular nouns (`Product`, `Cart`, `Order`)
- **Commands**: PascalCase verb phrases (`CreateProduct`, `AddItem`)
- **Events**: PascalCase past-tense verbs (`ProductCreated`, `ItemAdded`)
- **Queries**: PascalCase questions (`GetCartContents`, `FindProducts`)
- **Types**: PascalCase nouns (`Money`, `Address`, `ProductId`)

### Documentation

Every definition should have at least a `briefly` clause. Important
definitions should also have full `described as` blocks:

```riddl
entity Order is {
  // ... entity contents ...
} with {
  briefly "A customer's purchase order"
  described as {
    |An Order represents a customer's commitment to purchase one or
    |more products. Orders progress through states from Created to
    |either Fulfilled or Cancelled.
    |
    |## Lifecycle
    |1. Created - Order placed, awaiting payment
    |2. Paid - Payment confirmed, ready for fulfillment
    |3. Fulfilled - Items shipped to customer
    |4. Cancelled - Order cancelled before fulfillment
  }
}
```

### Organization with Includes

For large models, split content across multiple files:

```riddl
// main.riddl
domain OnlineRetail is {
  include "catalog.riddl"
  include "shopping.riddl"
  include "fulfillment.riddl"
}
```

```riddl
// catalog.riddl
context Catalog is {
  // All catalog-related definitions
}
```

### Define Terms

Use the `term` definition to establish your ubiquitous language:

```riddl
context Shopping is {
  term SKU is {
    briefly "Stock Keeping Unit"
    described as {
      |A unique identifier for a product variant. Each SKU represents
      |a specific combination of product attributes (size, color, etc.).
    }
  }

  term Abandonment is {
    briefly "When a customer leaves without completing purchase"
    described as {
      |Cart abandonment occurs when a customer adds items to their
      |cart but exits without completing the checkout process.
    }
  }
}
```

### Use Placeholder Syntax

When you know something needs to be defined but aren't ready to detail it:

```riddl
entity Product is {
  ??? // TODO: Define product entity
}
```

Or for partially complete definitions:

```riddl
handler OrderHandler is {
  on command CreateOrder {
    ???  // Implementation pending
  }

  on command CancelOrder {
    "validate order can be cancelled"
    set field status to OrderStatus.Cancelled
    send event OrderCancelled to outlet Events
  }
}
```

## Common Patterns

### Command-Event Pattern

Commands request changes; events record that changes happened:

```riddl
entity Account is {
  command Deposit is { amount is Money }
  command Withdraw is { amount is Money }

  event Deposited is { amount is Money, balance is Money, at is TimeStamp }
  event Withdrawn is { amount is Money, balance is Money, at is TimeStamp }

  state Active is {
    fields { balance is Money }
    handler ActiveHandler is {
      on command Deposit {
        "add amount to balance"
        send event Deposited to outlet Events
      }
      on command Withdraw {
        if "sufficient balance" then {
          "subtract amount from balance"
          send event Withdrawn to outlet Events
        } else {
          error "Insufficient funds"
        }
      }
    }
  }
}
```

### State Machine Pattern

Entities can morph between states to model lifecycles:

```riddl
entity Order is {
  state Pending is {
    handler PendingHandler is {
      on command ConfirmPayment {
        morph entity Order to state Paid
        send event PaymentConfirmed to outlet Events
      }
      on command Cancel {
        morph entity Order to state Cancelled
        send event OrderCancelled to outlet Events
      }
    }
  }

  state Paid is {
    handler PaidHandler is {
      on command Ship {
        morph entity Order to state Shipped
        send event OrderShipped to outlet Events
      }
    }
  }

  state Shipped is {
    // Final state - no transitions out
  }

  state Cancelled is {
    // Final state - no transitions out
  }
}
```

### Saga Pattern

For multi-step processes that need compensation on failure:

```riddl
saga PlaceOrder is {
  input is { cartId is CartId, paymentMethod is PaymentInfo }

  step ReserveInventory is {
    send command ReserveItems to context Inventory
    briefly "Reserve items in warehouse"
    reverted by {
      send command ReleaseReservation to context Inventory
    }
  }

  step ChargePayment is {
    send command ProcessPayment to context Payments
    briefly "Charge customer's payment method"
    reverted by {
      send command RefundPayment to context Payments
    }
  }

  step CreateOrder is {
    send command CreateOrder to entity Order
    briefly "Create the order record"
    reverted by {
      send command CancelOrder to entity Order
    }
  }
} with {
  briefly "Orchestrates the order placement process"
  described as {
    |This saga coordinates placing an order across multiple contexts.
    |If any step fails, previous steps are compensated in reverse order.
  }
}
```

## Validation and Iteration

### Running the Compiler

Always validate your model with `riddlc`:

```bash
# Basic validation
riddlc validate mymodel.riddl

# Verbose output for debugging
riddlc --verbose validate mymodel.riddl
```

Documentation generation will be available through [Synapify](../../../synapify/index.md).

### Common Validation Issues

| Issue | Cause | Solution |
|-------|-------|----------|
| "Undefined reference" | Using a type/entity not yet defined | Define the referenced item or check spelling |
| "Duplicate definition" | Same name used twice in same scope | Rename one definition |
| "Invalid containment" | Definition in wrong place | Check [hierarchy](../../concepts/index.md#hierarchy) |
| "Missing handler" | Entity has no way to process messages | Add handlers for commands/events |

### Iterating on Your Model

1. Start with a rough structure—domains and contexts
2. Add core types and entities
3. Define commands and events
4. Add handlers with pseudocode
5. Write epics to validate against use cases
6. Refine based on validation feedback
7. Add detailed descriptions and terms

## Next Steps

- Review the [Concepts](../../concepts/index.md) section for detailed
  information on each RIDDL definition type
- Consult the [Language Reference](../../references/language-reference.md)
  for syntax details
- Explore [example models](https://github.com/ossuminc/riddl/tree/main/examples)
  in the RIDDL repository
- Set up your development environment with
  [IDE support](../../tools/index.md)
