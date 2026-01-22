# Engineering Notebook: ossum.tech

## Current Status

Open source release documentation is now complete. The site includes:

- **OSS Section**: IntelliJ plugin and VS Code extension documentation
- **MCP Section**: RIDDL MCP Server with installation guides for 5 AI tools
- **Authoring Guide**: Common RIDDL writing best practices

Ready for review and testing with `mkdocs serve`.

## Work Completed (Recent)

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

None currently.

## Pending Tasks

### Before Deployment

| Task | Notes |
|------|-------|
| Run `mkdocs build --strict` | Verify all links work |
| Replace `{{MCP_SERVER_URL}}` | When public URL is available |
| Update release download links | When final releases are published |

### Lower Priority

| Task | File | Notes |
|------|------|-------|
| Type examples | `references/language-reference.md` | Add specialized examples |
| Future work review | `future-work/` | Update for current roadmap |
| Quick-start tutorial | New file | Optional getting started guide |

## Design Decisions Log

| Decision | Rationale | Date |
|----------|-----------|------|
| Separate MCP section | MCP is distinct from IDE plugins; deserves own nav section | 2026-01-21 |
| Per-tool MCP guides | Each AI tool has unique config; separate pages clearer | 2026-01-21 |
| Common authoring guide | Avoid duplication; same content for any IDE | 2026-01-21 |
| URL placeholder | `{{MCP_SERVER_URL}}` allows easy find/replace later | 2026-01-21 |
| 6-phase approach | Systematic improvement with commits after each phase | 2026-01-21 |
| Statement rewrite | Old statement.md listed obsolete types | 2026-01-21 |
| Processor docs in lang-ref | Language reference is authoritative | 2026-01-21 |

## Next Steps

1. Review documentation with `mkdocs serve`
2. Run `mkdocs build --strict` to verify links
3. Push commits to origin/main
4. Deploy to production with `mkdocs gh-deploy`
5. Update `{{MCP_SERVER_URL}}` when public URL available

## Files Created/Modified in This Session

### OSS Documentation
- `docs/OSS/index.md` (updated)
- `docs/OSS/authoring-riddl.md` (new)
- `docs/OSS/intellij-plugin/index.md` (rewritten)
- `docs/OSS/vscode-extension/index.md` (rewritten)

### MCP Documentation
- `docs/MCP/index.md` (new)
- `docs/MCP/claude-desktop.md` (new)
- `docs/MCP/claude-code.md` (new)
- `docs/MCP/gemini.md` (new)
- `docs/MCP/vscode-copilot.md` (new)
- `docs/MCP/intellij-ai.md` (new)
- `docs/MCP/intellij-junie.md` (new)

## Open Questions

- What is the public URL for the RIDDL MCP Server?
- Should there be a quick-start tutorial separate from the guides?
- Are there additional AI tools that need MCP configuration guides?