# IntelliJ AI Assistant Configuration

This guide explains how to configure IntelliJ IDEA's built-in AI Assistant
to use the RIDDL MCP Server for AI-assisted domain modeling.

## Prerequisites

- IntelliJ IDEA with the AI Assistant plugin (MCP support requires a recent
  version — 2025.1 or later)
- AI Assistant enabled in your JetBrains account
- `riddlg` installed and on your `PATH`
  (see [Installation](../riddl/tools/riddlg/installation.md)):
  ```bash
  brew install ossuminc/tap/riddlg
  ```

## Configuration

JetBrains AI Assistant launches MCP servers as local processes (stdio
transport).

### Settings UI Method

1. Open **Settings** (++cmd+comma++ or ++ctrl+alt+s++)
2. Navigate to **Tools** > **AI Assistant** > **Model Context Protocol (MCP)**
3. Click **Add** (**+**) and configure the server:

   | Field | Value |
   |-------|-------|
   | **Name** | `riddl` |
   | **Command** | `riddlg` |
   | **Arguments** | `mcp` |

4. Apply and let the IDE start the server.

### JSON Method

Some versions let you paste a server definition as JSON. The RIDDL server
uses the standard stdio form (the same shape Claude Desktop uses):

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

After configuring:

1. Close IntelliJ IDEA completely
2. Relaunch IntelliJ IDEA
3. Open a RIDDL file to verify the tools are available

## Verify Connection

Open the AI Assistant chat and ask:

> Can you validate this RIDDL code?
> ```riddl
> domain Example is { ??? }
> ```

The AI should use the `riddl_validate` tool and return validation results.

## Using with the RIDDL Plugin

For the best experience, install both:

- **RIDDL4IDEA Plugin** - Syntax highlighting, inline error markers, and
  local validation
- **AI Assistant with the RIDDL MCP server** - Natural-language queries, code
  generation, error explanations, and completeness analysis

## Usage Examples

### Validate the Open File

With a `.riddl` file open in the editor:

> Validate this RIDDL file and explain any errors

### Generate RIDDL Code

> Create a RIDDL entity for managing user accounts with login history
> and password reset functionality

### Understand Errors

> The RIDDL plugin shows "Undefined reference to type PaymentMethod" -
> what does this mean and how do I fix it?

### Check Completeness

> Is this domain model complete enough to generate a working application?

## Troubleshooting

### AI Assistant Not Available

- Verify the AI Assistant plugin is installed and enabled
- Check your JetBrains account has AI features enabled
- Update to a version with MCP support (2025.1+)

### MCP Tools Not Working

- Restart IntelliJ after configuration changes
- Verify `riddlg mcp` starts from a terminal (it waits on stdin)
- If `riddlg` isn't found, use its absolute path as the command
- Check **Help** > **Show Log in Finder/Explorer** for errors

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
