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
| `advise` | Report remediation advice for a model |
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
| `-c`, `--show-completeness-warnings` | Control completeness warning display |
| `--warnings-are-fatal` | Treat warnings as errors |
| `-B`, `--auto-generate-bast` | Auto-generate .bast files after parsing |
| `--provide-tips` | Include a remediation suggestion with each message that has one, for AI-assisted fixing |
| `--check-figma-drift` | Check `figma` references against the Figma REST API |

### Completeness Warnings

`--show-completeness-warnings` (default: on) controls severity-4 messages —
models that parse and validate but lack detail needed for a complete,
implementable specification.

When it is on, `validate` additionally runs the message-flow, entity-lifecycle
and use-case analyses, so epic and use-case completeness warnings surface here
rather than only through the analysis API. When it is off, those passes are
skipped entirely and cost nothing.

### Figma Drift Checking

`--check-figma-drift` is **off by default** and verifies that each
`figma "<file>" node "<id>"` reference in the model still resolves:

```bash
export FIGMA_TOKEN=figd_...
riddlc --check-figma-drift validate model.riddl
```

A node the API does not know about is an **Error**; a frame whose name no
longer corresponds to the annotated definition's name is a **Warning**.

An offline or token-less build cannot be affected. No token means no client at
all, and every failure to reach or understand the API produces nothing —
**only a successful API answer can produce a message**. With the flag on but
no client available, one informational message says so, and that is the whole
consequence.

The HOCON equivalent for a `from` configuration file is `check-figma-drift`.

### Deprecation Messages

RIDDL 2.0 gives deprecations their own `[deprecated]` label rather than
rendering them as ordinary warnings, so a model can be checked for zero
deprecations independently of zero warnings:

```bash
riddlc validate model.riddl 2>&1 | grep '\[deprecated\]'
```

They also surface under **every** command that parses — `parse`, `stats`,
`bastify`, `prettify` and the generation commands — not only `validate`. In
1.x a successful parse that accumulated any message discarded the result, so
parse-time warnings never reached the user at all.

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

Collapse a multi-file model into a single file:

```bash
riddlc flatten input-file.riddl -o output-file.riddl
```

This removes every `include` and `import` node, promoting its children into
the enclosing container. In RIDDL 2.0 it covers **both**: `import` nodes from
`.bast` modules are flattened alongside `include` nodes from source files.

!!! warning "Flattening is lossy, and is not a prerequisite for anything"
    An `include` or `import` is a **node** in the model whose children are the
    definitions it brought in. Passes traverse through it, so those definitions
    already resolve, validate and generate exactly as if written in place. You
    do **not** need to flatten to make a multi-file model work.

    What flattening removes is the **origin**: after it, nothing records which
    file or module a definition came from. That costs you the file attribution
    in diagnostics and the ability to tell your own model apart from what it
    imported.

    Use it only when a single self-contained file is the actual goal — handing
    one file to a tool that cannot follow includes, for instance — and keep the
    unflattened model as the source of truth.

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
[info]         version: 2.0.0-rc.1
[info]      git commit: ebce6ba945739bef06907445e5a570b2d030591b
[info]   documentation: https://ossum.tech/riddl
[info]       copyright: © 2019-2026 Ossum Inc.
[info]        licenses: Apache License, Version 2.0
[info]    organization: Ossum Inc.
[info]   scala version: 3.9.0
```

`git commit` is new in RIDDL 2.0: the full source SHA the binary was built
from. It lets a model repository locate the exact compiler changes a given
`riddlc` embodies — useful when a validation message appears that an older
build did not produce. Outside a git checkout it reads `unknown`.

### advise

Report remediation advice for a model. Pairs with `--provide-tips`, which
attaches a suggested fix to each message that has one — intended for
AI-assisted correction.

```bash
riddlc advise model.riddl
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
