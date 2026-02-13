---
title: "Loyalty Context"
description: "Loyalty program enrollment, point accrual, and redemption"
---

# Loyalty Context

The Loyalty context manages loyalty program enrollment, point
accrual from both dine-in and online purchases, and point
redemption. It is isolated as its own bounded context so the
loyalty program can be developed and rolled out independently
without touching any other context.

## Purpose

The CEO wanted a customer loyalty program but was told it
required a "major refactor" of the existing system. By modeling
loyalty as an isolated context that listens to payment events
via adaptors, the program can be developed and deployed
incrementally without modifying Front of House or Online
Ordering.

## Interview Connection

From the [CEO's interview](../personas/ceo.md):

> "I tried to get them to build a loyalty program... The
> development team told us that this would require a major
> refactor."

From the [Delivery Driver's interview](../personas/delivery-driver.md):

> "They tell me that those will go through the same app. That
> just sounds like more headache."

The isolation pattern means loyalty is additive — it receives
events but doesn't require changes to the systems that generate
those events.

## Types

```riddl
type LoyaltyAccountId is Id(Loyalty.LoyaltyAccount) with {
  briefly "Loyalty account identifier"
  described by "Unique identifier for a loyalty account."
}

type LoyaltyCustomerId is UUID with {
  briefly "Loyalty customer identifier"
  described by "Unique identifier for the loyalty customer."
}

type LoyaltyAccountStatus is any of {
  LoyaltyActive,
  LoyaltySuspended
} with {
  briefly "Account status"
  described by "Current status of a loyalty account."
}

type PointTransaction is {
  transactionId is UUID
  pointsChanged is Integer
  transactionReason is String(1, 200)
  sourceOrderRef is optional String(1, 50)
  transactionTimestamp is TimeStamp
} with {
  briefly "Point transaction"
  described by "A single loyalty point accrual or redemption."
}
```

Note that `pointsChanged` is an `Integer` (not `Natural`) —
it can be positive for accruals or negative for redemptions.

## Entity: LoyaltyAccount

The `LoyaltyAccount` entity has a 5-command lifecycle:

```riddl
entity LoyaltyAccount is {

  command EnrollCustomer is {
    loyaltyAccountId is LoyaltyAccountId
    loyaltyCustomerId is LoyaltyCustomerId
    customerDisplayName is String(1, 100)
    customerEmail is String(5, 254)
  }

  command AccruePoints is {
    loyaltyAccountId is LoyaltyAccountId
    accrualPoints is Natural
    accrualReason is String(1, 200)
    accrualOrderRef is optional String(1, 50)
  }

  command RedeemPoints is {
    loyaltyAccountId is LoyaltyAccountId
    redemptionPoints is Natural
    redemptionReason is String(1, 200)
  }

  command SuspendAccount is {
    loyaltyAccountId is LoyaltyAccountId
    suspensionReason is String(1, 500)
  }

  command ReactivateAccount is {
    loyaltyAccountId is LoyaltyAccountId
  }

  // Events: CustomerEnrolled, PointsAccrued, PointsRedeemed,
  //         AccountSuspended, AccountReactivated

  state ActiveAccount of LoyaltyAccount.LoyaltyAccountStateData

  handler LoyaltyAccountHandler is {
    on command EnrollCustomer {
      morph entity Loyalty.LoyaltyAccount to state
        Loyalty.LoyaltyAccount.ActiveAccount
        with command EnrollCustomer
      tell event CustomerEnrolled to
        entity Loyalty.LoyaltyAccount
    }
    on command AccruePoints {
      tell event PointsAccrued to
        entity Loyalty.LoyaltyAccount
    }
    on command RedeemPoints {
      tell event PointsRedeemed to
        entity Loyalty.LoyaltyAccount
    }
    on command SuspendAccount {
      tell event AccountSuspended to
        entity Loyalty.LoyaltyAccount
    }
    on command ReactivateAccount {
      tell event AccountReactivated to
        entity Loyalty.LoyaltyAccount
    }
  }
}
```

The state tracks both current `pointBalance` and
`lifetimePoints`, plus a list of `recentTransactions`. The
`PointsAccrued` event includes a `newBalance` field so
downstream systems know the current balance without querying.

## Repository

```riddl
repository LoyaltyAccountRepository is {
  schema LoyaltyAccountData is relational
    of accounts as LoyaltyAccount
    index on field LoyaltyAccount.loyaltyAccountId
    index on field LoyaltyAccount.loyaltyCustomerId
    index on field LoyaltyAccount.customerEmail
}
```

The index on `customerEmail` enables account lookup during
enrollment to prevent duplicate accounts.

## Adaptors

Loyalty has two inbound adaptors — one for dine-in payments,
one for online payments:

```riddl
adaptor FromPayment from context Restaurant.FrontOfHouse is {
  handler DineInLoyaltyIntake is {
    on event Restaurant.FrontOfHouse.TableOrder.PaymentProcessed {
      prompt "Accrue loyalty points from dine-in payment"
    }
  }
}

adaptor FromOnlinePayment from context Restaurant.OnlineOrdering is {
  handler OnlineLoyaltyIntake is {
    on event Restaurant.OnlineOrdering.OnlineOrder.OnlinePaymentProcessed {
      prompt "Accrue loyalty points from online payment"
    }
  }
}
```

Both adaptors listen for payment events and trigger point
accrual. The key insight: **neither Front of House nor Online
Ordering needs to know about loyalty.** They simply process
payments as normal, and the loyalty context reacts to those
events. This is why the CEO's loyalty program doesn't require
a "major refactor."

## Design Decisions

**Why isolated?** The entire value proposition of the Loyalty
context is independence. It can be developed, tested, and
deployed without modifying any existing context. The adaptors
pattern makes it purely additive — it consumes events that
are already being produced.

**Why two separate payment adaptors?** Dine-in and online
payments have different event structures
(`PaymentProcessed` vs `OnlinePaymentProcessed`) and different
contexts of origin. Separate adaptors keep the translation
logic clean and independently testable.

**Incremental rollout strategy:** Loyalty can be deployed to a
single location first, then rolled out chain-wide. Since it
only listens to events, enabling it at a location is just a
matter of routing payment events to the loyalty context — no
changes to the POS or online ordering systems.

## Source

- [`LoyaltyContext.riddl`](https://github.com/ossuminc/riddl-models/tree/main/hospitality/food-service/reactive-bbq/restaurant/LoyaltyContext.riddl)
- [`loyalty-types.riddl`](https://github.com/ossuminc/riddl-models/tree/main/hospitality/food-service/reactive-bbq/restaurant/loyalty-types.riddl)
- [`LoyaltyAccount.riddl`](https://github.com/ossuminc/riddl-models/tree/main/hospitality/food-service/reactive-bbq/restaurant/LoyaltyAccount.riddl)
