# RIDDLC - The RIDDL Compiler

`riddlc` is the command-line compiler for RIDDL. It parses, validates, and
transforms RIDDL specifications into various outputs.

## Installation

### Using Homebrew (macOS/Linux)

```bash
# Coming soon
brew install riddlc
```

### Building from Source

```bash
# Clone the repository
git clone https://github.com/ossuminc/riddl.git
cd riddl

# Build the compiler
sbt compile
sbt riddlc/stage

# Add to PATH (adjust for your shell)
export PATH="$PATH:$(pwd)/target/universal/stage/bin"
```

### Using SBT Plugin

Add to your `project/plugins.sbt`:

```scala
addSbtPlugin("com.ossuminc" % "sbt-riddl" % "latest.version")
```

See the [Implementor's Guide](../../guides/implementors/ways-to-use-riddl.md)
for detailed SBT integration instructions.

## Basic Usage

```bash
# Show help
riddlc help

# Show version
riddlc version

# Validate a RIDDL file
riddlc validate mymodel.riddl
```

Documentation generation will be available through [Synapify](../../../synapify/index.md).

## Commands

### validate

Parses and validates a RIDDL specification without producing output.

```bash
riddlc validate mymodel.riddl
```

Options:
- `-v, --verbose`: Show detailed validation messages
- `-w, --warnings`: Treat warnings as errors

### info

Displays build information about riddlc.

```bash
riddlc info
```

### version

Displays the riddlc version number.

```bash
riddlc version
```

## Configuration

### riddlc.conf

You can create a `riddlc.conf` file to set default options:

```hocon
common {
  verbose = false
  show-warnings = true
  show-missing-warnings = false
  show-style-warnings = false
}
```

### Environment Variables

- `RIDDL_HOME`: Directory containing riddlc configuration
- `RIDDL_OPTIONS`: Default command-line options

## Common Workflows

### Validate During Development

Run validation frequently while authoring:

```bash
# Validate and show all messages
riddlc validate -v mymodel.riddl
```

### CI/CD Integration

Add validation to your CI pipeline:

```yaml
# GitHub Actions example
- name: Validate RIDDL Model
  run: riddlc validate --warnings src/main/riddl/model.riddl
```

## Error Messages

### Common Errors

| Error | Cause | Solution |
|-------|-------|----------|
| "Undefined reference" | Reference to undefined definition | Define the referenced item |
| "Duplicate definition" | Same name used twice in scope | Rename one definition |
| "Invalid containment" | Definition in wrong container | Check hierarchy rules |
| "Syntax error" | Invalid RIDDL syntax | Check syntax near line number |

### Verbose Output

Use `-v` to get detailed diagnostic information:

```bash
riddlc validate -v mymodel.riddl
```

## Resources

- [RIDDL Repository](https://github.com/ossuminc/riddl)
- [Language Reference](../../references/language-reference.md)
- [EBNF Grammar](../../references/ebnf-grammar.md)
