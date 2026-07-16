# IntelliJ Junie Configuration

This guide explains how to configure JetBrains Junie (the autonomous coding
agent) to use the RIDDL MCP Server for AI-assisted domain modeling.

## What is Junie?

Junie is JetBrains' autonomous AI coding agent that can understand your
codebase, execute tasks, and make changes across multiple files. With the
RIDDL MCP Server connected, Junie gains specialized capabilities for working
with RIDDL domain models.

## Prerequisites

- IntelliJ IDEA with Junie support (MCP requires a recent version)
- Junie enabled in your JetBrains account
- `riddlg` installed and on your `PATH`
  (see [Installation](../riddl/tools/riddlg/installation.md)):
  ```bash
  brew install ossuminc/tap/riddlg
  ```

## Configuration

Junie launches MCP servers as local processes (stdio transport).

### Settings UI Method

1. Open **Settings** (++cmd+comma++ or ++ctrl+alt+s++)
2. Navigate to **Tools** > **Junie** > **MCP** (or **Model Context Protocol**)
3. Click **Add Server** and configure:

   | Field | Value |
   |-------|-------|
   | **Name** | `riddl` |
   | **Command** | `riddlg` |
   | **Arguments** | `mcp` |

### JSON Method

Where Junie accepts a JSON server definition, use the standard stdio form:

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

No URL and no API key are involved. If `riddlg` isn't on the system `PATH`,
use its absolute path as the command.

## Restart IntelliJ

After configuration:

1. Close IntelliJ IDEA
2. Relaunch IntelliJ IDEA
3. Open Junie to verify the RIDDL tools are available

## Junie Capabilities with RIDDL

### Autonomous Tasks

Junie can autonomously:

- Validate all RIDDL files in your project
- Fix validation errors across multiple files
- Generate new entities, contexts, or domains
- Refactor RIDDL structures
- Add missing documentation

### Example Autonomous Tasks

**"Validate and fix my RIDDL model"** — Junie scans all `.riddl` files, runs
validation, fixes resolvable errors, and reports issues needing a human
decision.

**"Make this model simulation-ready"** — Junie runs `check-simulability`,
identifies missing handlers and state definitions, adds placeholders, and
re-validates until the model is simulation-ready.

## Usage Examples

### Project-Wide Validation

> Validate all RIDDL files in this project and create a report of any issues

### Generate from Requirements

> Create RIDDL definitions for a subscription management system with monthly
> and annual plans, automatic renewal, cancellation handling, and usage
> tracking

### Refactoring

> Move the Payment entity from the Orders context to a new Payments
> context, updating all references

### Error Resolution

> The validation shows 15 undefined reference errors. Fix them by
> adding the missing type definitions

## Best Practices

1. **Start small**: Test Junie with simple RIDDL tasks first
2. **Review diffs**: Always review changes before applying
3. **Use version control**: Commit before running autonomous tasks
4. **Provide context**: Include relevant requirements in your prompts
5. **Iterate**: Break large tasks into smaller, verifiable steps

## Troubleshooting

### Junie Not Available

- Verify Junie is enabled in your JetBrains account
- Update to a version with MCP support

### MCP Tools Not Working

- Restart IntelliJ after configuration
- Verify `riddlg mcp` starts from a terminal (it waits on stdin)
- If `riddlg` isn't found, use its absolute path as the command
- Check Junie logs: **View** > **Tool Windows** > **Junie** > **Logs**

## Available RIDDL Tools

| Tool | Use For |
|------|---------|
| `riddl_validate` | Check RIDDL source for errors |
| `riddl_outline` | Summarize a model's definitions |
| `validate-partial` | Check incomplete models |
| `check-completeness` | Find missing elements |
| `check-simulability` | Verify simulation readiness |
| `map-domain-to-riddl` | Convert descriptions to RIDDL |
| `explain-error` | Understand validation errors |
| `suggest-next` | Get recommendations |

See [MCP Tools](../riddl/tools/riddlg/mcp-tools.md) for the full catalog of 13.

---

[Back to MCP Overview](./index.md)
