---
title: "GitHub Copilot CLI Configuration"
description: >-
  Configure GitHub Copilot CLI to use the RIDDL MCP Server for AI-assisted
  domain modeling from the command line.
---
# GitHub Copilot CLI Configuration

This guide explains how to configure GitHub Copilot CLI to use the RIDDL MCP
Server for AI-assisted domain modeling.

## Prerequisites

- GitHub Copilot CLI installed (`gh extension install github/gh-copilot`)
- GitHub Copilot subscription (Individual, Business, or Enterprise)
- `riddlg` installed and on your `PATH`
  (see [Installation](../riddl/tools/riddlg/installation.md)):
  ```bash
  brew install ossuminc/tap/riddlg
  ```

## Installation

### Install GitHub CLI

If you don't have the GitHub CLI installed:

=== "macOS"
    ```bash
    brew install gh
    ```

=== "Windows"
    ```bash
    winget install GitHub.cli
    ```

=== "Linux"
    ```bash
    # Debian/Ubuntu
    sudo apt install gh

    # Fedora
    sudo dnf install gh
    ```

### Install Copilot Extension

```bash
gh extension install github/gh-copilot
```

### Authenticate

```bash
gh auth login
gh copilot auth
```

## Configuration

GitHub Copilot CLI launches MCP servers as local processes (stdio transport)
via a JSON configuration file.

### Configuration File Location

| Platform | Path |
|----------|------|
| **macOS** | `~/.config/gh-copilot/mcp-servers.json` |
| **Windows** | `%APPDATA%\gh-copilot\mcp-servers.json` |
| **Linux** | `~/.config/gh-copilot/mcp-servers.json` |

### Adding the RIDDL MCP Server

Create or edit the configuration file:

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

No URL and no API key — Copilot runs `riddlg mcp` for you. If `riddlg` isn't
on the system `PATH`, use its absolute path as the `command`.

## Verify Connection

Test the connection with a simple RIDDL validation:

```bash
gh copilot suggest "validate this RIDDL: domain Test is { ??? }"
```

Or in explain mode:

```bash
gh copilot explain "What does this RIDDL code do: domain Shop is { context Orders is { ??? } }"
```

## Usage

### Command Modes

| Command | Description |
|---------|-------------|
| `gh copilot suggest` | Get command or code suggestions |
| `gh copilot explain` | Explain code, errors, or concepts |

### RIDDL-Specific Examples

Validate a file:

```bash
gh copilot suggest "validate this RIDDL file: $(cat mymodel.riddl)"
```

Explain an error:

```bash
gh copilot explain "What does 'Undefined reference to type OrderId' mean in RIDDL?"
```

Generate from a description:

```bash
gh copilot suggest "Create RIDDL code for an e-commerce domain with products and orders"
```

### Pre-Commit Validation

Since `riddlg` is installed, the most reliable pre-commit check calls it
directly rather than going through the assistant:

```bash
#!/bin/bash
# .git/hooks/pre-commit
for file in $(git diff --cached --name-only | grep '\.riddl$'); do
    echo "Validating $file..."
    riddlg validate "$file" || exit 1
done
```

## Troubleshooting

### MCP Server Not Connecting

- Verify `riddlg mcp` starts from a terminal (it waits on stdin)
- Check JSON syntax in the configuration file
- If `riddlg` isn't found, use its absolute path as `command`

### Extension Issues

```bash
gh extension upgrade github/gh-copilot
```

### Debug Mode

```bash
GH_DEBUG=1 gh copilot suggest "your query"
```

## Available RIDDL Tools

When connected, Copilot can use these RIDDL tools:

| Tool | Use For |
|------|---------|
| `riddl_validate` | Check RIDDL source for syntax/semantic errors |
| `riddl_outline` | Summarize a model's definitions |
| `validate-partial` | Check incomplete models (ignore missing refs) |
| `check-completeness` | Find missing elements and get suggestions |
| `check-simulability` | Verify a model is simulation-ready |
| `map-domain-to-riddl` | Convert natural language to RIDDL |
| `explain-error` | Get detailed error explanations |
| `suggest-next` | Get recommendations for next steps |

See [MCP Tools](../riddl/tools/riddlg/mcp-tools.md) for the full catalog of 13.

## Related Resources

- [GitHub Copilot CLI Documentation](https://docs.github.com/en/copilot/github-copilot-in-the-cli)
- [VS Code Copilot Integration](./vscode-copilot.md) - For IDE-based usage
- [RIDDL Language Reference](../riddl/references/language-reference.md)

---

[Back to MCP Overview](./index.md)
