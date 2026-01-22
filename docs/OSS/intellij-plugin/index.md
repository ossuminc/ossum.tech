# IntelliJ IDEA Plugin for RIDDL

The RIDDL4IDEA plugin provides comprehensive support for the RIDDL language
in IntelliJ IDEA, including syntax highlighting, real-time validation, and
integrated error navigation.

[Release Notes](https://github.com/ossuminc/riddl-idea-plugin/releases/tag/0.9.0-beta)

## Installation

### Beta Program

The plugin is currently in beta. 

To install:

1. Download the latest `.zip` release from the
   [GitHub Release Assets](https://github.com/ossuminc/riddl-idea-plugin/releases/download/0.9.0-beta/RIDDL4IDEA-0.9.0-beta.zip)
   page
2. In IntelliJ IDEA, go to **Settings** > **Plugins**
3. Click the gear icon and select **Install Plugin from Disk...**
4. Select the downloaded `.zip` file
5. Restart IntelliJ IDEA

### Marketplace (Coming Soon)

When version 1.0 is released, the plugin will be available from the JetBrains
Marketplace:

1. Go to **Settings** > **Plugins** > **Marketplace**
2. Search for "RIDDL"
3. Click **Install**

### Requirements

- IntelliJ IDEA 2024.1 or later (Community or Ultimate Edition)
- JDK 21 or later

---

## Features

### Syntax Highlighting

The plugin provides rich syntax highlighting for RIDDL files:

| Element | Color (Dark Theme) |
|---------|-------------------|
| Keywords | Purple (#c77dbb) |
| Punctuation | Teal (#0da19e) |
| Readability words | Yellow (#b3ae60) |
| Identifiers | Default text |
| Comments | Gray |
| Strings | Green |
| Numbers | Blue |

#### Customizing Colors

To customize the RIDDL color scheme:

1. Go to **Settings** > **Editor** > **Color Scheme** > **RIDDL**
2. Adjust colors for each token type
3. Click **Apply**

The plugin includes a dark theme based on Darcula. Light themes use IDE
defaults but are fully customizable.

### Real-Time Validation

As you type, the plugin validates your RIDDL source and displays errors
inline:

- **Syntax errors** appear immediately as you type
- **Semantic errors** (undefined references, type mismatches) show after parsing
- Errors appear as squiggly underlines in the editor
- Click errors in the console to jump to the source location

### RIDDL Tool Window

The plugin adds a **RIDDL** tool window to the left sidebar with:

#### Toolbar Actions

| Action | Icon | Description |
|--------|------|-------------|
| **New Window** | + | Create additional analysis tabs |
| **Compile** | Build | Run RIDDL validation |
| **Settings** | Gear | Open project configuration |

#### Console Output

The console displays:

- Validation results with severity (Error, Warning, Info)
- File locations with line and column numbers
- Clickable links to navigate directly to problems

#### Multiple Tabs

Create multiple tabs to work with different RIDDL configurations:

1. Click the **+** button to create a new tab
2. Configure each tab with different settings
3. Right-click a tab to rename it
4. Close tabs you no longer need (first tab cannot be closed)

---

## Configuration

Access settings via **Settings** > **Tools** > **RIDDL Project Settings**
or click the gear icon in the RIDDL tool window.

### Path Configuration

| Setting | Description |
|---------|-------------|
| **Top-level .riddl file** | Your project's main RIDDL file (entry point for validation) |
| **Configuration file** | Optional `.conf` file for advanced commands |

### Validation Command

Choose which RIDDL command to run:

| Command | Purpose |
|---------|---------|
| **about** | Display RIDDL version information |
| **info** | Show system information |
| **from** | Load configuration from file (requires config file) |

### Validation Options

Fine-tune validation behavior with these options:

#### Message Display

| Option | Description |
|--------|-------------|
| Show warnings | Display warning messages |
| Show missing warnings | Warn about undefined references |
| Show style warnings | Warn about style violations |
| Show usage warnings | Warn about unused definitions |
| Show info messages | Display informational messages |

#### Output Control

| Option | Description |
|--------|-------------|
| Verbose | Enable detailed output |
| Quiet | Suppress normal output |
| Debug | Enable debug information |
| Show times | Display parsing duration |

#### Error Handling

| Option | Description |
|--------|-------------|
| Warnings are fatal | Treat warnings as errors |
| Sort by location | Group messages by file location |

#### Performance

| Option | Range | Description |
|--------|-------|-------------|
| Max parallel parsing | 1 - 2x CPUs | Threads for parallel file parsing |
| Max include wait | < 60000 ms | Timeout for include file processing |

### Auto-Parse on Save

When enabled (default), the plugin automatically re-validates your RIDDL
files whenever you save. Disable this for large projects where validation
takes significant time.

---

## Tool Window Actions

The RIDDL tool window provides these actions:

### Compile/Validate

Click the **Build** icon or use the keyboard:

- Parses your top-level RIDDL file
- Validates all included files
- Displays results in the console
- Updates editor annotations

### Navigate to Error

Click any error message in the console to:

1. Open the containing file (if not already open)
2. Jump to the exact line and column
3. Position cursor at the error location

### Clear Output

Right-click in the console and select **Clear** to reset the output.

---

## File Types

The plugin recognizes files with the `.riddl` extension:

- Automatic syntax highlighting when opened
- Icon displayed in project tree
- Full validation support

---

## Usage Tips

### Setting Up a New Project

1. Create your main `.riddl` file (e.g., `myproject.riddl`)
2. Open **RIDDL Project Settings**
3. Set the **Top-level .riddl file** to your main file
4. Enable desired validation options
5. Click **Compile** to validate

### Working with Include Files

The plugin follows all `include` directives from your top-level file:

```riddl
// myproject.riddl
domain MyProject is {
  include "contexts/orders.riddl"
  include "types/common.riddl"
}
```

All included files are validated together, ensuring cross-file references
resolve correctly.

### Understanding Validation Messages

Messages include severity and location:

```
Error: [orders.riddl:42:15] Undefined reference to type 'CustomerID'
Warning: [types.riddl:10:1] Missing brief description for type 'Address'
```

Click the message to navigate to `orders.riddl`, line 42, column 15.

### Performance Tips

For large projects:

- Disable **Auto-parse on save** and validate manually
- Increase **Max parallel parsing** on multi-core systems
- Use separate tool window tabs for different subsystems

---

## Keyboard Shortcuts

The plugin does not register global keyboard shortcuts. All actions are
accessible through:

- The RIDDL tool window toolbar
- Right-click context menus
- Settings dialogs

Standard IntelliJ shortcuts work in RIDDL files:

| Shortcut | Action |
|----------|--------|
| ++ctrl+s++ (++cmd+s++ on Mac) | Save (triggers auto-validation if enabled) |
| ++ctrl+shift+f++ | Reformat code |
| ++ctrl+slash++ | Toggle line comment |
| ++ctrl+shift+slash++ | Toggle block comment |

---

## Troubleshooting

### Plugin Not Loading

- Verify IntelliJ IDEA version is 2024.1 or later
- Check **Settings** > **Plugins** > **Installed** for RIDDL4IDEA
- Try disabling and re-enabling the plugin

### No Syntax Highlighting

- Verify file has `.riddl` extension
- Check **Settings** > **Editor** > **File Types** for RIDDL registration
- Restart IntelliJ IDEA

### Validation Not Running

- Ensure **Top-level .riddl file** is configured in settings
- Check the file path is correct and file exists
- Look for error messages in the RIDDL console

### Slow Validation

- Reduce **Max parallel parsing** if memory is limited
- Disable **Show style warnings** and **Show usage warnings** for faster runs
- Consider splitting large models into smaller include files

---

## Authoring RIDDL

For tips on writing effective RIDDL source files, see the
[Authoring RIDDL Sources](../authoring-riddl.md) guide.

---

## Support

- **Bug Reports**: [GitHub Issues](https://github.com/ossuminc/riddl-idea-plugin/issues)
- **Questions**: support@ossuminc.com
- **Contributing**: [GitHub Repository](https://github.com/ossuminc/riddl-idea-plugin)

---

## License

Apache License 2.0

Copyright 2024 Ossum Inc.
