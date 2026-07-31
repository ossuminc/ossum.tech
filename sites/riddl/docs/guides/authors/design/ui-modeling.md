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

```riddl
application StoreFront is {
  group ProductSearch is {
    input SearchField acquires command SearchProducts
    input CategoryFilter acquires command FilterByCategory
  }
}
```

### Outputs

Outputs receive messages from the application and present them to the user:

```riddl
application StoreFront is {
  group ProductDisplay is {
    output ProductList presents result ProductSearchResults
    output ProductDetails presents result ProductInfo
  }
}
```

### Navigation

Navigation occurs when user input causes the UI to change what it presents:

```riddl
application StoreFront is {
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
application StoreFront is {
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
  application StoreFront is {
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
