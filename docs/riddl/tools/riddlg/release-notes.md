---
title: "Release Notes"
description: "What changed in each release of riddlg"
---

# riddlg Release Notes

The current release is **0.6.0** (20 July 2026). Install or upgrade with
`brew upgrade riddlg`, or see [Installation](installation.md) for direct
downloads.

| Version | Date | Headline |
|---------|------|----------|
| [0.6.0](#060) | 2026-07-20 | Eight new model-transform generators |
| [0.5.0](#050) | 2026-07-17 | Rich docs in four formats; streaming chat |
| [0.4.0](#040) | 2026-07-15 | Bring-your-own-key AI providers; MCP over HTTP |
| [0.3.1](#031) | 2026-07-13 | Linux GPU builds (CUDA and Vulkan) |
| [0.3.0](#030) | 2026-07-10 | Reliable code fill; public distribution |
| [0.2.0](#020) | 2026-07-06 | First release as `riddlg` |

---

## 0.6.0

*20 July 2026*

A RIDDL model describes a system precisely enough to derive far more than
documentation from it. This release acts on that: **eight new generators**
turn your model into schemas, catalogs, and structured documentation.

### New generators

| Generator | Command | Tier |
|-----------|---------|------|
| **AsyncAPI 3.0** — event-driven API specs with in/out/stream channels and request/reply | `gen api -f asyncapi` | Free |
| **JSON Schema 2020-12** — standalone validation schemas for contract enforcement | `gen api -f json-schema` | Free |
| **SQL DDL** — normalized DDL from entities and repositories, in five dialects | `gen sql` | Free |
| **DBML** — dialect-free logical schemas for dbdiagram.io | `gen dbml` | Free |
| **Backstage** — software catalogs with ownership resolution | `gen backstage` | Free |
| **EventCatalog** — event-driven doc sites with per-message schemas | `gen catalog` | Free |
| **Confluence** — storage-format pages plus a REST importer | `gen confluence` | **Pro** |
| **DocBook + DITA** — structured XML documentation | `gen docs -f docbook` / `-f dita` | **Pro** |

Every one of them is also exposed over
[`riddlg serve`](server-api.md) at `POST /generate/…`, so
[Synapify](../../../synapify/index.md) and your own tooling get them too. See
[Generators](generators.md) for what each produces.

### Model-carried generation options

riddl-lib 1.31.0 registers the options these generators read, so a model can
declare its own generation settings and still validate without warnings:
`sql_dialect`, `sql_table`, `backstage_owner`, `backstage_lifecycle`,
`backstage_type`, `confluence_space`, `confluence_parent`,
`event_catalog_version`, and `protocol`.

### Also in this release

- Release automation now publishes every platform that builds successfully,
  so one failing build leg no longer blocks the whole release.

---

## 0.5.0

*17 July 2026*

!!! warning "Breaking change: environment variables were renamed"
    Every `OSSUM_GEN_*` environment variable is now `RIDDLG_*` — for example
    `OSSUM_GEN_MODEL_URL` becomes `RIDDLG_MODEL_URL`, and
    `OSSUM_GEN_MAX_TOKENS` becomes `RIDDLG_MAX_TOKENS`. The old names are no
    longer read. See [Configuration](configuration.md#environment-variables)
    for the full list. Config file keys and CLI flags are unaffected.

### Documentation, rebuilt on a shared model

Every documentation format is now rendered from one shared document model, so
they are genuinely equivalent rather than each format being its own partial
implementation. All formats now include:

- Pages and in-page sections mirroring the model hierarchy
- Every definition's `briefly` and `described by` text
- Per-definition and overview diagrams, and attached images, as numbered
  figures
- A home page with a table of contents and a table of figures

### Four documentation formats

`gen docs -f` gained `hugo-book` and `hugo-geekdoc` alongside `asciidoc` and
`mkdocs`, with `hugo` as an alias for `hugo-geekdoc`. Hugo output had been on
the roadmap; this is where it landed.

### AsciiDoc output builds a website and a PDF

The `asciidoc` output now includes a `pom.xml`, a `Makefile`, and a
`README.adoc`, so the generated directory is a working build:

```bash
riddlg gen docs model.riddl -o docs/
cd docs/ && make site   # or: make pdf
```

### Streaming AI responses

[`POST /ai/messages`](server-api.md#post-aimessages) accepts `"stream": true`
and responds with an Anthropic-shaped `text/event-stream`. Anthropic profiles
forward the upstream stream verbatim, including `tool_use` blocks; other
providers get an equivalent synthesized event sequence, so clients need only
one code path.

### Fixes

- `riddlg serve` no longer holds its listening port after a model download.
  The download subprocess was inheriting the server's socket.

---

## 0.4.0

*15 July 2026*

### Bring your own key

riddlg is no longer limited to the local model. With a
[Pro subscription](index.md#free-and-pro) you can point it at **Anthropic,
Google Gemini, OpenAI, the OpenAI Responses API, or any OpenAI-compatible
service** — Ollama, vLLM, LM Studio, Groq, OpenRouter, Azure, and others —
using your own API key. That path needs no GPU and no 23 GB model download.

Keys can come from an environment variable, stdin, or the OS keychain, and
`riddlg ai` manages named profiles:

```bash
riddlg ai use anthropic --api-key-stdin
riddlg ai add ollama --type openai --base-url http://localhost:11434/v1
riddlg ai test ollama
```

See [AI Providers](ai-providers.md).

### Pro comes from your Ossum subscription

!!! warning "Breaking change: license files were removed"
    Earlier versions used an offline license token (`OSSUM_GEN_LICENSE`, or a
    file at `~/.ossum-gen/license`). That mechanism is **gone**. Your tier now
    comes from your Ossum account — the same subscription as Synapify — via
    `riddlg login`. Existing license tokens and files are ignored and can be
    deleted.

```bash
riddlg login    # device flow: prints a URL and a code
riddlg whoami   # account and tier
```

The session keeps working offline for up to 7 days between refreshes.

### MCP over HTTP, and more MCP tools

`riddlg serve` gained [`POST /mcp`](server-api.md#post-mcp) — the full MCP tool
set over Streamable HTTP, on the same port as everything else, identical to
what `riddlg mcp` serves over stdio. Eleven derivation tools joined the two
validation tools: `check-completeness`, `suggest-next`, `map-domain-to-riddl`,
`validate-partial`, `expand-pattern`, `get-template`, `generate-test-cases`,
`check-simulability`, `explain-error`, `list-patterns`, and `list-templates`.
See [MCP Tools](mcp-tools.md).

### Also in this release

- **Model auto-download.** The first command that needs the local model fetches
  it, with progress reported at
  [`GET /model/status`](server-api.md#get-modelstatus) so a UI can draw a
  banner.
- **`POST /ai/messages`** — one chat turn in the Anthropic Messages shape, so a
  client can hold a conversation through riddlg without ever handling API keys.

---

## 0.3.1

*13 July 2026*

- **Linux GPU builds.** `cuda` and `vulkan` variants join the CPU build. The
  CUDA variant vendors the CUDA runtime, so you need only the NVIDIA driver;
  the Vulkan variant runs on AMD, Intel, and NVIDIA alike. See
  [Installation](installation.md#direct-download).
- llama.cpp is now built from source on every release platform, which is what
  makes the GPU backends actually present in the shipped binary.
- A `latest.json` manifest is published alongside each release so download
  pages can resolve the current version.

---

## 0.3.0

*10 July 2026*

- **Generator correctness.** Five bugs that produced invalid RIDDL were fixed;
  the fidelity baseline reached 79 of 79 models generating valid output.
- **`gen code --fill` produces compiling output reliably.** The AI-filled
  method bodies are compile-verified with retries.
- **Public distribution.** Release artifacts moved to a public bucket, which
  is what makes `brew install ossuminc/tap/riddlg` work from a private source
  repository.
- Upgraded to riddl-lib 1.29.0.
- The simulator module was removed — it is outside riddlg's mission. RIDDL
  simulation is [on the roadmap](../../../coming-soon/index.md) elsewhere.

---

## 0.2.0

*6 July 2026*

The first release under the name **`riddlg`**, following `riddlc`'s naming
convention.

- **Compositional generation.** Large systems are generated by layered
  decomposition rather than in one shot, with shared types hoisted to domain
  scope. `--multi-file` emits an include tree with a file per context, and
  briefs longer than 240 characters select this strategy automatically.
- **Story layer.** Generated models include the epic / user / use-case layer.
- **HOCON configuration** at `~/.riddlg/config.conf`, with `riddlg config` to
  print the effective settings. See [Configuration](configuration.md).
- **GPU pre-flight.** Model-loading commands stop with a clear message rather
  than crawling on CPU; `--allow-cpu` overrides.
- **`version` and `info` commands**, the latter listing detected compute
  devices.
- Homebrew, `.deb`, and `.rpm` packaging.

---

## See Also

- [Installation](installation.md) — installing and upgrading
- [Generators](generators.md) — everything riddlg can generate today
- [Command Reference](command-reference.md) — every command and option
