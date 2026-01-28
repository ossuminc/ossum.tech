# Engineering Notebook: ossum.tech

## Current Status

Documentation site is complete and deployed. All major sections documented:

- **RIDDL**: Language reference, concepts, guides, tools
- **OSS**: IDE extensions (IntelliJ, VS Code) with authoring guide
- **MCP**: Installation guides for 6 AI tools
- **Synapify**: Overview documentation (product in development)

All changes pushed to origin/main.

## Work Completed (Recent)

### 2026-01-28: Documentation Editorial Review (Continued)

Comprehensive editorial review of all documentation sections:

- [x] **Concepts Section** (all files reviewed and fixed)
  - adaptor.md: Added missing "from", fixed link spacing
  - application.md: Complete rewrite - clarified applications are contexts with groups
  - case.md: Fixed "too"→"to" typo
  - connector.md: Removed unimplemented Subscriptions section
  - constant.md: Simplified to reference vital.md
  - definition.md: Removed outdated Hugo reference
  - description.md: Removed Hugo formatter reference
  - element.md: Fixed "Occurs In" and self-reference issues
  - entity.md: Fixed actor→user model, Eric Brewer, event-sourced hyphenation
  - epic.md: Fixed "an user"→"a user" (3 instances)
  - function.md: Fixed wrong handler link
  - group.md: Fixed broken Hugo icon shortcode
  - handler.md: Fixed Projection→Projector
  - interaction.md: Fixed "an Use Case"→"a Use Case"
  - message.md: Removed duplicate application line, fixed principal→principle,
    Projections→Projectors
  - onclause.md: Fixed receipient→recipient, whenthe→when the
  - option.md: Fixed link spacing, added missing period
  - output.md: Fixed "an user"→"a user"
  - processor.md: Complete rewrite explaining abstract concept and concrete types
  - projector.md: Fixed projections→projectors
  - repository.md: Fixed wrong anchor links (#query→#command, #result→#event)
  - sagastep.md: Fixed examples→clauses
  - type.md: Fixed Hugo TOC shortcode, RIDDL syntax (any of/one of)
  - user.md: Changed Actor→User per Use Cases 2.0 terminology
  - vital.md: Fixed truncation, removed Applications, added Streamlets

- [x] **Guides Section** (all files reviewed and fixed)
  - authors/index.md: Fixed event-sourced hyphenation, updated doc generation
    to reference Synapify
  - developers/index.md: Updated JDK 21→25, Scala 3.6.x→3.3.x LTS, noted hugo
    migration to Synapify, fixed sbt stage→sbt riddlc/stage
  - domain-experts/duties.md: Fixed "context or"→"context of"
  - domain-experts/index.md: Replaced Hugo toc-tree shortcode
  - domain-experts/relating-to-riddl.md: Fixed Riddl→RIDDL in title
  - implementors/index.md: Replaced Hugo toc-tree shortcode
  - implementors/ways-to-use-riddl.md: Fixed sbt stage commands, updated HOCON
    example for validate-only, removed hugo references, added Synapify links

- [x] **Tools Section** (all files reviewed and fixed)
  - index.md: Updated riddlc description to validation-only, added Synapify link
  - riddlc/index.md: Fixed sbt stage, removed hugo command sections, updated
    HOCON config to use common section, added Synapify links
  - riddl-idea-plugin/index.md: Updated JDK 21→25
  - riddl-mcp-server/index.md: Clean, no issues

- [x] **OSS Section** (all files reviewed and fixed)
  - authoring-riddl.md: Fixed "one of"→"any of" for enumerations (2 instances)
  - intellij-plugin/index.md: Updated JDK 21→25
  - vscode-extension/index.md: Clean, no issues
  - index.md: Clean, no issues

- [x] **MCP Section** (all files reviewed)
  - All files clean, no issues found

- [x] **References Section** (reviewed)
  - index.md: Clean, no issues

### 2026-01-27: Documentation Editorial Review

Grammar, style, spelling, and accuracy review of documentation:

- [x] **Introduction Section** (9 files, committed)
  - Fixed duplicate navigation list in index.md
  - Standardized RIDDL capitalization throughout
  - Updated what-can-riddl-do.md to reflect riddlc as validator only
  - Fixed invalid RIDDL syntax in code examples (why-is-riddl-needed.md)
  - Removed outdated technology references (Kalix, Kubernetes, etc.)
  - Fixed typos: Branchs→Branches, Kuberenetes→Kubernetes, Roland Kunh→Kuhn
  - Fixed broken anchor syntax and URLs
  - Fixed missing words and broken markdown links

- [x] **CLAUDE.md Updates**
  - Added Editorial Guidelines section with session learnings
  - Documented tooling separation (riddlc vs Synapify)
  - Added guidance on outdated technology references
  - Added Hugo remnant removal guidance
  - Documented RIDDL syntax validation rules for examples

### 2026-01-26: Synapify User Guide Expansion

Comprehensive expansion of Synapify documentation based on product discussion:

- [x] **Favicon Update**
  - Downloaded favicon from www.ossuminc.com (32x32, 192x192, 180x180 sizes)
  - Created template override (`overrides/main.html`) with proper link tags
  - Updated mkdocs.yml to use new favicon

- [x] **Synapify Index Rewrite** (`docs/synapify/index.md`)
  - "The Solution Architect's Toolbench" tagline
  - Sections targeting all four user types (Domain Experts, Authors,
    Implementors, Developers)
  - Core capabilities overview (visual editor, text editor, project
    management, validation)
  - Integrated services (simulation, generation, AI) with Coming Soon markers
  - Subscription tiers outline (Individual, Team, Enterprise)

- [x] **User Interface Guide** (`docs/synapify/user-interface.md`)
  - Accurate four-panel layout documentation:
    - Left: Model Tree (AST hierarchy navigation, hideable)
    - Center top: Visual Editor (primary, always visible)
    - Center bottom: Text Editor (Monaco, hideable)
    - Right: Metadata & Info (with clause editing, statistics, hideable)
  - Panel visibility controls and suggested layouts
  - Keyboard shortcuts reference

- [x] **Simulation Guide** (`docs/synapify/simulation.md`)
  - How riddlsim integration works (HTTP requests, streaming results)
  - Scenario structure and examples
  - Running single scenarios and suites
  - Understanding results and common issues
  - Integration with development workflow

- [x] **Code Generation Guide** (`docs/synapify/generation.md`)
  - How riddl-gen integration works
  - Documentation targets (AsciiDoc, Hugo)
  - Code targets (Akka/Scala, Quarkus/Java planned)
  - Structure mapping from RIDDL to generated artifacts
  - Iterative development workflow
  - Deep dive examples

### 2026-01-21: Synapify Documentation

- [x] **Synapify Overview** (`docs/synapify/index.md`)
  - Visual and textual editing modes
  - Automatic diagram generation (context maps, entity diagrams, etc.)
  - AI integration via MCP Server
  - Model simulation capabilities
  - Code generation (coming soon)
  - Getting started guide and requirements

### 2026-01-21: Open Source Release Documentation

Created comprehensive documentation for open source product releases:

- [x] **Authoring RIDDL Sources** (`docs/OSS/authoring-riddl.md`)
  - File organization and includes
  - Metadata with `with` clause (authors, terms, descriptions)
  - Type definitions and predefined types
  - Message types (commands, events, queries, results)
  - Entity design patterns
  - Handler statements reference
  - Common patterns (aggregates, sagas)

- [x] **IntelliJ Plugin Documentation** (`docs/OSS/intellij-plugin/index.md`)
  - Complete feature documentation
  - Installation instructions (beta and marketplace)
  - Configuration options reference
  - Tool window usage guide
  - Troubleshooting section

- [x] **VS Code Extension Documentation** (`docs/OSS/vscode-extension/index.md`)
  - All features documented (completion, diagnostics, navigation)
  - Keyboard shortcuts reference
  - Command palette commands
  - Configuration options
  - Troubleshooting section

- [x] **MCP Section** (`docs/MCP/`)
  - Main overview page with capabilities
  - Claude Desktop configuration guide
  - Claude Code configuration guide
  - Gemini CLI configuration guide
  - VS Code Copilot configuration guide
  - IntelliJ AI Assistant configuration guide
  - IntelliJ Junie configuration guide
  - Server URL placeholder (`{{MCP_SERVER_URL}}`)
  - Authentication documentation

- [x] **OSS Index Update** (`docs/OSS/index.md`)
  - Links to all IDE extensions
  - Links to authoring guide
  - Links to MCP section
  - Getting started workflow

### 2026-01-21: Documentation Improvement Plan Execution

Completed all 6 phases of the comprehensive documentation improvement:

- [x] **Phase 1**: Fix critical documentation accuracy issues
- [x] **Phase 2**: Add missing processor documentation
- [x] **Phase 3**: Complete introduction section
- [x] **Phase 4**: Complete tools documentation
- [x] **Phase 5**: Complete guides
- [x] **Phase 6**: Fix concepts section issues

### 2026-01-20: Initial Setup

- [x] Created CLAUDE.md for this repository
- [x] Created NOTEBOOK.md to track pending work
- [x] Audited all documentation for WIP markers
- [x] Completed Author's Guide
- [x] Improved hierarchy diagram in concepts

## In Progress

Editorial review complete. All sections reviewed and fixed. Ready to commit.

## Pending Tasks

### Before Production

| Task | Notes |
|------|-------|
| Replace `{{MCP_SERVER_URL}}` | When public URL is available |
| Update release download links | When final releases are published |

### Lower Priority

| Task | File | Notes |
|------|------|-------|
| RIDDL Pygments lexer | New file | Custom syntax highlighting for code blocks |
| Type examples | `references/language-reference.md` | Add specialized examples |
| Future work review | `future-work/` | Update for current roadmap |
| Quick-start tutorial | New file | Optional getting started guide |
| EBNF grammar validation | `references/ebnf-grammar.md` | See details below |

#### Synapify Generation Configuration Documentation

When documenting Synapify's documentation/code generation features, use this
HOCON configuration example as a starting point (preserved from riddlc hugo):

```hocon
hugo {
    input-file = "ReactiveBBQ.riddl"
    output-dir = "target/hugo/ReactiveBBQ"
    project-name = "Reactive BBQ"
    site-title = "Reactive BBQ Generated Specification"
    site-description = "Generated specification for the Reactive BBQ application"
    site-logo-path = "images/RBBQ.png"
    erase-output = true
    base-url = "https://bbq.riddl.tech"
    source-url = "https://github.com/ossuminc/riddl"
    edit-path = "/-/blob/main/src/riddl/ReactiveBBQ"
}
```

#### RIDDL Pygments Lexer Task

Create a custom Pygments lexer for RIDDL syntax highlighting in MkDocs code
blocks. Currently `riddl` fenced code blocks render without syntax coloring.

**Implementation approach:**
1. Create `riddl_lexer.py` with a `RiddlLexer` class extending `RegexLexer`
2. Define token patterns for RIDDL keywords, types, strings, comments, etc.
3. Register the lexer in `mkdocs.yml` or via a plugin
4. Test with existing code examples in documentation

**Key token categories:**
- Keywords: `domain`, `context`, `entity`, `handler`, `type`, `command`,
  `event`, `query`, `result`, `is`, `of`, `to`, `from`, `inlet`, `outlet`, etc.
- Predefined types: `String`, `Number`, `Boolean`, `Date`, `Time`, `UUID`, etc.
- Operators: `=`, `:`, `{`, `}`, `(`, `)`, `[`, `]`
- Comments: `//` line comments, `/* */` block comments
- Strings: quoted literals

#### EBNF Grammar Validation Task

The EBNF grammar (`docs/riddl/references/ebnf-grammar.md`) is derived from the
official fastparse grammar in the riddl module and is intended for AI tools to
quickly understand RIDDL syntax. It must accurately reflect the rules accepted
by the fastparse parser.

**Known discrepancies found during editorial review:**
- Missing `=` as alternative to `is` in type definitions
- Missing `:` as alternative to `is` in field definitions (Scala-style syntax)

**Validation approach:**
1. Create a functional parser from the EBNF grammar
2. Run it against all example RIDDL sources in the test suite
3. Compare results with the fastparse parser
4. Revise EBNF until there are no discrepancies

This ensures the EBNF remains a reliable reference for AI-assisted RIDDL work.

## Design Decisions Log

| Decision | Rationale | Date |
|----------|-----------|------|
| Synapify four-panel layout | Left=tree, center=visual+text, right=metadata; 3 hideable | 2026-01-26 |
| Visual editor primary | Cannot be hidden; text editor secondary and synchronized | 2026-01-26 |
| riddlsim via HTTP | Synapify sends model/scenarios, riddlsim streams results | 2026-01-26 |
| riddl-gen separate service | Will be at gen.ossuminc.com; handles code generation | 2026-01-26 |
| Synapify "Coming Soon" | Product in development; document planned features | 2026-01-21 |
| Separate MCP section | MCP is distinct from IDE plugins; deserves own nav | 2026-01-21 |
| Per-tool MCP guides | Each AI tool has unique config; separate pages clearer | 2026-01-21 |
| Common authoring guide | Avoid duplication; same content for any IDE | 2026-01-21 |
| URL placeholder | `{{MCP_SERVER_URL}}` allows easy find/replace later | 2026-01-21 |

## Commits This Session

| Hash | Description |
|------|-------------|
| `0922e1d` | Update favicon to match www.ossuminc.com |
| `d6d7896` | Add multiple favicon sizes and proper link tags |
| `1a6b6e2` | Add comprehensive Synapify user documentation |

## Open Questions

- What is the public URL for the RIDDL MCP Server?
- When will Synapify be available for beta testing?