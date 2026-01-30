---
title: "RIDDL MCP Server"
description: >-
  Connect AI assistants to RIDDL via the Model Context Protocol. Enable
  validation, analysis, and intelligent suggestions for domain modeling.
---
# RIDDL MCP Server

The RIDDL MCP Server is a Model Context Protocol (MCP) server that enables
AI assistants to reason about and generate RIDDL models. It provides
validation, analysis, and suggestion tools that AI tools can use to help
you build better domain models.

## What is MCP?

The Model Context Protocol (MCP) is an open standard that allows AI
assistants to connect to external tools and data sources. When you connect
the RIDDL MCP Server to your AI assistant, it gains the ability to:

- **Validate** RIDDL source code for syntax and semantic errors
- **Analyze** model completeness and suggest missing elements
- **Explain** error messages and provide fix recommendations
- **Check** if models are ready for simulation
- **Map** natural language domain descriptions to RIDDL structures

## Capabilities

### Available Tools

| Tool | Description |
|------|-------------|
| `validate-text` | Validate RIDDL source code from text |
| `validate-url` | Validate RIDDL from a URL (GitHub, web) |
| `validate-partial` | Validate incomplete models (ignore undefined refs) |
| `check-completeness` | Find missing elements with suggestions |
| `check-simulability` | Verify model can run in riddlsim |
| `map-domain-to-riddl` | Extract RIDDL structure from natural language |
| `explain-error` | Get detailed explanations for validation errors |
| `suggest-next` | Get recommendations for what to add next |

### Available Resources

| Resource | Description |
|----------|-------------|
| `riddl://grammar/ebnf` | Complete EBNF grammar for RIDDL |
| `riddl://grammar/guide` | Full language reference guide |
| `riddl://patterns/catalog` | Reusable RIDDL patterns and examples |

---

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

---

## Server URL

The hosted MCP server will be available at:

```
https://mcp.ossuminc.com/mcp/v1/
```

!!! warning "Coming Soon"
    The hosted server at `mcp.ossuminc.com` will be available in early 2026.
    For local development, use: `http://localhost:8080/mcp/v1/`

---

## Authentication

All requests to the MCP server require an API key. Three methods are
supported:

### Header Authentication (Recommended)

```
X-API-KEY: your-api-key
```

### Query Parameter

```
?api_key=your-api-key
```

### Bearer Token

```
Authorization: Bearer your-api-key
```

!!! note "Obtaining an API Key"
    Contact support@ossuminc.com to request an API key for the hosted
    service.

---

## Protocol Details

The server uses JSON-RPC 2.0 over HTTP:

- **Endpoint**: `POST /mcp/v1`
- **Content-Type**: `application/json`
- **Protocol Version**: `2025-11-25`

### Example Request

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "tools/call",
  "params": {
    "name": "validate-text",
    "arguments": {
      "content": "domain Example is { }"
    }
  }
}
```

### Example Response

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "result": {
    "content": [
      {
        "type": "text",
        "text": "Validation successful: 0 errors, 1 warning"
      }
    ]
  }
}
```

---

## Support

- **Bug Reports**: [GitHub Issues](https://github.com/ossuminc/riddl-mcp-server/issues)
- **Questions**: support@ossuminc.com
- **Contributing**: [GitHub Repository](https://github.com/ossuminc/riddl-mcp-server)

---

## License

Apache License 2.0
