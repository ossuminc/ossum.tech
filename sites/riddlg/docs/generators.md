---
title: "Generators"
description: "Every artifact riddlg can generate from a RIDDL model — docs, API specs, schemas, catalogs, and code"
---

# Generators

A RIDDL model is a structured description of a system, so it can be
mechanically transformed into a great many other things. This page catalogs
every artifact `riddlg` can emit, what each one is good for, and which tier it
requires. The [Command Reference](command-reference.md) covers the flags; this
page covers the *outputs*.

Everything here is also available over HTTP from
[`riddlg serve`](server-api.md) — the CLI and the server share one generator
implementation, so output is identical either way.

## At a Glance

| Command | Formats | Tier |
|---------|---------|------|
| [`gen docs`](#documentation) | `asciidoc`, `mkdocs`, `hugo-book`, `hugo-geekdoc` | Free |
| [`gen docs`](#documentation) | `docbook`, `dita` | **Pro** |
| [`gen api`](#api-specifications) | `smithy`, `grpc`, `openapi`, `json-schema`, `asyncapi` | Free |
| [`gen sql`](#sql-ddl) | 5 dialects | Free |
| [`gen dbml`](#dbml) | DBML | Free |
| [`gen backstage`](#backstage-catalog) | Backstage catalog | Free |
| [`gen catalog`](#eventcatalog) | EventCatalog site | Free |
| [`gen confluence`](#confluence) | Confluence storage format | **Pro** |
| [`gen code`](#code-generation) | `quarkus` | **Pro** |

## Documentation

All documentation formats are rendered from a **shared document model** built
from your RIDDL. That means every format gets the same content and the same
hierarchy — pages and in-page sections mirroring the model tree, every
definition's `briefly` and `described by` text, per-definition and overview
diagrams, attached images as numbered figures, a home page with a table of
contents, and a table of figures.

Picking a format is a rendering decision, not a content decision.

```bash
riddlg gen docs model.riddl -f mkdocs -o site/
```

| Format | Produces |
|--------|----------|
| `asciidoc` *(default)* | AsciiDoc sources plus a build harness — see [below](#asciidoc-builds-a-website-and-a-pdf) |
| `mkdocs` | A [Material for MkDocs](https://squidfunk.github.io/mkdocs-material/) site with navigation and Mermaid diagrams |
| `hugo-book` | A [Hugo](https://gohugo.io/) site using the [hugo-book](https://github.com/alex-shpak/hugo-book) theme, wired up via Hugo Modules |
| `hugo-geekdoc` | A Hugo site using the [hugo-geekdoc](https://github.com/thegeeklab/hugo-geekdoc) theme |
| `hugo` | Alias for `hugo-geekdoc` |
| `docbook` **(Pro)** | A single-file DocBook 5.0 `<book>` — preface, chapters, nested sections |
| `dita` **(Pro)** | One generic DITA `<topic>` per page, plus an `index.ditamap` |

### AsciiDoc builds a website and a PDF

The `asciidoc` output is not just `.adoc` files. It also emits a `pom.xml`
(wired to the asciidoctor-maven-plugin), a `Makefile`, and a `README.adoc`, so
the generated directory is a working build:

```bash
riddlg gen docs model.riddl -o docs/
cd docs/
make site    # HTML website
make pdf     # PDF book
```

This needs a JDK, Maven, and `mmdc` (the Mermaid CLI) for diagram rendering.
`README.adoc` in the output spells out the prerequisites.

!!! tip "DocBook and DITA are for structured-authoring shops"
    If your organization already runs a DocBook or DITA toolchain — DITA Open
    Toolkit, Oxygen, FrameMaker — these formats drop your model straight into
    it. Mermaid diagrams are preserved as `<programlisting language="mermaid">`
    for your pipeline to render. Both require a
    [Pro subscription](index.md#free-and-pro).

## API Specifications

```bash
riddlg gen api model.riddl -f openapi -o api/
```

| Format | Produces | Notes |
|--------|----------|-------|
| `smithy` *(default)* | Smithy IDL — one model per domain, one `service` per context | AWS's IDL; feeds the Smithy codegen ecosystem |
| `grpc` | proto3 `.proto` definitions | Cross-language RPC and streaming |
| `openapi` | OpenAPI 3.1 YAML | The REST API implied by your applications and their endpoints |
| `json-schema` | JSON Schema 2020-12, one `<context>.schema.json` per context | `$schema` / `$id` / `$defs` with cross-references |
| `asyncapi` | AsyncAPI 3.0 YAML, one `<context>.asyncapi.yaml` per context | Event-driven counterpart to OpenAPI |

### AsyncAPI and RIDDL's message model

AsyncAPI 3.0 fits RIDDL unusually well, because RIDDL already describes a
system in terms of messages flowing between components. The mapping is direct:

- Each definition gets `<name>-in` and `<name>-out` channels
- Connectors become `stream-<connector>` channels
- Handlers become `receive` and `send` operations
- Query/result pairs become request/reply operations

The transport protocol defaults to `kafka` and can be set per run or per model:

```bash
riddlg gen api model.riddl -f asyncapi --protocol amqp -o api/
```

A context's own `option protocol("...")` wins over `--protocol`.

### JSON Schema for contract enforcement

`json-schema` emits *standalone* validation schemas — unlike the schemas
embedded in the OpenAPI output, these are meant to be handed to a validator to
enforce message contracts at runtime, in CI, or at a system boundary.

## SQL DDL

Generates runnable, normalized DDL from your entities and repositories — one
`.sql` file per table source.

```bash
riddlg gen sql model.riddl -o sql/ --dialect postgres
```

| Dialect | Aliases |
|---------|---------|
| `postgres` *(default)* | `postgresql`, `pg` |
| `mysql` | `mariadb` |
| `ansi` | `sql`, `standard` |
| `oracle` | — |
| `sqlserver` | `mssql`, `tsql` |

!!! note "The model wins over the flag"
    Unusually, `option sql_dialect("mysql")` in the model takes precedence over
    `--dialect` on the command line. This is deliberate: a model that declares
    its own storage dialect knows something the caller may not, and each table
    source is generated in its own resolved dialect. Use `--dialect` to set the
    default for sources that don't declare one.

Use `option sql_table(...)` to control table naming.

## DBML

[DBML](https://dbml.dbdiagram.io/) is a dialect-free logical schema language —
useful when you want a *picture* of the data model rather than something to
run. Paste the output into [dbdiagram.io](https://dbdiagram.io/) for an
instant ER diagram.

```bash
riddlg gen dbml model.riddl -o dbml/
```

Emits a single `.dbml` file: every record type becomes a table, contexts become
table groups, and references become `Ref` links.

## Backstage Catalog

Generates a [Backstage](https://backstage.io/) software catalog, so your domain
model becomes the source of truth for your developer portal.

```bash
riddlg gen backstage model.riddl -o catalog/ --owner platform-team
```

The mapping follows Backstage's own hierarchy — Domain → System →
Component / Resource / API — and produces a root `catalog-info.yaml` (a
Location entity) pointing at one file per domain.

| Model option | Effect |
|--------------|--------|
| `backstage_owner` | Owning team; falls back to `--owner`, then the definition's `by author`, then `unassigned` |
| `backstage_lifecycle` | `experimental`, `production`, etc. |
| `backstage_type` | Entity type override |

## EventCatalog

Generates an [EventCatalog](https://www.eventcatalog.dev/) site — domains,
services, and messages, with a per-message `schema.json`.

```bash
riddlg gen catalog model.riddl -o catalog/
```

Where the Backstage output answers *"who owns what?"*, EventCatalog answers
*"what messages exist and who produces or consumes them?"* — which is
precisely the question RIDDL models are best at answering. Set
`option event_catalog_version(...)` to control versioning.

## Confluence

!!! warning "Pro subscription required"
    `gen confluence` needs a [Pro subscription](index.md#free-and-pro).

Generates Confluence **storage format** pages plus the tooling to push them:

```bash
riddlg gen confluence model.riddl -o conf/ --space DOCS
```

The output directory contains `pages/`, a `manifest.json`, a `publish.sh` that
imports everything over the Confluence REST API, and a `README.md` explaining
the credentials it needs.

Space and parent page can be baked into the model with
`option confluence_space("KEY")` and `option confluence_parent("Title")`;
`--space` overrides them. If neither is set, `publish.sh` reads `$SPACE_KEY`
from the environment at publish time.

## Code Generation

!!! warning "Pro subscription required"
    `gen code` needs a [Pro subscription](index.md#free-and-pro).

```bash
riddlg gen code model.riddl -o app/          # skeleton
riddlg gen code model.riddl --fill -o app/   # AI-filled bodies
```

Quarkus is currently the only target. The output is a complete Maven project —
`pom.xml`, JPA entities, records, and services — that compiles as generated.

With `--fill`, riddlg uses the [AI provider](ai-providers.md) to write the
`// TODO(AI)` method bodies and then **compiles the project to verify them**,
retrying on failure. This is the one generator whose output is not purely
deterministic, and the compile check is why its results are trustworthy.

## Model Options Reference

Several generators read options from the model itself, so that a model can
carry its own generation settings rather than depending on how it is invoked.
All of these are registered by riddl-lib and validate cleanly:

| Option | Used by |
|--------|---------|
| `protocol` | [`gen api -f asyncapi`](#asyncapi-and-riddls-message-model) |
| `sql_dialect`, `sql_table` | [`gen sql`](#sql-ddl) |
| `backstage_owner`, `backstage_lifecycle`, `backstage_type` | [`gen backstage`](#backstage-catalog) |
| `confluence_space`, `confluence_parent` | [`gen confluence`](#confluence) |
| `event_catalog_version` | [`gen catalog`](#eventcatalog) |

Set them in a definition's `with { }` block:

```riddl
context Ordering is {
  ???
} with {
  option is sql_dialect("mysql")
  option is backstage_owner("commerce-team")
}
```

!!! note "Requires riddlg 0.6.0 or later"
    These options were registered in riddl-lib 1.31.0, which ships with riddlg
    0.6.0. On earlier versions `riddlc` and `riddlg` will warn that they are
    not recognized options.

## See Also

- [Command Reference](command-reference.md) — every flag for every generator
- [Server API](server-api.md) — the same generators over HTTP
- [Release Notes](release-notes.md) — when each generator arrived
