---
title: "User Interface Modeling"
description: "Using RIDDL to design user interfaces with Epics and Applications"
---

# User Interface Modeling

<!-- riddl-prelude
  result OrderDetails is { total: Currency(USD) }
    // For the checkout handler fence: what it reads, tells and shows.
    type PaymentInfo is String
    type ReceiptData is String
    record ChargeData is { note is String }
    command SubmitPayment is { note is String }
    command Charge is { note is String }
-->

<!-- riddl-domain-prelude
    // The checkout fence declares its own application context, so what it
    // reaches for must sit at domain level, not in the page prelude.
    type PaymentInfo is String
    type ReceiptData is String
    command SubmitPayment is { note is String }
    command Charge is { note is String }
    context Billing is {
      command BillingCharge is { note is String }
    }
-->

RIDDL provides two main constructs for modeling user interfaces:
[Epics](../../../concepts/epic.md) and
[Applications](../../../concepts/application.md).

## Overview

```
                    ┌──────────────┐
                    │     User     │
                    └──────┬───────┘
                           │ interacts with
                           ▼
                    ┌──────────────┐
                    │  Application │
                    └──────┬───────┘
                           │ sends messages to
                           ▼
                    ┌──────────────┐
                    │    System    │
                    └──────────────┘
```

- **Epics** - Specify the interaction between users and the system
- **Applications** - Define the user interface components

## Epics Model Interactions

A RIDDL Epic models the interaction between a user, an application, and the
rest of the system. Epics contain related sets of use cases that detail each
interaction.

### Key Concepts

| Concept | Description |
|---------|-------------|
| **Epic** | A specification of related use cases that define a system feature |
| **Use Case** | A single flow of interactions between user and system |
| **User Story** | Summary of a use case: *{who}* wants to *{what}* so that *{why}* |
| **Interaction** | One step of a use case |

### Example: Shopping Cart

```riddl
domain ECommerce is {
  user Shopper is "A customer browsing and purchasing products"

  application context StoreFront is { ??? }
  context Inventory is { ??? }
  context Orders is { ??? }
  context Payments is { ??? }

  epic ShoppingCartJourney is {
    user Shopper wants to "shop" so that "they receive the products they need"

    case BrowseAndPurchase is {
      user Shopper wants to "browse products and complete a purchase"
        so that "they can receive desired items"

      // The shopper only ever touches StoreFront, the application...
      step from user Shopper "views the product catalog"
           to context StoreFront

      // ...which reaches into the domain on their behalf
      step from context StoreFront "reserves the selected items"
           to context Inventory

      step from user Shopper "initiates checkout"
           to context StoreFront

      step from context StoreFront "creates the order"
           to context Orders

      step from context Orders "requests payment capture"
           to context Payments

      step from context Orders "reports the order is confirmed"
           to context StoreFront

      step from context StoreFront "shows the confirmation"
           to user Shopper
    }
  }
}
```

## Applications Model the User's Tool

A RIDDL Application defines the user interface through which users control
the system. It represents the system facade that permits user interaction.

### What is a User?

In RIDDL, "user" is a term of art. It doesn't necessarily mean a human being.
A user is anything that uses the system:

<!-- riddl: in-domain -->
```riddl
user Shopper is "a human customer browsing products"
user APIClient is "an automated system consuming our API"
user AIAssistant is "an AI providing recommendations"
```

### Application Components

Applications are composed of:

- **Groups** - Containers for related UI elements
- **Inputs** - Ways to receive information from the user
- **Outputs** - Ways to show information to the user

```
┌─────────────────────────────────────┐
│           APPLICATION               │
│  ┌─────────────────────────────────┐│
│  │           GROUP                 ││
│  │  ┌─────────┐  ┌─────────┐       ││
│  │  │  INPUT  │  │ OUTPUT  │       ││
│  │  └─────────┘  └─────────┘       ││
│  └─────────────────────────────────┘│
└─────────────────────────────────────┘
```

### Inputs

Inputs are manipulated by the user and send messages to the application:

<!-- riddl: in-domain -->
```riddl
application context StoreFront is {
  command SearchProducts is { text: String }
  command FilterByCategory is { category: String }

  group ProductSearch is {
    input SearchField acquires command SearchProducts
    input CategoryFilter acquires command FilterByCategory
  }
}
```

### Outputs

Outputs receive messages from the application and present them to the user:

<!-- riddl: in-domain -->
```riddl
application context StoreFront is {
  result ProductSearchResults is { matches: Natural }
  result ProductInfo is { name: String }

  group ProductDisplay is {
    output ProductList presents result ProductSearchResults
    output ProductDetails presents result ProductInfo
  }
}
```

### Navigation

Navigation occurs when user input causes the UI to change what it presents:

<!-- riddl: in-domain -->
```riddl
application context StoreFront is {
  type CartId is UUID
  command NavigateToCheckout is { cartId: CartId }

  group Navigation is {
    button CheckoutButton activates command NavigateToCheckout
  }

  handler NavigationHandler is {
    on command NavigateToCheckout {
      do "move the user to the CheckoutFlow group"
    }
  }
}
```

### Control

Control of the underlying system occurs when the application sends messages
to system components:

<!-- riddl: in-domain -->
```riddl
application context StoreFront is {
  command PlaceOrder is { cartId: UUID }
  command CreateOrder is { cartId: UUID }
  outlet OrdersOut is command CreateOrder

  handler OrderHandler is {
    on command PlaceOrder {
      send command CreateOrder(cartId = "a value") to outlet OrdersOut
    }
  }
}
```

## Applications as Processors

Because RIDDL applications process messages, they are considered Processors
and define:

- **Inlets** - Where messages are received for processing
- **Outlets** - Where the application sends messages
- **Handlers** - Logic that processes incoming messages

## The Application Boundary

RIDDL 2.0 makes the application boundary explicit and then enforces it. Two
rules follow from that, and together they are the main thing to know when
modeling UI in 2.0.

### UI requires an `application` context

A [group](../../../concepts/group.md) — under any of its aliases, including
`page`, `pane`, `dialog` and `form` — may only appear in a context declared
with the `application` intention:

<!-- riddl: in-domain -->
```riddl
application context StoreFront is {
  page ProductSearch is { ??? }
}
```

A group in a plain `context` is a hard **Error**. In RIDDL 1.x any context
holding groups was treated as an application by convention; now it must say so.

### Users interact only at the boundary

A [user](../../../concepts/user.md) must not reach past the application
straight into the domain. The five dedicated user-interaction steps —
`show output`, `select input`, `take input`, `focus` and `direct` — already
hard-type their non-user side, so they satisfy this by construction.

The two untyped steps do not, and are checked. In an arbitrary or
send-message step where exactly one side is a User, the other side must be a
UI element or a definition whose enclosing context has the `application`
intention. Otherwise it is an **Error**:

<!-- riddl: skip reason="deliberate counter-example; shows what does NOT work" -->
```riddl
// Error: the user reaches directly into a domain entity
step send command PlaceOrder from user Shopper to entity Order

// Correct: the user reaches the application, which reaches the entity
step take form StoreFront.Checkout from user Shopper
step send command PlaceOrder from context StoreFront to entity Order
```

This is why the two rules belong together: pinning UI to application contexts
is what makes "the application boundary" a thing the validator can locate.

## Reading and Writing UI Data

An application handler reads an input's value and publishes to an output with
two statements added in RIDDL 2.0:

<!-- riddl: in-domain -->
```riddl
application context StoreFront is {
  page Checkout is {
    form PaymentDetails accepts type PaymentInfo
    document Receipt shows type ReceiptData
  }

  handler CheckoutHandler is {
    on command SubmitPayment {
      let details = get from input PaymentDetails
      tell command Charge(details) to context Billing
      put "Payment received" to output Receipt
    }
  }
}
```

`put` is valid only in application and context handlers, which is another way
the boundary is enforced structurally rather than by convention.

## Choosing Verbs

The verb in an input or output declaration is not decorative — one family of
them is checked.

**Acquisition verbs** (inputs): `acquires`, `reads`, `takes`, `accepts`,
`admits`, `enters`, `provides`, `selects`, `chooses`, `picks`, `initiates`,
`submits`, `triggers`, `activates`, `starts`

**Presentation verbs** (outputs): `presents`, `shows`, `displays`, `writes`,
`emits`

!!! warning "Selection verbs expect a choice type"
    An input using `selects`, `chooses` or `picks` whose type is not an
    Enumeration or Alternation draws a **StyleWarning**. A selection widget
    should choose among options:

    <!-- riddl: skip reason="two depths in one fence -- a context-level type above group-level widgets -- and the second widget is a deliberate counter-example marked StyleWarning" -->
    ```riddl
    type Country is any of { US, CA, MX, UK }

    picklist CountryChooser selects type Country   // fine
    text     Nickname       picks   type String    // StyleWarning
    ```

    It is never an Error — a predefined type is treated as
    resolved-but-not-a-choice, and a genuinely unresolved reference is skipped
    so this does not pile onto the real error.

    Noun/verb combinations are otherwise unconstrained. An earlier draft of
    RIDDL 2.0 warned when a `picklist` was paired with a non-selection verb;
    that check was removed, because all such combinations are legitimate.

## Linking to Designs

Beyond `shown by`, a UI definition may carry a structured
[figma reference](../../../concepts/metadata.md#figma-references) resolving to
one specific frame:

<!-- riddl: in-app-context -->
```riddl
page Checkout is { ??? } with {
  figma "aBcD1234" node "42:1337"
}
```

Unlike an opaque URL, this is machine-readable, so `riddlc --check-figma-drift`
can verify the frame still exists and still corresponds to the definition's
name. Drift checking is off by default and cannot affect an offline build.

## RIDDL and User Experience

RIDDL recognizes that UX is an art and science of its own. Applications do not
model the look, feel, or sensory aspects of user interfaces. Instead, they use
the `shown by` syntax to link to external UX artifacts:

<!-- riddl: in-app-context -->
```riddl
group CheckoutForm is {
  output OrderSummary presents result OrderDetails
  shown by { https://figma.com/checkout-summary-design }
}
```

This separation allows:

- UX designers to work with illustrations, wireframes, and prototypes
- RIDDL authors to focus on logical and functional details
- Both perspectives to reference each other

## Example: Complete Shopping Application

```riddl
domain ECommerce is {
  user Shopper is "a customer using the store"

  application context StoreFront is {

    // The vocabulary the UI elements and handlers exchange
    command SearchProducts is { text: String }
    command RemoveFromCart is { item: String }
    command UpdateItemQuantity is { item: String, quantity: Natural }
    command StartCheckout is { cartId: UUID }
    command SetShippingAddress is { address: String }
    command ProcessPayment is { amount: Currency(USD) }
    command ChargePayment is { amount: Currency(USD) }
    command RemoveCartItem is { item: String }
    query FindProducts is { text: String }
    result ProductList is { matches: Natural }
    result ProductDetails is { name: String }
    result CartItems is { count: Natural }
    result OrderConfirmed is { orderId: UUID }

    outlet CatalogOut is query FindProducts
    outlet CartOut is command RemoveCartItem
    outlet PaymentsOut is command ChargePayment

    // Product browsing
    group ProductCatalog is {
      input SearchBox acquires command SearchProducts
      output ProductGrid presents result ProductList
      output ProductCard presents result ProductDetails
    }

    // Shopping cart
    group ShoppingCart is {
      output CartContents presents result CartItems
      input RemoveItem acquires command RemoveFromCart
      input UpdateQuantity acquires command UpdateItemQuantity
      button CheckoutButton activates command StartCheckout
    }

    // Checkout flow
    group CheckoutFlow is {
      input ShippingForm acquires command SetShippingAddress
      input PaymentForm acquires command ProcessPayment
      output OrderConfirmation presents result OrderConfirmed
    }

    // Handlers
    handler ProductHandler is {
      on command SearchProducts {
        send query FindProducts(text = "a value") to outlet CatalogOut
      }
      on result ProductList {
        put result ProductList(matches = ProductList.matches) to output ProductGrid
      }
    }

    handler CartHandler is {
      on command RemoveFromCart {
        send command RemoveCartItem(item = "a value") to outlet CartOut
      }
    }

    handler CheckoutHandler is {
      on command StartCheckout {
        do "move the user to the CheckoutFlow group"
      }
      on command ProcessPayment {
        send command ChargePayment(amount = 1.00) to outlet PaymentsOut
      }
    }
  }
}
```

## Related Concepts

- [Epic](../../../concepts/epic.md) - Modeling user interactions
- [Application](../../../concepts/application.md) - Defining user interfaces
- [Use Case](../../../concepts/use-case.md) - Interaction sequences
- [User](../../../concepts/user.md) - Who uses the system
- [Input](../../../concepts/input.md) - User input elements
- [Output](../../../concepts/output.md) - Display elements
