# VS Code Copilot Configuration

This guide explains how to configure VS Code with GitHub Copilot to use
the RIDDL MCP Server for AI-assisted domain modeling.

## Prerequisites

- Visual Studio Code installed
- GitHub Copilot and Copilot Chat extensions installed and activated
- `riddlg` installed and on your `PATH`
  (see [Installation](../riddl/tools/riddlg/installation.md)):
  ```bash
  brew install ossuminc/tap/riddlg
  ```

## Configuration

VS Code has built-in MCP support. Define the server once and Copilot's agent
mode can use it. The simplest scope is per-workspace, in `.vscode/mcp.json`.

### Workspace Configuration

Create `.vscode/mcp.json` in your project root:

```json
{
  "servers": {
    "riddl": {
      "type": "stdio",
      "command": "riddlg",
      "args": ["mcp"]
    }
  }
}
```

VS Code launches `riddlg mcp` as a local process — no URL and no API key.
After saving, VS Code shows a **Start** action above the server entry; click
it (or reload the window) to bring the tools online.

### User-Level Configuration

To make the server available in every workspace, add an `mcp` block to your
user `settings.json` (open with ++cmd+shift+p++ → "Preferences: Open User
Settings (JSON)"):

```json
{
  "mcp": {
    "servers": {
      "riddl": {
        "type": "stdio",
        "command": "riddlg",
        "args": ["mcp"]
      }
    }
  }
}
```

!!! note "`riddlg` must be found on PATH"
    If the tools don't appear, use the absolute path (e.g.
    `/opt/homebrew/bin/riddlg`) as the `command`.

## Verify Connection

1. Open Copilot Chat (++cmd+shift+i++ or ++ctrl+shift+i++) and switch to
   **Agent** mode
2. Ask: "Can you validate this RIDDL code?" and paste some RIDDL
3. Copilot should invoke the `riddl_validate` tool

You can see and toggle the available tools with the **Tools** picker in the
Chat view.

## Using with RIDDL Files

For the best experience, install both:

- **GitHub Copilot** - AI assistance with MCP tools
- **RIDDL Language Support** - Syntax highlighting and local validation

This gives you real-time highlighting and local validation as you type, plus
AI-powered assistance via Copilot Chat.

## Usage Examples

### Validate the Open File

> Validate the RIDDL file I have open and explain any errors

### Check Model Completeness

> What's missing from my domain model in this folder?

### Generate RIDDL from a Description

> Create a RIDDL context for managing customer subscriptions with monthly
> billing, plan changes, and cancellation

### Fix Errors

> I'm getting "Undefined reference to type OrderId" - how do I fix this?

## Troubleshooting

### MCP Not Recognized

- Verify the Copilot Chat extension is installed and you're in Agent mode
- Reload the window after editing `.vscode/mcp.json` or settings
- Check the **Output** panel → "MCP" for startup logs

### Server Won't Start

- Verify `riddlg mcp` runs from a terminal (it waits on stdin)
- If `riddlg` isn't found, use its absolute path as `command`
- Confirm `riddlg version` works

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
