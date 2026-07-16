# Engineering Notebook: ossum.tech

## Incoming Tasks

**At session start**, check the `task/` directory for pending
work requests from other projects. Each `.md` file describes a
task (e.g., dependency upgrade). Treat unresolved tasks as to-do
items unless already completed (verifiable from this notebook,
CLAUDE.md, or git log). After completing a task, append results
to the task file and note completion in this notebook.

---

## Current Status

Documentation site is complete and deployed at https://ossum.tech.
All major sections are documented with proper RIDDL syntax
highlighting.

**Completed (2026-07-16):**

- Backlog sweep + accuracy fixes (Tier 1 + CI gate). Scoured CLAUDE.md,
  NOTEBOOK.md, and the whole tree (docs, code, nav, links, CI) for pending
  work; the full inventory is in the plan file. Site health is excellent
  (148 nav ↔ 148 files, 754 links resolve, no orphans, no code TODOs). Fixed
  the pages reality had overtaken:
  - **MCP section rewrite** — the hosted `mcp.ossuminc.com` server (planned
    "early 2026", now retired) was still documented across
    `docs/MCP/index.md` + 8 client pages, plus the standalone
    `docs/riddl/tools/riddl-mcp-server/index.md` (Docker/REST/API-key) and
    the idea-plugin MCP section. All rewritten to local `riddlg mcp` (stdio)
    / `riddlg serve` (`POST /mcp`, port 8910), no API key, with the real 13
    tool names replacing the fictional `validate-text`/`validate-url`.
  - `coming-soon/index.md` — Hugo generation was marked "Currently
    available" (it was dropped from riddlg); reframed to mark what ships
    today via riddlg (AsciiDoc/MkDocs docs, Smithy/gRPC/OpenAPI specs,
    Quarkus code) vs roadmap; dropped the Akka target per editorial policy.
  - `CLAUDE.md` — structure diagram referenced the deleted `future-work/`
    dir (now `coming-soon/`); Pending Updates table refreshed.
  - `NOTEBOOK.md` — grammar-extraction facts corrected against `build.sbt`:
    task is `extractGrammar` (not `extractEbnf`), target is
    `riddl-grammar.ebnf` (not `ebnf-grammar.ebnf`), and it is **manual**
    (not wired to `sbt update`).
  - Env-var prefix verified `RIDDLG_*` throughout (linter had already fixed
    `models.md`/`configuration.md`; only the historical `OSSUM_GEN_LICENSE`
    removed-license note remains, correctly).
  - **CI**: added a `mkdocs build --strict` gate before deploy (was missing
    despite the notebook claiming strict verification), pinned
    `mkdocs-material>=9.5,<10` (Material 10 / MkDocs 2.0 are breaking) and
    Python to 3.12; removed the empty, referenced `docs/javascripts/extra.js`.
  - Verified with `mkdocs build --strict` (exit 0, no warnings).

**Completed (2026-07-15):**

- Documented riddlg 0.4.0 — riddl-generator PRs #1 (multi-provider
  BYOK + Keycloak Pro entitlement) and #2 (Synapify serve tasks).
  Details were read from the riddl-generator **source**, not its
  README, which is stale (see Open Questions).
  - `index.md` — the "nothing leaves your computer" claim is now
    conditional (cloud providers are opt-in and Pro). Replaced the
    **removed** offline license mechanism (`OSSUM_GEN_LICENSE`,
    `~/.ossum-gen/license`) with the Keycloak device flow
    (`riddlg login` / `whoami` / `logout`, 7-day offline grace).
  - New `ai-providers.md` — five provider types (llama, anthropic,
    gemini, openai, responses), BYOK profiles, the `riddlg ai`
    family, key precedence (env > keychain > file), OS-keychain
    storage, redaction, `--provider` / `--stream`.
  - New `configuration.md` — config file precedence, the full
    baked-in HOCON (incl. `model.gpu-layers`, the real `model.url`
    default, the `riddlg.ai` block), and the env var table.
  - New `server-api.md` — every `riddlg serve` route, incl.
    `POST /mcp`, `POST /ai/messages`, `GET /model/status`, the
    202-while-downloading contract, per-request provider override.
  - New `mcp-tools.md` — all 13 MCP tools (2 pre-existing + the 11
    derivation tools ported from the hosted server) and the
    6-pattern catalog.
  - Updated `command-reference.md` (`ai`, `login`/`logout`/`whoami`,
    `--provider`, `--stream`, exit codes), `models.md`
    (auto-download is now the default path; `RIDDLG_MODEL_FILE`
    is read only by `fetch-default-model.sh`, not by riddlg),
    `installation.md` (0.4.0; GPU is only needed for the local
    model), `docs/riddl/tools/index.md`, `docs/MCP/index.md`.

**Completed (2026-02-14):**

- Added Standard Highlighting reference page
  (`docs/riddl/references/standard-highlighting.md`)
  - Documents the 11 `Token` enum types from the RIDDL compiler
  - Dark and light theme color tables with hex codes and swatches
  - Implementation notes for each platform (IntelliJ, VS Code,
    Synapify/ossum.ai Monaco, Pygments/MkDocs)
  - Design principles and guidance for new tool implementors
  - Colors sourced from Pygments lexer (`riddl_lexer/style.py`)
    and CSS overrides (`extra.css`) as canonical reference
  - Updated references index and mkdocs.yml nav

**Completed (2026-02-13):**

- Rectified Reactive BBQ tutorial with verbatim riddl-models source
  - Replaced all fabricated RIDDL snippets with actual code from
    `riddl-models/hospitality/food-service/reactive-bbq/`
  - Created 14 new per-context pages:
    - Restaurant: front-of-house, kitchen, bar, online-ordering,
      delivery, loyalty
    - BackOffice: scheduling, inventory, reporting
    - Corporate: menu-management, supply-chain, marketing
    - Cross-cutting: external-contexts, patterns
  - Rewrote 5 existing pages: index, reactive-bbq, restaurant/index,
    backoffice/index, corporate/index
  - Updated mkdocs.yml nav with hierarchical context sub-pages
  - All GitHub links updated from riddl-examples to riddl-models
  - Each context page follows consistent structure: Purpose,
    Interview Connection, Types, Entity, Repository, Projector,
    Adaptors, Design Decisions, Source
  - Patterns page covers 7 cross-cutting RIDDL patterns with
    real code and links to where each appears
  - Build verified with `mkdocs build --strict` (no broken links)
  - 20 files changed, 3,860 lines added (commit 95e751a)

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
| Implement playground           | Monaco + riddlg validation; currently a placeholder page in nav |
| Update non-riddlg download links | riddlc / vscode / idea-plugin tool pages, when their final releases publish |
| Update Synapify "Coming Soon"  | simulation, code-gen, installers, pricing — when Synapify reaches public release |
| Re-scope playground MCP refs   | `docs/riddl/playground/index.md` still shows `/mcp/v1` + `validate-text` in its planned-architecture diagram; fix when the playground is built |

**Resolved 2026-07-16:** "Remove Coming Soon warnings when the MCP server
goes live" — reality inverted the expectation. The hosted `mcp.ossuminc.com`
server was **retired**, not launched; MCP now ships in `riddlg`. All MCP
guides (`docs/MCP/*`, `docs/riddl/tools/riddl-mcp-server/index.md`, the
idea-plugin MCP section) were rewritten to configure local `riddlg mcp` /
`riddlg serve` with the real 13 tools and no API key. riddlg download links
resolved at 0.4.0 (verified live on GCS).

#### riddlg distribution: how to verify (learned 2026-07-15)

`installation.md` documents **0.4.0** — the first release containing
`riddlg ai` / `riddlg login`, i.e. every feature the riddlg docs
describe. Pinning it to an older release would document commands the
binary does not have.

riddl-generator is a **private** repo, so GitHub release assets are
**not** publicly downloadable. The public channel is the GCS bucket
`synapify-releases/riddlg/<version>/`. A tagged GitHub release does
**not** imply a usable download — check GCS, not `gh release`:

```bash
curl -s https://storage.googleapis.com/synapify-releases/riddlg/latest.json
curl -s "https://storage.googleapis.com/storage/v1/b/synapify-releases/o?prefix=riddlg/0.4.0&fields=items(name)"
```

All six 0.4.0 artifacts (Darwin-arm64, Linux-x86_64, -cuda, -vulkan,
deb, rpm), `latest.json`, and the Homebrew formula were verified at
0.4.0 before this commit.

Two historical traps worth remembering:

- The **0.3.1** release workflow failed, so 0.3.1 was tagged and had
  GitHub assets but never mirrored to GCS — it was never installable.
- **cuda and vulkan tarballs were documented but never published**
  until 0.4.0 (0.3.0 mirrored only Darwin-arm64, Linux-x86_64, deb,
  rpm), so those links 404'd for the whole 0.3.0 era. 0.4.0 is the
  first release where every documented variant actually exists.

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

The EBNF grammar is extracted from the `riddl-language` library (pinned to
`1.29.0` in `build.sbt`) via the Grammar API:

- **Task**: `sbt extractGrammar` (a manual `taskKey` in `build.sbt:12,26`;
  it compiles the project and runs `tools/extract-grammar.sh`)
- **Target**: `docs/riddl/references/riddl-grammar.ebnf` (`build.sbt:32`),
  which `docs/riddl/references/ebnf-grammar.md` snippet-includes
- **Trigger**: **Manual** — it is *not* wired to `sbt update`; run it
  explicitly when bumping the riddl-language version
- **Note**: `riddl-grammar.ebnf` is checked in, so it can go stale relative
  to a newer riddl-language release until `extractGrammar` is re-run

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
