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

<!-- riddl: in-domain -->
<!-- riddl: in-domain -->
```riddl
// `external` marks a context the chain does NOT build. It still declares a
// real interface, because everything inside must be typed against it.
external context PaymentGateway is {
  command AuthorizePayment yields event PaymentAuthorized is {
    paymentGatewayTransactionId: String(1,100)
    authorizeAmount: Decimal(10,2)
  }
  event PaymentAuthorized is {
    paymentGatewayTransactionId: String(1,100)
    authorizeAmount: Decimal(10,2)
  }
}
```

The `option is external` metadata tells the compiler and any code
generators that this context won't be implemented — it's a
boundary definition only.

## Restaurant Domain — External Contexts

### PaymentGateway

<!-- riddl: in-domain -->
<!-- riddl: in-domain -->
```riddl
external context PaymentGateway as flow is {

  // An external context that publishes declares its OWN portlets: a
  // cross-context connector must land on the context's own outlet, never
  // reach past the boundary to something the context contains.
  inlet PaymentGatewayIn is type PaymentGatewayEvent
  outlet PaymentGatewayOut is type PaymentGatewayEvent

  command AuthorizePayment yields event PaymentAuthorized is {
    paymentGatewayTransactionId: String(1,100)
    authorizeAmount: Decimal(10,2)
  }
  event PaymentAuthorized is {
    paymentGatewayTransactionId: String(1,100)
    authorizeAmount: Decimal(10,2)
  }
  type PaymentGatewayEvent is PaymentAuthorized

  handler PaymentGatewayHandler is {
    on cmd: command AuthorizePayment is {
      yield event PaymentAuthorized(paymentGatewayTransactionId = cmd.paymentGatewayTransactionId)
      do "submit the authorization request to the payment processor"
    }
    // An adaptor or boundary handler must say what it does with what it does
    // not recognise.
    on other is {
      error "Unexpected message at the PaymentGateway boundary"
    }
  }
}
```

The PaymentGateway models the authorize-then-capture payment
flow used by credit card processors. The two-step process
(authorize, then capture) is standard in payment processing —
authorization holds the funds, capture completes the transfer.

### NotificationService

<!-- riddl: in-domain -->
<!-- riddl: in-domain -->
```riddl
external context NotificationService as flow is {

  // An external context that publishes declares its OWN portlets: a
  // cross-context connector must land on the context's own outlet, never
  // reach past the boundary to something the context contains.
  inlet NotificationServiceIn is type NotificationServiceEvent
  outlet NotificationServiceOut is type NotificationServiceEvent

  command SendPushNotification yields event NotificationSent is {
    notificationRecipient: String(1,120)
    notificationBody: String(1,500)
  }
  event NotificationSent is {
    notificationRecipient: String(1,120)
    notificationBody: String(1,500)
  }
  type NotificationServiceEvent is NotificationSent

  handler NotificationServiceHandler is {
    on cmd: command SendPushNotification is {
      yield event NotificationSent(notificationRecipient = cmd.notificationRecipient)
      do "hand the message to the push provider"
    }
    // An adaptor or boundary handler must say what it does with what it does
    // not recognise.
    on other is {
      error "Unexpected message at the NotificationService boundary"
    }
  }
}
```

The NotificationService is used by the
[Bar context](restaurant/bar.md) to send push notifications
when drinks are ready. It's also available for the
[Delivery context](restaurant/delivery.md) to notify drivers
of new orders.

## BackOffice Domain — External Contexts

### HRSystem

<!-- riddl: in-domain -->
<!-- riddl: in-domain -->
```riddl
external context HRSystem as flow is {

  // An external context that publishes declares its OWN portlets: a
  // cross-context connector must land on the context's own outlet, never
  // reach past the boundary to something the context contains.
  inlet HRSystemIn is type HRSystemEvent
  outlet HRSystemOut is type HRSystemEvent

  command SyncEmployeeData yields event EmployeeDataSynced is {
    employeeRecordId: String(1,50)
    syncedAt: TimeStamp
  }
  event EmployeeDataSynced is {
    employeeRecordId: String(1,50)
    syncedAt: TimeStamp
  }
  type HRSystemEvent is EmployeeDataSynced

  handler HRSystemHandler is {
    on cmd: command SyncEmployeeData is {
      yield event EmployeeDataSynced(employeeRecordId = cmd.employeeRecordId)
      do "reconcile the employee record with the HR system of record"
    }
    // An adaptor or boundary handler must say what it does with what it does
    // not recognise.
    on other is {
      error "Unexpected message at the HRSystem boundary"
    }
  }
}
```

The HRSystem provides employee master data to the
[Scheduling context](backoffice/scheduling.md). The
`SyncEmployeeData` command enables the scheduling system to
pull current employee records — roles, availability, and
contact information.

### AccountingSystem

<!-- riddl: in-domain -->
<!-- riddl: in-domain -->
```riddl
external context AccountingSystem as flow is {

  // An external context that publishes declares its OWN portlets: a
  // cross-context connector must land on the context's own outlet, never
  // reach past the boundary to something the context contains.
  inlet AccountingSystemIn is type AccountingSystemEvent
  outlet AccountingSystemOut is type AccountingSystemEvent

  command PostTransaction yields event TransactionPosted is {
    transactionId: String(1,50)
    postedAmount: Decimal(12,2)
  }
  event TransactionPosted is {
    transactionId: String(1,50)
    postedAmount: Decimal(12,2)
  }
  type AccountingSystemEvent is TransactionPosted

  handler AccountingSystemHandler is {
    on cmd: command PostTransaction is {
      yield event TransactionPosted(transactionId = cmd.transactionId)
      do "post the transaction to the general ledger"
    }
    // An adaptor or boundary handler must say what it does with what it does
    // not recognise.
    on other is {
      error "Unexpected message at the AccountingSystem boundary"
    }
  }
}
```

The AccountingSystem receives financial transactions from
the restaurant operations. Sales revenue, labor costs, and
inventory purchases are posted to the general ledger for
financial reporting.

## Corporate Domain — External Contexts

### PrintingService

<!-- riddl: in-domain -->
<!-- riddl: in-domain -->
```riddl
external context PrintingService as flow is {

  // An external context that publishes declares its OWN portlets: a
  // cross-context connector must land on the context's own outlet, never
  // reach past the boundary to something the context contains.
  inlet PrintingServiceIn is type PrintingServiceEvent
  outlet PrintingServiceOut is type PrintingServiceEvent

  command PrintMenus yields event MenusPrinted is {
    printJobId: String(1,50)
    printQuantity: Natural
  }
  event MenusPrinted is {
    printJobId: String(1,50)
    printQuantity: Natural
  }
  type PrintingServiceEvent is MenusPrinted

  handler PrintingServiceHandler is {
    on cmd: command PrintMenus is {
      yield event MenusPrinted(printJobId = cmd.printJobId)
      do "send the menu artwork to the print vendor"
    }
    // An adaptor or boundary handler must say what it does with what it does
    // not recognise.
    on other is {
      error "Unexpected message at the PrintingService boundary"
    }
  }
}
```

The PrintingService is triggered when a
[MenuRelease](corporate/menu-management.md) is published,
sending the updated menu to the printer for physical copies
distributed to all locations.

### PhotographyService

<!-- riddl: in-domain -->
<!-- riddl: in-domain -->
```riddl
external context PhotographyService as flow is {

  // An external context that publishes declares its OWN portlets: a
  // cross-context connector must land on the context's own outlet, never
  // reach past the boundary to something the context contains.
  inlet PhotographyServiceIn is type PhotographyServiceEvent
  outlet PhotographyServiceOut is type PhotographyServiceEvent

  command SchedulePhotoShoot yields event PhotoShootScheduled is {
    photoShootId: String(1,50)
    scheduledFor: TimeStamp
  }
  event PhotoShootScheduled is {
    photoShootId: String(1,50)
    scheduledFor: TimeStamp
  }
  type PhotographyServiceEvent is PhotoShootScheduled

  handler PhotographyServiceHandler is {
    on cmd: command SchedulePhotoShoot is {
      yield event PhotoShootScheduled(photoShootId = cmd.photoShootId)
      do "book the photographer for the new menu items"
    }
    // An adaptor or boundary handler must say what it does with what it does
    // not recognise.
    on other is {
      error "Unexpected message at the PhotographyService boundary"
    }
  }
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
