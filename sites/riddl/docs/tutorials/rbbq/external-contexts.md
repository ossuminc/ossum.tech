---
title: "External Contexts"
description: "Third-party system integrations in the Reactive BBQ model"
---

# External Contexts

The Reactive BBQ model includes six external contexts — bounded
contexts that represent third-party systems the business depends
on but doesn't own. These are marked with `option is external`
to signal that the implementation is outside the model boundary.

## The `option is external` Pattern

In RIDDL, external contexts define the *interface* to a
third-party system without modeling its internals. The context
specifies the commands you can send and the events you expect to
receive, but the implementation is someone else's responsibility.

```riddl
context PaymentGateway is {
  // Define the interface...
} with {
  option is external
  briefly "External payment gateway"
  described by "Third-party payment processing service."
}
```

The `option is external` metadata tells the compiler and any code
generators that this context won't be implemented — it's a
boundary definition only.

## Restaurant Domain — External Contexts

### PaymentGateway

```riddl
context PaymentGateway is {

  command AuthorizePayment is {
    paymentGatewayTransactionId is String(1, 100)
    authorizeAmount is Decimal(10, 2)
    authorizeMethod is String(1, 50)
  }

  event PaymentAuthorized is {
    paymentGatewayTransactionId is String(1, 100)
    authorizedAmount is Decimal(10, 2)
    authorizationCode is String(1, 50)
  }

  command CapturePayment is {
    captureTransactionId is String(1, 100)
    captureAmount is Decimal(10, 2)
  }

  event PaymentCaptured is {
    captureTransactionId is String(1, 100)
    capturedAmount is Decimal(10, 2)
  }

} with {
  option is external
  briefly "External payment gateway"
  described by "Third-party payment processing service."
}
```

The PaymentGateway models the authorize-then-capture payment
flow used by credit card processors. The two-step process
(authorize, then capture) is standard in payment processing —
authorization holds the funds, capture completes the transfer.

### NotificationService

```riddl
context NotificationService is {

  command SendPushNotification is {
    notificationRecipient is String(1, 100)
    notificationTitle is String(1, 200)
    notificationBody is String(1, 1000)
  }

  event PushNotificationSent is {
    notificationRecipient is String(1, 100)
    sentAt is TimeStamp
  }

} with {
  option is external
  briefly "External notification service"
  described by "Push notification delivery service for mobile devices."
}
```

The NotificationService is used by the
[Bar context](restaurant/bar.md) to send push notifications
when drinks are ready. It's also available for the
[Delivery context](restaurant/delivery.md) to notify drivers
of new orders.

## BackOffice Domain — External Contexts

### HRSystem

```riddl
context HRSystem is {

  command SyncEmployeeData is {
    hrEmployeeId is String(1, 50)
    hrEmployeeName is String(1, 100)
    hrEmployeeRole is String(1, 50)
  }

  event EmployeeDataSynced is {
    hrEmployeeId is String(1, 50)
    syncedAt is TimeStamp
  }

} with {
  option is external
  briefly "External HR system"
  described by "Human resources management system."
}
```

The HRSystem provides employee master data to the
[Scheduling context](backoffice/scheduling.md). The
`SyncEmployeeData` command enables the scheduling system to
pull current employee records — roles, availability, and
contact information.

### AccountingSystem

```riddl
context AccountingSystem is {

  command PostTransaction is {
    accountingTransactionId is String(1, 100)
    accountCode is String(1, 20)
    transactionAmount is Decimal(12, 2)
    transactionDescription is String(1, 500)
  }

  event TransactionPosted is {
    accountingTransactionId is String(1, 100)
    postedAt is TimeStamp
  }

} with {
  option is external
  briefly "External accounting system"
  described by "General ledger and accounting system."
}
```

The AccountingSystem receives financial transactions from
the restaurant operations. Sales revenue, labor costs, and
inventory purchases are posted to the general ledger for
financial reporting.

## Corporate Domain — External Contexts

### PrintingService

```riddl
context PrintingService is {

  command PrintMenus is {
    printJobId is String(1, 100)
    menuVersion is String(1, 50)
    printQuantity is Natural
  }

  event MenusPrinted is {
    printJobId is String(1, 100)
    printedAt is TimeStamp
  }

} with {
  option is external
  briefly "External printing service"
  described by "Third-party printing service for physical menus."
}
```

The PrintingService is triggered when a
[MenuRelease](corporate/menu-management.md) is published,
sending the updated menu to the printer for physical copies
distributed to all locations.

### PhotographyService

```riddl
context PhotographyService is {

  command SchedulePhotoShoot is {
    shootId is String(1, 100)
    shootDate is Date
    menuItemsToPhotograph is many String(1, 50)
  }

  event PhotoShootCompleted is {
    shootId is String(1, 100)
    completedAt is TimeStamp
  }

} with {
  option is external
  briefly "External photography service"
  described by "Food photography service for menu images."
}
```

From the Head Chef's interview: working with a photographer
is part of the monthly menu update process. The
PhotographyService captures this relationship in the model.

## Design Decisions

**Why model external systems at all?** Even though we don't
implement these systems, modeling them provides several
benefits:

1. **Interface documentation** — The commands and events
   define the exact integration contract
2. **Validation** — The compiler can check that references
   to external context commands and events are valid
3. **Completeness** — The model shows the full system
   boundary, not just the parts we build
4. **Code generation** — Integration adapters and API
   clients can be generated from the interface definitions

**Why not use adaptors instead?** Adaptors bridge between
two bounded contexts you own. External contexts model
systems you *don't* own. The interface is defined on the
external context itself, and adaptors in your contexts
reference it.

**Minimal interfaces:** External contexts define only the
commands and events relevant to this system. The actual
payment gateway has hundreds of operations — we only model
the ones Reactive BBQ uses.

## Source

- [`restaurant/external-contexts.riddl`](https://github.com/ossuminc/riddl-models/tree/main/hospitality/food-service/reactive-bbq/restaurant/external-contexts.riddl)
- [`backoffice/external-contexts.riddl`](https://github.com/ossuminc/riddl-models/tree/main/hospitality/food-service/reactive-bbq/backoffice/external-contexts.riddl)
- [`corporate/external-contexts.riddl`](https://github.com/ossuminc/riddl-models/tree/main/hospitality/food-service/reactive-bbq/corporate/external-contexts.riddl)
