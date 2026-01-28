# Developers Guide

This guide is for developers who want to contribute to RIDDL itself—the
compiler, tools, and ecosystem. If you're looking to use RIDDL to specify
systems, see the [Author's Guide](../authors/index.md) or
[Implementor's Guide](../implementors/index.md).

## Prerequisites

To work on RIDDL development, you'll need:

- **JDK 25 or later** (Temurin recommended)
- **Scala 3.3.x LTS** (managed by sbt)
- **sbt 1.10+** (Scala Build Tool)
- **Git** for version control

## Getting Started

### Clone the Repository

```bash
git clone https://github.com/ossuminc/riddl.git
cd riddl
```

### Build the Project

```bash
# Compile all modules
sbt compile

# Run tests
sbt test

# Build riddlc executable
sbt riddlc/stage
```

The staged executable will be at `riddlc/target/universal/stage/bin/riddlc`.

## Project Structure

RIDDL is organized as a multi-module sbt project:

```
riddl/
├── language/          # Core language model and AST
├── passes/            # Compiler passes (parsing, validation, etc.)
├── commands/          # riddlc command implementations
├── riddlc/            # Command-line interface
├── hugo/              # Hugo documentation generator
├── testkit/           # Testing utilities
└── project/           # sbt build configuration
```

### Key Modules

**language** - The foundation of RIDDL:

- AST definitions in `com.ossuminc.riddl.language.AST`
- Parser combinators using fastparse
- Source location tracking

**passes** - Compiler transformation passes:

- Parsing pass (text → AST)
- Resolution pass (resolve references)
- Validation pass (semantic checks)
- Symbol table construction

**commands** - The riddlc CLI:

- Command parsing and dispatch
- Option handling
- Output formatting

**hugo** - Documentation generator (being migrated to [Synapify](../../../../synapify/index.md)):

- Converts RIDDL models to Hugo-compatible markdown
- Generates diagrams (Mermaid)
- Produces glossaries and indexes

## Development Workflow

### Running Tests

```bash
# Run all tests
sbt test

# Run tests for a specific module
sbt "language/test"
sbt "passes/test"

# Run a specific test class
sbt "testOnly com.ossuminc.riddl.language.ParserSpec"

# Run tests continuously on file changes
sbt ~test
```

### Code Coverage

```bash
sbt coverage test coverageReport
```

Coverage reports are generated in `target/scala-3.x/scoverage-report/`.

### Code Formatting

RIDDL uses scalafmt for consistent formatting:

```bash
# Format all code
sbt scalafmt test:scalafmt

# Check formatting without changes
sbt scalafmtCheck test:scalafmtCheck
```

## Architecture Overview

### Compiler Pipeline

RIDDL compilation follows a multi-pass architecture:

```
Source Text
    │
    ▼
┌─────────┐
│ Parsing │  → AST (Abstract Syntax Tree)
└────┬────┘
     ▼
┌────────────┐
│ Resolution │  → Resolved references
└─────┬──────┘
      ▼
┌────────────┐
│ Validation │  → Errors/Warnings
└─────┬──────┘
      ▼
┌────────────┐
│ Translation│  → Output (Hugo, etc.)
└────────────┘
```

### AST Design

The AST is defined in `language/src/main/scala/com/ossuminc/riddl/language/AST.scala`.
Key design principles:

- **Immutable** - All AST nodes are immutable case classes
- **Hierarchical** - Nodes form a tree with `Definition` as the base
- **Location-tracked** - Every node carries source location information

### Parser Design

RIDDL uses fastparse for its parser, defined in
`language/src/main/scala/com/ossuminc/riddl/language/parsing/`.

The parser is organized by language construct:

- `CommonParser.scala` - Shared parsing utilities
- `TypeParser.scala` - Type expression parsing
- `StatementParser.scala` - Statement parsing
- `DefinitionParser.scala` - Definition parsing

## Adding New Features

### Adding a New Statement Type

1. **Define the AST node** in `AST.scala`:
   ```scala
   case class MyStatement(
     loc: At,
     // ... fields
   ) extends Statement
   ```

2. **Add parser rule** in `StatementParser.scala`:
   ```scala
   def myStatement[u: P]: P[MyStatement] = ...
   ```

3. **Add validation** in the validation pass

4. **Add translation** in output generators (Hugo, etc.)

5. **Write tests** covering parsing, validation, and output

### Adding a New Pass

1. Create a new pass class extending `Pass`:
   ```scala
   class MyPass extends Pass {
     def name: String = "MyPass"
     def process(root: Root): PassOutput = ...
   }
   ```

2. Register the pass in the compiler pipeline

3. Write tests for the pass behavior

## Testing Guidelines

### Test Organization

- **Unit tests** - Test individual components in isolation
- **Integration tests** - Test component interactions
- **Example tests** - Test full RIDDL specifications

### Writing Parser Tests

```scala
class MyParserSpec extends ParsingTestBase {
  "MyParser" should {
    "parse valid input" in {
      val input = """my construct { ... }"""
      parseDefinition(input) shouldBe a[MyConstruct]
    }

    "report errors for invalid input" in {
      val input = """invalid syntax"""
      parseDefinition(input) shouldBe a[ParsingError]
    }
  }
}
```

### Writing Validation Tests

```scala
class MyValidationSpec extends ValidatingTestBase {
  "MyValidation" should {
    "detect invalid references" in {
      val input = """domain D { context C { entity E { ??? } } }"""
      val messages = validate(input)
      messages should contain(a[MissingError])
    }
  }
}
```

## Contributing

### Contribution Process

1. **Fork** the repository
2. **Create a branch** for your feature: `git checkout -b feature/my-feature`
3. **Make changes** with tests and documentation
4. **Ensure tests pass**: `sbt test`
5. **Format code**: `sbt scalafmt`
6. **Submit a pull request** to the `development` branch

### Code Review

Pull requests are reviewed for:

- Correctness and test coverage
- Code style consistency
- Documentation completeness
- Performance considerations

### Commit Messages

Follow conventional commit style:

```
feat: add new statement type for async operations

Add AsyncStatement to support asynchronous message handling.
Includes parser, validation, and Hugo output support.

Co-Authored-By: Your Name <email>
```

## Debugging Tips

### Parser Debugging

Enable parse tracing for detailed output:

```scala
implicit val ctx = ParsingContext(tracing = true)
```

### AST Inspection

Use the `dump` command to see parsed AST:

```bash
riddlc dump mymodel.riddl
```

### Logging

RIDDL uses SLF4J logging. Configure log levels in `logback.xml`:

```xml
<logger name="com.ossuminc.riddl" level="DEBUG"/>
```

## Resources

- [GitHub Repository](https://github.com/ossuminc/riddl)
- [EBNF Grammar](../../references/ebnf-grammar.md)
- [Language Reference](../../references/language-reference.md)
- [Scala 3 Documentation](https://docs.scala-lang.org/scala3/)
- [fastparse Documentation](https://com-lihaoyi.github.io/fastparse/)
