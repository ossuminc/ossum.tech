---
title: "Configuration"
description: "Configuring riddlc with HOCON files"
---

# Configuration

You can store riddlc options in a configuration file and use them with the
`from` command. Configuration files use [HOCON](https://github.com/lightbend/config/blob/main/HOCON.md)
format.

## Basic Usage

```bash
riddlc from path/to/config.conf validate
```

This loads the configuration file and runs the `validate` command with the
options specified in the file.

## Configuration File Format

A typical configuration file has three sections:

1. **command** - The default command to run
2. **common** - Options that apply to all commands
3. **command-specific** - Options for each command

### Example Configuration

```hocon
# Default command when not specified on command line
command = validate

# Options common to all commands
common = {
  show-times = true
  verbose = true
  quiet = false
  dry-run = false
  hide-warnings = false
  hide-missing-warnings = true
  hide-style-warnings = true
  debug = false
  show-unused-warnings = false
}

# Options for the validate command
validate {
  input-file = "src/main/riddl/MyModel.riddl"
}

# Options for the stats command
stats {
  input-file = "src/main/riddl/MyModel.riddl"
}
```

## Common Options

These options can be set in the `common` section:

| Option | Type | Description |
|--------|------|-------------|
| `show-times` | boolean | Print phase execution durations |
| `verbose` | boolean | Print detailed information |
| `quiet` | boolean | Suppress all output |
| `dry-run` | boolean | Process options without executing |
| `hide-warnings` | boolean | Hide all warning messages |
| `hide-missing-warnings` | boolean | Hide warnings about missing definitions |
| `hide-style-warnings` | boolean | Hide style warnings |
| `debug` | boolean | Print debug information |
| `show-unused-warnings` | boolean | Warn about unused definitions |

## Command-Specific Options

### validate

```hocon
validate {
  input-file = "path/to/input.riddl"
}
```

### stats

```hocon
stats {
  input-file = "path/to/input.riddl"
}
```

### prettify

```hocon
prettify {
  input-file = "path/to/input.riddl"
  output-dir = "path/to/output/"
  project-name = "MyProject"
  single-file = false
}
```

## Multiple Configurations

You can have multiple command configurations in one file:

```hocon
command = validate

common {
  verbose = true
}

validate {
  input-file = "src/main/riddl/MyModel.riddl"
}

stats {
  input-file = "src/main/riddl/MyModel.riddl"
}

prettify {
  input-file = "src/main/riddl/MyModel.riddl"
  output-dir = "target/prettified/"
}
```

Then run different commands:

```bash
# Run validate (the default)
riddlc from config.conf

# Run stats
riddlc from config.conf stats

# Run prettify
riddlc from config.conf prettify
```

## Environment Variable Substitution

HOCON supports environment variable substitution:

```hocon
validate {
  input-file = ${RIDDL_MODEL_PATH}
}
```

## Includes

You can split configuration across multiple files:

```hocon
include "common.conf"

validate {
  input-file = "MyModel.riddl"
}
```

## Best Practices

1. **Keep one config per project** - Store `riddl.conf` in your project root
2. **Use common section** - Avoid repeating options across commands
3. **Version control** - Commit your config file for reproducible builds
4. **CI/CD alignment** - Use the same config locally and in CI

## Next Steps

- [GitHub Actions](github-actions.md) - Use config files in CI/CD
- [Command Reference](command-reference.md) - Full list of available options
