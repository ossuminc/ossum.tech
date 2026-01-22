# Gemini CLI Configuration

This guide explains how to configure Google's Gemini CLI to use the RIDDL
MCP Server for AI-assisted domain modeling.

## Prerequisites

- Gemini CLI installed (`npm install -g @anthropic-ai/gemini-cli` or via Google)
- API key for the RIDDL MCP Server (contact support@ossuminc.com)

## Configuration

Gemini CLI uses a JSON settings file for MCP server configuration.

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

### Using Environment Variables

Gemini CLI supports environment variable substitution in configuration:

```json
{
  "mcpServers": {
    "riddl": {
      "url": "${RIDDL_MCP_URL}/mcp/v1",
      "headers": {
        "X-API-KEY": "${RIDDL_API_KEY}"
      }
    }
  }
}
```

Then set environment variables:

```bash
export RIDDL_MCP_URL="{{MCP_SERVER_URL}}"
export RIDDL_API_KEY="your-api-key"
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

## Verify Connection

Start Gemini CLI and test the connection:

```bash
gemini
```

Then ask:

> Can you validate this RIDDL code?
> ```riddl
> domain Example is { }
> ```

Gemini should use the `validate-text` tool and return results.

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
      "url": "{{MCP_SERVER_URL}}/mcp/v1",
      "headers": {
        "X-API-KEY": "your-api-key"
      },
      "includeTools": [
        "validate-text",
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
      "url": "{{MCP_SERVER_URL}}/mcp/v1",
      "headers": {
        "X-API-KEY": "your-api-key"
      },
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

### Trust Mode

For development environments where you trust the server completely:

```json
{
  "mcpServers": {
    "riddl": {
      "url": "http://localhost:8080/mcp/v1",
      "headers": {
        "X-API-KEY": "dev-key"
      },
      "trust": true
    }
  }
}
```

!!! danger "Security Warning"
    The `trust` option bypasses confirmation dialogs. Only use this for
    servers you completely control in development environments.

## Debugging

### Enable Debug Mode

Run Gemini CLI with verbose output:

```bash
gemini --debug
```

In interactive mode, press ++f12++ to open the debug console.

### Check MCP Connection

The debug output shows:

- MCP server connection attempts
- Tool discovery results
- Request/response details
- Any error messages

## Troubleshooting

### Server Not Connecting

- Test the server: `curl {{MCP_SERVER_URL}}/health`
- Verify JSON syntax in settings file
- Check URL doesn't have trailing slashes
- Enable debug mode for detailed logs

### Authentication Errors

- Verify API key is correct
- Check for environment variable resolution issues
- Try hardcoding the key temporarily to isolate the issue

### Tools Not Available

- Restart Gemini CLI after configuration changes
- Check that `includeTools` doesn't filter out needed tools
- Verify server is returning tool list correctly

### Slow Responses

- Large RIDDL models may take longer to validate
- Check network latency to server
- Consider using a local server for development

## Available RIDDL Tools

| Tool | Use Case |
|------|----------|
| `validate-text` | Check RIDDL source for errors |
| `validate-url` | Validate RIDDL from URLs |
| `validate-partial` | Check incomplete models |
| `check-completeness` | Find missing elements |
| `check-simulability` | Verify simulation readiness |
| `map-domain-to-riddl` | Convert descriptions to RIDDL |
| `explain-error` | Understand validation errors |
| `suggest-next` | Get recommendations |

## Resources

- [Gemini CLI Documentation](https://google-gemini.github.io/gemini-cli/docs/tools/mcp-server.html)
- [MCP Server Integration Guide](https://geminicli.com/docs/tools/mcp-server/)

---

[Back to MCP Overview](./index.md)