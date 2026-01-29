---
title: "Getting Started with RIDDL"
description: "A basic introduction to RIDDL concepts and syntax"
---

# Getting Started with RIDDL

This tutorial introduces the fundamental concepts of RIDDL through simple
examples. After completing this tutorial, you'll understand:

- How to structure a RIDDL specification
- The core building blocks: domains, contexts, entities
- How to define types and messages
- Basic handler patterns

## Your First RIDDL Specification

Every RIDDL specification starts with a domain. A domain represents a
knowledge area or business capability:

```riddl
domain Greeting is {
  context HelloWorld is {
    // Context contents go here
  }
}
```

## Adding Types

Types define the data structures in your domain:

```riddl
domain Greeting is {
  context HelloWorld is {
    type Name is String
    type Greeting is {
      recipient: Name,
      message: String
    }
  }
}
```

## Defining an Entity

Entities are stateful objects that respond to commands and emit events:

```riddl
domain Greeting is {
  context HelloWorld is {
    type Name is String

    entity Greeter is {
      state GreeterState of Greeter.State

      record State is {
        greetingsCount: Integer
      }

      command SayHello is { to: Name }
      event HelloSaid is { to: Name, message: String }

      handler GreeterHandler is {
        on command SayHello {
          send event HelloSaid(
            to = @SayHello.to,
            message = "Hello, " + @SayHello.to + "!"
          ) to Greeter
        }
      }
    }
  }
}
```

## Key Concepts Illustrated

### Domains

Domains group related concepts and provide namespace isolation. A real
system might have domains like `Sales`, `Inventory`, `CustomerService`.

### Contexts

Bounded contexts define clear boundaries within a domain. Each context has
its own ubiquitous language - the same term can mean different things in
different contexts.

### Entities

Entities are the core business objects. They:
- Have identity (each instance is unique)
- Have state (data that changes over time)
- Have behavior (handlers that process commands)

### Types

RIDDL supports rich type definitions:
- Simple types: `type UserId is UUID`
- Records: `type Address is { street: String, city: String }`
- Enumerations: `type Status is any of { Pending, Active, Closed }`
- Alternations: `type Response is one of { Success, Failure }`

### Messages

Commands and events are the primary communication mechanism:
- **Commands** - Requests to perform an action
- **Events** - Facts that have occurred
- **Queries** - Requests for information
- **Results** - Responses to queries

## Next Steps

Now that you understand the basics, explore the
[Reactive BBQ Case Study](rbbq/index.md) to see how these concepts apply
to a real-world domain model.

For detailed syntax, see the [Language Reference](../references/language-reference.md).
