# Claude Code Configuration

This guide explains how to configure Claude Code (Anthropic's CLI tool) to
use the RIDDL MCP Server for AI-assisted domain modeling.

## Prerequisites

- Claude Code CLI installed (`npm install -g @anthropic-ai/claude-code`)
- API key for the RIDDL MCP Server (contact support@ossuminc.com)

## Configuration

Claude Code uses a JSON settings file for MCP server configuration.

### Configuration File Location

| Platform | Path |
|----------|------|
| **macOS** | `~/.claude/settings.json` |
| **Windows** | `%USERPROFILE%\.claude\settings.json` |
| **Linux** | `~/.claude/settings.json` |

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

### Project-Level Configuration

You can also configure the RIDDL MCP server for a specific project by
creating a `.claude/settings.json` file in your project root:

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

Project-level settings merge with user-level settings, with project
settings taking precedence.

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

Start Claude Code and ask it to test the connection:

```bash
claude
```

Then in the session:

> "Can you validate this RIDDL: `domain Test is { }`"

Claude should use the `validate-text` tool and return results.

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

Claude will use `validate-text` and `explain-error` to help you resolve
issues.

### Checking Model Quality

> "Check if my order management model is complete enough for simulation"

Claude will use `check-completeness` and `check-simulability` to analyze
your model.

## Workflow Integration

### With Git Repositories

Claude Code works well with RIDDL projects under version control:

```bash
cd my-riddl-project
claude
```

> "Review all the .riddl files in this project and create a summary of
> the domain model"

### Continuous Validation

As you edit RIDDL files, ask Claude to validate your changes:

> "I just updated src/contexts/orders.riddl - can you validate it?"

### Documentation Generation

> "Generate documentation for the entity definitions in this model"

## Troubleshooting

### Server Not Connecting

- Test the server directly: `curl {{MCP_SERVER_URL}}/health`
- Verify JSON syntax in settings file
- Check that the URL doesn't have trailing slashes

### Authentication Errors

- Verify API key is correct
- Check for accidental whitespace in the key
- Ensure headers are properly formatted in JSON

### Tools Not Available

- Restart Claude Code after configuration changes
- Check the MCP server logs for connection attempts
- Verify the `mcpServers` object exists in settings

## Available RIDDL Tools

| Tool | Use Case |
|------|----------|
| `validate-text` | Check RIDDL source for errors |
| `validate-url` | Validate RIDDL from GitHub URLs |
| `validate-partial` | Check incomplete/in-progress models |
| `check-completeness` | Find missing elements |
| `check-simulability` | Verify simulation readiness |
| `map-domain-to-riddl` | Convert descriptions to RIDDL |
| `explain-error` | Understand validation errors |
| `suggest-next` | Get recommendations for next steps |

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