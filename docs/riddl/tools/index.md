# Tools

There are several tools for working with RIDDL models:

## [Playground](../playground/index.md) :material-new-box:{ .bounce }

Try RIDDL in your browser without installing anything. The playground provides
a Monaco-based editor with real-time validation—perfect for learning and
experimentation. *(Coming soon)*

## [riddlc](riddlc/index.md)

The RIDDL compiler (`riddlc`) is the command-line tool for parsing and
validating RIDDL models. It can:

- Validate syntax and semantics
- Output analysis reports

Documentation and diagram generation will be available through
[Synapify](../../synapify/index.md).

## [riddlg](riddlg/index.md)

The RIDDL generator (`riddlg`) is a locally-run native binary that
validates RIDDL models and generates from them — documentation (AsciiDoc,
MkDocs), API specifications (Smithy, gRPC, OpenAPI), and (Pro) Quarkus
code. It can also generate RIDDL models from natural-language descriptions
using a local AI model, so nothing need leave your machine — or, with a Pro
subscription, using your own API key for a cloud provider. It doubles as a
[RIDDL MCP server](riddlg/mcp-tools.md) for AI assistants.

## [riddl-idea-plugin](riddl-idea-plugin/index.md)

An IntelliJ IDEA plugin (2024.3+) that provides IDE support for editing RIDDL
files, including syntax highlighting, validation, and navigation.

## [riddl-mcp-server](riddl-mcp-server/index.md)

An MCP (Model Context Protocol) server that provides AI assistants with RIDDL
language intelligence, enabling AI-assisted model authoring.

## Synapify

A desktop application for visual RIDDL modeling with AI assistance. Synapify
provides a graphical interface for creating and editing RIDDL models, with
integrated AI support for generating definitions.

See the [Synapify Section](../../synapify/index.md) for more details.

## VS Code Extension

A Visual Studio Code extension for RIDDL editing. Provides syntax highlighting
and basic language support for VS Code users.

See the [riddl-vscode repository](https://github.com/ossuminc/riddl-vscode)
for installation instructions.
