---
title: "RIDDL Playground"
description: >-
  Try RIDDL in your browser. Write, validate, and experiment with RIDDL
  models without installing anything.
---
# RIDDL Playground

!!! warning "Coming Soon"
    The interactive playground is under development. This page describes the
    planned functionality.

The RIDDL Playground lets you experiment with RIDDL directly in your browser—no
installation required. Write models, see instant validation feedback, and learn
the language interactively.

---

## Planned Features

### Browser-Based Editor

A full-featured RIDDL editor powered by Monaco (the same engine as VS Code):

- **Syntax highlighting** for all RIDDL keywords and structures
- **Real-time validation** as you type
- **Error markers** with inline explanations
- **Code folding** for managing complex models

### Instant Validation

Your model is validated automatically using the RIDDL MCP Server:

- Syntax checking
- Semantic analysis
- Missing reference detection
- Helpful error messages

### Example Templates

Start from pre-built examples:

- Empty domain template
- E-commerce starter
- Event-sourced entity pattern
- Saga pattern example

### Share Your Work

Generate shareable links to your models for:

- Asking questions in discussions
- Sharing patterns with colleagues
- Embedding in documentation

---

## Technical Architecture

The playground integrates:

1. **Monaco Editor** - Browser-based code editing with RIDDL syntax support
2. **RIDDL MCP Server** - Server-side validation via the `/validate-text` tool
3. **Static Hosting** - No backend required beyond the MCP server

```
┌─────────────────────────────────────┐
│         Browser                     │
│  ┌─────────────────────────────┐   │
│  │     Monaco Editor           │   │
│  │  (RIDDL syntax support)     │   │
│  └─────────────────────────────┘   │
│              │                      │
│              │ RIDDL source         │
│              ▼                      │
│  ┌─────────────────────────────┐   │
│  │   Validation Display        │   │
│  │  (errors, warnings, info)   │   │
│  └─────────────────────────────┘   │
└─────────────────────────────────────┘
              │
              │ HTTP POST /mcp/v1
              │ validate-text
              ▼
┌─────────────────────────────────────┐
│       RIDDL MCP Server              │
│  - Parses RIDDL source              │
│  - Runs semantic validation         │
│  - Returns structured diagnostics   │
└─────────────────────────────────────┘
```

---

## Try It Now (Alternative)

While the playground is under development, you can try RIDDL using:

### VS Code Extension

Install the [RIDDL VS Code extension](../../OSS/vscode-extension/index.md) for
local editing with syntax highlighting and validation.

### IntelliJ Plugin

Install the [RIDDL IntelliJ plugin](../../OSS/intellij-plugin/index.md) for
JetBrains IDE support.

### AI Assistant

Configure the [RIDDL MCP Server](../../MCP/index.md) with your AI assistant
to get interactive help writing and validating models.

---

## Development Status

The playground is being built using components from:

- **Synapify** - Monaco editor integration and RIDDL syntax definitions
- **riddl-mcp-server** - Validation API

Follow progress on [GitHub](https://github.com/ossuminc).

---

## Request Early Access

Interested in trying the playground before general availability? Contact us:

- **Email**: support@ossuminc.com
- **Subject**: "Playground Early Access"
