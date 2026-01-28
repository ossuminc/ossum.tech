---
title: "What is RIDDL Based On?"
date: 2022-02-24T14:15:51-07:00
draft: false
weight: 30
---

The RIDDL specification language borrows concepts from:

* [Domain Driven Design (DDD)](https://en.wikipedia.org/wiki/Domain-driven_design)
* [Reactive System Architecture (RSA)](https://www.reactivemanifesto.org/)
* [C4 Model Of Software Architecture](https://c4model.com)
* [Akka](https://akka.io)
* [Jacobsen Use Cases 2.0](https://www.ivarjacobson.com/publications/white-papers/use-case-20-e-book)
* [Agile User Stories](https://en.wikipedia.org/wiki/User_story)
* [Behavior Driven Development (BDD)](https://en.wikipedia.org/wiki/Behavior-driven_development)
* [Finite State Machines](https://en.wikipedia.org/wiki/Finite-state_machine)
* [Command/Query Separation](https://en.wikipedia.org/wiki/Command%E2%80%93query_separation)
* [CQRS](https://martinfowler.com/bliki/CQRS.html)
* [Event Sourcing](https://learn.microsoft.com/en-us/azure/architecture/patterns/event-sourcing)
* [Saga Pattern](https://microservices.io/patterns/data/saga.html)
* [Unified Modeling Language (UML)](https://en.wikipedia.org/wiki/Unified_Modeling_Language)

RIDDL aims to capture business concepts, system designs, and architectural
details in a way that is consumable by business professionals yet structured
enough to enable translation into various artifacts:

* Living documentation that stays in sync with the model
* Architectural diagrams (context maps, sequence diagrams, state machines)
* Code scaffolding and implementation templates
* API specifications and deployment configurations

Because RIDDL captures both structure and intent, delivery teams can iterate
on the design while tools generate appropriate outputs for each stage of
development.

## Domain Driven Design (DDD)
RIDDL is based on concepts from 
[DDD](https://en.wikipedia.org/wiki/Domain-driven_design). This allows domain 
experts and technical teams to work at a higher level of abstraction by 
co-creating a ubiquitous language for the target domain enabling them to 
develop a system specification that is familiar and comprehensible by business 
and technical leaders alike.

For best comprehension of the RIDDL language, it is best to be familiar with
DDD concepts. For a four-minute overview 
[watch this video](https://elearn.domainlanguage.com/). 
For a more in depth understanding we recommend reading Vaughn Vernon's more 
concise book
[Domain Driven Design Distilled](https://www.amazon.com/Domain-Driven-Design-Distilled-Vaughn-Vernon/dp/0134434420/),
or Eric Evans' original tome [Domain Driven Design: Tackling Complexity in the Heart of Software](https://www.amazon.com/Domain-Driven-Design-Tackling-Complexity-Software/dp/0321125215/)

## Reactive System Architecture (RSA)
The [Reactive Manifesto](https://www.reactivemanifesto.org/) was authored in
2014 by Jonas Bonér, Dave Farley, Roland Kuhn, and Martin Thompson. As the
computing landscape evolved and companies began to operate at "internet scale"
it became evident that the old ways of constructing systems were not adequate.
We needed an approach to system architecture back then that was fundamentally
different in order to meet user expectations.

The central thesis of reactive architectures is that the overriding objective
in any system must be responsiveness. Users are conditioned to expect systems
that perform well and are generally available. If these conditions are not met,
users tend to go elsewhere to get what they want. That, of course, is clearly
unacceptable for any business endeavor. To remain responsive to users, a
system must address several challenges:

* system or component failure (resiliency)
* increasing work load (scalability)
* high operational cost (efficiency)
* slow responses (performance)

A reactive system aims to be responsive in the face of all of these challenges.  

Without going into too much detail here, among the key means of achieving 
responsiveness is to decompose the concerns of a domain into well isolated 
blocks of functionality (DDD), and then, establishing clear non-blocking, 
asynchronous, message-driven interfaces between them. Together, the concepts 
of, Responsiveness, Elasticity, Resiliency, and Message-Driven form the basis
of a Reactive Architecture.

To get more information on Reactive Architecture please refer to the excellent
6 part course by Lightbend. You can find the first course in that series
[here](https://academy.lightbend.com/courses/course-v1:lightbend+LRA-IntroToReactive+v1/about).

![Reactive Architecture Overview](../../assets/images/ReactiveArchitectureOverview.svg){ align=center, loading=lazy }

## Unified Modeling Language (UML)
One of the key insights brought forward by UML is that it is far easier for 
humans to comprehend the intended design of a system by communicating these 
ideas with pictures. UML is a language of very precise graphical symbols that
communicate different concerns of a system design.

This idea has been further leveraged by other design artifacts and activities.
For example, a very common DDD exercise is called Event Storming. In this 
exercise a group of experts brainstorms about the things that happen, concrete
events, within a system. Event Storming uses a very low fidelity tool to capture 
the details of the exercise. In this exercise, traditionally events are captured
first on orange sticky notes. The commands that generate those notes are then
captured on blue stickies. And the actors that initiate those commands are
captured on yellow stickies. And so on. More information on event storming can
be found [here](https://en.wikipedia.org/wiki/Event_storming) and 
[here](https://www.lucidchart.com/blog/ddd-event-storming)

RIDDL uses many of the design artifacts detailed under the UML specification 
to help communicate the design and intent of a system. For example, Sequence
Diagrams are used extensively to document the interactions between bounded
contexts in a system. A State Machine Diagram may be used to document the 
lifecycle of an entity or user in a system, and so on. However, RIDDL's
diagram output is not limited to UML diagrams. Peter Chen's 1971 invention of 
the entity relationship diagram is very well adapted to the concept of entity
in DDD. DDD also has its own diagrams:
* the System Context Diagram provides a depiction of the actors, internal 
  systems, external systems, and how they interact (use cases).
* the Context Map is a high level diagram that portrays the general 
  relationships between bounded contexts.
* Business Use Case Diagram - same idea as the UML version but simpler

More on that can be found [here](https://medium.com/nick-tune-tech-strategy-blog/domain-driven-architecture-diagrams-139a75acb578)

## Jacobsen Use Cases 2.0

Ivar Jacobson, one of the founders of UML, developed
[Use Case 2.0](https://www.ivarjacobson.com/publications/white-papers/use-case-20-e-book)
as a modernized, lightweight approach to capturing system requirements.

Key principles from Use Case 2.0 that influence RIDDL:

- **Slices**: Use cases are "sliced" into smaller, implementable pieces that
  deliver value incrementally. RIDDL's `case` definitions within an `epic`
  support this incremental approach.

- **Stories within Use Cases**: Use Case 2.0 bridges traditional use cases
  with agile user stories. RIDDL combines both: epics contain the high-level
  user goal while cases capture specific interaction flows.

- **Test-Driven**: Use cases directly inform test scenarios. RIDDL's
  structured cases can be translated into acceptance tests.

- **Lightweight**: Use Case 2.0 emphasizes capturing just enough detail.
  RIDDL follows this by allowing both detailed specifications and high-level
  `???` placeholders during iterative refinement.

Example of Use Case 2.0 concepts in RIDDL:

```riddl
epic Checkout is {
  user Customer wants to "complete a purchase"
  so that "they receive their ordered items"

  // Each case is a "slice" of the use case
  case EnterShippingInfo is { /* ... */ }
  case SelectPaymentMethod is { /* ... */ }
  case ReviewAndConfirm is { /* ... */ }
  case ReceiveConfirmation is { /* ... */ }
}
```

## Agile User Stories
Agile user stories are used to capture the requirements of various components
within a system. In RIDDL, user stories are part of an  
[epic](../concepts/epic.md) definition 

As a [persona], I [want to], [so that]...

In other words, it provides WHO (persona), WHAT (want to), and WHY (so that). 


## Behavior Driven Design (BDD)

<blockquote>
Behavior-driven development was pioneered by Daniel Terhorst-North. It grew 
from a response to test-driven development (TDD), as a way to help programmers
on new agile teams “get straight to the good stuff” of knowing how to approach
testing and coding, and minimize misunderstandings. BDD has evolved into both
analysis and automated testing at the acceptance level.
<a href="https://cucumber.io/docs/bdd/history/">Cucumber Documentation</a></a>
</blockquote>

BDD provides a simple specification language named Gherkin which is used heavily
in RIDDL. Even if you are not familiar with the Gherkin language, it is simple 
enough and intuitive enough to be grasped quickly. 

Gherkin scenarios follow a simple structural pattern, like this:

* **SCENARIO**: *\<scenario description\>*
  * **GIVEN** *\<a precondition\>*
  * **WHEN** *\<an event occurs\>*
  * **THEN** *\<take an action\>*

RIDDL uses this structure to inform how handlers should process messages.
While RIDDL's statements aren't as rigid as Gherkin's Given-When-Then format,
the influence is clear: handlers respond to events (Given a condition, When
an event occurs) and take actions (Then do something).

If you've worked in agile circles or considered BDD as a tool for testing,
you'll find RIDDL's approach familiar. The emphasis on behavior over
implementation details, and the use of natural language to describe actions,
draws directly from BDD's philosophy.
