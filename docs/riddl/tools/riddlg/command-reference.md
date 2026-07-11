---
title: "Command Reference"
description: "Every riddlg command and option, with examples"
---

# riddlg Command Reference

```text
riddlg — generate, validate & code-gen RIDDL, locally
Usage: riddlg [validate|serve|gen|mcp|version|info|config] [options] <args>...
```

Run `riddlg --help` for the full usage text, or `riddlg <command> --help`
for one command's options.

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

Generate a RIDDL model from a natural-language description, using a local
AI model. The generated model is validated before it is returned — riddlg
retries generation until the model validates cleanly (up to
`--max-retries`).

| Option | Description |
|--------|-------------|
| `-m, --model <value>` | GGUF model path (default: the 32B coder in `~/.ossum-ai/models`) |
| `-o, --out <value>` | Output `.riddl` file (default: stdout) |
| `--max-retries <value>` | Validation retry attempts (default 2) |
| `--complete` | Fill `???` TBD markers (empty records/messages) with fields |
| `--compositional` | Build via layered decomposition (for large systems; auto-selected for long briefs) |
| `--multi-file` | Emit an include tree (a file per context) into `-o <dir>` instead of one flat file |
| `--allow-cpu` | Run without a GPU (impractically slow) |

```bash
# A small model, straight to a file
riddlg gen riddl "an order-management system" -o orders.riddl

# A large system, decomposed layer by layer into one file per context
riddlg gen riddl --compositional "a hospital system" --multi-file -o hospital/
```

!!! tip
    Descriptions longer than 240 characters automatically use the
    compositional strategy, so `--compositional` is only needed to force it
    for short briefs describing large systems.

### gen code (Pro)

Generate source code from a RIDDL model. Requires a
[Pro license](index.md#free-and-pro).

| Option | Description |
|--------|-------------|
| `-t, --target <value>` | Target: `quarkus` (default) |
| `-o, --out <value>` | Output project directory (default: `.`) |
| `--fill` | Fill `// TODO(AI)` bodies with the AI and compile-verify |
| `-m, --model <value>` | GGUF model for `--fill` (default: the 32B coder) |
| `--allow-cpu` | Run `--fill` without a GPU (slow) |

```bash
# A Quarkus project skeleton
riddlg gen code model.riddl -o app/

# ...with method bodies AI-filled and compile-verified
riddlg gen code model.riddl --fill -o app/
```

## serve

Run riddlg as a localhost HTTP + WebSocket service (this is how
[Synapify](../../../synapify/index.md) drives it):

| Option | Description |
|--------|-------------|
| `--host <value>` | Host/interface to bind (default `127.0.0.1`) |
| `--port <value>` | Port to listen on (default `8910`) |
| `--allow-cpu` | Serve without a GPU |

```bash
riddlg serve --port 8080
```

## mcp

Run the MCP stdio server — RIDDL tools over JSON-RPC on stdin/stdout, for
AI assistants like Claude:

```bash
riddlg mcp
```

See the [MCP section](../../../MCP/index.md) for configuring MCP clients.

## version, info, config

```bash
# Print the riddlg version
riddlg version

# Print build info and the available compute devices (GPUs)
riddlg info

# Print the effective configuration (HOCON)
riddlg config
```

`riddlg info` is the first thing to run after installation — it shows
whether a GPU was detected. `riddlg config` prints every setting riddlg is
using (model paths, generation tuning, server host/port, license lookup);
settings can be overridden in `~/.riddlg/config.conf`.

## Exit Codes

| Code | Meaning |
|------|---------|
| `0` | Success |
| `1` | Parse or validation errors in the RIDDL input |
| `2` | I/O error, unsupported format, or model error |
| `3` | No usable GPU (run `riddlg info`; override with `--allow-cpu`) or Pro license required |
