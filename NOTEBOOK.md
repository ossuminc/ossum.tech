# Engineering Notebook: ossum.tech

## Current Status

Documentation site is complete and deployed at https://ossum.tech. All major
sections are documented with proper RIDDL syntax highlighting.

**Recent completion (2026-01-28):**
- RIDDL Pygments lexer with custom color scheme matching IDE tools
- Comprehensive editorial review of all documentation sections
- CI workflow updated to install lexer before building

---

## Pending Tasks

### Before Production

| Task | Notes |
|------|-------|
| Replace `{{MCP_SERVER_URL}}` | When public URL is available |
| Update release download links | When final releases are published |

### Lower Priority

| Task | File | Notes |
|------|------|-------|
| Type examples | `references/language-reference.md` | Add specialized examples |
| Quick-start tutorial | New file | Optional getting started guide |
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

## Open Questions

- What is the public URL for the RIDDL MCP Server?
- When will Synapify be available for beta testing?
