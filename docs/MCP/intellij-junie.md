# IntelliJ Junie Configuration

This guide explains how to configure JetBrains Junie (the autonomous coding
agent) to use the RIDDL MCP Server for AI-assisted domain modeling.

## What is Junie?

Junie is JetBrains' autonomous AI coding agent that can understand your
codebase, execute tasks, and make changes across multiple files. With the
RIDDL MCP Server connected, Junie gains specialized capabilities for working
with RIDDL domain models.

## Prerequisites

- IntelliJ IDEA 2024.2 or later with Junie support
- Junie enabled in your JetBrains account
- API key for the RIDDL MCP Server (contact support@ossuminc.com)

## Configuration

### Settings UI Method

1. Open **Settings** (++cmd+comma++ or ++ctrl+alt+s++)
2. Navigate to **Tools** > **Junie**
3. Find the **MCP Servers** or **External Tools** section
4. Click **Add Server** and enter:

| Field | Value |
|-------|-------|
| **Name** | `riddl` |
| **URL** | `https://mcp.ossuminc.com/mcp/v1` |
| **API Key Header** | `X-API-KEY` |
| **API Key** | `your-api-key` |

### Configuration File Method

If your version requires file-based configuration:

**Location**: `~/.config/JetBrains/IntelliJIdea2024.x/junie/mcp-servers.json`

```json
{
  "mcpServers": {
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

## Restart IntelliJ

After configuration:

1. Close IntelliJ IDEA
2. Relaunch IntelliJ IDEA
3. Open Junie to verify RIDDL tools are available

## Junie Capabilities with RIDDL

### Autonomous Tasks

Junie can autonomously:

- Validate all RIDDL files in your project
- Fix validation errors across multiple files
- Generate new entities, contexts, or domains
- Refactor RIDDL structures
- Add missing documentation

### Example Autonomous Tasks

#### "Validate and fix my RIDDL model"

Junie will:

1. Scan all `.riddl` files in the project
2. Run validation on each file
3. Identify and fix resolvable errors
4. Report issues requiring human decision

#### "Create a complete order management context"

Junie will:

1. Understand your existing domain structure
2. Generate entities, commands, events, and handlers
3. Ensure proper references between definitions
4. Validate the generated code

#### "Make this model simulation-ready"

Junie will:

1. Run `check-simulability` on your model
2. Identify missing handlers and state definitions
3. Add placeholder implementations
4. Re-validate until simulation-ready

## Usage Examples

### Project-Wide Validation

Open Junie and ask:

> Validate all RIDDL files in this project and create a report of any issues

### Generate from Requirements

> Create RIDDL definitions for a subscription management system with:
> - Monthly and annual plans
> - Automatic renewal
> - Cancellation handling
> - Usage tracking

### Refactoring

> Move the Payment entity from the Orders context to a new Payments
> context, updating all references

### Documentation

> Add brief descriptions to all entities and types that are missing
> documentation

### Error Resolution

> The validation shows 15 undefined reference errors. Fix them by
> adding the missing type definitions

## Junie + RIDDL4IDEA

For the best experience, use both:

### RIDDL4IDEA Plugin

- Real-time syntax highlighting
- Inline validation as you type
- Clickable error navigation
- Manual validation control

### Junie with RIDDL MCP

- Autonomous multi-file operations
- Natural language task execution
- Intelligent code generation
- Batch error fixing

### Workflow Example

1. **Write code** - RIDDL4IDEA shows instant feedback
2. **Hit a complex issue** - Ask Junie for help
3. **Need new features** - Describe to Junie in natural language
4. **Review changes** - Junie shows diffs before applying
5. **Validate** - Both tools confirm correctness

## Advanced Usage

### Custom Prompts

Create reusable prompts for common RIDDL tasks:

```
# .junie/prompts/validate-model.md

Validate all RIDDL files in the project using the MCP server.
For each error:
1. Explain what's wrong
2. Suggest a fix
3. Apply the fix if it's unambiguous
4. Ask for confirmation on ambiguous fixes
```

### Integration with Tests

> After generating RIDDL code, validate it and check if it would pass
> simulation. Report any issues that would prevent simulation.

### Continuous Improvement

> Review my RIDDL model and suggest improvements for:
> - Better naming conventions
> - Missing error handling
> - Incomplete handlers
> - Documentation gaps

## Troubleshooting

### Junie Not Available

- Verify Junie is enabled in your JetBrains account
- Check IntelliJ version supports Junie
- Update to latest IntelliJ version

### MCP Tools Not Working

- Restart IntelliJ after configuration
- Check Junie logs: **View** > **Tool Windows** > **Junie** > **Logs**
- Verify network connectivity to MCP server

### Tasks Timing Out

- Large projects may need longer timeouts
- Consider running validation on subsets of files
- Check server response times

### Unexpected Changes

- Always review Junie's proposed changes before applying
- Use version control to track and revert if needed
- Start with smaller tasks to build confidence

## Best Practices

1. **Start small**: Test Junie with simple RIDDL tasks first
2. **Review diffs**: Always review changes before applying
3. **Use version control**: Commit before running autonomous tasks
4. **Provide context**: Include relevant requirements in your prompts
5. **Iterate**: Break large tasks into smaller, verifiable steps

---

[Back to MCP Overview](./index.md)