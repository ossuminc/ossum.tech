# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with
code in this repository.

## Project Overview

**ossum.tech** is the technical documentation website for Ossum Inc., built
with [MkDocs Material](https://squidfunk.github.io/mkdocs-material/). The
primary focus is documenting the RIDDL language and its ecosystem of tools.

### Repository Structure

```
ossum.tech/
├── docs/                    # All documentation content (Markdown)
│   ├── riddl/               # RIDDL language documentation
│   │   ├── introduction/    # What is RIDDL, why it exists
│   │   ├── concepts/        # RIDDL language concepts (domain, context, etc.)
│   │   ├── guides/          # User guides by role (authors, domain experts, etc.)
│   │   ├── examples/        # Model gallery linking to riddl-models repo
│   │   ├── playground/      # Interactive RIDDL editor (coming soon)
│   │   ├── references/      # Language reference and EBNF grammar
│   │   ├── tools/           # Documentation for riddlc, IDE plugins, etc.
│   │   └── future-work/     # Planned features and roadmap
│   ├── MCP/                 # RIDDL MCP Server documentation
│   ├── OSS/                 # Open source tools documentation
│   ├── synapify/            # Synapify visual editor docs
│   ├── stylesheets/         # Custom CSS (includes RIDDL syntax colors)
│   └── about/               # Company info, privacy policy
├── riddl_lexer/             # Custom Pygments lexer for RIDDL syntax highlighting
│   ├── __init__.py          # Package exports
│   ├── lexer.py             # Token definitions and regex patterns
│   └── style.py             # Color scheme matching IDE tools
├── overrides/               # MkDocs theme customizations
├── mkdocs.yml               # MkDocs configuration
├── pyproject.toml           # Python package config for riddl_lexer
└── .github/workflows/       # CI/CD (publishes to GitHub Pages)
```

### Key Documentation Files

When working on RIDDL-related tasks, these files are essential context:

- **EBNF Grammar**: `docs/riddl/references/ebnf-grammar.md`
- **Language Reference**: `docs/riddl/references/language-reference.md`
- **Concepts Index**: `docs/riddl/concepts/index.md`

### Reactive BBQ Tutorial Structure

The tutorial at `docs/riddl/tutorials/rbbq/` is a comprehensive
case study with 30 pages based on the actual RIDDL model in
`riddl-models/hospitality/food-service/reactive-bbq/`. All RIDDL
code blocks are verbatim from the model source.

```
rbbq/
├── index.md              # Landing page
├── scenario.md           # Business challenge
├── reactive-bbq.md       # Top-level domain model
├── patterns.md           # 7 cross-cutting patterns
├── external-contexts.md  # 6 third-party integrations
├── restaurant/           # 6 context pages + index
├── backoffice/           # 3 context pages + index
├── corporate/            # 3 context pages + index
└── personas/             # 9 persona interviews + index
```

Each context page follows a consistent structure: Purpose,
Interview Connection, Types, Entity, Repository, Projector
(if applicable), Adaptors, Design Decisions, Source links.
The source links point to `riddl-models` (not `riddl-examples`).

---

## Build and Development

### Prerequisites

- Python 3.8+ with pip
- MkDocs Material: `pip install mkdocs-material`

### Local Development

```bash
# Install the RIDDL lexer for syntax highlighting
pip install -e .

# Serve locally with hot reload
mkdocs serve

# Build static site
mkdocs build

# Deploy to GitHub Pages
mkdocs gh-deploy
```

The site will be available at `http://localhost:8000` when serving locally.

### RIDDL Syntax Highlighting

The `riddl_lexer/` package provides custom Pygments syntax highlighting for
RIDDL code blocks. It's automatically installed in CI via `pip install -e .`
before building.

**Token categories and colors (dark theme):**

| Token Type | Color | Examples |
|------------|-------|----------|
| Keywords | Burnt orange `#fa8b61` | `domain`, `context`, `entity`, `handler` |
| Readability | Yellow `#b3ae60` | `is`, `of`, `to`, `with`, `by` |
| Predefined types | Teal `#19c4bf` | `String`, `Integer`, `UUID`, `Timestamp` |
| Option values | Green `#57d07c` | `event-sourced`, `aggregate` |
| Punctuation | Teal `#0da19e` | `{`, `}`, `(`, `)`, `,`, `:` |
| Comments | Gray `#808080` | `// comment`, `/* block */` |
| Strings | Bright green `#98c379` | `"quoted text"` |
| Markdown docs | Dim green `#629755` | `\|## Heading` |

CSS overrides in `docs/stylesheets/extra.css` apply these colors to both
dark and light themes.

### MkDocs Configuration

The site uses MkDocs Material theme with these notable features:
- Automatic light/dark mode with visible toggle
- Navigation tabs
- Search with highlighting
- Admonitions (info boxes, warnings, etc.)
- Code highlighting via Pygments with custom RIDDL lexer
- Custom CSS in `docs/stylesheets/`
- **Edit links** - Each page links to GitHub for community contributions
- **PWA/offline support** - Service worker caches pages for offline access
- **SEO meta descriptions** - Key pages have frontmatter descriptions

### Markdown Extensions

The following Python Markdown extensions are enabled:
- `admonition` - Info boxes, warnings, tips
- `pymdownx.details` - Collapsible sections
- `pymdownx.superfences` - Fenced code blocks with syntax highlighting
- `pymdownx.tabbed` - Tabbed content
- `pymdownx.tasklist` - Checkbox lists
- `pymdownx.keys` - Keyboard key styling (++ctrl+s++)
- `attr_list` - HTML attributes on elements
- `md_in_html` - Markdown inside HTML blocks

---

## Documentation Standards

### File Structure

- Use `index.md` for section landing pages
- Use descriptive filenames with hyphens: `what-is-riddl.md`
- Keep files focused on single topics
- Use front matter for titles and metadata

### Writing Style

- Write for domain experts who may not be programmers
- Explain concepts before showing syntax
- Use concrete examples from realistic domains
- Link to related concepts liberally
- Define jargon when first used

### Admonitions

Use MkDocs Material admonitions for callouts:

```markdown
!!! info "Title"
    Information content here.

!!! warning "Caution"
    Warning content here.

!!! tip "Pro Tip"
    Helpful tip here.
```

### Code Examples

Use fenced code blocks with the `riddl` language hint:

````markdown
```riddl
domain Example is {
  context MyContext is {
    // Context contents
  }
}
```
````

### Cross-References

Link to other documentation pages using relative paths:

```markdown
See [Domain concepts](../concepts/domain.md) for more details.
```

---

## Editorial Guidelines

These guidelines were established during documentation review sessions:

### Tooling Separation

**Important**: The RIDDL ecosystem has a clear separation of concerns:

- **`riddlc`** (open source): Syntax and semantic validation only. It reads
  RIDDL files, checks them, and reports errors. No code generation.
- **Synapify** (commercial): Provides advanced features including code
  generation, documentation generation, and AI-assisted development. These
  features are available via subscription.

When documenting capabilities, do NOT claim that `riddlc` generates code,
diagrams, Kubernetes manifests, etc. Those capabilities exist in Synapify.

### Outdated Technology References

Remove or generalize references to specific generation targets that are no
longer accurate:

- ~~Kalix~~ (no longer a target)
- ~~Kubernetes deployment descriptors~~ (not in OSS tooling)
- ~~Akka code generation~~ (not in OSS tooling)

Instead, describe RIDDL's *capability* to enable such translation without
claiming specific tool support.

### Hugo Remnants

This site migrated from Hugo to MkDocs Material. Remove any Hugo shortcodes:

- `{{< toc-tree >}}` — doesn't work in MkDocs
- `{{< icon "..." >}}` — use Font Awesome syntax or remove
- Any other `{{< ... >}}` patterns

### Capitalization

Always use **RIDDL** (all caps) in prose. It's an acronym. Not "Riddl" or
"riddl" except in code/filenames where lowercase is conventional.

### Metadata vs Body Definitions

RIDDL has a critical distinction between **body definitions**
(inside `{ }`) and **metadata** (in `with { }` after the body):

- **Body**: types, handlers, entities, states, functions, etc.
- **Metadata**: term, option, author_ref (`by author`), briefly,
  described by, attachment

**Author definitions** (not references) only occur in Module and
Domain bodies. All other definitions use `by author Name` in
their `with { }` block to reference an author.

**Option syntax** requires `is`: `option is event-sourced`,
`option is technology("Kafka")`.

**Term syntax**: `term SKU is { |Stock Keeping Unit... }` — not
`term "SKU" is described by "..."`.

### RIDDL Syntax in Examples

Code examples must match the EBNF grammar. Common issues to avoid:

1. **Enumerations vs Alternations**:
   - `any of { A, B, C }` — enumeration of constants
   - `one of { TypeA, TypeB }` — alternation of types

2. **User terminology**: Use "User" not "Actor" (per Use Cases 2.0)

3. **Hyphenation**: `event-sourced` (hyphenated as compound
   modifier)

4. **Version requirements**:
   - JDK 25 (current LTS)
   - Scala 3.3.x (current LTS)
   - `sbt riddlc/stage` (not `sbt stage`)

### Tone and Style

- Light, accessible, occasionally jovial
- Technical precision without being dry
- Explain concepts before showing syntax
- Use em-dashes for asides—they read more naturally
- Prefer active voice

---

## RIDDL Language Context

When editing RIDDL documentation, understand these core concepts:

### Definition Hierarchy

```
Root
└── Domain (knowledge domain boundary)
    └── Context (bounded context from DDD)
        ├── Entity (stateful business object)
        ├── Repository (persistent storage)
        ├── Projector (event projection)
        ├── Saga (multi-step process coordination)
        ├── Streamlet (stream processing)
        └── Adaptor (message translation)
```

### Key Patterns

- **Event Sourcing**: Entities can store state as event logs
- **CQRS**: Commands and queries are separate message types
- **Handlers**: Define behavior in response to messages
- **Statements**: Pseudocode for business logic (not Turing-complete)

### Target Audience

Documentation serves multiple audiences:
- **Authors**: Write RIDDL models, need syntax and semantics
- **Domain Experts**: Review models, need concept understanding
- **Implementors**: Generate code from models, need technical details
- **Developers**: Maintain RIDDL tooling, need architecture info

---

## Related Repositories

This documentation site covers tools from other Ossum Inc. repositories:

- **riddl**: The RIDDL compiler (`riddlc`) and language implementation
- **synapify**: Desktop application for visual RIDDL editing
- **riddl-idea-plugin**: IntelliJ IDEA plugin for RIDDL
- **riddl-vscode**: VS Code extension for RIDDL (source for lexer tokens)
- **riddl-mcp-server**: MCP server for AI-assisted RIDDL modeling
- **riddl-models**: Curated example models (linked from `docs/riddl/examples/`)

Refer to the parent `../CLAUDE.md` for cross-project coordination guidance.

---

## Quick Reference

| Task | Command |
|------|---------|
| Install lexer | `pip install -e .` |
| Start dev server | `mkdocs serve` |
| Build site | `mkdocs build` |
| Check links | `mkdocs build --strict` |
| Deploy | `mkdocs gh-deploy` |

---

## Pending Updates

These items need updating when conditions are met:

| Item | Location | Update When |
|------|----------|-------------|
| "Coming Soon" warnings | All MCP guides | MCP server goes live (~early 2026) |
| Download links | Tool pages | Final releases published |
