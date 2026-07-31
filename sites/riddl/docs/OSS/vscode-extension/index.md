# VS Code Extension for RIDDL

The RIDDL Language Support extension provides comprehensive development tools
for the RIDDL language in Visual Studio Code, including intelligent code
completion, real-time diagnostics, and code navigation.

[Release Notes](https://github.com/ossuminc/riddl-vscode/releases/tag/0.9.0-beta)

## Installation

### Beta Program

The extension is currently in beta. To install:

1. Download the `.vsix` file from
   [GitHub Release Assets](https://github.com/ossuminc/riddl-vscode/releases/download/0.9.0-beta/riddl-vscode-0.9.0-beta.vsix)
2. Open VS Code
3. Press ++cmd+shift+p++ (Mac) or ++ctrl+shift+p++ (Windows/Linux)
4. Type "Install from VSIX" and select it
5. Browse to the downloaded `.vsix` file
6. Click **Install** and reload VS Code

Or via command line:

```bash
code --install-extension /path/to/riddl-vscode-0.9.0-beta.vsix
```

### VS Code Marketplace (Coming Soon)

When version 1.0 is released, installation will be simpler:

1. Open VS Code
2. Click the **Extensions** tab in the left sidebar
3. Search for "RIDDL"
4. Click **Install**

### Requirements

- VS Code 1.75.0 or later
- No additional runtime dependencies (RIDDL parser is bundled)

---

## Features

### Syntax Highlighting

The extension provides rich syntax highlighting using both TextMate grammar
(fast initial highlighting) and semantic tokens (context-aware refinement):

| Element | Description |
|---------|-------------|
| **Keywords** | `domain`, `context`, `entity`, `type`, `command`, `event`, etc. |
| **Predefined Types** | `String`, `Integer`, `Boolean`, `Timestamp`, `UUID`, etc. |
| **Readability Words** | `is`, `of`, `by`, `for`, `to`, `from`, `with`, `and`, etc. |
| **Comments** | Line (`//`) and block (`/* */`) comments |
| **Strings** | Quoted string literals with escape sequences |
| **Documentation** | Markdown lines starting with `\|` |

### Code Completion (IntelliSense)

Press ++ctrl+space++ to trigger completion, or just start typing. The
extension provides:

#### Keywords with Snippets

Over 50 keywords with intelligent snippets:

| Keyword | Snippet Produces |
|---------|-----------------|
| `domain` | Full domain structure with braces |
| `context` | Context definition template |
| `entity` | Entity with state and handlers |
| `type` | Type definition |
| `command` | Command message definition |
| `event` | Event message definition |
| `handler` | Handler with `on` clause template |
| `saga` | Saga with steps template |

**Example:** Type `entity` and press ++tab++:

```riddl
entity Name is {
  // cursor here
}
```

#### Predefined Types

All RIDDL predefined types with documentation:

- `String`, `Integer`, `Number`, `Boolean`, `Decimal`
- `Date`, `Time`, `DateTime`, `Timestamp`, `Duration`
- `Id`, `UUID`, `URL`, `UserId`
- `List`, `Set`, `Map`, `Sequence`
- And more...

#### Readability Words

Structural keywords that improve RIDDL readability:

- `is`, `of`, `by`, `for`, `to`, `from`, `with`
- `and`, `or`, `not`, `in`, `on`, `at`

### Hover Documentation

Hover over any keyword, type, or readability word to see documentation:

- **Keywords**: Comprehensive descriptions with usage notes
- **Types**: Type-specific documentation with examples
- **Readability Words**: Explanations of structural role
- **User Definitions**: Location information (line/column)

### Real-Time Diagnostics

The extension validates your RIDDL as you type:

| Severity | Indicator | Examples |
|----------|-----------|----------|
| **Error** | Red squiggly | Syntax errors, undefined references |
| **Warning** | Yellow squiggly | Missing documentation, style issues |
| **Info** | Blue squiggly | Suggestions and hints |

Diagnostics integrate with the VS Code **Problems** panel (++cmd+shift+m++).

!!! tip "Performance"
    Validation is debounced by 500ms to avoid excessive parsing while typing.

### Code Navigation

#### Go to Definition

Navigate to where a symbol is defined:

- Press ++f12++ with cursor on a symbol
- Or ++cmd++ + click (Mac) / ++ctrl++ + click (Windows/Linux)

Works for:

- Type definitions
- Entity, context, domain references
- Command, event, query references

#### Find All References

Find everywhere a symbol is used:

- Press ++shift+f12++ with cursor on a symbol
- Or right-click and select **Find All References**

---

## Commands

Access commands via the Command Palette (++cmd+shift+p++ / ++ctrl+shift+p++):

### RIDDL: Version Information

Shows RIDDL build information including:

- RIDDL library version
- Build date
- Scala/sbt versions
- Feature list
- Documentation links

### RIDDL: Parse Current File

Parses the active `.riddl` file and displays:

- Full AST structure (JSON format)
- Parse errors with locations

Useful for debugging complex syntax issues.

### RIDDL: Validate Current File

Runs full validation (syntax + semantic) and shows:

- Error count
- Warning count
- Info message count
- Detailed messages with locations

### RIDDL: Translate to Output Format

Placeholder for future translation features. Shows available `riddlc`
commands.

---

## Keyboard Shortcuts

### Extension Commands

| Shortcut | Command |
|----------|---------|
| ++cmd+shift+p++ / ++ctrl+shift+p++ | Open Command Palette (type "RIDDL" to filter) |

### Code Navigation

| Shortcut | Action |
|----------|--------|
| ++f12++ | Go to Definition |
| ++shift+f12++ | Find All References |
| ++cmd++ + click / ++ctrl++ + click | Go to Definition |
| ++ctrl+space++ | Trigger code completion |

### Editor Features

| Shortcut | Action |
|----------|--------|
| ++cmd+slash++ / ++ctrl+slash++ | Toggle line comment (`//`) |
| ++shift+alt+a++ | Toggle block comment (`/* */`) |
| ++cmd+shift+bracket-left++ / ++ctrl+shift+bracket-left++ | Fold region |
| ++cmd+shift+bracket-right++ / ++ctrl+shift+bracket-right++ | Unfold region |

### Built-in RIDDL Editor Features

The extension configures these editor behaviors:

- **Auto-closing brackets**: `{`, `[`, `(`, `"`, and triple backticks
- **Bracket matching**: All bracket types highlighted
- **Code folding**: Fold on braces and `//region` markers
- **Smart indentation**: Automatic indent after opening brackets

---

## Output Panel

Commands write results to the **RIDDL** output channel:

1. Open **View** > **Output** (or ++cmd+shift+u++)
2. Select **RIDDL** from the dropdown

Output includes:

- Command results with formatting
- Numbered error/warning messages
- Clean text (ANSI codes stripped)

---

## File Association

The extension automatically activates for files with the `.riddl` extension:

- **Language ID**: `riddl`
- **File Icon**: Custom RIDDL icon (light and dark variants)
- **Content Type**: Text with RIDDL grammar

---

## Configuration

The extension works out-of-the-box with sensible defaults. No user
configuration is required.

### Editor Settings for RIDDL

You can customize VS Code editor settings specifically for RIDDL files:

```json
{
  "[riddl]": {
    "editor.tabSize": 2,
    "editor.insertSpaces": true,
    "editor.formatOnSave": false,
    "editor.wordWrap": "on"
  }
}
```

### Semantic Highlighting

Semantic highlighting is enabled by default. To disable:

```json
{
  "editor.semanticHighlighting.enabled": false
}
```

---

## Usage Tips

### Efficient Editing

1. **Use snippets**: Type a keyword and press ++tab++ for full structure
2. **Hover for docs**: Check documentation without leaving the editor
3. **Navigate quickly**: ++f12++ to jump to definitions, ++alt+left++ to go back
4. **Check Problems panel**: ++cmd+shift+m++ for all issues at a glance

### Working with Large Models

1. **Use folding**: Collapse sections you're not editing
2. **Split editor**: Work on multiple files side-by-side
3. **Use includes**: Break large models into smaller files

```riddl
// main.riddl
domain MyProject is {
  include "contexts/orders.riddl"
  include "contexts/inventory.riddl"
}
```

### Understanding Errors

Error messages include file location:

```
[orders.riddl:42:15] Error: Undefined reference to type 'CustomerID'
```

This means: `orders.riddl`, line 42, column 15.

Click the error in the Problems panel to jump directly to the location.

### Validation Source Labels

Diagnostics show their source:

- `RIDDL` - Parse/syntax errors
- `RIDDL (validation)` - Semantic validation errors/warnings
- `RIDDL (info)` - Informational messages

---

## Troubleshooting

### Extension Not Activating

- Verify file has `.riddl` extension
- Check **Output** > **Extension Host** for errors
- Try **Developer: Reload Window**

### No Syntax Highlighting

- Check file type in status bar (should show "RIDDL")
- Verify extension is enabled in Extensions panel
- Try disabling other extensions that might conflict

### Slow Performance

- Large files may take longer to parse
- Semantic highlighting has 500ms debounce
- Check for syntax errors that might confuse the parser

### Errors Not Showing

- Check **Problems** panel is visible (++cmd+shift+m++)
- Verify the file has been saved (diagnostics run on save)
- Look for parse errors that might prevent full validation

---

## Authoring RIDDL

For tips on writing effective RIDDL source files, see the
[Authoring RIDDL Sources](../authoring-riddl.md) guide.

---

## Support

- **Bug Reports**: [GitHub Issues](https://github.com/ossuminc/riddl-vscode/issues)
- **Questions**: support@ossuminc.com
- **Contributing**: [GitHub Repository](https://github.com/ossuminc/riddl-vscode)

---

## License

Apache License 2.0

Copyright 2024 Ossum Inc.
