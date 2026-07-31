---
title: "User"
draft: false
---

A User represents a participant in the system's [Epics](epic.md) and
[Use Cases](use-case.md). Users are typically named after the role they play
(Customer, Administrator, Reviewer) rather than specific individuals, following
the persona pattern from user experience design.

## Purpose

Users serve to:

- **Identify system actors**: Who interacts with the system
- **Enable use case modeling**: Users are participants in interactions
- **Support sequence diagrams**: Show user-system communication flows
- **Document requirements**: Clarify who needs what capabilities

## Syntax

```riddl
domain Marketplace is {
  user Buyer is {
    |A person who browses products and makes purchases.
    |May or may not have a registered account.
  }

  user Seller is {
    |A merchant who lists products for sale and fulfills orders.
    |Must have an approved seller account.
  }

  user Administrator is {
    |Internal staff who manage the platform, resolve disputes,
    |and maintain system configuration.
  }
}
```

## Users in Epics

Users are the protagonists of epics and use cases:

```riddl
domain ECommerce is {
  user Customer is {
    |A registered user who can browse, purchase, and review products.
  }

  user Guest is {
    |An unregistered visitor who can browse but must register to purchase.
  }

  epic CheckoutFlow is {
    user Customer wants to "complete a purchase"
    so that "they receive products they need"

    case RegisteredCheckout is {
      user Customer "reviews cart contents"
      then user Customer "confirms shipping address"
      then entity PaymentService "processes payment"
      then user Customer "receives order confirmation"
    }
  }

  epic GuestBrowsing is {
    user Guest wants to "explore available products"
    so that "they can decide whether to register"

    case BrowseCatalog is {
      user Guest "searches for products"
      then entity Catalog "returns matching items"
      then user Guest "views product details"
    }
  }
}
```

## User vs. Entity

| Concept | Purpose | Location |
|---------|---------|----------|
| **User** | External actor participating in use cases | Defined in domains |
| **Entity** | Internal system component with state | Defined in contexts |

Users interact *with* the system; entities are *part of* the system.

```riddl
domain Banking is {
  // User: External actor
  user AccountHolder is {
    |A customer who owns one or more bank accounts.
  }

  context Accounts is {
    // Entity: Internal system component
    entity Account is {
      state Active is { balance: Money, holder: CustomerId }
      handler Operations is {
        on command Deposit { /* ... */ }
        on command Withdraw { /* ... */ }
      }
    }
  }

  epic TransferMoney is {
    user AccountHolder wants to "move funds between accounts"
    so that "they can manage their money flexibly"

    case SuccessfulTransfer is {
      user AccountHolder "initiates transfer request"
      then entity Account "debits source account"
      then entity Account "credits destination account"
      then user AccountHolder "sees confirmation"
    }
  }
}
```

## Naming Conventions

Good user names are:

- **Role-based**: `Customer`, `Administrator`, `Reviewer`
- **Singular**: `Customer` not `Customers`
- **Clear**: `PremiumMember` vs `Type2User`

Avoid:

- Generic names: `User1`, `Actor`
- Implementation details: `DatabaseAdmin`
- Specific people: `JohnSmith`

## Best Practices

1. **Define all actors**: Every external participant should be a User
2. **Use meaningful names**: Names should convey the role
3. **Add descriptions**: Explain what distinguishes this user type
4. **Consider permissions**: Different users may have different capabilities
5. **Include system users**: APIs, scheduled jobs, and integrations are users too

```riddl
// System actors are users too
user PaymentWebhook is {
  |External payment processor calling back with transaction results.
}

user NightlyBatchJob is {
  |Scheduled process that reconciles accounts and generates reports.
}
```

## Occurs In

* [Domains](domain.md)

## Contains

Nothing (leaf definition)