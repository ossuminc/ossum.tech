# Engineering Notebook: ossum.tech

## Current Status

Documentation site is complete and deployed at https://ossum.tech. All major
sections are documented with proper RIDDL syntax highlighting.

**Completed (2026-01-28):**

- MCP Server URL updated to `https://mcp.ossuminc.com/mcp/v1/` in all guides
- Added GitHub Copilot CLI integration guide (`docs/MCP/github-copilot.md`)
- Strategic site improvements Phase 1 (quickstart, examples gallery, SEO,
  edit links, PWA support, about page, playground placeholder)
- RIDDL Pygments lexer with custom color scheme
- Comprehensive editorial review
- CI workflow with lexer installation

---

## Pending Tasks

### Before Production

| Task                           | Notes                                                          |
|--------------------------------|----------------------------------------------------------------|
| Update release download links  | When final releases are published                              |
| Implement playground           | Integrate Monaco + MCP server validation                       |
| Remove "Coming Soon" warnings  | When MCP server goes live (~early 2026)                        |
| Single source for EBNF Grammar | Depend on riddl-language which contains the EBNF as a resource |

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
| Future work review | `future-work/` | Update for current roadmap |
| EBNF grammar validation | `references/ebnf-grammar.md` | See details below |
| Synapify generation docs | `synapify/generation.md` | Use preserved config |

---

## Task Details

### EBNF Grammar Validation

The EBNF grammar (`docs/riddl/references/ebnf-grammar.md`) is derived from the
official fastparse grammar in the riddl module. It must accurately reflect the
rules accepted by the parser.

**Known discrepancies found during editorial review:**
- Missing `=` as alternative to `is` in type definitions
- Missing `:` as alternative to `is` in field definitions (Scala-style syntax)

**Validation approach:**
1. Create a functional parser from the EBNF grammar
2. Run it against all example RIDDL sources in the test suite
3. Compare results with the fastparse parser
4. Revise EBNF until there are no discrepancies

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
| RIDDL lexer colors from IDE tools | Consistency across VS Code, IntelliJ, docs | 2026-01-28 |
| Lexer installed via pip in CI | Ensures syntax highlighting works in deployment | 2026-01-28 |
| CSS overrides for dark/light | MkDocs Material uses CSS, not Pygments styles | 2026-01-28 |
| Synapify four-panel layout | Left=tree, center=visual+text, right=metadata | 2026-01-26 |
| riddlc validation-only | Code generation moved to Synapify | 2026-01-27 |
| Separate MCP section | MCP distinct from IDE plugins; deserves own nav | 2026-01-21 |
| URL placeholder pattern | `{{MCP_SERVER_URL}}` allows easy find/replace | 2026-01-21 |

---

## Resolved Questions

| Question | Answer | Date |
|----------|--------|------|
| MCP Server public URL | `https://mcp.ossuminc.com/mcp/v1/` | 2026-01-28 |
| Synapify beta availability | March 1, 2026 | 2026-01-28 |
