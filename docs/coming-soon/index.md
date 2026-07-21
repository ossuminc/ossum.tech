---
title: "Coming Soon"
description: "Upcoming features for the RIDDL ecosystem"
---

# :material-creation: Coming Soon

This page outlines capabilities across the RIDDL ecosystem — some already
shipping in the [`riddlg`](../riddl/tools/riddlg/index.md) tool, others still
under active development and coming through
[Synapify](../synapify/index.md) and related tooling. Each entry below is
marked with its status.

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

The RIDDL ecosystem generates code and artifacts from validated models,
transforming your domain model into documentation, API specifications, and
runnable infrastructure.

!!! tip "Most generation is available today"
    Documentation, API specifications, schemas, and software catalogs already
    generate from your model with the
    [`riddlg`](../riddl/tools/riddlg/index.md) tool — see
    [Generators](../riddl/tools/riddlg/generators.md) for the full catalog. The
    tables below mark what ships now versus what is still on the roadmap.

### Documentation Generators

| Target | Status | Description |
|--------|--------|-------------|
| **AsciiDoc** | Available (`riddlg gen docs`) | Technical documentation in AsciiDoc, with a Maven build that produces an HTML site and a PDF book. |
| **MkDocs** | Available (`riddlg gen docs -f mkdocs`) | A Material for MkDocs site with navigation, Mermaid diagrams, and cross-references. |
| **Hugo** | Available (`riddlg gen docs -f hugo`) | A Hugo static site, in either the `hugo-book` or `hugo-geekdoc` theme. |
| **DocBook** | Available (Pro, `riddlg gen docs -f docbook`) | A single-file DocBook 5.0 book for structured-authoring toolchains. |
| **DITA** | Available (Pro, `riddlg gen docs -f dita`) | DITA topics with a ditamap, for DITA Open Toolkit and friends. |
| **Confluence** | Available (Pro, `riddlg gen confluence`) | Confluence storage-format pages plus a REST importer script. |
| **Diagrams** | Available (within every doc format) | Mermaid-based context maps, data flow, sequence diagrams, and entity relationships. |

### API & Schema Generators

| Target      | Status | Description                                                                                                 |
|-------------|--------|-------------------------------------------------------------------------------------------------------------|
| **Smithy**  | Available (`riddlg gen api`) | AWS Interface Definition Language for defining services that integrate with AWS infrastructure.             |
| **gRPC**    | Available (`riddlg gen api -f grpc`) | Protobuf definitions enabling gRPC services and cross-language interoperability. |
| **OpenAPI** | Available (`riddlg gen api -f openapi`) | OpenAPI (Swagger) specifications documenting the REST APIs implied by Applications and their endpoints.         |
| **AsyncAPI** | Available (`riddlg gen api -f asyncapi`) | AsyncAPI 3.0 specifications for the event-driven surface — channels, operations, and request/reply. |
| **JSON Schema** | Available (`riddlg gen api -f json-schema`) | Standalone JSON Schema 2020-12 documents for enforcing message contracts. |
| **SQL DDL** | Available (`riddlg gen sql`) | Normalized DDL from entities and repositories, in Postgres, MySQL, ANSI, Oracle, or SQL Server dialects. |
| **DBML** | Available (`riddlg gen dbml`) | A dialect-free logical schema for visualization in dbdiagram.io. |

### Catalog Generators

| Target | Status | Description |
|--------|--------|-------------|
| **Backstage** | Available (`riddlg gen backstage`) | A Backstage software catalog mapping domains to systems, components, resources, and APIs, with ownership. |
| **EventCatalog** | Available (`riddlg gen catalog`) | An EventCatalog site of domains, services, and messages, with per-message JSON schemas. |

### Runtime Code Generators

| Target      | Status | Description                                                                                                                         |
|-------------|--------|-----------------------------------------------------------------------------------------------------------------------------------|
| **Quarkus** | Available (Pro, `riddlg gen code`) | A Java/Quarkus project — JPA entities, records, and services — with optional AI-filled, compile-verified handler bodies (`--fill`). |
| **Other runtimes** | Roadmap | RIDDL's model carries enough structure to target additional runtimes and frameworks; more will follow as they reach production quality. |

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
