---
title: "MCP Tools"
description: "The RIDDL tools riddlg exposes to AI assistants over MCP"
---

# MCP Tools

riddlg is an [MCP](../../../MCP/index.md) server, giving AI assistants real
RIDDL analysis instead of guesswork. The same 13 tools are available two ways:

```bash
riddlg mcp          # stdio JSON-RPC — for Claude Desktop, IDEs, CLIs
riddlg serve        # the same tools at POST /mcp
```

Tool behavior is identical across both transports. All MCP tools are **free** —
no subscription needed.

!!! info "These replace the hosted MCP server"
    riddlg's derivation tools are ported from the hosted server at
    `mcp.ossuminc.com`, keeping the same names and result shapes. Running them
    locally means your models never leave your machine — and nothing to be shut
    down under you.

## Analysis Tools

| Tool | Arguments | Returns |
|------|-----------|---------|
| `riddl_validate` | `source` | Parse/validation errors and warnings, as prose |
| `riddl_outline` | `source` | The named definitions — domains, contexts, entities, types |
| `check-completeness` | `source` | `{isComplete, items[]}` — empty handlers, unresolved references, placeholders |
| `validate-partial` | `source` | `{success, messages[]}` — validates a fragment, ignoring references into the unwritten rest |
| `check-simulability` | `source` | `{isSimulatable, issues[], coverage{}}` — whether the model can be simulated, and handler coverage stats |
| `explain-error` | `message`, *`source`* | `{category, explanation, cause, suggestion, examples[]}` — a diagnostic in plain language |

## Authoring Tools

| Tool | Arguments | Returns |
|------|-----------|---------|
| `suggest-next` | `source` | `{suggestions[], modelStatus, completionPercent}` — prioritized next definitions to add |
| `map-domain-to-riddl` | `description` | `{suggestions[], suggestedContexts[], suggestedEntities[], suggestedEvents[], suggestedCommands[]}` — a first cut at structure from a plain-language description |
| `generate-test-cases` | `source`, *`coverage`* | `{testCases[], entityCount, commandCount, coverage}` — Given/When/Then scenarios. `coverage` is `basic` (default) or `comprehensive` |

## Pattern Tools

| Tool | Arguments | Returns |
|------|-----------|---------|
| `list-patterns` | *none* | `{patterns[]}` — every pattern with its parameters |
| `expand-pattern` | `pattern`, *pattern parameters* | `{patternName, description, parameters, expandedCode}` — RIDDL with your names substituted |
| `list-templates` | *none* | `{path, description, entries[]}` |
| `get-template` | `template` | `{path, name, content, ...}` — the raw template, placeholders unexpanded |

*Italic* arguments are optional.

### The Pattern Catalog

Six modeling patterns ship built in. `expand-pattern` substitutes your names
into the template; `get-template` returns it raw.

| Pattern id | Name | Required parameters |
|------------|------|---------------------|
| `event-sourced-entity` | Event-Sourced Entity | `EntityName` |
| `aggregate-root` | Aggregate Root | `AggregateName`, `ChildName` |
| `saga` | Saga (Distributed Transaction) | `SagaName` |
| `repository` | Repository | `RepositoryName`, `EntityName` |
| `projector` | Projector (Read Model) | `ProjectorName`, `ViewName`, `EntityName` |
| `process-manager` | Process Manager | `ProcessName` |

Templates are addressed as `patterns/<id>.riddl` (a bare `<id>` also works).

Example `expand-pattern` call:

```json
{
  "name": "expand-pattern",
  "arguments": {"pattern": "repository", "RepositoryName": "Orders", "EntityName": "Order"}
}
```

!!! warning "`expand-pattern`'s schema under-reports its parameters"
    The published input schema advertises only `EntityName`, but every pattern
    parameter above is accepted and applied. If your MCP client validates
    strictly against the schema, it may not offer the others — pass them
    anyway. Call `list-patterns` for the authoritative list.

## Results and Errors

Every tool answers with a single text content block. The analysis and
authoring tools put **JSON** in that block (pretty-printed, in the shapes
above); `riddl_validate` and `riddl_outline` put prose.

A model that fails validation is **not** a tool error — the report is the
result. Tool errors are reserved for things like a missing required argument
or an unknown pattern name.

## How the Tools Work

Ten of the eleven derivation tools are **pure deterministic analysis** — real
parsing and validation via the RIDDL compiler library, handler-completeness
classification, and AST walking. No model is loaded, so they work identically
over stdio with no AI configured at all, and they return instantly.

`map-domain-to-riddl` is the exception. It has an optional AI hook: in
`serve` mode it shares the server's [resident provider](ai-providers.md), and
a keyword heuristic is the fallback. The heuristic runs whenever no AI is
wired (all of stdio mode), the request fails, or the model returns something
malformed. Availability and result shape never vary — only quality.

## Configuring a Client

For stdio clients such as Claude Desktop:

```json
{
  "mcpServers": {
    "riddl": {
      "command": "riddlg",
      "args": ["mcp"]
    }
  }
}
```

For HTTP clients, point at `http://127.0.0.1:8910/mcp` with `riddlg serve`
running. See [Server API](server-api.md#post-mcp) for session headers and
status-code semantics, and the [MCP section](../../../MCP/index.md) for more
client configuration.

## See Also

- [Server API](server-api.md#post-mcp) — MCP over HTTP
- [AI Providers](ai-providers.md) — what backs `map-domain-to-riddl` in serve mode
- [Command Reference](command-reference.md#mcp) — the `mcp` command
