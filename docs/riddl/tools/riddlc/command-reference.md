---
title: "Command Reference"
description: "Complete reference for riddlc commands and options"
---

# Command Reference

`riddlc` uses a subcommand structure. The general syntax is:

```bash
riddlc [common-options] command [command-options]
```

## Available Commands

| Command | Description |
|---------|-------------|
| `about` | Print out information about RIDDL |
| `bastify` | Convert a RIDDL file to BAST (Binary AST) format |
| `dump` | Dump the AST of the input file |
| `flatten` | Flatten all includes into a single file |
| `from` | Load options from a configuration file |
| `help` | Print usage information |
| `info` | Print build information |
| `onchange` | Watch a directory and run a command on changes |
| `parse` | Parse the input file and report syntax errors |
| `prettify` | Reformat RIDDL source to a standard layout |
| `repeat` | Repeatedly run a command for edit-build-check cycles |
| `stats` | Generate statistics about a RIDDL model |
| `unbastify` | Convert a BAST file back to RIDDL source |
| `validate` | Parse and validate the input file |
| `version` | Print the version and exit |

!!! info
    Hugo documentation generation and diagram generation have been moved to
    the [riddl-gen](https://github.com/ossuminc/riddl-gen) repository.

## Common Options

These options apply to all commands:

| Option | Description |
|--------|-------------|
| `-t`, `--show-times` | Show parsing phase execution times |
| `-I`, `--show-include-times` | Show parsing of included files times |
| `-d`, `--dry-run` | Go through the motions but don't write changes |
| `-v`, `--verbose` | Provide verbose output |
| `-D`, `--debug` | Enable debug output (for developers) |
| `-q`, `--quiet` | No output, just execute the command |
| `-a`, `--no-ansi-messages` | Disable ANSI formatting in messages |
| `-w`, `--show-warnings` | Control warning message display |
| `-m`, `--show-missing-warnings` | Control missing definition warnings |
| `-s`, `--show-style-warnings` | Control style warning display |
| `-u`, `--show-usage-warnings` | Control usage warning display |
| `-i`, `--show-info-messages` | Control info message display |
| `-S`, `--sort-messages-by-location` | Sort messages by file and line |
| `-G`, `--group-messages-by-kind` | Group messages by severity |
| `-x`, `--max-parallel-parsing` | Max parallel include file parsing |
| `--max-include-wait` | Max time to wait for include parsing |
| `--warnings-are-fatal` | Treat warnings as errors |
| `-B`, `--auto-generate-bast` | Auto-generate .bast files after parsing |

## Command Details

### parse

Parse a RIDDL file for syntactic correctness without semantic validation:

```bash
riddlc parse input-file.riddl
```

This is useful for quickly checking if a file is syntactically valid.

### validate

Parse and semantically validate a RIDDL file:

```bash
riddlc validate input-file.riddl
```

This performs full validation including:

- Reference resolution (all referenced definitions exist)
- Type checking
- Containment rules
- Style checks (optional)

### prettify

Reformat RIDDL source to a standard layout:

```bash
riddlc prettify input-file.riddl -o output-dir
```

Options:

| Option | Description |
|--------|-------------|
| `-o`, `--output-dir` | Required output directory |
| `--project-name` | Project name for the output |
| `-s`, `--single-file` | Merge all includes into a single file |

### bastify

Convert RIDDL to Binary AST (BAST) format for faster loading:

```bash
riddlc bastify input-file.riddl
```

Creates a `.bast` file next to the input file. BAST files can be loaded
significantly faster than parsing RIDDL source, making them useful for
large models.

### unbastify

Convert a BAST file back to RIDDL source:

```bash
riddlc unbastify input-file.bast -o output-dir
```

Options:

| Option | Description |
|--------|-------------|
| `-o`, `--output-dir` | Output directory (default: next to input) |

### flatten

Resolve all includes into a single file:

```bash
riddlc flatten input-file.riddl -o output-file.riddl
```

### stats

Generate statistics about a RIDDL model:

```bash
riddlc stats -I input-file.riddl
```

Reports counts of domains, contexts, entities, types, and other definitions.

### from

Load options from a HOCON configuration file:

```bash
riddlc from config-file.conf target-command
```

See [Configuration](configuration.md) for details on the configuration format.

### repeat

Support edit-build-check cycles by repeating a command:

```bash
riddlc repeat config-file.conf target-command [refresh-rate] [max-cycles]
```

Options:

| Option | Description |
|--------|-------------|
| `refresh-rate` | How often to check for changes |
| `max-cycles` | Maximum number of cycles |
| `-n`, `--interactive` | Exit on EOF from stdin |

### onchange

Watch a directory and run a command when changes occur:

```bash
riddlc onchange config-file.conf watch-directory target-command
```

### info

Display build information:

```bash
riddlc info
```

Example output:

```
[info] About riddlc:
[info]            name: riddlc
[info]         version: 1.1.2
[info]   documentation: https://riddl.tech
[info]       copyright: © 2019-2026 Ossum Inc.
[info]        licenses: Apache License, Version 2.0
[info]    organization: Ossum Inc.
[info]   scala version: 3.3.7
```

### help

Display usage information:

```bash
riddlc help
riddlc help validate  # Help for specific command
```

### version

Display the version number:

```bash
riddlc version
```
