---
title: "5-Minute Quickstart"
description: >-
  Get started with RIDDL in 5 minutes. Build your first domain model with
  this hands-on tutorial.
---
# 5-Minute Quickstart

This tutorial takes you from zero to a working RIDDL model. By the end, you'll
have a simple e-commerce domain with a product catalog and shopping cart.

---

## Step 1: Create Your First Domain

A **domain** is a knowledge boundary. Start with a file called `shop.riddl`:

```riddl
domain OnlineShop is {
  // Your model goes here
} with {
  briefly "A simple e-commerce system"
}
```

The `with` clause adds metadata. `briefly` is a short description.

---

## Step 2: Add a Bounded Context

A **context** is a self-contained subsystem with its own terminology:

```riddl
domain OnlineShop is {
  context Catalog is {
    // Product management goes here
  } with {
    briefly "Product catalog and inventory"
  }
}
```

---

## Step 3: Define Types

Types describe your data. Here's a product:

```riddl
context Catalog is {
  type ProductId is Id(Product)

  type Product is {
    id is ProductId,
    name is String(1, 200),
    price is Decimal(10, 2),
    inStock is Boolean
  } with {
    briefly "A product available for purchase"
  }
}
```

`Id(Product)` creates a type-safe identifier. `String(1, 200)` is a string
between 1 and 200 characters.

---

## Step 4: Create an Entity

An **entity** is something with identity that persists and responds to
messages:

```riddl
context Catalog is {
  type ProductId is Id(Product)
  type Product is { ??? }  // defined above

  entity Product is {
    option event-sourced

    command CreateProduct is {
      name is String,
      price is Decimal(10, 2)
    }

    event ProductCreated is {
      id is ProductId,
      name is String,
      price is Decimal(10, 2),
      at is TimeStamp
    }

    state Active is {
      fields {
        info is Product
      }
      handler Main is {
        on command CreateProduct {
          "create the product with a new ID"
          send event ProductCreated to outlet Events
        }
      }
    }
  } with {
    briefly "A product in the catalog"
  }
}
```

Key concepts:

- **Commands** request changes (imperative: `CreateProduct`)
- **Events** record what happened (past tense: `ProductCreated`)
- **State** holds the entity's data
- **Handlers** define behavior when messages arrive

---

## Step 5: Add a Shopping Cart

Let's add another context for shopping:

```riddl
domain OnlineShop is {
  context Catalog is { ??? }  // from above

  context Shopping is {
    type CartId is Id(Cart)
    type CartItem is {
      productId is Catalog.ProductId,
      quantity is Integer,
      price is Decimal(10, 2)
    }

    entity Cart is {
      option event-sourced

      command AddItem is {
        productId is Catalog.ProductId,
        quantity is Integer
      }

      event ItemAdded is {
        cartId is CartId,
        productId is Catalog.ProductId,
        quantity is Integer,
        at is TimeStamp
      }

      query GetContents is { cartId is CartId }
      result CartContents is { items is CartItem* }

      state Active is {
        fields {
          items is CartItem*
        }
        handler Main is {
          on command AddItem {
            "add or update item in cart"
            send event ItemAdded to outlet Events
          }
          on query GetContents {
            reply result CartContents
          }
        }
      }
    }
  }
}
```

Note: `CartItem*` means a list of zero or more items. You can reference types
from other contexts with `Catalog.ProductId`.

---

## Complete Example

Here's the full model in one file:

```riddl
domain OnlineShop is {

  context Catalog is {
    type ProductId is Id(Product)
    type Product is {
      id is ProductId,
      name is String(1, 200),
      price is Decimal(10, 2),
      inStock is Boolean
    }

    entity Product is {
      option event-sourced

      command CreateProduct is {
        name is String,
        price is Decimal(10, 2)
      }

      event ProductCreated is {
        id is ProductId,
        name is String,
        price is Decimal(10, 2),
        at is TimeStamp
      }

      state Active is {
        fields { info is Product }
        handler Main is {
          on command CreateProduct {
            "create the product with a new ID"
            send event ProductCreated to outlet Events
          }
        }
      }
    }
  }

  context Shopping is {
    type CartId is Id(Cart)
    type CartItem is {
      productId is Catalog.ProductId,
      quantity is Integer,
      price is Decimal(10, 2)
    }

    entity Cart is {
      option event-sourced

      command AddItem is {
        productId is Catalog.ProductId,
        quantity is Integer
      }

      event ItemAdded is {
        cartId is CartId,
        productId is Catalog.ProductId,
        quantity is Integer,
        at is TimeStamp
      }

      query GetContents is { cartId is CartId }
      result CartContents is { items is CartItem* }

      state Active is {
        fields { items is CartItem* }
        handler Main is {
          on command AddItem {
            "add or update item in cart"
            send event ItemAdded to outlet Events
          }
          on query GetContents {
            reply result CartContents
          }
        }
      }
    }
  }

} with {
  briefly "A simple e-commerce system"
}
```

---

## Validate Your Model

Use the RIDDL compiler to check your model for errors.

**Install riddlc (macOS):**

```bash
brew install ossuminc/tap/riddlc
```

For other platforms, see the [installation guide](tools/riddlc/installation.md).

**Validate your model:**

```bash
riddlc validate shop.riddl
```

You can also get real-time validation in your editor with RIDDL IDE support:

- [VS Code Extension](../OSS/vscode-extension/index.md)
- [IntelliJ Plugin](../OSS/intellij-plugin/index.md)

---

## What's Next?

You've built a working RIDDL model! Here's where to go from here:

- **[Concepts](concepts/index.md)** - Deep dive into domains, contexts,
  entities, and more
- **[Author's Guide](guides/authors/index.md)** - Complete guide to writing
  RIDDL models
- **[Language Reference](references/language-reference.md)** - Full syntax
  and semantics
- **[Example Models](https://github.com/ossuminc/riddl-models)** - Real-world
  examples to learn from

---

## Quick Reference

| Concept | Purpose | Example |
|---------|---------|---------|
| `domain` | Knowledge boundary | `domain Shop is { ... }` |
| `context` | Bounded subsystem | `context Catalog is { ... }` |
| `type` | Data shape | `type Product is { name is String }` |
| `entity` | Stateful object | `entity Cart is { ... }` |
| `command` | Request to change | `command AddItem is { ... }` |
| `event` | Record of change | `event ItemAdded is { ... }` |
| `query` | Request for info | `query GetContents is { ... }` |
| `state` | Entity's data | `state Active is { fields { ... } }` |
| `handler` | Message behavior | `handler Main is { on command ... }` |
