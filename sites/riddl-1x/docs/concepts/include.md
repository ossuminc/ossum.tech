---
title: "Includes"
draft: false
---

Includes allow you to split a RIDDL model across multiple files, inserting
content from one file into another. This is essential for organizing large
models and enabling team collaboration.

## Purpose

Includes help you:

- **Organize large models**: Split domains, contexts, or entities into
  separate files
- **Enable parallel work**: Team members can edit different files
  simultaneously
- **Improve readability**: Keep individual files focused and manageable
- **Reuse definitions**: Share common types or patterns across contexts

## Syntax

```riddl
include "path/to/file.riddl"
```

The path is relative to the file containing the include statement.

## Example: Organizing a Domain

A complex domain might be organized like this:

**main.riddl**
```riddl
domain ECommerce is {
  include "types/common-types.riddl"
  include "contexts/catalog.riddl"
  include "contexts/orders.riddl"
  include "contexts/payments.riddl"
  include "epics/checkout-flow.riddl"
}
```

**types/common-types.riddl**
```riddl
type Money is { amount: Decimal, currency: CurrencyCode }
type CurrencyCode is any of { USD, EUR, GBP, JPY }
type Address is {
  street: String,
  city: String,
  country: String,
  postalCode: String
}
```

**contexts/catalog.riddl**
```riddl
context Catalog is {
  entity Product is {
    // Product definition
  }
  entity Category is {
    // Category definition
  }
}
```

## Containment Rules

The included content must be valid for the location where it's included.
RIDDL enforces the [definition hierarchy](index.md#hierarchy):

| Include Location | Valid Included Content |
|-----------------|----------------------|
| Root level | Domains, modules |
| Domain | Contexts, types, epics, users |
| Context | Entities, repositories, sagas, types |
| Entity | States, handlers, functions |

Including content that violates the hierarchy produces a validation error.

## File Organization Patterns

### By Bounded Context

```
myproject/
├── main.riddl
├── contexts/
│   ├── sales.riddl
│   ├── inventory.riddl
│   └── shipping.riddl
└── shared/
    └── common-types.riddl
```

### By Definition Type

```
myproject/
├── main.riddl
├── types/
│   └── domain-types.riddl
├── entities/
│   ├── customer.riddl
│   └── order.riddl
└── epics/
    └── user-journeys.riddl
```

## Best Practices

1. **Use meaningful paths**: Organize files to reflect your domain structure
2. **Keep files focused**: One context or major entity per file
3. **Share types carefully**: Common types should be truly universal
4. **Document dependencies**: Note which files depend on which

## Occurs In

All [vital definitions](vital.md) (domains, contexts, entities, etc.)

## Contains

Content relevant to the definition in which it is used. The included content
must conform to the [hierarchy shown in the index](index.md#hierarchy).