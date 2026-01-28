# IntelliJ AI Assistant Configuration

This guide explains how to configure IntelliJ IDEA's built-in AI Assistant
to use the RIDDL MCP Server for AI-assisted domain modeling.

## Prerequisites

- IntelliJ IDEA 2024.1 or later (Ultimate or Community with AI plugin)
- AI Assistant plugin enabled
- API key for the RIDDL MCP Server (contact support@ossuminc.com)

## Configuration

IntelliJ AI Assistant uses JSON configuration for MCP servers.

### Configuration File Location

| Platform | Path |
|----------|------|
| **macOS** | `~/Library/Application Support/JetBrains/IntelliJIdea2024.x/options/ai.xml` |
| **Windows** | `%APPDATA%\JetBrains\IntelliJIdea2024.x\options\ai.xml` |
| **Linux** | `~/.config/JetBrains/IntelliJIdea2024.x/options/ai.xml` |

!!! note "Version-Specific Path"
    Replace `2024.x` with your actual IntelliJ version number.

### Alternative: Settings UI

Some versions support configuring MCP servers through the UI:

1. Open **Settings** (++cmd+comma++ or ++ctrl+alt+s++)
2. Navigate to **Tools** > **AI Assistant**
3. Look for **MCP Servers** or **External Tools** section
4. Add the RIDDL server configuration

### Adding via Configuration File

If your version requires direct file editing, add this to your AI
configuration:

```xml
<component name="AiAssistantSettings">
  <option name="mcpServers">
    <map>
      <entry key="riddl">
        <value>
          <McpServerConfig>
            <option name="url" value="https://mcp.ossuminc.com/mcp/v1" />
            <option name="headers">
              <map>
                <entry key="X-API-KEY" value="your-api-key" />
              </map>
            </option>
          </McpServerConfig>
        </value>
      </entry>
    </map>
  </option>
</component>
```

### JSON-Based Configuration

If your IntelliJ version uses JSON configuration, create or edit the MCP
settings file:

**Location**: `~/.config/JetBrains/IntelliJIdea2024.x/mcp-servers.json`

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

After modifying the configuration:

1. Close IntelliJ IDEA completely
2. Relaunch IntelliJ IDEA
3. Open a RIDDL file to verify the tools are available

## Verify Connection

Open the AI Assistant chat and ask:

> Can you validate this RIDDL code?
> ```riddl
> domain Example is { }
> ```

The AI should use the `validate-text` tool and return validation results.

## Using with RIDDL Plugin

For the best experience, install both:

- **RIDDL4IDEA Plugin** - Syntax highlighting and local validation
- **AI Assistant with MCP** - AI-powered assistance

### Combined Benefits

1. **RIDDL4IDEA** provides:
   - Real-time syntax highlighting
   - Inline error markers
   - Clickable error navigation
   - Validation tool window

2. **AI Assistant with RIDDL MCP** provides:
   - Natural language queries
   - Code generation assistance
   - Error explanations
   - Model completeness analysis

## Usage Examples

### Validate Open File

With a `.riddl` file open in the editor:

> @file Validate this RIDDL file and explain any errors

### Generate RIDDL Code

> Create a RIDDL entity for managing user accounts with login history
> and password reset functionality

### Understand Errors

> The RIDDL plugin shows "Undefined reference to type PaymentMethod" -
> what does this mean and how do I fix it?

### Check Completeness

> Is this domain model complete enough to generate a working application?

### Convert Requirements

> Convert this user story to RIDDL:
> "As a customer, I want to add items to my shopping cart so I can
> purchase them later"

## AI Assistant Actions

### Context Menu

Right-click in a RIDDL file for AI options:

- **AI Actions** > **Explain**
- **AI Actions** > **Suggest**
- **AI Actions** > **Generate**

### Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| ++alt+enter++ | Show AI suggestions (if available) |
| ++cmd+shift+a++ | Search actions (type "AI") |

## Troubleshooting

### AI Assistant Not Available

- Verify AI Assistant plugin is installed and enabled
- Check your JetBrains account has AI features enabled
- Update to latest IntelliJ version

### MCP Tools Not Working

- Restart IntelliJ after configuration changes
- Check **Help** > **Show Log in Finder/Explorer** for errors
- Verify JSON/XML configuration syntax

### Connection Errors

- Test the server: `curl https://mcp.ossuminc.com/health`
- Check firewall settings
- Verify API key is correct

### Tools Not Recognized

- Ensure the AI Assistant supports MCP (check version requirements)
- Try the JSON-based configuration if XML doesn't work
- Contact JetBrains support for version-specific guidance

## Recommended Workflow

1. **Open RIDDL file** - RIDDL4IDEA highlights syntax
2. **Write code** - Get real-time validation feedback
3. **Ask AI for help** - Use chat for complex questions
4. **Generate code** - Let AI create boilerplate
5. **Validate thoroughly** - Use `check-completeness` before finalizing

---

[Back to MCP Overview](./index.md)