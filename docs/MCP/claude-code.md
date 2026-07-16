# Claude Code Configuration

This guide explains how to configure Claude Code (Anthropic's CLI tool) to
use the RIDDL MCP Server for AI-assisted domain modeling.

## Prerequisites

- Claude Code CLI installed (`npm install -g @anthropic-ai/claude-code`)
- `riddlg` installed and on your `PATH`
  (see [Installation](../riddl/tools/riddlg/installation.md)):
  ```bash
  brew install ossuminc/tap/riddlg
  ```

## Configuration

The quickest way is the `claude mcp` command, which registers `riddlg mcp`
as a stdio server:

```bash
claude mcp add riddl -- riddlg mcp
```

To make it available in every project, add `--scope user`:

```bash
claude mcp add --scope user riddl -- riddlg mcp
```

### Project-Level Configuration

To share the server with everyone who checks out a project, add a `.mcp.json`
file at the project root:

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

Claude Code picks this up automatically when you run it in that directory. No
URL and no API key are involved — Claude Code launches `riddlg mcp` for you.

## Verify Connection

Start Claude Code and ask it to test the connection:

```bash
claude
```

Then in the session:

> "Can you validate this RIDDL: `domain Test is { ??? }`"

Claude should use the `riddl_validate` tool and return results. You can also
list configured servers with `claude mcp list`.

## Usage Examples

### Validating RIDDL Files

When working in a directory with `.riddl` files:

> "Please validate the file src/domain.riddl"

Claude Code can read the file and use the RIDDL MCP server to validate it.

### Creating New Models

> "Help me create a RIDDL model for a hotel reservation system with
> bookings, rooms, and guests"

Claude will use `map-domain-to-riddl` to suggest a structure, then help
you refine it.

### Fixing Validation Errors

> "I'm getting validation errors in my RIDDL file. Can you explain them
> and suggest fixes?"

Claude will use `riddl_validate` and `explain-error` to help you resolve
issues.

### Checking Model Quality

> "Check if my order management model is complete enough for simulation"

Claude will use `check-completeness` and `check-simulability` to analyze
your model.

## Available RIDDL Tools

| Tool | Use Case |
|------|----------|
| `riddl_validate` | Check RIDDL source for errors |
| `riddl_outline` | Summarize a model's definitions |
| `validate-partial` | Check incomplete/in-progress models |
| `check-completeness` | Find missing elements |
| `check-simulability` | Verify simulation readiness |
| `map-domain-to-riddl` | Convert descriptions to RIDDL |
| `explain-error` | Understand validation errors |
| `suggest-next` | Get recommendations for next steps |

See [MCP Tools](../riddl/tools/riddlg/mcp-tools.md) for the full catalog of 13.

## Troubleshooting

### Server Not Connecting

- Run `claude mcp list` to confirm `riddl` is registered
- Verify `riddlg mcp` starts from a terminal (it waits on stdin; ++ctrl+c++
  to exit)
- If `riddlg` isn't found, register it by absolute path:
  `claude mcp add riddl -- /opt/homebrew/bin/riddlg mcp`

### Tools Not Available

- Restart Claude Code after configuration changes
- Check `riddlg version` runs successfully

## Tips for Effective Use

1. **Be specific**: Instead of "validate my code", say "validate the
   Order entity in src/orders.riddl"
2. **Provide context**: Share relevant parts of your model when asking
   questions
3. **Iterate**: Use `suggest-next` to build models incrementally
4. **Learn from errors**: Ask Claude to explain any validation errors
   you encounter

---

[Back to MCP Overview](./index.md)
