# Claude Desktop Configuration

This guide explains how to configure Claude Desktop to use the RIDDL MCP
Server for AI-assisted domain modeling.

## Prerequisites

- Claude Desktop application installed
- API key for the RIDDL MCP Server (contact support@ossuminc.com)

## Configuration

Claude Desktop uses a JSON configuration file to define MCP servers.

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
      "url": "{{MCP_SERVER_URL}}/mcp/v1",
      "headers": {
        "X-API-KEY": "your-api-key"
      }
    }
  }
}
```

!!! warning "Replace Placeholders"
    - Replace `{{MCP_SERVER_URL}}` with the actual server URL when available
    - Replace `your-api-key` with your actual API key

### Complete Example

If you have other MCP servers configured, add RIDDL alongside them:

```json
{
  "mcpServers": {
    "riddl": {
      "url": "{{MCP_SERVER_URL}}/mcp/v1",
      "headers": {
        "X-API-KEY": "your-api-key"
      }
    },
    "filesystem": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "/path/to/files"]
    }
  }
}
```

### Using a Local Server

For development with a locally running server:

```json
{
  "mcpServers": {
    "riddl": {
      "url": "http://localhost:8080/mcp/v1",
      "headers": {
        "X-API-KEY": "your-local-api-key"
      }
    }
  }
}
```

## Restart Claude Desktop

After modifying the configuration:

1. Quit Claude Desktop completely
2. Relaunch Claude Desktop
3. The RIDDL tools should now be available

## Verify Connection

Ask Claude to verify the connection:

> "Can you validate this RIDDL code for me?"
> ```riddl
> domain Example is { }
> ```

Claude should use the `validate-text` tool and return validation results.

## Usage Examples

### Validate RIDDL Code

> "Please validate this RIDDL model and explain any errors:"
> ```riddl
> domain OrderManagement is {
>   context Orders is {
>     entity Order is { }
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

## Troubleshooting

### Server Not Connecting

- Verify the URL is correct and accessible
- Check that your API key is valid
- Ensure the server is running (test with `curl {{MCP_SERVER_URL}}/health`)

### Tools Not Appearing

- Restart Claude Desktop after configuration changes
- Check for JSON syntax errors in the configuration file
- Verify the `mcpServers` key is at the top level of the JSON

### Authentication Errors

- Verify your API key is correctly entered
- Check for extra spaces or quotes around the key
- Contact support@ossuminc.com if issues persist

## Available RIDDL Tools in Claude

Once connected, Claude can use these tools:

| Tool | Ask Claude To... |
|------|-----------------|
| `validate-text` | "Validate this RIDDL code" |
| `validate-partial` | "Check this incomplete model" |
| `check-completeness` | "What's missing from this model?" |
| `check-simulability` | "Can this model be simulated?" |
| `map-domain-to-riddl` | "Convert this description to RIDDL" |
| `explain-error` | "Explain this error message" |
| `suggest-next` | "What should I add next?" |

---

[Back to MCP Overview](./index.md)