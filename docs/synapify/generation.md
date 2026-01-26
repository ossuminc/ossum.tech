# Code Generation Guide

!!! note "Coming Soon"
    Code generation integration is under active development. This guide
    describes the planned capabilities.

Synapify integrates with riddl-gen to transform your validated RIDDL models
into implementation artifacts. Rather than manually translating designs into
code, you generate a starting point that preserves your model's structure
and intent.

---

## Why Generate?

A RIDDL model captures the essential design of your system—domains, contexts,
entities, commands, events, and handlers. Code generation bridges the gap
between this design and working software.

**Benefits of generation:**

- **Accelerate implementation** by producing boilerplate automatically
- **Ensure consistency** between design and code structure
- **Reduce translation errors** that occur with manual coding
- **Maintain traceability** from requirements through implementation
- **Enable iteration** by regenerating after model changes

---

## How It Works

Synapify connects to riddl-gen via HTTP requests. When you generate artifacts:

1. **Synapify sends your validated model** to riddl-gen
2. **You select target platforms and options** for generation
3. **riddl-gen processes the model** and produces artifacts
4. **Artifacts are returned** to Synapify or written to a specified location
5. **You review and integrate** the generated code into your project

Generation produces a starting point, not finished software. Human developers
refine the generated code, implement business logic placeholders, and add
infrastructure details.

---

## Generation Targets

riddl-gen supports multiple output formats. Initial targets focus on
documentation and reactive microservices, with additional platforms planned.

### Documentation

Generate human-readable documentation from your model:

| Format | Description |
|--------|-------------|
| **AsciiDoc** | Technical documentation suitable for PDF or HTML |
| **Hugo** | Static site content for Hugo-based documentation sites |

Documentation generation extracts:

- Model structure and hierarchy
- Definition descriptions (`briefly` and `described as` content)
- Type definitions with field documentation
- Message catalogs (commands, events, queries)
- Glossary terms from `term` definitions

### Akka/Scala

Generate reactive microservice code targeting the Akka framework:

| Artifact | Description |
|----------|-------------|
| **Entity classes** | Akka Persistence actors with command handlers |
| **Message definitions** | Case classes for commands, events, queries |
| **Type definitions** | Scala case classes matching RIDDL types |
| **State classes** | Immutable state representations |
| **API endpoints** | Akka HTTP routes for external interfaces |

The generated Scala code follows Akka best practices:

- Event sourcing for entity persistence
- CQRS separation of commands and queries
- Cluster sharding for entity distribution
- Typed actors for compile-time safety

### Quarkus/Java (Planned)

Generate reactive microservice code targeting the Quarkus framework:

| Artifact | Description |
|----------|-------------|
| **Entity classes** | Hibernate Reactive entities |
| **Message definitions** | Java records for commands, events, queries |
| **Type definitions** | Java records matching RIDDL types |
| **API endpoints** | JAX-RS resources for external interfaces |

---

## Using Generation

### Prerequisites

Before generating code:

1. **Validate your model** - Generation requires a valid RIDDL model with no
   errors
2. **Complete handlers** - Handlers with `???` placeholders generate stub
   implementations
3. **Document thoroughly** - Descriptions become code comments and
   documentation

### Generation Workflow

1. **Open generation panel** in Synapify
2. **Select target** (documentation format or code platform)
3. **Configure options** for the selected target
4. **Choose output location** (download or write to directory)
5. **Generate** and review the results
6. **Integrate** generated artifacts into your project

### Configuration Options

Each target has specific options:

**Documentation:**

- Output format (single file vs. multiple files)
- Include/exclude specific sections
- Diagram generation settings

**Akka/Scala:**

- Package naming conventions
- Serialization format (JSON, Protobuf)
- Test scaffold generation
- Build file format (sbt, Mill)

**Quarkus/Java:**

- Package naming conventions
- Build file format (Maven, Gradle)
- Database configuration hints

---

## Understanding Generated Code

### Structure Mapping

RIDDL definitions map to code artifacts:

| RIDDL Definition | Generated Artifact |
|------------------|-------------------|
| Domain | Package/module namespace |
| Context | Service boundary/module |
| Entity | Actor/entity class with handlers |
| Type | Data class/record |
| Command | Inbound message class |
| Event | Outbound message class |
| Query | Request/response pair |
| Handler | Method implementations |

### Placeholder Implementation

Handlers containing pseudocode (quoted strings) or `???` markers generate
stub implementations:

**RIDDL:**
```riddl
on command AddItem {
  "validate item exists in catalog"
  "add item to cart with specified quantity"
  send event ItemAdded to outlet Events
}
```

**Generated Scala:**
```scala
def handleAddItem(cmd: AddItem): Effect[Event, State] = {
  // TODO: validate item exists in catalog
  // TODO: add item to cart with specified quantity
  Effect.persist(ItemAdded(...))
}
```

The structure is in place; developers fill in the implementation details.

### What's Not Generated

Generation produces structure, not complete applications. You still need to:

- **Implement business logic** in handler placeholders
- **Configure infrastructure** (databases, message brokers, etc.)
- **Add authentication/authorization** appropriate to your environment
- **Write tests** beyond the generated scaffolds
- **Handle deployment** configuration and orchestration

---

## Iterative Development

Generation supports an iterative workflow where model and implementation
evolve together.

### Initial Generation

Start with a basic model and generate initial scaffolding:

1. Define domains, contexts, and core entities
2. Add key commands and events
3. Generate code to establish project structure
4. Commit generated code as baseline

### Incremental Updates

As the model evolves:

1. Add new definitions or modify existing ones
2. Regenerate affected artifacts
3. Merge generated changes with existing implementations
4. Preserve custom code in designated areas

### Handling Conflicts

When regenerating after model changes:

- **New definitions** generate new files (no conflict)
- **Removed definitions** leave orphaned files (manual cleanup)
- **Modified definitions** may conflict with customizations

Strategies for managing conflicts:

- **Separate generated and custom code** into distinct directories
- **Use extension points** where generators provide hooks
- **Review diffs carefully** before accepting regenerated code

---

## Best Practices

### Generate Early

Run generation early in the design process, even with incomplete models.
Seeing generated code reveals:

- Whether naming conventions work in practice
- How complex the implementation will be
- Where the model needs more detail

### Keep Models and Code Synchronized

When implementation reveals design issues:

1. Update the RIDDL model first
2. Regenerate to get updated structure
3. Merge implementation changes

The model remains the source of truth.

### Document for Generation

Thorough documentation in your model produces better generated artifacts:

- `briefly` descriptions become class/method comments
- `described as` content becomes documentation sections
- `term` definitions create glossaries

### Version Generated Code

Commit generated code to version control:

- Track what was generated and when
- Enable diff comparison after regeneration
- Provide baseline for manual modifications

---

## Target Platform Details

### Akka/Scala Deep Dive

The Akka generator produces idiomatic Scala code following these patterns:

**Entity Implementation:**
```scala
object Product {
  // Commands
  sealed trait Command
  case class CreateProduct(...) extends Command
  case class UpdatePrice(...) extends Command

  // Events
  sealed trait Event
  case class ProductCreated(...) extends Event
  case class PriceUpdated(...) extends Event

  // State
  case class State(info: ProductInfo)

  // Behavior
  def apply(id: ProductId): Behavior[Command] =
    EventSourcedBehavior(...)
}
```

**Configuration generated:**

- `application.conf` with Akka settings
- Cluster sharding configuration
- Serialization bindings
- Persistence plugin setup

### Documentation Deep Dive

Documentation generation produces structured content:

**AsciiDoc output:**
```asciidoc
= OnlineRetail Domain
:toc:

== Overview
The OnlineRetail domain encompasses all aspects of selling
products to consumers through digital channels.

== Contexts

=== Catalog Context
Product catalog and browsing experience.

==== Entities

===== Product Entity
A product available for purchase.

.Commands
[cols="1,2"]
|===
|Command |Description
|CreateProduct |Creates a new product in the catalog
|UpdatePrice |Changes the price of an existing product
|===
```

---

## Related Documentation

- [RIDDL Language Reference](../riddl/references/language-reference.md) -
  Complete language syntax
- [Author's Guide](../riddl/guides/authors/index.md) - Writing effective
  models
- [Implementor's Guide](../riddl/guides/implementors/index.md) - Working
  with generated code