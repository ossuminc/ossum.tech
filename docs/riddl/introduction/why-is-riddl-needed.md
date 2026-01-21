---
title: "Why Is RIDDL Needed?"
date: 2022-02-25T10:07:32-07:00
draft: false
weight: 60
---

## The Problem

Software development has become increasingly complex. Modern systems are
distributed, event-driven, and must operate at scale. Yet the gap between
business requirements and technical implementation remains wide:

- **Business experts** understand *what* the system should do but struggle to
  communicate precise requirements
- **Technical teams** understand *how* to build systems but often misinterpret
  business intent
- **Documentation** becomes outdated the moment it's written
- **Code generation** from specifications has been limited to narrow domains

The result? Miscommunication, rework, and systems that don't meet business needs.

## Historical Context

### The Rise of 4GLs (1990s)

In the 1990s, Fourth Generation Languages (4GLs) promised to let business
users create software without programming. Tools like PowerBuilder, Progress,
and various RAD environments made it easier to build database applications.

However, 4GLs had limitations:
- Tied to specific platforms and databases
- Poor support for distributed systems
- Limited scalability
- Vendor lock-in

### Specification Languages

Formal specification languages like Z, VDM, and Alloy provided mathematical
rigor but were too abstract for business users and too disconnected from
implementation for developers.

UML attempted to bridge this gap visually but:
- Diagrams don't compile or validate
- Multiple diagram types create fragmentation
- No direct path to implementation
- Tooling became complex and expensive

## The RIDDL Approach

RIDDL addresses these challenges with a different philosophy:

### 1. Business-Readable Specifications

RIDDL uses natural language constructs that domain experts can understand:

```riddl
domain OnlineRetail is {
  user Customer wants to "browse products and make purchases"

  epic Shopping is {
    case AddToCart is {
      user Customer "selects a product"
      then entity Cart "adds the item"
      then user Customer "sees updated cart"
    }
  }
}
```

The specification reads like requirements documentation, not code.

### 2. Formally Structured

Despite being readable, RIDDL has precise semantics:

- Every definition has a specific type and containment rules
- References are validated across the model
- Event flows and state transitions are explicit
- The compiler catches inconsistencies

### 3. Multi-Target Translation

A single RIDDL specification can generate:

- **Documentation**: Websites, API docs, architecture diagrams
- **Code Scaffolding**: Scala/Akka, Kalix, Kubernetes manifests
- **Analysis**: Dependency graphs, complexity metrics
- **Diagrams**: Context maps, sequence diagrams, state machines

### 4. AI-Ready

RIDDL was designed with AI code generation in mind:

- Structured enough for AI to understand context
- Detailed enough for accurate code generation
- Natural language descriptions guide implementation
- The `prompt` statement explicitly captures implementation intent

```riddl
handler OrderHandler is {
  on command CreateOrder {
    prompt "Validate inventory availability for all items"
    prompt "Calculate total including tax and shipping"
    prompt "Reserve inventory and create order record"
    send event OrderCreated to outlet Events
  }
}
```

AI systems can translate these prompts into actual implementation code while
maintaining the specified structure.

### 5. Self-Documenting

The specification *is* the documentation:

- `briefly` clauses provide glossary definitions
- `described by` blocks contain detailed documentation
- The model structure defines the architecture
- Generated documentation is always in sync with the specification

## Why Now?

Several trends make RIDDL timely:

1. **Distributed Systems Are Standard**: Microservices, event-driven
   architecture, and reactive systems are now the norm, not the exception.

2. **AI Can Write Code**: Large language models can generate implementation
   code from specifications, but need structured input to do so reliably.

3. **Domain-Driven Design Matured**: DDD concepts are well understood and
   provide a solid foundation for specification languages.

4. **Complexity Demands Rigor**: As systems grow more complex, informal
   documentation and tribal knowledge become insufficient.

## The Vision

RIDDL's originator, Reid Spencer, envisioned a future where:

- Business experts write specifications that directly inform implementation
- Technical teams focus on solving hard problems, not translating requirements
- Documentation is generated, not written separately
- AI assistants help author and implement specifications
- Systems are specified once and translated to many targets

RIDDL is a step toward that vision—a language that is simple enough for
business users, precise enough for validation, and structured enough for
code generation.
