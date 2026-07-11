---
title: "riddlg - The RIDDL Generator"
description: "Generate RIDDL models, documentation, API specs, and code — locally, with AI"
---

# riddlg - The RIDDL Generator

`riddlg` is a single locally-run native binary that generates things from — and
into — RIDDL. It validates RIDDL models, generates documentation and API
specifications from them, generates RIDDL models *from natural-language
descriptions* using a local AI model, and (with a Pro license) generates
runnable code. Everything runs on your machine: the AI inference happens
in-process via [llama.cpp](https://github.com/ggml-org/llama.cpp), so your
models and descriptions never leave your computer.

## Quick Start

```bash
# Install (macOS Apple Silicon or Linux x86_64)
brew install ossuminc/tap/riddlg

# Verify the install and check GPU detection
riddlg info

# Validate a RIDDL model
riddlg validate model.riddl

# Generate a RIDDL model from a description (local AI)
riddlg gen riddl "an order-management system" -o orders.riddl

# Generate documentation from a RIDDL model
riddlg gen docs model.riddl -f mkdocs -o site/
```

!!! info "AI commands need a GPU"
    `gen riddl` and `gen code --fill` run a large language model locally and
    require a GPU (Apple Silicon Metal, or CUDA/Vulkan on Linux). See
    [Installation](installation.md) for hardware recommendations. All other
    commands run anywhere.

## Key Features

- **Validation** - Parse and validate RIDDL files (same checks as `riddlc`)
- **Documentation generation** - AsciiDoc or MkDocs sites from your model
- **API specification generation** - Smithy, gRPC, or OpenAPI
- **AI RIDDL generation** - Describe a system in plain language, get a
  validated RIDDL model; large systems can be built compositionally across
  multiple files
- **Code generation** (Pro) - Quarkus project skeletons, with optional
  AI-filled method bodies that are compile-verified
- **Server & MCP modes** - Run as a localhost HTTP/WebSocket service (used
  by [Synapify](../../../synapify/index.md)) or as an
  [MCP](../../../MCP/index.md) stdio server for AI assistants

## Free and Pro

`riddlg` is proprietary software with a freemium model. The download is free,
and the free tier includes validation, documentation generation, API spec
generation, and AI RIDDL generation. Quarkus code generation requires a Pro
license (set `OSSUM_GEN_LICENSE` or place a license token at
`~/.ossum-gen/license`).

## Documentation

| Section | Description |
|---------|-------------|
| [Installation](installation.md) | Homebrew, direct download, Linux packages, and hardware guidance |
| [Command Reference](command-reference.md) | Every command and option, with examples |
| [AI Models](models.md) | The default model, downloading alternatives, and sizing for your hardware |

## How riddlg Relates to Other Tools

- [`riddlc`](../riddlc/index.md) is the open-source compiler: validation
  only. `riddlg` includes the same validation and adds generation.
- [Synapify](../../../synapify/index.md) is the visual editor; it drives
  `riddlg serve` under the hood for its generation features.
- The [MCP Server](../riddl-mcp-server/index.md) capabilities are also
  available directly from `riddlg mcp`.

## Getting Help

```bash
# Full usage text
riddlg --help

# Options for one command
riddlg gen riddl --help
```
