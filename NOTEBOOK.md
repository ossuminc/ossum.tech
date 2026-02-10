# Engineering Notebook: ossum.tech

## Current Status

Documentation site is complete and deployed at https://ossum.tech.
All major sections are documented with proper RIDDL syntax
highlighting.

**Completed (2026-02-09):**

- Fixed metadata vs body definition confusion across 10 files
  - Rewrote metadata.md, author.md, term.md, option.md to show
    correct `with { }` placement and syntax
  - Removed incorrect Contains entries (Authors, Options, Terms)
    from context.md, entity.md, projector.md, adaptor.md
  - Removed Options and Terms from domain.md Contains (kept
    Authors — correct per grammar)
  - Updated cheat-sheet.md containment table to distinguish body
    definitions from metadata, fixed "Lives in" entries for Term,
    Option, and Author
  - All examples now match EBNF grammar

**Completed (2026-01-29):**

- Reorganized "Future Work" into top-level "Coming Soon" section
  - Created consolidated `docs/coming-soon/index.md` with Simulation and
    Generation sections
  - Removed old `docs/riddl/future-work/` directory (8 files)
  - Generation section includes targets from riddl-gen NOTEBOOK.md
- Fixed broken fontawesome icons (`:fontawesome-regular-rotate-left:`) with
  Material Design icons (`:material-recycle:`) in concept pages
- Added generator suggestion form link (Google Form) to Coming Soon page
- Added sparkle icon (`:material-creation:`) to Coming Soon page title
- Fixed snippets base_path config for EBNF grammar inclusion
- Documentation audit and fixes:
  - Removed Docker section from MCP/index.md (not open source)
  - Expanded stub concept pages with full content: interaction, comment,
    include, sagastep, term, user
  - Added syntax examples and "when to use" guidance to adaptor and streamlet
  - Updated developer guide: removed Hugo refs, noted generation via Synapify
  - Added DDD glossary with key terms mapping + link to archi-lab.io glossary
  - Added type cardinality notation (`*`, `+`, `?`) to command-event patterns
  - Standardized all "Coming Soon" admonitions to use warning type
- Migrated RIDDL documentation from riddl.tech (Hugo) to ossum.tech (MkDocs)
- Created migration script: `scripts/migrate-hugo.py`
- Added Tutorials section with complete RBBQ case study (18 files)
- Expanded Tools/riddlc with installation, commands, configuration, etc.
- Added sbt-riddl plugin documentation
- Added Design Guide (contexts, command-event patterns, UI modeling)
- Added Developer Guide (principles, releasing)
- Updated mkdocs.yml navigation for all new sections
- Verified build with `mkdocs build --strict`

**Completed (2026-01-28):**

- Navigation reordered: RIDDL → Synapify → MCP → IDE Support → About
- Renamed "OSS" section to "IDE Support" in navigation
- EBNF grammar single-sourced from riddl-language jar (auto-extracts on
  `sbt update`)
- Header logo size increased
- MCP Server URL updated to `https://mcp.ossuminc.com/mcp/v1/` in all guides
- Added GitHub Copilot CLI integration guide (`docs/MCP/github-copilot.md`)
- Strategic site improvements Phase 1 (quickstart, examples gallery, SEO,
  edit links, PWA support, about page, playground placeholder)
- RIDDL Pygments lexer with custom color scheme
- Comprehensive editorial review
- CI workflow with lexer installation
- Updated sbt-ossuminc to 1.2.4

---

## Pending Tasks

### Before Production

| Task                           | Notes                                      |
|--------------------------------|--------------------------------------------|
| Update release download links  | When final releases are published          |
| Implement playground           | Integrate Monaco + MCP server validation   |
| Remove "Coming Soon" warnings  | When MCP server goes live (~early 2026)    |

### Deferred Strategic Improvements (Soon)

| ID | Task | Priority | Notes |
|----|------|----------|-------|
| 1.3 | Product landing pages by role | Medium | CTO, Architect, Developer pages |
| 1.4 | Comparison pages | Medium | RIDDL vs OpenAPI/AsyncAPI/UML |
| 1.5 | Demo video | High | 3-5 min screen recording with voiceover |
| 2.2 | Troubleshooting/FAQ | Medium | Seed from riddl-mcp-server idioms |
| 2.3 | Changelog links | Low | Link to GitHub releases |
| 2.4 | Learning paths | Medium | Beginner → Intermediate → Advanced |
| 2.5 | Mermaid diagrams | Low | Enable in mkdocs.yml, add to concepts |
| 3.3 | Social proof | Medium | Testimonials when available |
| 3.4 | Newsletter signup | Low | Mailchimp/ConvertKit embed |
| 4.1 | Community (Discord/GH) | Medium | GitHub Discussions or Discord |
| 4.4 | Page feedback | Low | "Was this helpful?" buttons |
| 5.2 | PDF export | Low | mkdocs-pdf plugin |
| 5.3 | API documentation | Medium | OpenAPI spec for MCP server |
| 6.2 | Pricing page | Medium | When Synapify pricing finalized |
| 6.3 | Contact form | Low | Replace email link with form |

**Note:** Blog/news (3.2) will be on www.ossuminc.com or LinkedIn, not here.

### Lower Priority

| Task | File | Notes |
|------|------|-------|
| Type examples | `references/language-reference.md` | Add specialized examples |
| Synapify generation docs | `synapify/generation.md` | Use preserved config |

---

## Task Details

### EBNF Grammar Single-Sourcing

The EBNF grammar is now automatically extracted from the `riddl-language` jar:

- **Source**: `riddl/grammar/ebnf-grammar.ebnf` resource in riddl-language jar
- **Target**: `docs/riddl/references/ebnf-grammar.ebnf`
- **Trigger**: Runs automatically on `sbt update`
- **Logic**: Only extracts if jar version is newer than local copy

To manually extract: `sbt extractEbnf`

### Synapify Generation Configuration

When documenting Synapify's generation features, use this HOCON configuration
example as a starting point (preserved from riddlc hugo):

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

---

## Design Decisions

| Decision | Rationale | Date |
|----------|-----------|------|
| EBNF single-sourced from jar | Keeps docs in sync with compiler grammar | 2026-01-28 |
| Nav order: RIDDL first | Primary product should be most prominent | 2026-01-28 |
| OSS renamed to IDE Support | Clearer purpose for visitors | 2026-01-28 |
| RIDDL lexer colors from IDE tools | Consistency across VS Code, IntelliJ, docs | 2026-01-28 |
| Lexer installed via pip in CI | Ensures syntax highlighting works in deployment | 2026-01-28 |
| CSS overrides for dark/light | MkDocs Material uses CSS, not Pygments styles | 2026-01-28 |
| Synapify four-panel layout | Left=tree, center=visual+text, right=metadata | 2026-01-26 |
| riddlc validation-only | Code generation available via Synapify | 2026-01-27 |
| Don't mention riddl-gen | Closed source; say generation is "via Synapify" | 2026-01-30 |
| Separate MCP section | MCP distinct from IDE plugins; deserves own nav | 2026-01-21 |

---

## Resolved Questions

| Question | Answer | Date |
|----------|--------|------|
| MCP Server public URL | `https://mcp.ossuminc.com/mcp/v1/` | 2026-01-28 |
| Synapify beta availability | March 1, 2026 | 2026-01-28 |
