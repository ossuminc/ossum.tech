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
- API key for the RIDDL MCP Server (contact support@ossuminc.com)

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

GitHub Copilot CLI uses a JSON configuration file for MCP servers.

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

### Using Environment Variables

You can use environment variables for sensitive values:

```json
{
  "mcpServers": {
    "riddl": {
      "url": "${RIDDL_MCP_URL:-https://mcp.ossuminc.com}/mcp/v1",
      "headers": {
        "X-API-KEY": "${RIDDL_API_KEY}"
      }
    }
  }
}
```

Then set in your shell profile:

```bash
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

Test the connection with a simple RIDDL validation:

```bash
gh copilot suggest "validate this RIDDL: domain Test is { }"
```

Or in explain mode:

```bash
gh copilot explain "What does this RIDDL code do: domain Shop is { context Orders is { } }"
```

## Usage

### Command Modes

GitHub Copilot CLI has two main modes:

| Command | Description |
|---------|-------------|
| `gh copilot suggest` | Get command or code suggestions |
| `gh copilot explain` | Explain code, errors, or concepts |

### RIDDL-Specific Examples

#### Validate RIDDL Code

```bash
gh copilot suggest "validate this RIDDL file: $(cat mymodel.riddl)"
```

#### Explain RIDDL Errors

```bash
gh copilot explain "What does 'Undefined reference to type OrderId' mean in RIDDL?"
```

#### Generate RIDDL from Description

```bash
gh copilot suggest "Create RIDDL code for an e-commerce domain with products and orders"
```

#### Check Model Completeness

```bash
gh copilot suggest "Check what's missing from this RIDDL model: $(cat mymodel.riddl)"
```

### Piping File Contents

For larger files, pipe content directly:

```bash
cat src/domain.riddl | gh copilot suggest "validate this RIDDL and list any errors"
```

### Interactive Mode

Start an interactive session:

```bash
gh copilot suggest
```

Then type your RIDDL-related questions at the prompt.

## Integration with Scripts

### Validation Script

Create a validation helper script:

```bash
#!/bin/bash
# validate-riddl.sh

if [ -z "$1" ]; then
    echo "Usage: validate-riddl.sh <file.riddl>"
    exit 1
fi

gh copilot suggest "Validate this RIDDL code and report any errors: $(cat $1)"
```

### Pre-Commit Hook

Add RIDDL validation to your Git workflow:

```bash
#!/bin/bash
# .git/hooks/pre-commit

for file in $(git diff --cached --name-only | grep '\.riddl$'); do
    echo "Validating $file..."
    gh copilot suggest "Validate this RIDDL: $(cat $file)" | grep -q "error" && {
        echo "Validation failed for $file"
        exit 1
    }
done
```

## Troubleshooting

### Authentication Issues

```bash
# Re-authenticate GitHub CLI
gh auth logout
gh auth login

# Re-authenticate Copilot
gh copilot auth
```

### MCP Server Not Connecting

- Test server directly: `curl https://mcp.ossuminc.com/health`
- Verify JSON syntax in configuration file
- Check API key is valid

### Extension Issues

```bash
# Update the extension
gh extension upgrade github/gh-copilot

# Reinstall if needed
gh extension remove github/gh-copilot
gh extension install github/gh-copilot
```

### Debug Mode

Enable verbose output:

```bash
GH_DEBUG=1 gh copilot suggest "your query"
```

## Available RIDDL Tools

When connected, Copilot can use these RIDDL tools:

| Tool | Use For |
|------|---------|
| `validate-text` | Check RIDDL source for syntax/semantic errors |
| `validate-url` | Validate RIDDL from GitHub URLs |
| `validate-partial` | Check incomplete models (ignore missing refs) |
| `check-completeness` | Find missing elements and get suggestions |
| `check-simulability` | Verify model can run in riddlsim |
| `map-domain-to-riddl` | Convert natural language to RIDDL |
| `explain-error` | Get detailed error explanations |
| `suggest-next` | Get recommendations for next steps |

## Tips for Effective Use

1. **Be specific**: Include context about what you're trying to achieve

2. **Quote RIDDL code**: Use proper quoting to preserve syntax
   ```bash
   gh copilot suggest "validate: $(cat file.riddl)"
   ```

3. **Use explain for learning**: Ask Copilot to explain RIDDL concepts
   ```bash
   gh copilot explain "What is a bounded context in RIDDL?"
   ```

4. **Iterate**: Start with high-level structure, then refine details

5. **Combine with local tools**: Use `gh copilot` alongside `riddlc` for
   comprehensive validation

## Related Resources

- [GitHub Copilot CLI Documentation](https://docs.github.com/en/copilot/github-copilot-in-the-cli)
- [VS Code Copilot Integration](./vscode-copilot.md) - For IDE-based usage
- [RIDDL Language Reference](../riddl/references/language-reference.md)

---

[Back to MCP Overview](./index.md)
