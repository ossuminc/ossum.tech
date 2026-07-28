---
title: "Messages"
draft: false
---

Messages are a foundational concept in RIDDL because a RIDDL model implies 
an implementation that is a message-driven system per the 
[Reactive Manifesto](https://reactivemanifesto.org). Messages in RIDDL are 
a special case of an [aggregate type](type.md#aggregation) 
and the _lingua franca_ of many RIDDL definitions. They define the API for
all the [processors](./processor.md):
* [`adaptor`s](adaptor.md)
* [`context`s](context.md)
* [`entity`s](entity.md)
* [`processor`s](processor.md)
* [`projector`s](projector.md)
* and [`repository`s](repository.md)

These are the fundamental building blocks of a
[message-driven system](https://developer.lightbend.com/docs/akka-platform-guide/concepts/message-driven-event-driven.html).

## Differences Between Kinds of Messages
RIDDL follows
[Bertrand Meyer's](https://www.linkedin.com/in/bertrandmeyer/) notion of
[command/query separation](https://en.wikipedia.org/wiki/Command%E2%80%93query_separation)
which states, in the context of object-oriented programming in Eiffel that:
> every method should either be a command that performs an action, or a query
> that returns data to the caller, but not both. In other words, asking a
> question should not change the answer.[^1]

Consequently, RIDDL adheres to this principle and employs the notion in message
definitions since RIDDL is message-oriented not object-oriented. However, 
RIDDL also includes message types for the responses from commands and 
queries, events and results, respectively. The following subsections provide 
definitions of these four things

[^1]: Meyer, Bertrand. "Eiffel: a language for software engineering". p. 22


### Command
A directive to perform an action, likely resulting in a change to some 
information.

### Event
A recordable fact resulting from a change to some information.

### Query
A request for information from something

### Result
A response to a query containing the information sought. 

### A Record Is Not a Message

RIDDL has exactly **four** messages: command, event, query and result. A
`record` is *data*, not a message. It can never be sent, told, yielded, or
handled by an [on clause](onclause.md); it types an entity
[state](state.md) and supplies the payload of a `morph`.

!!! warning "Changed in RIDDL 2.0"
    In 1.x a `record` reference was accepted wherever a message reference was.
    It no longer is. `send`, `tell`, `yield` and `on <ref>` accept the four
    real messages only.

    The reference hierarchy now says so directly: `MessageRef` covers the four
    messages, and `RecordRef` sits beside it rather than beneath it.

### Declared Responses

A command or query may declare the response it produces, with an optional
`yields` clause between the identifier and the body:

```riddl
command PlaceOrder yields event OrderPlaced is {
  cartId is CartId
}

query GetOrder yields result OrderInfo is {
  orderId is OrderId
}
```

This makes the request/response pairing declarative, so a generator can emit
precise signatures rather than inferring them.

A command's `yields` must resolve to an **event**, and a query's to a
**result**; anything else is an **Error**, as is `yields` on a type that is
neither a command nor a query.

`yields` is **optional**. When declared, the handler for that message must
`yield` exactly that message, and a mismatch or a handler that never yields is
an Error. When not declared, a handler may still yield whatever it likes — so
adding `yields` to an existing model is opt-in, one message at a time.

### Summary
The various characteristics of the four kinds of messages are shown in the 
table below.

|  Kind   | Request? | Response? | Cancellable? |     Relationship      |
|:-------:|:--------:|:---------:|:------------:|:---------------------:|
| Command |   Yes    |    No     |     Yes      |      Independent      |
|  Event  |  Maybe   |    Yes    |      No      | Consequent Of Command |
|  Query  |   Yes    |    No     |     Yes      |      Independent      |
| Result  |    No    |    Yes    |      No      | Consequent Of Query   |

The truth table above helps you understand the relationship between the kind of
message and how it is handled by a model component. The sections below get 
even more specific.

#### How Messages Are Handled By Adaptors
|  Kind   | In Regard To Handling By Adaptor    |
|:-------:|:-----------------------------------:|
| Command |   Intent To Translate For Context   |
|  Event  |   Intent To Translate For Context   |
|  Query  |   Intent to Translate For Context   |
| Result  |   Intent to Translate For Context   |

#### How Messages Are Handled By Applications
|  Kind   |  In Regard To Handling By Application  |
|:-------:|:--------------------------------------:|
| Command |  Data given from user to application   |
|  Event  |             Not Applicable             |
|  Query  |             Not Applicable             |
| Result  | Data provided to user from application |

#### How Messages Are Handled By Contexts
|  Kind   |  In Regard To Handling By Context     |
|:-------:|:-------------------------------------:|
| Command | Intent To Take Some Stateless Action  |
|  Event  | Notification That a Command Completed |
|  Query  |    Intent to Read From The Context    |
| Result  |    Result Of Reading From Context     |

#### How Messages Are Handled By Entities
|  Kind   | In Regard To Handling By  Entity |   
|:-------:|:--------------------------------:|
| Command |  Intent To Modify Entity State   |
|  Event  |     Entity State Was Changed     |
|  Query  |   Intent To Read Entity state    |
| Result  |       Consequent Of Query        |

#### How Messages Are Handled By Streaming Processors
|  Kind   | In Regard To Handling By a Streaming Processor |
|:-------:|:---------------------------------------------:|
| Command |          Intent To Transform Or Route          |
|  Event  |         A Fact Arriving On An Inlet            |
|  Query  |        Intent To Interrogate The Stream        |
| Result  |         Response Emitted On An Outlet          |

#### How Messages Are Handled By Projectors
|  Kind   | In Regard To Handling By Projector  |
|:-------:|:-----------------------------------:|
| Command |         Rejected at parse time      |
|  Event  | The Projection's State Was Modified |
|  Query  |         Rejected at parse time      |
| Result  | Result Of Reading Projection State  |

A [projector](projector.md) is **event-only** as of RIDDL 2.0: `on command`,
`on query` and `on record` are rejected at parse time. Queries against
projected data are served by the [repository](repository.md) the projector
updates, not by the projector itself.

## Occurs In
All [Vital Definitions](vital.md)

## Contains
[Fields](field.md)
