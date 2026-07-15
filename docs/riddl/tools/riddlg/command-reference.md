---
title: "Command Reference"
description: "Every riddlg command and option, with examples"
---

# riddlg Command Reference

Run `riddlg --help` for the full usage text, or `riddlg <command> --help`
for one command's options. Running `riddlg` with no command prints the usage
text.

| Command | Purpose |
|---------|---------|
| [`validate`](#validate) | Parse and validate a RIDDL file |
| [`gen`](#gen) | Generate docs, API specs, RIDDL, or code |
| [`ai`](#ai) | Manage AI provider profiles |
| [`serve`](#serve) | Run the local HTTP service |
| [`mcp`](#mcp) | Run the MCP stdio server |
| [`login`, `logout`, `whoami`](#login-logout-whoami) | Manage your Ossum subscription session |
| [`version`, `info`, `config`](#version-info-config) | Inspect the installation |

## validate

Parse and validate a RIDDL file, reporting errors and warnings:

```bash
riddlg validate model.riddl
```

Exits with code `0` when the model is valid, `1` when there are parse or
validation errors.

## gen

The `gen` command has four subcommands: `docs`, `api`, `riddl`, and `code`.

### gen docs

Generate documentation from a RIDDL model:

| Option | Description |
|--------|-------------|
| `-f, --format <value>` | Output format: `asciidoc` (default) or `mkdocs` |
| `-o, --out <value>` | Output directory (default: `.`) |

```bash
# AsciiDoc documentation into docs/
riddlg gen docs model.riddl -o docs/

# A complete MkDocs site (with Mermaid diagrams) into site/
riddlg gen docs model.riddl -f mkdocs -o site/
```

### gen api

Generate API specifications from a RIDDL model:

| Option | Description |
|--------|-------------|
| `-f, --format <value>` | Output format: `smithy` (default), `grpc`, or `openapi` |
| `-o, --out <value>` | Output directory (default: `.`) |

```bash
# Smithy models
riddlg gen api model.riddl -o api/

# OpenAPI specifications
riddlg gen api model.riddl -f openapi -o api/

# gRPC / protobuf definitions
riddlg gen api model.riddl -f grpc -o api/
```

### gen riddl

Generate a RIDDL model from a natural-language description, using AI. The
generated model is validated before it is returned — riddlg retries
generation until the model validates cleanly (up to `--max-retries`).

| Option | Description |
|--------|-------------|
| `--provider <value>` | [AI provider profile](ai-providers.md) for this run (default: the active profile) |
| `-m, --model <value>` | Model for the effective provider: a GGUF path (local) or a cloud model id |
| `-o, --out <value>` | Output `.riddl` file (default: stdout) |
| `--max-retries <value>` | Validation retry attempts (default 2) |
| `--complete` | Fill `???` TBD markers (empty records/messages) with fields |
| `--compositional` | Build via layered decomposition (for large systems; auto-selected for long briefs) |
| `--multi-file` | Emit an include tree (a file per context) into `-o <dir>` instead of one flat file |
| `--stream` | Echo the model's output to stderr as it is generated |
| `--allow-cpu` | Run the local model without a GPU (impractically slow) |

```bash
# A small model, straight to a file
riddlg gen riddl "an order-management system" -o orders.riddl

# A large system, decomposed layer by layer into one file per context
riddlg gen riddl --compositional "a hospital system" --multi-file -o hospital/

# Watch the generation happen, and use a cloud provider for this run
riddlg gen riddl --stream --provider anthropic "a ticketing system" -o t.riddl
```

`--stream` writes to **stderr**, leaving stdout clean, so you can still pipe
or redirect the RIDDL itself while watching progress on a multi-minute run.

!!! tip
    Descriptions longer than 240 characters automatically use the
    compositional strategy, so `--compositional` is only needed to force it
    for short briefs describing large systems. Note that the compositional
    path runs its own layered descent — it ignores `--max-retries` and
    `--complete`.

### gen code (Pro)

Generate source code from a RIDDL model. Requires a
[Pro subscription](index.md#free-and-pro).

| Option | Description |
|--------|-------------|
| `-t, --target <value>` | Target: `quarkus` (default) |
| `-o, --out <value>` | Output project directory (default: `.`) |
| `--fill` | Fill `// TODO(AI)` bodies with the AI and compile-verify |
| `--provider <value>` | [AI provider profile](ai-providers.md) for `--fill` |
| `-m, --model <value>` | Model for `--fill`: a GGUF path (local) or a cloud model id |
| `--allow-cpu` | Run `--fill` on the local model without a GPU (slow) |

```bash
# A Quarkus project skeleton
riddlg gen code model.riddl -o app/

# ...with method bodies AI-filled and compile-verified
riddlg gen code model.riddl --fill -o app/
```

Without `--fill`, no model is loaded — `--provider`, `-m`, and `--allow-cpu`
have no effect.

## ai

Manage AI provider profiles — the local llama.cpp model, or a cloud service
with your own key. [AI Providers](ai-providers.md) covers this in depth; the
option tables are here.

| Subcommand | Purpose |
|------------|---------|
| `ai list` | List the configured profiles and mark the active one |
| `ai add <name>` | Add a profile (requires `--type`) |
| `ai set <name>` | Update a profile without switching to it |
| `ai use <name>` | Make a profile the active provider (flags allow inline setup) |
| `ai remove <name>` | Remove a profile's configuration |
| `ai show` | Show the effective AI configuration, keys redacted |
| `ai test [<name>]` | Check a provider is reachable (default: the active one) |

`add`, `set`, and `use` share these options:

| Option | Description |
|--------|-------------|
| `--type <value>` | `llama`, `anthropic`, `gemini`, `openai`, or `responses` |
| `--api-key <value>` | API key (prefer `--api-key-stdin` or the provider's env var) |
| `--api-key-stdin` | Read the key from stdin (keeps it out of shell history) |
| `--api-key-keychain` | Store the key in the OS keychain; the config file keeps only a marker |
| `--model <value>` | Model id (cloud) or GGUF path (local) |
| `--base-url <value>` | Endpoint base URL (e.g. `http://localhost:11434/v1` for Ollama) |
| `--max-tokens <value>` | Generation cap per request |
| `--timeout <value>` | Request timeout in seconds (default 600) |

`ai show` additionally takes `--reveal` to print API keys in full instead of
redacted.

```bash
# What's configured, and which profile is active?
riddlg ai list

# Switch to Anthropic, reading the key from stdin
riddlg ai use anthropic --api-key-stdin

# Add any OpenAI-compatible service
riddlg ai add ollama --type openai \
  --base-url http://localhost:11434/v1 --model qwen2.5-coder:32b

# Confirm it works, without paying for a real generation
riddlg ai test ollama
```

## serve

Run riddlg as a localhost HTTP service (this is how
[Synapify](../../../synapify/index.md) drives it). See
[Server API](server-api.md) for the endpoints.

| Option | Description |
|--------|-------------|
| `--host <value>` | Host/interface to bind (default `127.0.0.1`) |
| `--port <value>` | Port to listen on (default `8910`) |
| `--provider <value>` | [AI provider profile](ai-providers.md) to serve with |
| `--allow-cpu` | Serve without a GPU |

```bash
riddlg serve --port 8080
```

The server locks its AI provider at startup — restart it to switch providers,
or override per request with the `provider` field on
[`POST /generate/riddl`](server-api.md#post-generateriddl).

## mcp

Run the MCP stdio server — RIDDL tools over JSON-RPC on stdin/stdout, for AI
assistants like Claude:

```bash
riddlg mcp
```

The same tools are available over HTTP at
[`POST /mcp`](server-api.md#post-mcp) in serve mode. See
[MCP Tools](mcp-tools.md) for the tool catalog and the
[MCP section](../../../MCP/index.md) for configuring MCP clients.

## login, logout, whoami

Pro features are unlocked by signing in to your Ossum account — the same
subscription as [Synapify](../../../synapify/index.md).

```bash
# Device flow: prints a URL and a code; approve in your browser
riddlg login

# Show the signed-in account and subscription tier
riddlg whoami

# Remove the local session
riddlg logout
```

`login` uses the OAuth Device Authorization Grant against the Ossum identity
server, so no password is typed into the terminal. The session is written to
`~/.ossum-gen/session.json` with `0600` permissions, is refreshed
automatically as it expires, and honors the last known tier for up to **7
days** offline. `whoami` exits `1` when you are not signed in.

## version, info, config

```bash
# Print the riddlg version
riddlg version

# Print build info and the available compute devices (GPUs)
riddlg info

# Print the effective configuration (HOCON)
riddlg config
```

`riddlg info` is the first thing to run after installation — it shows whether
a GPU was detected. `riddlg config` prints every setting riddlg is using
(model paths, generation tuning, server host/port, AI profiles), with API
keys redacted; see [Configuration](configuration.md).

## Exit Codes

| Code | Meaning |
|------|---------|
| `0` | Success |
| `1` | Parse or validation errors in the RIDDL input, generation failure, or not signed in (`whoami`) |
| `2` | I/O error, unsupported format, model error, or an `ai` command usage/configuration error |
| `3` | No usable GPU (run `riddlg info`; override with `--allow-cpu`), or a Pro subscription is required |
