---
title: "Compilation Process"
description: "How riddlc compiles RIDDL specifications"
---

# Compilation Process

The `riddlc` compiler processes RIDDL specifications through several phases.
Understanding these phases helps you interpret error messages and optimize
your workflow.

## Compilation Phases

```
┌─────────────────┐
│  RIDDL Source   │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Lexical Analysis│  Parse syntax, build AST
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│   Structural    │  Build symbol table, hierarchy
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│     Style       │  Check stylistic conventions
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│    Semantic     │  Validate references, types
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│   Valid AST     │
└─────────────────┘
```

## Lexical Analysis

The first phase parses the raw textual input to verify syntactic correctness.
RIDDL uses [fastparse](https://www.lihaoyi.com/fastparse/) for high-performance
parsing.

**What happens:**
- Tokenize input text
- Match against RIDDL grammar rules
- Construct Abstract Syntax Tree (AST)

**Errors at this phase:**
- Invalid syntax
- Unrecognized keywords
- Malformed strings or identifiers

**Example error:**
```
[error] mymodel.riddl:15:10: Expected '}' but found 'entity'
```

## Structural Analysis

Once parsing succeeds, the compiler builds internal data structures from the
AST.

**What happens:**
- Create symbol table of all definitions
- Map containment hierarchy (what's inside what)
- Track definition locations for error reporting

**Errors at this phase:**
- Duplicate definitions in same scope
- Invalid nesting (e.g., entity outside context)

## Style Analysis

This optional phase checks for deviations from recommended RIDDL conventions.

**What's checked:**
- Naming conventions (PascalCase for types, etc.)
- Documentation presence
- Structural organization

**Controlling style warnings:**
```bash
# Show all style warnings
riddlc validate --show-style-warnings true mymodel.riddl

# Hide style warnings
riddlc validate --show-style-warnings false mymodel.riddl
```

## Semantic Analysis

The most comprehensive validation phase checks logical correctness.

**What's validated:**

| Check | Description |
|-------|-------------|
| Reference resolution | All referenced definitions exist |
| Type compatibility | Type expressions are valid |
| Containment rules | Definitions are in valid containers |
| Usage consistency | Definitions are used correctly |
| Completeness | Required elements are present |

**Example errors:**

*Undefined reference:*
```
[error] mymodel.riddl:25:15: Reference to undefined type 'CustomerInfo'
```

*Invalid containment:*
```
[error] mymodel.riddl:10:5: Entity cannot be defined directly in Domain;
        must be inside a Context
```

*Missing required element:*
```
[warning] mymodel.riddl:30:5: Entity 'Order' has no state defined
```

## Understanding Messages

Messages are categorized by severity:

| Severity | Meaning | Action |
|----------|---------|--------|
| **Error** | Invalid specification | Must fix before proceeding |
| **Warning** | Questionable but valid | Review and fix if appropriate |
| **Info** | Informational notice | No action required |

### Message Sorting

Control how messages are displayed:

```bash
# Sort by file location
riddlc validate --sort-messages-by-location true mymodel.riddl

# Group by severity
riddlc validate --group-messages-by-kind true mymodel.riddl
```

## Performance Tips

### Use BAST for Large Models

For large models, generate BAST files for faster subsequent loading:

```bash
# Generate BAST file
riddlc bastify mymodel.riddl

# Subsequent validations load faster
riddlc validate mymodel.bast
```

### Parallel Include Parsing

Control parallel processing of includes:

```bash
# Increase parallelism for many include files
riddlc validate --max-parallel-parsing 8 mymodel.riddl
```

### Show Timing Information

Identify slow phases:

```bash
riddlc validate --show-times mymodel.riddl
```

## Common Validation Scenarios

### Full Validation

Standard validation with all warnings:

```bash
riddlc validate mymodel.riddl
```

### CI/CD Validation

Strict mode for continuous integration:

```bash
riddlc validate --warnings-are-fatal true mymodel.riddl
```

### Development Validation

Faster feedback during development:

```bash
riddlc validate \
  --show-missing-warnings false \
  --show-style-warnings false \
  mymodel.riddl
```

## Next Steps

- [Command Reference](command-reference.md) - Full command documentation
- [Configuration](configuration.md) - Store options in config files
