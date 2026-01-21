# Engineering Notebook: ossum.tech

## Current Status

The ossum.tech documentation site has undergone a comprehensive 6-phase
improvement. All major sections are now complete with accurate, well-organized
content. The site is ready for review and deployment.

**7 commits pending push to origin/main.**

## Work Completed (Recent)

### 2026-01-21: Documentation Improvement Plan Execution

Completed all 6 phases of the comprehensive documentation improvement:

- [x] **Phase 1**: Fix critical documentation accuracy issues
  - Updated `statement.md` with current statement types
  - Fixed containment rules in language reference to match EBNF
  - Corrected include directive syntax

- [x] **Phase 2**: Add missing processor documentation
  - Expanded Handlers section with all `on` clause types
  - Added Adaptors, Projectors, Streamlets, Connectors to language reference

- [x] **Phase 3**: Complete introduction section
  - Rewrote `why-is-riddl-needed.md` (was TODO notes)
  - Completed Jacobsen Use Cases 2.0 section

- [x] **Phase 4**: Complete tools documentation
  - Wrote comprehensive `riddlc/index.md`
  - Wrote `riddl-idea-plugin/index.md` with features and troubleshooting
  - Wrote `riddl-mcp-server/index.md` with setup, auth, API reference

- [x] **Phase 5**: Complete guides
  - Wrote full Developers Guide with architecture and contribution info
  - Completed Domain Experts duties and relating-to-riddl guides
  - Completed Implementors ways-to-use-riddl with SBT integration

- [x] **Phase 6**: Fix concepts section issues
  - Fixed broken links, heading levels, typos
  - Completed metadata.md, conditional.md, streamlet.md, use-case.md
  - Fixed incorrect "Occurs In" references

### 2026-01-20: Initial Setup

- [x] Created CLAUDE.md for this repository
- [x] Created NOTEBOOK.md to track pending work
- [x] Audited all documentation for WIP markers
- [x] Completed Author's Guide (`docs/riddl/guides/authors/index.md`)
- [x] Improved hierarchy diagram in `docs/riddl/concepts/index.md`

## In Progress

None currently. All planned phases complete.

## Pending Tasks

### Lower Priority (Not in original plan)

| Task | File | Notes |
|------|------|-------|
| Type examples | `references/language-reference.md` | Add more specialized type examples |
| Future work review | `future-work/` | May need updates for current roadmap |
| Verify link integrity | All files | Run `mkdocs build --strict` |

## Design Decisions Log

| Decision | Rationale | Date |
|----------|-----------|------|
| 6-phase approach | Systematic improvement with commits after each phase | 2026-01-21 |
| Statement rewrite | Old statement.md listed obsolete types from removed features | 2026-01-21 |
| Processor docs in lang-ref | Language reference is authoritative; concepts link to it | 2026-01-21 |
| Domain expert focus | Guides written for non-programmers working with AI | 2026-01-21 |

## Next Steps

1. Push 7 commits to origin/main
2. Run `mkdocs build --strict` to verify all links
3. Deploy to production with `mkdocs gh-deploy`
4. Consider adding Quick Start tutorial (optional)

## Files Modified in This Session

### Introduction
- `docs/riddl/introduction/why-is-riddl-needed.md` (rewritten)
- `docs/riddl/introduction/what-is-riddl-based-on.md` (completed)
- `docs/riddl/introduction/what-conventions-does-riddl-use.md` (fixed)

### Language Reference
- `docs/riddl/references/language-reference.md` (expanded significantly)

### Tools
- `docs/riddl/tools/index.md` (fixed)
- `docs/riddl/tools/riddlc/index.md` (written)
- `docs/riddl/tools/riddl-idea-plugin/index.md` (written)
- `docs/riddl/tools/riddl-mcp-server/index.md` (written)

### Guides
- `docs/riddl/guides/developers/index.md` (written)
- `docs/riddl/guides/domain-experts/duties.md` (completed)
- `docs/riddl/guides/domain-experts/relating-to-riddl.md` (completed)
- `docs/riddl/guides/implementors/ways-to-use-riddl.md` (completed)

### Concepts
- `docs/riddl/concepts/statement.md` (rewritten)
- `docs/riddl/concepts/epic.md` (fixed)
- `docs/riddl/concepts/case.md` (fixed)
- `docs/riddl/concepts/field.md` (fixed)
- `docs/riddl/concepts/processor.md` (fixed)
- `docs/riddl/concepts/handler.md` (completed)
- `docs/riddl/concepts/context.md` (completed)
- `docs/riddl/concepts/outlet.md` (fixed)
- `docs/riddl/concepts/value.md` (completed)
- `docs/riddl/concepts/sagastep.md` (fixed)
- `docs/riddl/concepts/element.md` (completed)
- `docs/riddl/concepts/metadata.md` (written)
- `docs/riddl/concepts/conditional.md` (completed)
- `docs/riddl/concepts/streamlet.md` (written)
- `docs/riddl/concepts/use-case.md` (expanded)

## Open Questions

- Should there be a quick-start tutorial separate from the guides?
- Are there additional processor types that need documentation?
