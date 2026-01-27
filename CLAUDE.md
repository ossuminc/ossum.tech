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
│   │   ├── references/      # Language reference and EBNF grammar
│   │   ├── tools/           # Documentation for riddlc, IDE plugins, etc.
│   │   └── future-work/     # Planned features and roadmap
│   ├── MCP/                 # RIDDL MCP Server documentation
│   │   ├── index.md         # Overview, capabilities, tools
│   │   ├── claude-desktop.md
│   │   ├── claude-code.md
│   │   ├── gemini.md
│   │   ├── vscode-copilot.md
│   │   ├── intellij-ai.md
│   │   └── intellij-junie.md
│   ├── OSS/                 # Open source tools documentation
│   │   ├── index.md         # OSS landing page
│   │   ├── authoring-riddl.md  # Common RIDDL authoring guide
│   │   ├── intellij-plugin/ # IntelliJ IDEA plugin docs
│   │   └── vscode-extension/# VS Code extension docs
│   ├── synapify/            # Synapify visual editor docs
│   │   ├── index.md         # Overview and getting started
│   │   ├── user-interface.md # Four-panel UI documentation
│   │   ├── simulation.md    # riddlsim integration (coming soon)
│   │   └── generation.md    # riddl-gen integration (coming soon)
│   └── about/               # Company info, privacy policy
├── overrides/               # MkDocs theme customizations
├── mkdocs.yml               # MkDocs configuration
└── build.sbt                # SBT build for any Scala-based generation
```

### Key Documentation Files

When working on RIDDL-related tasks, these files are essential context:

- **EBNF Grammar**: `docs/riddl/references/ebnf-grammar.md`
- **Language Reference**: `docs/riddl/references/language-reference.md`
- **Concepts Index**: `docs/riddl/concepts/index.md`

---

## Build and Development

### Prerequisites

- Python 3.8+ with pip
- MkDocs Material: `pip install mkdocs-material`

### Local Development

```bash
# Serve locally with hot reload
mkdocs serve

# Build static site
mkdocs build

# Deploy to GitHub Pages (if configured)
mkdocs gh-deploy
```

The site will be available at `http://localhost:8000` when serving locally.

### MkDocs Configuration

The site uses MkDocs Material theme with these notable features:
- Automatic light/dark mode
- Navigation tabs
- Search with highlighting
- Admonitions (info boxes, warnings, etc.)
- Code highlighting with line numbers
- Custom CSS in `overrides/`

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

!!! note "Work In Progress"
    This section is under development.
```

### Code Examples

Use fenced code blocks with language hints:

```markdown
```riddl
domain Example {
  context MyContext {
    // Context contents
  }
}
```
```

### Cross-References

Link to other documentation pages using relative paths:

```markdown
See [Domain concepts](../concepts/domain.md) for more details.
```

---

## Documentation Status

As of 2026-01-26, documentation is complete for all major sections:

### Completed Sections

- **Introduction**: All pages complete
- **Language Reference**: Complete with all processor types and handlers
- **Tools**: Complete documentation for `riddlc`, IDE plugins, MCP server
- **Guides**: Complete guides for Authors, Developers, Domain Experts,
  Implementors
- **Concepts**: All concept pages complete with proper links
- **OSS**: IDE extension documentation with authoring guide
- **MCP**: Installation guides for 6 AI tools (Claude, Gemini, Copilot, etc.)
- **Synapify**: Comprehensive user guide with UI, simulation, and generation
  documentation (features marked "Coming Soon" where in development)

### Placeholders

| Placeholder | Location | Replace When |
|-------------|----------|--------------|
| `{{MCP_SERVER_URL}}` | All MCP guides | Public URL available |

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
- **riddl-vscode**: VS Code extension for RIDDL
- **riddl-mcp-server**: MCP server for AI-assisted RIDDL modeling

Refer to the parent `../CLAUDE.md` for cross-project coordination guidance.

---

## Quick Reference

| Task | Command |
|------|---------|
| Start dev server | `mkdocs serve` |
| Build site | `mkdocs build` |
| Check links | `mkdocs build --strict` |
| Deploy | `mkdocs gh-deploy` |