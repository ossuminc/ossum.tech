---
title: "Metadata"
draft: false
---

Metadata in RIDDL provides supplementary information about definitions that
doesn't affect the core semantics but aids documentation, organization, and
tooling.

## Common Metadata

All definitions support these metadata elements:

### Brief Description

A short, one-line description using `briefly`:

```riddl
entity Customer is {
  briefly "A person or organization that purchases products"
  // ...
}
```

### Extended Description

Longer documentation using `described by` (or `described as`, `explained by`,
`explained as`):

```riddl
entity Customer is {
  described by {
    |Customers are the primary actors in our e-commerce system.
    |They can browse products, place orders, and manage their
    |account information.
  }
}
```

The `|` prefix indicates lines of documentation text (Markdown format).

### Terms

Domain-specific terminology with definitions:

```riddl
domain ECommerce is {
  term "SKU" is described by "Stock Keeping Unit - unique product identifier"
  term "Cart" is described by "Temporary collection of items before checkout"
}
```

### Authors

Attribution for definitions:

```riddl
author Reid is {
  name "Reid Spencer"
  email "reid@example.com"
}

domain MyDomain by author Reid is { ... }
```

## Options

Options modify the behavior of definitions. Common options include:

- `technology("x")`: Implementation technology hints
- `kind("x")`: Classification of the definition
- `css("x")`: Styling hints for documentation
- `faicon("x")`: Font Awesome icon for documentation

```riddl
context OrderManagement is {
  option technology("Akka")
  option kind("core")
  // ...
}
```

## Occurs In

Metadata can appear in any definition, including:

* [Domains](domain.md)
* [Contexts](context.md)
* [Entities](entity.md)
* [Types](type.md)
* All other definitions

## Contains

Metadata does not contain other definitions; it contains:

* Literal strings (descriptions, term definitions)
* Options with parameters
* Author references
