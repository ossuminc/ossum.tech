---
title: "Reactive BBQ Domain"
description: "Top-level domain model for the Reactive BBQ restaurant chain"
---

# Reactive BBQ Domain

Everything in RIDDL revolves around creating domains and subdomains. These
are logical groupings of definitions that *belong* together, presumably
because they mimic an organization's structure or some other logical, real
world groupings. Domains can be nested.

## Domain Structure

At the top level of definition, a single
[`domain`](../../concepts/domain.md)
named `ReactiveBBQ` represents the entire enterprise:

```riddl
domain ReactiveBBQ is {
  include "restaurant/domain"
  include "backoffice/domain"
  include "corporate/domain"
}
```

The details of the top level domain are abstracted away via three
[`include`](../../concepts/include.md)
statements within its body, one for each of the subdomains:

- [Restaurant](restaurant/index.md) - Core restaurant operations
- [Back Office](backoffice/index.md) - Administrative and management functions
- [Corporate](corporate/index.md) - Corporate headquarters operations

## Why Subdomains?

Separating the business into distinct subdomains provides several benefits:

1. **Bounded Contexts** - Each subdomain can define its own ubiquitous language
   without ambiguity
2. **Team Alignment** - Development teams can own specific subdomains
3. **Independent Evolution** - Subdomains can be modified without affecting others
4. **Scalability** - Different subdomains can be deployed and scaled independently

## Cross-Domain Communication

The subdomains communicate through well-defined interfaces. For example:

- **Restaurant → Corporate**: Sales reports, inventory requests
- **Corporate → Restaurant**: Menu updates, policy changes
- **BackOffice → Restaurant**: Staff schedules, equipment maintenance

These communication patterns are modeled using RIDDL's
[adaptor](../../concepts/adaptor.md) and
[connector](../../concepts/connector.md) constructs.

## Source Code

The complete RIDDL specification for Reactive BBQ is available in the
[riddl-examples repository](https://github.com/ossuminc/riddl-examples/tree/main/src/riddl/ReactiveBBQ).
