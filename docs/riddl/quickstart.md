---
title: "5-Minute Quickstart"
description: >-
  Get started with RIDDL in 5 minutes. Build your first domain model with
  this hands-on tutorial.
---
# 5-Minute Quickstart

This tutorial takes you from zero to a working RIDDL model. By the end, you'll
have a simple e-commerce domain with a product catalog and shopping cart.

Every example on this page is validated against the RIDDL compiler, so you can
copy any of them and expect them to work.

---

## Step 1: Create Your First Domain

A **domain** is a knowledge boundary. Start with a file called `shop.riddl`:

```riddl
domain OnlineShop is {
  ???
} with {
  briefly "A simple e-commerce system"
}
```

The `with` clause adds metadata. `briefly` is a short description. The `???`
is RIDDL's placeholder for "not specified yet" — it lets an incomplete model
still parse.

---

## Step 2: Add a Bounded Context

A **context** is a self-contained subsystem with its own terminology:

```riddl
domain OnlineShop is {
  context Catalog is {
    ???
  } with {
    briefly "Product catalog and inventory"
  }
}
```

---

## Step 3: Define Types

Types describe your data. Here is a product:

<!-- riddl: in-domain -->
```riddl
context Catalog is {
  type ProductId is Id(Catalog.Product)

  record ProductInfo is {
    id is ProductId,
    name is String(1, 200),
    price is Decimal(10, 2),
    inStock is Boolean
  } with {
    briefly "A product available for purchase"
  }

  entity Product is { ??? }
}
```

`Id(Catalog.Product)` creates an identifier tied to the `Product` entity.
`String(1, 200)` is a string between 1 and 200 characters.

Note this is a **`record`**, not a plain `type`. A record is aggregate-shaped
data, and it is what an entity's state is built from — which is exactly what
Step 4 needs.

---

## Step 4: Create an Entity

An **entity** is something with identity that persists and responds to
messages:

<!-- riddl: in-domain -->
```riddl
context Catalog is {
  type ProductId is Id(Catalog.Product)

  record ProductInfo is {
    id is ProductId,
    name is String(1, 200),
    price is Decimal(10, 2),
    inStock is Boolean
  }

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

  source ProductFeed is {
    outlet Events is event ProductCreated
  }

  entity Product is {
    state Active of record ProductInfo is {
      handler Main is {
        on command CreateProduct {
          do "create the product with a new ID"
          send event ProductCreated to outlet ProductFeed.Events
        }
      }
    }
  } with {
    option is event-sourced
    briefly "A product in the catalog"
  }
}
```

Key concepts:

- **Commands** request changes (imperative: `CreateProduct`)
- **Events** record what happened (past tense: `ProductCreated`)
- **State** holds the entity's data, and is built from a `record`
- **Handlers** define behavior when messages arrive
- **Streamlets** such as `source` carry events out of the context, through
  their outlets

Three details that are easy to get wrong:

- **Options go in `with { }`**, not in the body. `option is event-sourced`
  inside the entity body is a parse error.
- **`do "..."`** describes work for a human or AI to implement later. A bare
  quoted string on its own is not a statement.
- **An outlet belongs to a streamlet**, not to the entity. The entity sends to
  it by its qualified name, `ProductFeed.Events`.

---

## Step 5: Add a Shopping Cart

Let's add another context for shopping:

<!-- riddl: in-domain -->
```riddl
context Catalog is {
  type ProductId is Id(Catalog.Product)
  entity Product is { ??? }
}

context Shopping is {
  type CartId is Id(Shopping.Cart)

  record CartItem is {
    productId is Catalog.ProductId,
    quantity is Integer,
    price is Decimal(10, 2)
  }

  record CartState is {
    items is CartItem*
  }

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

  source CartFeed is {
    outlet Events is event ItemAdded
  }

  entity Cart is {
    state Active of record CartState is {
      handler Main is {
        on command AddItem {
          do "add or update the item in the cart"
          send event ItemAdded to outlet CartFeed.Events
        }
        on query GetContents {
          reply result CartContents
        }
      }
    }
  } with {
    option is event-sourced
  }
}
```

Note: `CartItem*` means a list of zero or more items. You can reference types
from other contexts with `Catalog.ProductId`.

`reply` produces a query's answer without the handler needing to know who
asked.

---

## Complete Example

Here is the full model in one file:

```riddl
domain OnlineShop is {

  context Catalog is {
    type ProductId is Id(Catalog.Product)

    record ProductInfo is {
      id is ProductId,
      name is String(1, 200),
      price is Decimal(10, 2),
      inStock is Boolean
    }

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

    source ProductFeed is {
      outlet Events is event ProductCreated
    }

    entity Product is {
      state Active of record ProductInfo is {
        handler Main is {
          on command CreateProduct {
            do "create the product with a new ID"
            send event ProductCreated to outlet ProductFeed.Events
          }
        }
      } with {
        briefly "The live product record"
      }
    } with {
      option is event-sourced
      briefly "A product in the catalog"
    }
  } with {
    briefly "Product catalog and inventory"
  }

  context Shopping is {
    type CartId is Id(Shopping.Cart)

    record CartItem is {
      productId is Catalog.ProductId,
      quantity is Integer,
      price is Decimal(10, 2)
    }

    record CartState is {
      items is CartItem*
    }

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

    source CartFeed is {
      outlet Events is event ItemAdded
    }

    entity Cart is {
      state Active of record CartState is {
        handler Main is {
          on command AddItem {
            do "add or update the item in the cart"
            send event ItemAdded to outlet CartFeed.Events
          }
          on query GetContents {
            reply result CartContents
          }
        }
      } with {
        briefly "The live cart contents"
      }
    } with {
      option is event-sourced
      briefly "A customer's shopping cart"
    }
  } with {
    briefly "Shopping cart management"
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

A clean model exits 0. RIDDL also reports non-fatal findings — style, missing
descriptions, completeness — which are worth reading even when the model
validates.

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
| `domain` | Knowledge boundary | `domain Shop is { ??? }` |
| `context` | Bounded subsystem | `context Catalog is { ??? }` |
| `type` | Data shape | `type Name is String(1, 80)` |
| `record` | Aggregate data | `record Info is { name is String }` |
| `entity` | Stateful object | `entity Cart is { ??? }` |
| `command` | Request to change | `command AddItem is { qty is Integer }` |
| `event` | Record of change | `event ItemAdded is { at is TimeStamp }` |
| `query` | Request for info | `query GetContents is { id is CartId }` |
| `result` | Answer to a query | `result Contents is { items is Item* }` |
| `state` | Entity's data | `state Active of record Info` |
| `handler` | Message behavior | `handler Main is { on command X { ??? } }` |
| `source` | Emits events | `source Feed is { outlet Events is event E }` |
| `do` | Describe work to do | `do "recalculate the total"` |
| `reply` | Answer a query | `reply result Contents` |
