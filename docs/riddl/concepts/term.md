---
title: "Terms"
draft: false
---

A Term is a glossary entry that defines vocabulary used within a
domain or context. Since Domain-Driven Design requires bounded
contexts to have precise, unambiguous terminology, RIDDL provides
the Term definition to capture word meanings that aren't modeled as
types or entities.

## Purpose

Terms help you:

- **Establish ubiquitous language**: Define the shared vocabulary
  of your domain
- **Avoid ambiguity**: Clarify words that might mean different
  things to different people
- **Document domain knowledge**: Capture business concepts that
  don't need formal modeling
- **Generate glossaries**: Tools can extract terms into
  documentation

## Syntax

Terms appear in `with { }` metadata blocks, not inside a
definition's body. The syntax is `term` *identifier* `is`
*doc_block*:

```riddl
domain ECommerce is {
  ???
} with {
  term Customer is {
    |A person or organization that has purchased products or
    |services from us, or has expressed interest in doing so.
    |Distinguished from a "Lead" (who hasn't yet engaged) and
    |a "User" (who accesses our systems but may not be the
    |purchaser).
  }
}
```

## Example: E-Commerce Domain

```riddl
domain ECommerce is {
  context Catalog is {
    // ... body definitions (entities, types, etc.) ...
    ???
  } with {
    term Listing is {
      |A product's presence in the catalog, including its
      |description, images, pricing, and availability. One
      |product may have multiple listings in different
      |categories.
    }
  }

  context Orders is {
    ???
  } with {
    term Fulfillment is {
      |The complete process of receiving, processing, and
      |delivering an order to the customer. Includes picking,
      |packing, shipping, and delivery confirmation.
    }
    term Backorder is {
      |An order for a product that is temporarily out of stock.
      |The order is accepted but fulfillment is delayed until
      |inventory is replenished.
    }
  }
} with {
  term SKU is {
    |Stock Keeping Unit. A unique identifier for a specific
    |product variant, including size, color, and other
    |attributes. Example: "SHIRT-BLU-L" for a large blue shirt.
  }
  term CartAbandonment is {
    |When a customer adds items to their shopping cart but leaves
    |the site without completing the purchase. A key metric for
    |conversion optimization.
  }
}
```

## Terms vs. Types

| Concept | When to Use |
|---------|-------------|
| **Term** | Word definitions, business jargon, conceptual explanations |
| **Type** | Data structures that appear in messages, states, or APIs |

If you need to pass it in a message or store it in state, use a
Type. If you're defining what a word means, use a Term.

```riddl
context Orders is {
  // Use a Type when you need the data structure
  type Money is { amount: Decimal, currency: CurrencyCode }
  ???
} with {
  // Use a Term when you're defining the concept
  term Revenue is {
    |The total income generated from sales before deducting
    |costs and expenses. Distinct from "profit" which is
    |revenue minus costs.
  }
}
```

## Best Practices

1. **Define early**: Add terms as soon as domain vocabulary emerges
2. **Be specific**: Include examples and distinguish from similar
   concepts
3. **Keep current**: Update terms as understanding evolves
4. **Cross-reference**: Mention related terms and types in
   definitions
5. **Involve domain experts**: Terms should reflect how the
   business talks

## Occurs In

[Metadata](metadata.md) blocks (`with { }`) on any definition.

## Contains

Nothing (leaf definition with description only)
