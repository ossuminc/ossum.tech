---
title: "Coming Soon"
description: "Upcoming features for the RIDDL ecosystem"
---

# :material-creation: Coming Soon

This page outlines upcoming capabilities for the RIDDL ecosystem. These
features are under active development and will be available through
[Synapify](../synapify/index.md) and related tooling.

---

## Simulation

The [riddlsim](https://github.com/ossuminc/riddlsim) engine executes RIDDL
models against test scenarios, validating behavior before implementation.

**Why simulate?**

- **Catch design errors early** before they become expensive implementation
  bugs
- **Verify state transitions** to ensure entities move through expected
  lifecycles
- **Test edge cases** that might be overlooked in manual review
- **Build stakeholder confidence** by demonstrating working behavior early
- **Document expected behavior** through executable scenarios

Simulation scenarios define inputs, expected events, and state assertions.
When a scenario runs, the simulator parses your model, executes the 
scenario steps, and reports whether outcomes match expectations.

For detailed information on simulation capabilities and integration with
Synapify, see the [Synapify Simulation Guide](../synapify/simulation.md).

---

## Generation

The RIDDL ecosystem will support code and artifact generation from validated
models. Generation transforms your domain model into runnable infrastructure,
documentation, and integration artifacts.

### Documentation Generators

| Target | Description |
|--------|-------------|
| **Hugo** | Static documentation site with navigation, diagrams, and cross-references. Currently available. |
| **AsciiDoc** | Technical documentation in AsciiDoc format for integration with enterprise documentation systems. |
| **Diagrams** | Mermaid-based visualizations including context maps, data flow, sequence diagrams, and entity relationships. |

### API & Schema Generators

| Target      | Description                                                                                                 |
|-------------|-------------------------------------------------------------------------------------------------------------|
| **OpenAPI** | OpenAPI (Swagger) specifications documenting REST APIs implied by Applications and their endpoints.         |
| **gRPC**    | Google's efficient serialization format protobuf enables gRPC services and cross-language interoperability. |
| **Smithy**  | AWS Interface Definition Language for defining services that integrate with AWS infrastructure.             |

### Runtime Code Generators

| Target      | Description                                                                                                                                                                                                  |
|-------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **Akka**    | Complete Scala/Akka project including actors, protobuffers, sbt build files, and runtime dependencies. Generates infrastructure code while leaving business logic to developers or have AI do the whole job. |
| **Quarkus** | Complete Java/Quarkus project using many Quarkus ecosystem features for reactive distributed systems.                                                                                                        |

### Integration Generators

| Target | Description                                                                                                                                                 |
|--------|-------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **Backstage** | Catalog entries for [Spotify Backstage](https://backstage.io/) developer portals, documenting service ownership and relationships.                          |
| **BAST** | Binary Abstract Syntax Tree format for faster parsing. Saves validated models in a binary format that loads quickly, avoiding re-parsing and re-validation. |

### Extending Generation

The generation architecture is designed for extensibility. Custom generators can
be implemented to target additional platforms, frameworks, or output formats.

### Suggest a Generator

Have an idea for a new generator? We'd love to hear it!

[**:material-lightbulb-on: Submit Your Idea**](https://docs.google.com/forms/d/e/1FAIpQLSclhKBpyj3kzXAmv7isxUOaqarX4U7__I7lYSx6NT5HvWkF3A/viewform?usp=sf_link){ .md-button .md-button--primary }

---

!!! note "Timeline"
    These features are being developed iteratively. Generators will be released
    as they reach production quality. For the latest status, see the
    [Synapify documentation](../synapify/index.md).
