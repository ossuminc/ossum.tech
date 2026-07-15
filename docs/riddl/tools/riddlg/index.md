---
title: "riddlg - The RIDDL Generator"
description: "Generate RIDDL models, documentation, API specs, and code — locally, with AI"
---

# riddlg - The RIDDL Generator

`riddlg` is a single locally-run native binary that generates things from —
and into — RIDDL. It validates RIDDL models, generates documentation and API
specifications from them, generates RIDDL models *from natural-language
descriptions* using AI, provides a RIDDL-based MCP server, and (with a Pro
subscription) generates runnable code.

By default the AI runs **on your machine**: inference happens in-process via
[llama.cpp](https://github.com/ggml-org/llama.cpp), so your models and
descriptions never leave your computer. If you would rather use a hosted
model, a Pro subscription lets you point riddlg at Anthropic, Google Gemini,
OpenAI, or any OpenAI-compatible service with your own API key — see
[AI Providers](ai-providers.md).

## Quick Start (macOS Apple Silicon)

```bash
# Install (macOS Apple Silicon)
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

The first command that needs the AI model downloads it (~23 GB) into
`~/.ossum-ai/models`. See [AI Models](models.md) to fetch it ahead of time or
pick a smaller one.

!!! info "The local model needs a GPU"
    `gen riddl` and `gen code --fill` run a large language model and require a
    GPU (Apple Silicon Metal, or CUDA/Vulkan on Linux) *when using the local
    model*. See [Installation](installation.md) for hardware recommendations.
    [Cloud providers](ai-providers.md) (Pro) need no GPU at all, and every
    other command runs anywhere.

## Key Features

- **Validation** - Parse and validate RIDDL files (same checks as `riddlc`)
- **Documentation generation** - AsciiDoc or MkDocs sites from your model
- **API specification generation** - Smithy, gRPC, or OpenAPI
- **AI RIDDL generation** - Describe a system in plain language, get a
  validated RIDDL model; large systems can be built compositionally across
  multiple files
- **Choice of AI backend** - The bundled local model (Free), or bring your own
  key for Anthropic, Gemini, OpenAI, or any OpenAI-compatible service (Pro)
- **Code generation** (Pro) - Quarkus project skeletons, with optional
  AI-filled method bodies that are compile-verified
- **Server & MCP modes** - Run as a localhost HTTP service (used by
  [Synapify](../../../synapify/index.md)) or as an
  [MCP](../../../MCP/index.md) server for AI assistants — over stdio, or over
  HTTP on the same port as everything else

## Free and Pro

`riddlg` is proprietary software with a freemium model. The download is free,
and the free tier includes validation, documentation generation, API spec
generation, AI RIDDL generation with the local model, and all of the MCP
tools.

Two features require a **Pro subscription**:

| Pro feature | What it covers |
|-------------|----------------|
| Quarkus code generation | `riddlg gen code` and `POST /generate/code` |
| Cloud AI providers | Any non-local [AI provider](ai-providers.md) profile |

Pro comes from your Ossum account — the **same subscription as Synapify**, not
a separate purchase. Sign in with the device flow:

```bash
riddlg login    # prints a URL and a code; approve in your browser
riddlg whoami   # show the signed-in account and tier
riddlg logout
```

The session is stored at `~/.ossum-gen/session.json` (mode `0600`) and keeps
working offline for up to 7 days between refreshes, so a flight doesn't
disable code generation.

!!! warning "License files are gone"
    Earlier versions used an offline license token (`OSSUM_GEN_LICENSE`, or a
    file at `~/.ossum-gen/license`). That mechanism has been **removed** — the
    tier now comes from your Ossum subscription via `riddlg login`. If you have
    those set, they are ignored and can be deleted.

## Documentation

| Section | Description |
|---------|-------------|
| [Installation](installation.md) | Homebrew, direct download, Linux packages, and hardware guidance |
| [Command Reference](command-reference.md) | Every command and option, with examples |
| [AI Providers](ai-providers.md) | Using the local model or a cloud provider (BYOK), and managing profiles |
| [AI Models](models.md) | The default local model, downloading alternatives, and sizing for your hardware |
| [Configuration](configuration.md) | The config file, every setting, and environment variables |
| [Server API](server-api.md) | The HTTP API served by `riddlg serve` |
| [MCP Tools](mcp-tools.md) | The RIDDL tools exposed to AI assistants |

## How `riddlg` Relates to Other Tools

- [`riddlc`](../riddlc/index.md) is the open-source compiler: validation
  only. `riddlg` includes the same validation and adds generation.
- [Synapify](../../../synapify/index.md) is the visual editor; it drives
  `riddlg serve` under the hood for its generation, AI, and MCP features.
- The [MCP Server](../riddl-mcp-server/index.md) capabilities are also
  available directly from `riddlg mcp` (stdio) or `POST /mcp` in serve mode.

## Getting Help

```bash
# Full usage text
riddlg --help

# Options for one command
riddlg gen riddl --help
```
