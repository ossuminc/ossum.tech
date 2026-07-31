---
title: "User Interface Modeling"
description: "Using RIDDL to design user interfaces with Epics and Applications"
---

# User Interface Modeling

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
  epic ShoppingCartJourney is {
    user Shopper is "A customer browsing and purchasing products"

    case BrowseAndPurchase is {
      user Shopper wants to "browse products and complete a purchase"
        so that "they can receive desired items"

      // Step 1: Browse products
      step from user Shopper "views product catalog"
           to application StoreFront "displays products"

      // Step 2: Add to cart
      step from user Shopper "selects items"
           to context Inventory "reserves items"

      // Step 3: Checkout
      step from user Shopper "initiates checkout"
           to context Orders "creates order"

      // Step 4: Payment
      step from user Shopper "provides payment"
           to context Payments "processes payment"

      // Step 5: Confirmation
      step from context Orders "confirms order"
           to user Shopper "receives confirmation"
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

<!-- riddl: skip reason="illustrative fragment; references vocabulary this page does not define" -->
```riddl
application context StoreFront is {
  group ProductSearch is {
    input SearchField acquires command SearchProducts
    input CategoryFilter acquires command FilterByCategory
  }
}
```

### Outputs

Outputs receive messages from the application and present them to the user:

<!-- riddl: skip reason="illustrative fragment; references vocabulary this page does not define" -->
```riddl
application context StoreFront is {
  group ProductDisplay is {
    output ProductList presents result ProductSearchResults
    output ProductDetails presents result ProductInfo
  }
}
```

### Navigation

Navigation occurs when user input causes the UI to change what it presents:

```riddl
application context StoreFront is {
  command NavigateToCheckout is { cartId: CartId }

  group Navigation is {
    input CheckoutButton directs user Shopper with command NavigateToCheckout
  }

  handler NavigationHandler is {
    on command NavigateToCheckout {
      focus on group CheckoutFlow
    }
  }
}
```

### Control

Control of the underlying system occurs when the application sends messages
to system components:

```riddl
application context StoreFront is {
  handler OrderHandler is {
    on command PlaceOrder {
      send command CreateOrder to context Orders
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

<!-- riddl: skip reason="illustrative fragment; references vocabulary this page does not define" -->
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

    <!-- riddl: skip reason="illustrative fragment; references vocabulary this page does not define" -->
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

<!-- riddl: skip reason="illustrative fragment; references vocabulary this page does not define" -->
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

```riddl
group CheckoutForm is {
  output OrderSummary presents result OrderDetails
    shown by "https://figma.com/checkout-summary-design"
}
```

This separation allows:

- UX designers to work with illustrations, wireframes, and prototypes
- RIDDL authors to focus on logical and functional details
- Both perspectives to reference each other

## Example: Complete Shopping Application

```riddl
domain ECommerce is {
  application context StoreFront is {
    // Define user
    user Shopper is "a customer using the store"

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
      input CheckoutButton directs user Shopper with command StartCheckout
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
        send query FindProducts to context Catalog
      }
      on result ProductList {
        show result ProductList on output ProductGrid
      }
    }

    handler CartHandler is {
      on command RemoveFromCart {
        send command RemoveItem to context Cart
      }
    }

    handler CheckoutHandler is {
      on command StartCheckout {
        focus on group CheckoutFlow
      }
      on command ProcessPayment {
        send command ChargePayment to context Payments
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
