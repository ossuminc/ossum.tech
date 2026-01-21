# RIDDL IDEA Plugin

The RIDDL IDEA plugin provides IntelliJ IDEA integration for editing RIDDL
specifications. It brings IDE-quality editing features to RIDDL authors,
including syntax highlighting, validation, code completion, and navigation.

## Requirements

- IntelliJ IDEA 2024.3 or later (Community or Ultimate)
- JDK 21 or later

## Installation

### From JetBrains Marketplace

1. Open IntelliJ IDEA
2. Go to **Settings** → **Plugins** → **Marketplace**
3. Search for "RIDDL"
4. Click **Install**
5. Restart IDEA when prompted

### Manual Installation

For development or preview versions:

1. Build the plugin:
   ```bash
   git clone https://github.com/ossuminc/riddl-idea-plugin.git
   cd riddl-idea-plugin
   sbt packageArtifactZip
   ```

2. Install in IDEA:
   - Go to **Settings** → **Plugins**
   - Click the gear icon → **Install Plugin from Disk...**
   - Select the generated `.zip` file from `target/`

## Features

### Syntax Highlighting

The plugin provides comprehensive syntax highlighting for RIDDL files (`.riddl`):

- **Keywords**: Domain, context, entity, handler, etc.
- **Types**: Predefined types and custom type definitions
- **Strings**: Documentation strings and descriptions
- **Comments**: Line and block comments
- **Operators**: Braces, brackets, and punctuation

Colors are customizable via **Settings** → **Editor** → **Color Scheme** →
**RIDDL**.

### Code Completion

As you type, the plugin suggests:

- RIDDL keywords in appropriate contexts
- Type names and references
- Definition names within scope

Trigger completion with `Ctrl+Space` (Windows/Linux) or `Cmd+Space` (macOS).

### Real-Time Validation

The plugin validates your RIDDL files as you type, showing:

- **Syntax errors**: Invalid RIDDL syntax
- **Semantic errors**: Undefined references, invalid containment
- **Warnings**: Style issues, missing documentation

Errors appear as red underlines with descriptions in the gutter and Problems
view.

### Structure View

View your RIDDL model hierarchy in the Structure tool window (`Alt+7`):

- Domains, contexts, entities
- Handlers and their clauses
- Types and fields
- Collapsible tree navigation

Click any element to navigate directly to its definition.

### Navigation

- **Go to Declaration**: `Ctrl+B` or `Cmd+B` to jump to a definition
- **Find Usages**: `Alt+F7` to find all references to a definition
- **File Structure**: `Ctrl+F12` to see current file structure

### Code Folding

Collapse and expand definition blocks to focus on relevant sections:

- Domain and context bodies
- Handler definitions
- Type definitions
- Documentation blocks

### Brace Matching

The plugin highlights matching braces, brackets, and parentheses. Place your
cursor on any brace to see its partner highlighted.

### Commenting

Use standard IDE shortcuts:

- `Ctrl+/` or `Cmd+/`: Toggle line comment (`//`)
- `Ctrl+Shift+/` or `Cmd+Shift+/`: Toggle block comment (`/* */`)

## RIDDL Tool Window

The plugin adds a dedicated RIDDL tool window with:

- **Compile**: Run riddlc validation on current file
- **Settings**: Quick access to plugin settings
- **Terminal**: View compilation output and messages

Access via **View** → **Tool Windows** → **RIDDL** or click the RIDDL icon
in the tool window bar.

## MCP Integration

The plugin can connect to the [riddl-mcp-server](../riddl-mcp-server/index.md)
for AI-assisted model generation. When configured:

- Get AI suggestions for completing definitions
- Generate handler implementations from descriptions
- Expand brief descriptions into full specifications

### Configuring MCP

1. Go to **Settings** → **Tools** → **RIDDL**
2. Enter your MCP server URL (e.g., `http://localhost:8080`)
3. Enter your API key
4. Click **Test Connection** to verify

## Settings

Access plugin settings at **Settings** → **Tools** → **RIDDL**:

| Setting | Description |
|---------|-------------|
| RIDDL Path | Path to riddlc executable for validation |
| MCP Server URL | URL of riddl-mcp-server for AI features |
| API Key | Authentication key for MCP server |
| Validate on Save | Automatically validate when saving files |
| Show Warnings | Display warning-level messages |

## Troubleshooting

### Plugin Not Recognizing .riddl Files

1. Check that files have the `.riddl` extension
2. Go to **Settings** → **Editor** → **File Types**
3. Verify "RIDDL" is listed and associated with `*.riddl`

### Validation Not Working

1. Ensure riddlc is installed and in your PATH
2. Check the RIDDL path setting in plugin configuration
3. Verify the file has valid RIDDL syntax

### Slow Performance

For large RIDDL specifications:

1. Increase IDEA's heap size in `idea.vmoptions`
2. Consider splitting large files using `include` directives
3. Disable "Validate on Save" for faster editing

## Building from Source

```bash
# Clone the repository
git clone https://github.com/ossuminc/riddl-idea-plugin.git
cd riddl-idea-plugin

# Build
sbt compile

# Run tests
sbt test

# Package for local testing
sbt packageArtifactZip

# Publish to JetBrains Marketplace (maintainers only)
sbt publishPlugin
```

## Resources

- [GitHub Repository](https://github.com/ossuminc/riddl-idea-plugin)
- [RIDDL Language Reference](../../references/language-reference.md)
- [Author's Guide](../../guides/authors/index.md)
