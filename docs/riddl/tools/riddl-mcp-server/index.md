# RIDDL MCP Server

The RIDDL MCP (Model Context Protocol) server gives AI assistants real RIDDL
language intelligence — parsing, validation, analysis, and generation — so
domain experts can describe what they want in natural language and have an
assistant turn it into valid RIDDL.

!!! info "The MCP server now ships in riddlg"
    What used to be a separately hosted Docker service is now built into the
    [`riddlg`](../riddlg/index.md) binary and runs **locally**. There is no
    container to build, no port to expose to the network, and no API key —
    your models never leave your machine. The tool names and result shapes
    are unchanged from the hosted server, so existing MCP clients keep working
    once pointed at the local server.

## What it does

When connected, an AI assistant can:

- **Validate** RIDDL source for syntax and semantic correctness
- **Outline** and **analyze** a model's structure and completeness
- **Explain** diagnostics in plain language, with likely fixes
- **Map** a natural-language domain description to RIDDL structure
- **Expand** built-in modeling patterns into RIDDL

## Running the server

Install riddlg (see [Installation](../riddlg/installation.md)):

```bash
brew install ossuminc/tap/riddlg
```

Then run it as an MCP server over either transport:

| Transport | Command | Connect via |
|-----------|---------|-------------|
| **stdio** | `riddlg mcp` | `command: riddlg`, `args: ["mcp"]` |
| **HTTP** | `riddlg serve` | `POST http://127.0.0.1:8910/mcp` |

Neither needs an API key. See
[Server API](../riddlg/server-api.md#post-mcp) for the HTTP session and
status-code details.

## Tools

Thirteen tools are exposed — two validators plus eleven derivation tools
(`check-completeness`, `suggest-next`, `map-domain-to-riddl`,
`validate-partial`, `expand-pattern`, `get-template`, `generate-test-cases`,
`check-simulability`, `explain-error`, `list-patterns`, `list-templates`).
See [MCP Tools](../riddlg/mcp-tools.md) for arguments and return shapes.

## Connecting an assistant

Step-by-step setup guides for each client live in the
[MCP section](../../../MCP/index.md):

- [Claude Desktop](../../../MCP/claude-desktop.md)
- [Claude Code](../../../MCP/claude-code.md)
- [Gemini CLI](../../../MCP/gemini.md)
- [GitHub Copilot CLI](../../../MCP/github-copilot.md)
- [VS Code with Copilot](../../../MCP/vscode-copilot.md)
- [IntelliJ AI Assistant](../../../MCP/intellij-ai.md)
- [IntelliJ Junie](../../../MCP/intellij-junie.md)

## Usage example

The typical AI-assisted authoring loop:

1. **Author describes** what they want in natural language
2. **The assistant** uses `map-domain-to-riddl` to draft a structure
3. **The assistant** validates the result with `riddl_validate`
4. **Author refines** and the assistant iterates using `suggest-next`

> **Author**: I need an entity to track user sessions with login time,
> last activity, and expiration.
>
> **AI**: Here's a starting point:
> ```riddl
> entity Session is {
>   state Active of record Fields is {
>     loginTime: TimeStamp
>     lastActivity: TimeStamp
>     expiration: TimeStamp
>     userId: Id(User)
>   }
>   handler SessionHandler is {
>     on command CreateSession { ??? }
>     on command UpdateActivity { ??? }
>     on command ExpireSession { ??? }
>   }
> }
> ```

## Resources

- [riddlg MCP Tools](../riddlg/mcp-tools.md) - the full tool catalog
- [riddlg Server API](../riddlg/server-api.md) - the HTTP surface
- [MCP Protocol Specification](https://modelcontextprotocol.io/)
- [Author's Guide](../../guides/authors/index.md) - AI-assisted authoring workflow
