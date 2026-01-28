# VS Code Copilot Configuration

This guide explains how to configure VS Code with GitHub Copilot to use
the RIDDL MCP Server for AI-assisted domain modeling.

## Prerequisites

- Visual Studio Code installed
- GitHub Copilot extension installed and activated
- GitHub Copilot Chat extension (for MCP support)
- API key for the RIDDL MCP Server (contact support@ossuminc.com)

## Configuration

VS Code Copilot uses the `settings.json` file for MCP server configuration.

### Opening Settings

1. Open VS Code
2. Press ++cmd+comma++ (Mac) or ++ctrl+comma++ (Windows/Linux)
3. Click the **Open Settings (JSON)** icon in the top right
4. Or open directly: ++cmd+shift+p++ > "Preferences: Open User Settings (JSON)"

### Adding the RIDDL MCP Server

Add the MCP server configuration to your `settings.json`:

```json
{
  "github.copilot.chat.mcpServers": {
    "riddl": {
      "url": "https://mcp.ossuminc.com/mcp/v1",
      "headers": {
        "X-API-KEY": "your-api-key"
      }
    }
  }
}
```

!!! warning "Server Coming Soon"
    The hosted MCP server at `mcp.ossuminc.com` will be available in early 2026.
    For now, use a [local server](#using-a-local-server) for development.
    Replace `your-api-key` with your actual API key.

### Workspace-Level Configuration

For project-specific configuration, create or edit `.vscode/settings.json`
in your workspace:

```json
{
  "github.copilot.chat.mcpServers": {
    "riddl": {
      "url": "https://mcp.ossuminc.com/mcp/v1",
      "headers": {
        "X-API-KEY": "your-api-key"
      }
    }
  }
}
```

### Using a Local Server

For development with a locally running server:

```json
{
  "github.copilot.chat.mcpServers": {
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

1. Open Copilot Chat (++cmd+shift+i++ or ++ctrl+shift+i++)
2. Ask: "Can you validate this RIDDL code?"
3. Paste some RIDDL code
4. Copilot should use the RIDDL validation tool

## Using with RIDDL Files

### Combined with RIDDL Extension

For the best experience, install both:

- **GitHub Copilot** - AI assistance with MCP tools
- **RIDDL Language Support** - Syntax highlighting and local validation

This gives you:

- Real-time syntax highlighting
- Local validation as you type
- AI-powered assistance via Copilot Chat

### Inline Assistance

While editing a `.riddl` file, use Copilot Chat:

> "Add a command handler to this entity for updating the address"

Copilot can:

1. Understand the context of your current file
2. Use RIDDL MCP tools to validate suggestions
3. Generate correct RIDDL syntax

## Usage Examples

### Validate Current File

In Copilot Chat:

> @workspace Validate the RIDDL file I have open

### Check Model Completeness

> @workspace What's missing from my domain model in this folder?

### Generate RIDDL from Description

> Create a RIDDL context for managing customer subscriptions with these
> features: monthly billing, plan changes, cancellation

### Fix Errors

> I'm getting "Undefined reference to type OrderId" - how do I fix this?

### Get Suggestions

> What should I add next to make this entity ready for implementation?

## Chat Commands

Use Copilot Chat participants for different contexts:

| Command | Description |
|---------|-------------|
| `@workspace` | Include workspace context in query |
| `@vscode` | Ask about VS Code features |
| `/explain` | Explain selected code |
| `/fix` | Fix issues in selected code |

### Examples

```
@workspace /explain the Order entity in src/orders.riddl

@workspace /fix the validation errors in this RIDDL file
```

## Troubleshooting

### MCP Not Recognized

- Verify GitHub Copilot Chat extension is installed
- Check that MCP support is enabled in your Copilot subscription
- Restart VS Code after configuration changes

### Connection Errors

- Test the server: `curl https://mcp.ossuminc.com/health`
- Verify URL doesn't have trailing slashes
- Check API key is correct

### Tools Not Working

- Look in Output panel > "GitHub Copilot Chat" for errors
- Verify JSON syntax in settings
- Try removing and re-adding the configuration

## Integration with RIDDL Extension

When both extensions are active:

1. **RIDDL extension** provides:
   - Syntax highlighting
   - Local validation (instant feedback)
   - Code completion for keywords

2. **Copilot with RIDDL MCP** provides:
   - Deep semantic analysis
   - Natural language to RIDDL conversion
   - Error explanations
   - Model completeness checking
   - Simulation readiness analysis

### Recommended Workflow

1. Use RIDDL extension for real-time syntax feedback
2. Use Copilot Chat for complex questions and generation
3. Ask Copilot to validate when making significant changes
4. Use `check-completeness` before finalizing models

---

[Back to MCP Overview](./index.md)