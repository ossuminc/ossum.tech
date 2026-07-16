---
title: "RIDDL MCP Server"
description: >-
  Connect AI assistants to RIDDL via the Model Context Protocol. Enable
  validation, analysis, and intelligent suggestions for domain modeling.
---
# RIDDL MCP Server

!!! info "The MCP server now runs locally in riddlg"
    The RIDDL MCP tools ship inside the
    [riddlg](../riddl/tools/riddlg/index.md) binary and run **on your
    machine** — `riddlg mcp` for stdio clients, or `POST /mcp` while
    [`riddlg serve`](../riddl/tools/riddlg/server-api.md#post-mcp) is running.
    No account, no API key, and your models never leave your computer. The
    previously planned hosted server at `mcp.ossuminc.com` has been retired in
    favor of this local-first approach; the tool names and result shapes are
    unchanged, so existing clients keep working after you point them at the
    local server.

The RIDDL MCP Server is a Model Context Protocol (MCP) server that lets AI
assistants reason about and generate RIDDL models. It provides validation,
analysis, and suggestion tools that AI tools can use to help you build better
domain models.

## What is MCP?

The Model Context Protocol (MCP) is an open standard that allows AI
assistants to connect to external tools and data sources. When you connect
the RIDDL MCP Server to your AI assistant, it gains the ability to:

- **Validate** RIDDL source for syntax and semantic errors
- **Analyze** model completeness and suggest missing elements
- **Explain** error messages and provide fix recommendations
- **Check** whether a model is ready for simulation
- **Map** natural-language domain descriptions to RIDDL structures
- **Expand** built-in modeling patterns into RIDDL

## Running the Server

First, install riddlg (see [Installation](../riddl/tools/riddlg/installation.md)):

```bash
brew install ossuminc/tap/riddlg
```

The MCP tools are then available over two transports — pick whichever your
assistant supports:

| Transport | Command | How the client connects |
|-----------|---------|-------------------------|
| **stdio** | `riddlg mcp` | The client launches the process; configure `command: riddlg`, `args: ["mcp"]` |
| **HTTP** | `riddlg serve` | The client POSTs to `http://127.0.0.1:8910/mcp` (Streamable HTTP) |

Neither transport needs an API key. The two expose the identical tool set;
see [Server API](../riddl/tools/riddlg/server-api.md#post-mcp) for the HTTP
session and status-code details.

## Available Tools

Thirteen tools are exposed; see
[MCP Tools](../riddl/tools/riddlg/mcp-tools.md) for arguments and return
shapes.

| Tool | Description |
|------|-------------|
| `riddl_validate` | Validate RIDDL source; report parse/validation errors and warnings |
| `riddl_outline` | Outline the named definitions (domains, contexts, entities, types) |
| `check-completeness` | Find gaps: empty handlers, unresolved references, placeholders |
| `suggest-next` | Suggest the next definitions to add, prioritized |
| `map-domain-to-riddl` | Extract RIDDL structure from a natural-language description |
| `validate-partial` | Validate an in-progress fragment, ignoring references to the unwritten rest |
| `check-simulability` | Report whether (and why not) a model can be simulated |
| `explain-error` | Explain a RIDDL diagnostic in plain language, with a likely fix |
| `generate-test-cases` | Generate Given/When/Then scenarios for the model's entities |
| `expand-pattern` | Expand a named modeling pattern into RIDDL |
| `get-template` | Return a built-in RIDDL template |
| `list-patterns` | List the available modeling patterns |
| `list-templates` | List the built-in templates |

## Installation Guides

The RIDDL MCP Server can be connected to various AI tools. Choose your
platform:

- [Claude Desktop](./claude-desktop.md) - Anthropic's desktop application
- [Claude Code](./claude-code.md) - Anthropic's CLI tool for developers
- [Gemini CLI](./gemini.md) - Google's Gemini command-line interface
- [GitHub Copilot CLI](./github-copilot.md) - GitHub Copilot command-line tool
- [VS Code with Copilot](./vscode-copilot.md) - GitHub Copilot in VS Code
- [IntelliJ AI Assistant](./intellij-ai.md) - JetBrains AI integration
- [IntelliJ Junie](./intellij-junie.md) - JetBrains Junie agent

## Protocol Details

The stdio server speaks JSON-RPC 2.0 on stdin/stdout; the HTTP server accepts
one JSON-RPC message per `POST /mcp`. Example `tools/call` request:

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "tools/call",
  "params": {
    "name": "riddl_validate",
    "arguments": {
      "source": "domain Example is { ??? }"
    }
  }
}
```

Example response:

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "result": {
    "content": [
      { "type": "text", "text": "Validation successful: 0 errors, 1 warning" }
    ],
    "isError": false
  }
}
```

## Support

- **Bug Reports**: [GitHub Issues](https://github.com/ossuminc/riddl-mcp-server/issues)
- **Questions**: support@ossuminc.com

## License

The MCP tools are part of `riddlg`, which is proprietary software with a free
tier. See [Free and Pro](../riddl/tools/riddlg/index.md#free-and-pro) — all
MCP tools are free.
