---
title: "Loyalty Context"
description: "Loyalty program enrollment, point accrual, and redemption"
---

<!-- riddl-domain-prelude
context FrontOfHouse is {
  event PaymentProcessed is { tableOrderId: String(1,50) }
}
-->

<!-- riddl-prelude
type LoyaltyAccountId is Id(LoyaltyAccount)
type LoyaltyCustomerId is UUID
record StoredLoyaltyAccount is { loyaltyAccountId: LoyaltyAccountId }
event CustomerEnrolled is { loyaltyAccountId: LoyaltyAccountId }
event AccountSuspended is { loyaltyAccountId: LoyaltyAccountId }
event SuspendAccountRejected is { loyaltyAccountId: LoyaltyAccountId, rejectionReason: String(1,500) }
type LoyaltyAccountEvent is CustomerEnrolled | AccountSuspended | SuspendAccountRejected
entity LoyaltyAccount is { ??? }
repository LoyaltyAccountRepository is { ??? }
command PersistAccountSuspended is { loyaltyAccountId: LoyaltyAccountId }
-->

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

<!-- riddl: in-context no-prelude=LoyaltyAccountId,LoyaltyCustomerId -->
```riddl
type LoyaltyAccountId is Id(LoyaltyAccount)

type LoyaltyCustomerId is UUID
```

Note that `pointsChanged` is an `Integer` (not `Natural`) —
it can be positive for accruals or negative for redemptions.

## Entity: LoyaltyAccount

The `LoyaltyAccount` entity has a 5-command lifecycle:

<!-- riddl: in-context no-prelude=LoyaltyAccount,CustomerEnrolled,AccountSuspended,SuspendAccountRejected,LoyaltyAccountCommand,LoyaltyAccountEvent -->
```riddl
event-sourced entity LoyaltyAccount as flow is {

  // An event-sourced entity OWNS the commands and events that change it, so
  // they are declared INSIDE it, and every command names the event it yields.
  command EnrollCustomer yields event CustomerEnrolled is { loyaltyAccountId: LoyaltyAccountId }
  command SuspendAccount yields event AccountSuspended is { loyaltyAccountId: LoyaltyAccountId }

  event CustomerEnrolled is { loyaltyAccountId: LoyaltyAccountId }
  event AccountSuspended is { loyaltyAccountId: LoyaltyAccountId }
  event SuspendAccountRejected is { loyaltyAccountId: LoyaltyAccountId, rejectionReason: String(1,500) }

  record LoyaltyAccountData is { loyaltyAccountId: LoyaltyAccountId }

  // Lifecycle phases are named STATES, not a status field: each state
  // declares the commands it accepts, so the compiler knows the machine.
  initial state Active of record LoyaltyAccountData is {
    handler ActiveHandler is {
      on cmd: command SuspendAccount is {
        yield event AccountSuspended(loyaltyAccountId = cmd.loyaltyAccountId)
      }
      // `set` and `morph` may appear ONLY in an `on event` clause here:
      // replay has to re-apply exactly the same change.
      on evt: event AccountSuspended is {
        morph entity LoyaltyAccount to state Suspended
          with record LoyaltyAccountData(loyaltyAccountId = evt.loyaltyAccountId)
      }
    }
  }

  state Suspended of record LoyaltyAccountData is {
    handler SuspendedHandler is {
      // A command this state does not accept is refused -- and the refusal
      // is PUBLISHED before it is raised, so the attempt is recorded.
      on cmd: command SuspendAccount is {
        send event SuspendAccountRejected(loyaltyAccountId = cmd.loyaltyAccountId,
          rejectionReason = "LoyaltyAccount does not accept SuspendAccount in this state")
          to outlet LoyaltyAccountEvents
        error "LoyaltyAccount does not accept SuspendAccount in this state"
      }
    }
  }

  // A processor receives on its OWN inlet and publishes on its OWN outlet,
  // and a portlet's type must ADMIT everything that travels on it.
  type LoyaltyAccountCommand is EnrollCustomer | SuspendAccount
  type LoyaltyAccountEvent is CustomerEnrolled | AccountSuspended | SuspendAccountRejected

  inlet LoyaltyAccountCommands is type LoyaltyAccountCommand
  outlet LoyaltyAccountEvents is type LoyaltyAccountEvent
}
```

The state tracks both current `pointBalance` and
`lifetimePoints`, plus a list of `recentTransactions`. The
`PointsAccrued` event includes a `newBalance` field so
downstream systems know the current balance without querying.

## Repository

<!-- riddl: in-context no-prelude=LoyaltyAccountRepository,StoredLoyaltyAccount,PersistAccountSuspended -->
```riddl
repository LoyaltyAccountRepository as flow is {
  inlet LoyaltyAccountRepositoryFromLoyaltyAccount is type LoyaltyAccountEvent
  outlet LoyaltyAccountRepositoryResponses is type LoyaltyAccountEvent

  record StoredLoyaltyAccount is { loyaltyAccountId: LoyaltyAccountId }

  // A repository that answers queries and declares NO index at all is a
  // sequential scan by construction, and draws a warning saying so.
  schema LoyaltyAccountSchema is relational
    of rows as type StoredLoyaltyAccount
      index on field StoredLoyaltyAccount.loyaltyAccountId

  command PersistAccountSuspended is { loyaltyAccountId: LoyaltyAccountId }

  handler LoyaltyAccountPersistence is {
    on command PersistAccountSuspended is {
      do "update the stored loyaltyAccount row for this loyaltyAccountId"
    }
    // An inlet admitting an alternation needs a clause that receives it.
    // Handling each member is not enough -- say what ARRIVING means.
    on other is {
      do "persist whatever else arrives on this inlet"
    }
  }
}
```

The index on `customerEmail` enables account lookup during
enrollment to prevent duplicate accounts.

## Adaptors

Loyalty has two inbound adaptors — one for dine-in payments,
one for online payments:

<!-- riddl: in-domain -->
```riddl
context Loyalty is {
  // An adaptor is the translation seam at a context boundary: it is the only
  // place that knows the OTHER context's message shapes.
  adaptor FromPayment from context FrontOfHouse is {
    handler FromPaymentIntake is {
      on event FrontOfHouse.PaymentProcessed is {
        do "accrue loyalty points for the paying customer"
      }
      // Every adaptor handler must say what it does with what it does not
      // recognise. Silence is not an option in 2.0.
      on other is {
        error "Unexpected message from FrontOfHouse"
      }
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
