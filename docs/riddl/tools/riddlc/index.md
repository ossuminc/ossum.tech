---
title: "riddlc - The RIDDL Compiler"
description: "Command-line compiler for parsing and validating RIDDL specifications"
---

# riddlc - The RIDDL Compiler

`riddlc` is the command-line compiler for RIDDL. It parses, validates, and
transforms RIDDL specifications.

## Quick Start

```bash
# Validate a RIDDL file
riddlc validate mymodel.riddl

# Show help
riddlc help

# Show version
riddlc version
```

## Key Features

- **Syntax validation** - Verify RIDDL files are syntactically correct
- **Semantic validation** - Check references, types, and containment rules
- **BAST serialization** - Convert to binary format for faster loading
- **Style checking** - Optional warnings for convention violations
- **Reformatting** - Standardize RIDDL source layout

!!! info "Documentation Generation"
    Hugo documentation generation and diagram generation have been moved to
    the [riddl-gen](https://github.com/ossuminc/riddl-gen) repository.
    Use [Synapify](../../../synapify/index.md) for integrated documentation
    generation with AI assistance.

## Documentation

| Section | Description |
|---------|-------------|
| [Installation](installation.md) | Download or build from source |
| [Command Reference](command-reference.md) | Full command and option documentation |
| [Configuration](configuration.md) | Using HOCON configuration files |
| [Compilation](compilation.md) | Understanding the compilation process |
| [GitHub Actions](github-actions.md) | CI/CD integration |

## Example Usage

### Basic Validation

```bash
riddlc validate mymodel.riddl
```

### Verbose Output with Timing

```bash
riddlc validate --verbose --show-times mymodel.riddl
```

### Using Configuration File

```bash
riddlc from riddl.conf validate
```

### Generate BAST for Faster Loading

```bash
riddlc bastify mymodel.riddl
```

## Common Workflows

### Development Cycle

1. Edit RIDDL source files
2. Run `riddlc validate` to check for errors
3. Fix any issues reported
4. Repeat

### CI/CD Pipeline

```yaml
- name: Validate RIDDL
  run: riddlc validate --warnings-are-fatal src/main/riddl/model.riddl
```

### Using with sbt

See [sbt-riddl](../sbt-riddl/index.md) for sbt integration.

## Getting Help

```bash
# General help
riddlc help

# Help for specific command
riddlc help validate
```

## Build Information

Check your installed version:

```bash
riddlc info
```

Output:

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

## Resources

- [RIDDL Repository](https://github.com/ossuminc/riddl)
- [Language Reference](../../references/language-reference.md)
- [EBNF Grammar](../../references/ebnf-grammar.md)
