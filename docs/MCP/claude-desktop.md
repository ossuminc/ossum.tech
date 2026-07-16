# Claude Desktop Configuration

This guide explains how to configure Claude Desktop to use the RIDDL MCP
Server for AI-assisted domain modeling.

## Prerequisites

- Claude Desktop application installed
- `riddlg` installed and on your `PATH`
  (see [Installation](../riddl/tools/riddlg/installation.md)):
  ```bash
  brew install ossuminc/tap/riddlg
  ```

## Configuration

Claude Desktop launches MCP servers as local processes (stdio transport) via
a JSON configuration file.

### Configuration File Location

| Platform | Path |
|----------|------|
| **macOS** | `~/Library/Application Support/Claude/claude_desktop_config.json` |
| **Windows** | `%APPDATA%\Claude\claude_desktop_config.json` |
| **Linux** | `~/.config/Claude/claude_desktop_config.json` |

### Adding the RIDDL MCP Server

Edit your configuration file to add the RIDDL server:

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

That's the whole setup — no URL, no API key. Claude Desktop starts
`riddlg mcp` for you when it launches.

### Complete Example

If you have other MCP servers configured, add RIDDL alongside them:

```json
{
  "mcpServers": {
    "riddl": {
      "command": "riddlg",
      "args": ["mcp"]
    },
    "filesystem": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "/path/to/files"]
    }
  }
}
```

!!! note "`riddlg` must be found on PATH"
    Claude Desktop does not run your shell profile, so if `riddlg` isn't on
    the system `PATH` it may not be found. Use the absolute path (e.g.
    `/opt/homebrew/bin/riddlg`) as the `command` if the tools don't appear.

## Restart Claude Desktop

After modifying the configuration:

1. Quit Claude Desktop completely
2. Relaunch Claude Desktop
3. The RIDDL tools should now be available

## Verify Connection

Ask Claude to validate some RIDDL:

> "Can you validate this RIDDL code for me?"
> ```riddl
> domain Example is { ??? }
> ```

Claude should use the `riddl_validate` tool and return validation results.

## Usage Examples

### Validate RIDDL Code

> "Please validate this RIDDL model and explain any errors:"
> ```riddl
> domain OrderManagement is {
>   context Orders is {
>     entity Order is { ??? }
>   }
> }
> ```

### Check Completeness

> "Analyze this model for completeness and tell me what's missing:"
> ```riddl
> domain Inventory is {
>   context Warehouse is {
>     type ProductId is Id(Product)
>   }
> }
> ```

### Convert Natural Language

> "I need to model an e-commerce system with shopping carts, orders, and
> inventory tracking. What RIDDL structure would you suggest?"

### Explain Errors

> "I got this error: 'Undefined reference to type CustomerID'. What does
> this mean and how do I fix it?"

## Available RIDDL Tools

Once connected, Claude can use all of the RIDDL MCP tools — for example:

| Tool | Ask Claude to... |
|------|-----------------|
| `riddl_validate` | "Validate this RIDDL code" |
| `riddl_outline` | "Outline the definitions in this model" |
| `validate-partial` | "Check this incomplete model" |
| `check-completeness` | "What's missing from this model?" |
| `check-simulability` | "Can this model be simulated?" |
| `map-domain-to-riddl` | "Convert this description to RIDDL" |
| `explain-error` | "Explain this error message" |
| `suggest-next` | "What should I add next?" |

See [MCP Tools](../riddl/tools/riddlg/mcp-tools.md) for the full catalog of 13.

## Troubleshooting

### Tools Not Appearing

- Restart Claude Desktop after configuration changes
- Check for JSON syntax errors in the configuration file
- Verify `riddlg` runs from a terminal: `riddlg mcp` should start and wait
  for input (press ++ctrl+c++ to exit)
- If `riddlg` isn't found, use its absolute path as the `command`

### Verifying riddlg Itself

```bash
riddlg version
riddlg validate model.riddl
```

---

[Back to MCP Overview](./index.md)
