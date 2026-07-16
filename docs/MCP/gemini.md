# Gemini CLI Configuration

This guide explains how to configure Google's Gemini CLI to use the RIDDL
MCP Server for AI-assisted domain modeling.

## Prerequisites

- Gemini CLI installed (via Google)
- `riddlg` installed and on your `PATH`
  (see [Installation](../riddl/tools/riddlg/installation.md)):
  ```bash
  brew install ossuminc/tap/riddlg
  ```

## Configuration

Gemini CLI uses a JSON settings file for MCP server configuration and can
launch a local server over stdio.

### Configuration File Location

| Platform | Path |
|----------|------|
| **macOS** | `~/.gemini/settings.json` |
| **Windows** | `%USERPROFILE%\.gemini\settings.json` |
| **Linux** | `~/.gemini/settings.json` |

### Adding the RIDDL MCP Server

Edit your settings file to add the RIDDL server under `mcpServers`:

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

No URL and no API key — Gemini CLI runs `riddlg mcp` for you.

### Using the HTTP Transport Instead

If you prefer a long-running server (or want to share one), start
[`riddlg serve`](../riddl/tools/riddlg/server-api.md#post-mcp) and point
Gemini at its HTTP endpoint:

```bash
riddlg serve            # listens on 127.0.0.1:8910
```

```json
{
  "mcpServers": {
    "riddl": {
      "httpUrl": "http://127.0.0.1:8910/mcp"
    }
  }
}
```

## Verify Connection

Start Gemini CLI and test the connection:

```bash
gemini
```

Then ask:

> Can you validate this RIDDL code?
> ```riddl
> domain Example is { ??? }
> ```

Gemini should use the `riddl_validate` tool and return results.

## Usage Examples

### Validate RIDDL Files

> Please validate the RIDDL code in this file and explain any errors

### Generate RIDDL from Description

> Create a RIDDL model for a library management system with books,
> members, and loans

### Check Model Completeness

> What's missing from this domain model to make it complete?

### Explain Errors

> I got "Undefined reference to type OrderId" - what does this mean?

### Get Suggestions

> What should I add next to this entity to make it implementation-ready?

## Advanced Configuration

### Tool Filtering

You can include or exclude specific RIDDL tools:

```json
{
  "mcpServers": {
    "riddl": {
      "command": "riddlg",
      "args": ["mcp"],
      "includeTools": [
        "riddl_validate",
        "check-completeness",
        "explain-error"
      ]
    }
  }
}
```

Or exclude tools you don't need:

```json
{
  "mcpServers": {
    "riddl": {
      "command": "riddlg",
      "args": ["mcp"],
      "excludeTools": [
        "check-simulability"
      ]
    }
  }
}
```

!!! note "Tool Precedence"
    If both `includeTools` and `excludeTools` are specified, `excludeTools`
    takes precedence.

## Debugging

Run Gemini CLI with verbose output:

```bash
gemini --debug
```

The debug output shows MCP server startup, tool discovery, and any error
messages.

## Troubleshooting

### Server Not Connecting

- Verify `riddlg mcp` starts from a terminal (it waits on stdin)
- Check JSON syntax in the settings file
- If `riddlg` isn't found, use its absolute path as `command`
- Enable debug mode for detailed logs

### Tools Not Available

- Restart Gemini CLI after configuration changes
- Check that `includeTools` doesn't filter out needed tools

## Available RIDDL Tools

| Tool | Use Case |
|------|----------|
| `riddl_validate` | Check RIDDL source for errors |
| `riddl_outline` | Summarize a model's definitions |
| `validate-partial` | Check incomplete models |
| `check-completeness` | Find missing elements |
| `check-simulability` | Verify simulation readiness |
| `map-domain-to-riddl` | Convert descriptions to RIDDL |
| `explain-error` | Understand validation errors |
| `suggest-next` | Get recommendations |

See [MCP Tools](../riddl/tools/riddlg/mcp-tools.md) for the full catalog of 13.

## Resources

- [Gemini CLI MCP Documentation](https://google-gemini.github.io/gemini-cli/docs/tools/mcp-server.html)

---

[Back to MCP Overview](./index.md)
