# RIDDL Language Guide

## Overview

RIDDL (Reactive Interface to Domain Definition Language) is a domain-specific 
language designed for modeling reactive systems using Domain-Driven Design (DDD)
principles. It bridges the gap between business domain experts and software 
engineers by providing a language that's both expressive for domain modeling and
precise enough for implementation. This language was also designed to provide
a GPT AI Model with sufficient context to generate code accurately from the
specification. 

## Language Design Emphasis

RIDDL emphasizes:
- Declarative syntax with natural language readability
- Hierarchical structure with domains, (bounded) contexts, entities, streamlets,
  repositories, projectors, adaptors, and other definitions that specify the 
  behavior of a system. 
- Event-driven and reactive design patterns
- State-based entity modeling with explicit state transitions
- Streaming of data between components from inlet to outlet via connectors 
- Clear separation of commands, events, queries and results
- Saga-based coordination of complex atomic processes and possibly distributed
- Comprehensive domain modeling through DDD concepts
- Asynchronous, non-blocking communications (implied)

## Language Structure

### Definitions
Everything that has a name and can have metadata is known as a Definition in RIDDL.

### Branches
Branch definitions are containers that hold other definitions. They form the
hierarchical structure of a RIDDL model:
- **Root**: The implicit top-level container (not explicitly defined)
- **Module**: Organizes root content for large models
- **Domain**: Contains bounded contexts and domain-wide definitions
- **Context**: Contains entities, repositories, sagas, and other processors
- **Entity**: Contains states, handlers, functions, and message types
- **Epic**: Contains use cases describing user interactions
- **Saga**: Contains steps for multi-step processes with compensation

### Processors

Processors are definitions that can receive and process messages. They form the
active components of a RIDDL model:

- **Entity**: Stateful processor with commands, events, states, and handlers.
  Entities are the primary business objects that maintain state and respond to
  commands.
- **Adaptor**: Translates messages between contexts. Defined with a direction
  (`from` or `to`) relative to a context.
- **Repository**: Handles persistence of data. Contains schemas and handlers
  for storage operations.
- **Projector**: Projects events to a repository, often transforming or
  aggregating data for read models (CQRS pattern).
- **Streamlet**: Processes streaming data. Subtypes include `source`, `sink`,
  `flow`, `merge`, `split`, `router`, and `void`.
- **Saga**: Orchestrates multi-step processes with compensation logic for
  failure recovery.

All processors can contain handlers, functions, types, and other processor-
specific definitions.

### Domain Hierarchy

RIDDL models are organized hierarchically:
- **Root**: The top-level container for the entire system. Roots are not defined but 
  consist of the top level definitions in a file. Roots can contain Modules,
  Domains, and Authors
- **Nebula**: The top-level container to be used as a scratch pad. It can contain any of the main
  definitions without regard to structure. 
- **Module**: A way of modularizing root content for large models that need to save compilation 
  output 
- **Domain**: A container for the specification of some knowledge domain. Domains 
  may only contain Contexts
- **Context**: Bounded context containing related entities and components. Also used to model
  user interfaces from their data flow perspective. 
- **Entity**: Stateful business objects with commands, events, and handlers
- **Repository**: Persistent storage for entities
- **Projector**: A component that projects messages, typically events, to a repository for later 
  retrieval, possibly transforming the data or merging multiple streams of events. 
- **Saga**: A component that defines the orchestration of multi-step atomic process with 
  compensation actions to undo the process when errors arise.
- **Epic**: A collection of use cases to show an expected usage pattern
- **Case**: A specific user interaction flow

The hierarchy follows strict containment rules: Root → Module/Domain → Context →
Entity/Repository/Saga/Streamlet → States/Handlers/Functions. Each level can
only contain specific definition types as detailed in the Containment Rules
section below.

### Data Types

RIDDL has a rich type system supporting both simple and complex data structures:

**Predefined Types:**
- **Strings**: `String`, `String(min,max)` with length constraints
- **Numbers**: `Integer`, `Natural`, `Whole`, `Real`, `Number`, `Decimal(w,f)`
- **Boolean**: `Boolean`
- **Temporal**: `Date`, `Time`, `DateTime`, `TimeStamp`, `Duration`,
  `ZonedDateTime(zone)`
- **Identifiers**: `UUID`, `UserId`, `Id(entity path)`
- **Other**: `URL`, `URL(scheme)`, `Currency(code)`, `Location`, `Nothing`,
  `Abstract`
- **Physical**: `Length`, `Mass`, `Current`, `Temperature`, `Luminosity`, `Mole`

**Pattern Types:**
- `Pattern("regex")` - String matching a regular expression

**Compound Types:**
- **Aggregation**: `{ field1 is Type1, field2 is Type2 }` - Named field collections
- **Alternation**: `one of { TypeA, TypeB, TypeC }` - Union/sum types
- **Enumeration**: `any of { Value1, Value2, Value3 }` - Enumerated values

**Collection Types:**
- **Sequence**: `sequence of Type` or `many Type`
- **Set**: `set of Type`
- **Mapping**: `mapping from KeyType to ValueType`
- **Optional**: `optional Type` or `Type?`

**Special Types:**
- **Entity Reference**: `reference to entity Path`
- **Unique ID**: `Id(entity Path)` - Type-safe entity identifier

### Basic Syntax Elements

1. **Readability Words**: Optional words that improve human readability of a model
   - The complete list is: `and`, `are`, `as`, `at`, `by`, `for`, `from`, `in`, `is`, `of`, `so`,
     `that`, `to`,  and `wants`
   - A synonym for `is` is `:`
   - These words are accepted by the grammar but not required. 

2. **Definition Structure**:
   ```
   [type] [name] is {
     // definition contents
   } with {
     // meta data
   }
   ```
   - The `[type]` indicates the kind of definition (domain, context, entity, etc.)
   - The `[name]` is the identifier for this definition which must be unique amongst its peers.
   - The "definition contents" depend on the `[type]` of definition being defined. 
   The metadata section (with `briefly` and `described by`) must always come 
   after the closing brace of the definition, not within it.

3. **Type References**: Always specify the kind of reference
   - `entity Product`
   - `command CreateCart`
   - `event OrderCreated`
   - `state ProductData`
   - `user Customer`

## Containment Rules

RIDDL follows strict containment rules that define what elements can be defined within other elements:

1. **Domain** can contain:
   - Authors (metadata)
   - Types
   - Contexts
   - Nested Domains
   - Users
   - Epics

2. **Context** can contain:
   - Types
   - Entities
   - Repositories
   - Sagas
   - Streamlets
   - Pages (UI components)

3. **Entity** can contain:
   - States
   - Commands
   - Events
   - Functions
   - Handlers

4. **Authors** contain only their metadata and cannot contain any other RIDDL definitions.

## Type System

### Basic Types
- `UUID`, `String(min, max)`, `Integer`, `Decimal(whole, fractional)`
- `Boolean`, `Pattern("regex")`, `Real`, `Natural`, etc.

### Complex Types
- **Record Types**: Named collections of fields
  ```
  type Address is {
    street1 is String
    city is String
    state is String
    zipCode is String
    country is String
  } with {
    briefly as "Physical mailing address"
    described by {
      | Represents a physical address with standard components
      | used for shipping and billing purposes.
    }
  }
  ```

- **Enumerations**:
  ```
  type Status is any of {
    Active
    Inactive
    Suspended
  } with {
    briefly as "Possible entity statuses"
    described by {
      | Defines the possible states for an entity's lifecycle.
    }
  }
  ```

- **Collections**:
  ```
  items is many Item
  ```

## Entities and States

Entities are stateful objects with explicit states:

```
entity Product is {
  state ProductData of ProductRecord with {
    briefly as "Product state containing all product information"
    described by {
      | Contains the complete product information including identification,
      | pricing, and inventory information.
    }
  }
  
  // Commands, events, handlers
} with {
  briefly as "Represents a purchasable item"
  described by {
    | The Product entity represents items that can be purchased.
    | It contains all product attributes and responds to commands.
  }
}
```

States reference record types that define the data structure:

```
type ProductRecord is {
  id is ProductId
  name is Name
  price is Price
  // other fields
} with {
  briefly as "Record type containing product data"
  described by {
    | Defines the structure of product data including identification and pricing.
  }
}
```

## Commands and Events

Commands represent requests to change state:

```
command UpdatePrice is {
  productId is ProductId
  newPrice is Price
} with {
  briefly as "Command to change a product's price"
  described by {
    | Updates the price of a specific product identified by productId.
    | The new price must be a positive value.
  }
}
```

Events represent state changes that have occurred:

```
event PriceUpdated is {
  productId is ProductId
  oldPrice is Price
  newPrice is Price
} with {
  briefly as "Event indicating a product price change"
  described by {
    | Emitted when a product's price is successfully updated.
    | Contains both old and new prices for auditing and UI updates.
  }
}
```

### Command-Event Relationship

Commands should always result in one or more events being emitted. This follows the reactive principles of RIDDL:

```
handler ProductCommandHandler is {
  on command UpdatePrice is {
    when "newPrice > 0" then {
      morph entity Product to state ProductData with command UpdatePrice
      tell event PriceUpdated to entity Product  // Emitting an event is essential
    } end
  }
} with {
  briefly as "Processes commands for product management"
  described by {
    | Handles commands related to product information management.
    | Validates input data, updates product state, and emits relevant events.
  }
}
```

## Handlers

Handlers process commands and emit events:

```
handler ProductCommandHandler is {
  on command UpdatePrice is {
    when "newPrice > 0" then {
      morph entity Product to state ProductData with command UpdatePrice
      tell event PriceUpdated to entity Product
    } end
    when "newPrice <= 0" then {
      error "Price must be greater than zero"
    } end
  }
} with {
  briefly as "Processes commands for product management"
  described by {
    | Handles commands related to product information and pricing management.
    | Validates input data, updates product state, and emits relevant events.
  }
}
```

## Statement Syntax

### Morph Statement
Changes entity state:
```
morph entity Product to state ProductData with command UpdatePrice
```

### Tell Statement
Sends events or commands:
```
tell event ItemAdded to entity Cart
tell command ProcessPayment to entity PaymentService
```

### Set Statement
Assigns values to fields:
```
set field status to "Active"
```

### Let Statement
Creates a local variable binding:
```
let totalPrice = "subtotal + tax + shipping"
```

### When Statement
Conditional logic (replaces the former `if` statement):
```
when "condition" then {
  // actions
} end
```

The `end` keyword is required to terminate when statements.

**Condition Types:**
The `when` statement accepts three forms of conditions:
- Literal string: `when "user is authenticated" then`
- Identifier reference: `when authorized then` (using a `let` binding)
- Negated identifier: `when !authorized then`

**Optional Else Block:**
An `else` clause can handle the false case:
```
let authorized = "user has permission"
when authorized then {
  send event ActionCompleted to outlet Events
} else {
  error "User not authorized"
} end
```

Alternatively, use multiple `when` statements with negation:
```
when authorized then { ... } end
when !authorized then { ... } end
```

### Match Statement
Pattern matching for multiple conditions:
```
match "orderStatus" {
  case "pending" {
    tell event OrderPending to entity Order
  }
  case "shipped" {
    tell event OrderShipped to entity Order
  }
  case "delivered" {
    tell event OrderDelivered to entity Order
  }
  default {
    error "Unknown order status"
  }
}
```

### Prompt Statement
Describes an action in natural language for implementation:
```
prompt "Calculate the total price including all applicable taxes and discounts"
```

This is useful for describing complex business logic that will be implemented
in target code.

## Functions

Functions define reusable operations:

```
function calculateTotal is {
  requires {
    subtotal is Price
    taxes is Price
    shipping is Price
    discount is Price
  }
  returns {
    total is Price
  }

  // Implementation using prompt statement
  prompt "Calculate total by adding subtotal, taxes, and shipping, then subtracting discount"
} with {
  briefly as "Calculates the final cart total"
  described by {
    | Calculates the final amount by adding subtotal, taxes, and shipping,
    | then subtracting any discounts.
  }
}
```

## Sagas

Sagas coordinate multi-step processes with compensation:

```
saga CheckoutProcess is {
  requires {
    cartId is CartId
    customerInfo is CustomerInfo
  }
  
  returns {
    success is Boolean
    orderId is UUID
  }
  
  step ProcessPayment is {
    // Payment processing logic
    tell command ProcessPayment to entity PaymentService
  } reverted by {
    // Compensation logic to refund
    tell command RefundPayment to entity PaymentService
  } with {
    briefly as "Processes payment for the order"
    described by {
      | Attempts to process payment using the provided payment details.
      | If payment fails, the checkout process is aborted.
      | If later steps fail, payment is refunded as part of compensation.
    }
  }
  
  // Additional steps
} with {
  briefly as "Orchestrates the checkout process steps"
  described by {
    | This saga orchestrates the multi-step process of completing a checkout,
    | including validating the cart and inventory, processing payment,
    | creating an order, and sending confirmation.
  }
}
```

## Repositories

Repositories define persistence:

```
repository CartRepository is {
  schema CartData is relational of
    cart as Cart
    link cartItems as field Cart.items.id to field Product.id

  handler CartRepositoryHandler is {
    on event CartCreated is {
      prompt "Persist the new cart record to the database"
    }

    // Other event handlers
  } with {
    briefly as "Handles persistence of cart events"
    described by {
      | Handles all event-driven persistence operations related to shopping carts.
      | Responds to cart events by updating the persistent state of carts.
    }
  }
} with {
  briefly as "Persistent storage for shopping cart data"
  described by {
    | The CartRepository provides persistent storage for shopping cart data,
    | including the cart itself and all items within it.
  }
}
```

## UI Components

RIDDL supports UI modeling:

```
context UserInterface is {
  page ProductDetails is { /* ... */ } with {
    briefly as "Page showing product information"
    described by {
      | Displays detailed information about a product including name,
      | description, price, and images.
    }
  }
  
  page ShoppingCart is {
    button Checkout activates type Boolean with {
      briefly as "Checkout button to proceed to payment"
      described by {
        | Button that initiates the checkout process when clicked.
        | Transitions the user from the shopping cart view to the 
        | checkout information entry page.
      }
    }
  } with {
    briefly as "Page showing cart contents"
    described by {
      | Displays all items added to the cart with quantities and prices.
      | Allows customers to update quantities and proceed to checkout.
    }
  }
  
  page Payment is {
    form PaymentEntry submits type PaymentDetails with {
      briefly as "Form for entering payment information"
      described by {
        | Collects payment method and details from the customer.
        | Payment information is tokenized for security before processing.
      }
    }
  } with {
    briefly as "Page for payment processing"
    described by {
      | Allows customers to enter and submit payment information.
    }
  }
} with {
  briefly as "User interface components for the system"
  described by {
    | Contains all UI components used in the system including
    | product details, shopping cart, and checkout pages.
  }
}
```

## Epics and Use Cases

Epics model user stories:

```
epic ShoppingCartEpic is {
  user Customer wants to "add items to a shopping cart" 
  so that "they can purchase multiple items at once"
  
  case AddingToCart is {
    user Customer wants to "add products to cart" 
    so that "they can purchase them later"
    
    step from user Customer "views" page UserInterface.ProductDetails
    step send command AddToCart from user Customer to entity Cart
    step from entity Cart "updates" to page UserInterface.ShoppingCart
    step focus user Customer on page UserInterface.ShoppingCart
  } with {
    briefly as "Adding products to the shopping cart"
    described by {
      | This use case describes the process of a customer adding a product
      | to their shopping cart from a product detail page.
    }
  }
  
  // Additional cases
} with {
  briefly as "User stories related to shopping cart management"
  described by {
    | This epic covers the core shopping cart functionality including
    | adding items to carts, updating quantities, and removing items.
  }
}
```

## Metadata Placement

Metadata should always be placed after the closing brace of the definition, not within it:

**Correct:**
```
entity Product is {
  // Entity definition content
} with {
  briefly as "Product available for purchase"
  described by {
    | Represents a product in the catalog that customers can purchase.
    | Contains pricing, inventory, and product details.
  }
}
```

**Incorrect:**
```
entity Product is {
  // Entity definition content
  with {  // <-- This is wrong
    briefly as "Product available for purchase"
    described by {
      | Represents a product in the catalog that customers can purchase.
      | Contains pricing, inventory, and product details.
    }
  }
}
```

## Best Practices

1. **Include Metadata**: Add descriptions to all definitions with `with` clauses after their closing braces
2. **Be Explicit**: Always specify reference types (entity, command, event, etc.)
3. **Place Functions Close to Usage**: Define functions within the entities that use them
4. **End When Statements**: Always terminate `when` statements with the `end` keyword
5. **Use Match for Multiple Conditions**: Prefer `match` over multiple `when` statements for readability
6. **Use Prompt for Complex Logic**: Use `prompt` to describe business logic for implementation
7. **Model Complete Flows**: Include UI components and user interactions
8. **Maintain Semantic Consistency**: Use the same field names for the same concepts
9. **Emit Events from Commands**: Ensure commands emit events to follow reactive principles
10. **Document UI Components**: Provide clear descriptions for UI elements that interact with users
11. **Follow Containment Rules**: Only define elements within their appropriate containers (domain, context, entity, etc.)
12. **Separate Metadata**: Always place metadata sections after a definition's closing brace, never inside it

## Common Syntax Issues

1. Don't use assignment operators (`=`) for fields; use `set field x to "value"` (but `let x = "value"` is valid for local bindings)
2. Don't forget `end` after `when` statements
3. Always include reference types before identifiers
4. Use proper syntax for function parameters and return values
5. Make sure all morph/tell statements have correct type references
6. Place comments only where definitions are allowed, not within clauses
7. Ensure metadata blocks follow their definitions rather than being nested within them
8. Never place entity, type, or repository definitions directly within a domain - they must be in a context
9. Never place definitions inside an author - authors only contain metadata
10. Make sure each context contains related definitions that form a bounded context
11. Use `when` for conditionals (not `if` which is no longer supported)
12. Use `prompt` for describing implementation logic (not bare quoted strings)

## Incomplete Definitions

Use `???` as a placeholder for incomplete definitions:

```
record PaymentDetails is { ??? } with {
  briefly as "Record for payment information details"
  described by {
    | Contains all payment information required for processing.
  }
}

page Checkout is { ??? } with {
  briefly as "Checkout page for completing purchase"
  described by {
    | Allows customers to review items and provide checkout information.
  }
}
```

## Author Inheritance

Authors are defined once and inherited throughout the model hierarchy, but cannot contain any definitions:

```
domain ShopifyCart is {
  author Claude is {
    name is "Anthropic Claude"
    email is "support@anthropic.com"
  } with {
    briefly as "Model creator and maintainer"
    described by {
      | Primary architect responsible for designing this model.
    }
  }
  
  // All definitions within the domain inherit Claude as author
  context ShoppingContext is {
    // No need to repeat author information here
  } with {
    briefly as "Main shopping context containing commerce entities"
    described by {
      | The ShoppingContext is the primary bounded context for the shopping system.
    }
  }
} with {
  briefly as "Shopping cart domain model"
  described by {
    | This domain model represents a shopping cart system.
    | It includes core entities, commands, events, and processes.
  }
}
```

## Additional Syntax Clarifications

From the formal grammar analysis, several important syntax points deserve special emphasis:

1. **Sequential Execution**: Statement blocks are executed sequentially, and while actions appear to flow naturally, there's no "implicit flow" - each action in handlers and functions must be explicitly defined.

2. **Reference Type Consistency**: When referring to entities, commands, events, etc., always use the correct reference type (e.g., `entity Product`, not just `Product`).

3. **Nested Element Validation**: Elements can only be nested within specific parent elements according to strict containment rules. For example, types must be defined within contexts, not directly within domains.

4. **Termination of Statements**: Control flow statements must be properly terminated:
   - `when` statements must end with the `end` keyword
   - `match` statements are terminated by the closing brace
   - Other statements are implicitly terminated

5. **Handler Clauses**: Handlers must use specific clause types:
   - `on command X` for command handlers
   - `on event X` for event handlers
   - `on init` for initialization
   - `on term` for termination
   - `on other` for default/catch-all behavior

6. **Readability Words**: While readability words like `is`, `as`, `by`, etc. are often optional, their proper placement significantly improves model clarity. Use them consistently.

7. **New Statement Types** (as of January 2026):
   - `when` replaces the former `if-then-else` statement
   - `match` provides pattern matching for multiple conditions
   - `let` creates local variable bindings
   - `prompt` replaces bare quoted strings for describing implementation logic

8. **Removed Statements**: The following statements have been removed from the language:
   - `if`, `foreach`, `call`, `stop`, `focus`, `reply`, `return`, `read`, `write`
   - Use `when` for conditionals, `match` for pattern matching, and `prompt` for implementation descriptions

