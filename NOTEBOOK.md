# Engineering Notebook: ossum.tech

## Current Status

The ossum.tech documentation site is functional but several sections are
incomplete. The RIDDL language documentation is the most developed area,
with comprehensive coverage of concepts and a detailed language reference.
Several user guides and tool documentation pages remain as placeholders.

## Work Completed (Recent)

- [x] Created CLAUDE.md for this repository - 2026-01-20
- [x] Created NOTEBOOK.md to track pending work - 2026-01-20
- [x] Audited all documentation for WIP markers - 2026-01-20
- [x] Completed Author's Guide (`docs/riddl/guides/authors/index.md`) - 2026-01-20
  - Comprehensive guide covering workflow, AI collaboration, best practices
  - Includes common patterns: Command-Event, State Machine, Saga
  - Covers validation and iteration process

## In Progress

None currently.

## Pending Documentation Tasks

### High Priority - User Guides

| Task | File | Notes |
|------|------|-------|
| ~~Author's Guide~~ | ~~`guides/authors/index.md`~~ | **COMPLETED** 2026-01-20 |
| Developer's Guide | `guides/developers/index.md` | Guide for RIDDL maintainers |
| Domain Expert Duties | `guides/domain-experts/duties.md` | Several incomplete sections |

### Medium Priority - Concepts

| Task | File | Notes |
|------|------|-------|
| Metadata concept | `concepts/metadata.md` | "Coming Soon" placeholder |
| Conditional concept | `concepts/conditional.md` | Two TBD sections |
| Element concept | `concepts/element.md` | TBD section at end |

### Medium Priority - Introduction

| Task | File | Notes |
|------|------|-------|
| Why RIDDL is needed | `introduction/why-is-riddl-needed.md` | Has notes, needs prose |
| What RIDDL is based on | `introduction/what-is-riddl-based-on.md` | TODO section incomplete |

### Lower Priority - Tools

| Task | File | Notes |
|------|------|-------|
| RIDDL IDEA Plugin | `tools/riddl-idea-plugin/index.md` | TBD placeholder |
| RIDDL MCP Server | `tools/riddl-mcp-server/index.md` | Empty file |
| Implementor Ways to Use | `guides/implementors/ways-to-use-riddl.md` | TBD section |

## Design Decisions Log

| Decision | Rationale | Alternatives Considered | Date |
|----------|-----------|-------------------------|------|
| Use MkDocs Material | Industry standard, good search, responsive | Hugo, Docusaurus | Pre-existing |
| Separate guides by role | Different audiences need different focus | Single comprehensive guide | Pre-existing |
| AI context files in refs | Language ref designed for AI consumption | Inline AI hints | Pre-existing |

## Next Steps

1. Complete the Author's Guide (in progress)
2. Fill in Domain Expert Duties sections
3. Document the RIDDL MCP Server
4. Complete the Developer's Guide
5. Fill in TBD sections in concepts

## Open Questions

- Should the Author's Guide assume AI assistance is always available?
- What level of RIDDL syntax detail belongs in guides vs. references?
- Should there be a quick-start tutorial separate from the guides?

## Content Strategy Notes

### Author's Guide Direction

The Author's Guide should focus on:
1. **Workflow**: How to approach domain modeling with RIDDL
2. **AI Collaboration**: Using the Ossum MCP Service effectively
3. **Best Practices**: Naming conventions, organization, documentation
4. **Common Patterns**: Typical entity, handler, saga structures
5. **Validation**: Using riddlc to check models
6. **Iteration**: Refining models based on feedback

### Target Reader Profile

- Domain expert with business knowledge
- May not be a programmer
- Will use AI assistance for syntax details
- Needs to understand DDD concepts
- Focus on "what to model" not "how to code"