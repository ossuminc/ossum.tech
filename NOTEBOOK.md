# Engineering Notebook: ossum.tech

## Incoming Tasks

**At session start**, check the `task/` directory for pending
work requests from other projects. Each `.md` file describes a
task (e.g., dependency upgrade). Treat unresolved tasks as to-do
items unless already completed (verifiable from this notebook,
CLAUDE.md, or git log). After completing a task, append results
to the task file and note completion in this notebook.

---

## RESUME HERE — open work as of 2026-07-30

### TASK D — navigation and content rework ✅ **DEPLOYED 2026-07-31**

Top menu carries RIDDL / riddlg / Synapify (root-relative, into each product's
`latest`) plus **IDE help** and About. The old "OSS" label is gone: the three
IDE-tool pages are now unversioned at `/ide-help/`, while `authoring-riddl.md`
stayed version-tracked and moved to the RIDDL author guides — it teaches the
language, not a tool. Coming Soon and `/find/` are deleted.

**Search is two fields, deliberately additive.** Material's title-bar box still
searches the current site *and version*; a **Full Search** field directly below
it queries Pagefind across all products. An earlier design replaced the
title-bar box, which would have cost version-scoped search; that was rejected.
Rendered from `overrides/main.html` into Material's `{% block hero %}`, which
sits below the whole sticky header — no partial override, so no pinning to a
Material release.

**Three faults this turned up, all fixed:**

- The shell deploy used `cp -r`, which only adds — so `/coming-soon/` and
  `/find/` kept serving 200 after deletion. Now `rsync --delete` with an
  exclude list covering everything the shell does not own. That list is
  load-bearing: getting it wrong deletes a whole product site, so it was tested
  against a tree containing all three prefixes before being pushed.
- **Two publishing branches racing.** Pushing `main` and `docs/1.x` seconds
  apart ran both workflows at once and `main`'s deploy was rejected with
  "fetch first" — silently lost. A `concurrency` group now queues them;
  `cancel-in-progress: false`, because cancelling a publish drops a deploy.
- `check-cross-site-links.py` judged sub-site presence by the `docs/` directory,
  which survives branch switches because shared assets are copied there and
  gitignored. On `docs/1.x` that made all 15 cross-branch links look broken.
  It now keys off the tracked `mkdocs.yml`.

---

### TASK C — per-product versioning split ✅ **DEPLOYED 2026-07-31**

Live. The site is four MkDocs projects, each product independently versioned.

| Deployed at | Source | Published from |
|---|---|---|
| `/` | `sites/shell/` | `main`, unversioned |
| `/riddl/<ver>/` | `sites/riddl/` + `OSS/` | `main` 2.0·next, `docs/1.x` 1.31·latest |
| `/riddlg/<ver>/` | `sites/riddlg/` + `MCP/` | `main` 0.6·latest |
| `/synapify/<ver>/` | `sites/synapify/` | `main` 0.17·latest |

Also live: cross-site search at `/find/` (Pagefind), a generated `robots.txt`
listing all five sitemaps, and directory-style URLs (`offline` plugin dropped).

**Rollback:** `git push --force origin gh-pages-2026-07-preprefix:gh-pages`.
That backup is the state immediately before this migration — *not*
`gh-pages-preversioning`, which predates the mike migration entirely and would
discard weeks of deploys.

**Deploy order that worked**, and why: `docs/1.x` first so `/riddl/latest/`
existed before `main` published links to it, then `main`, and only then the
removal of the old root-level `1.31/ 2.0/ latest/ next/`. Deleting the old
layout *last* rather than first meant no outage — the old URLs kept serving
until their replacements were live.

**Still outstanding:** `task/publish-riddl-license-page.md`. The page is live at
`/riddl/2.0/licenses/`, but `riddlc info` still prints `/riddl/licenses/`, which
404s and cannot be made to work — the second path segment is a version. riddl
must change three places, not the one the task file mentions.

**Known wart:** the merge to `main` bypassed a branch-protection rule ("must not
contain merge commits") because it was `--no-ff`. It was allowed through rather
than rejected. Use a fast-forward or rebase on `main` next time.

**Traps found, all now guarded in code:**

- `mike set-default` reads `mkdocs.yml` from the CWD to resolve the branch, so
  it needs `-F` as well as `--deploy-prefix`. There is no root config any more.
- A broken `--8<--` include renders as **nothing**, silently, and `--strict`
  stays quiet. The EBNF grammar page shipped empty this way. `check_paths` is on.
- `overrides/` is `custom_dir` for all four sites, so a hard-coded outdated
  banner made **Synapify** announce itself as a preview of RIDDL 2.0.
- The search-index completeness check originally required every product to be
  present, which would have made the *first* deploy of the split impossible.
- `pagefind[bin]`, not `pagefind` — the bare package is only the API wrapper.
- `TMPDIR` on macOS is not `/tmp`, and the `python3` first on `PATH` is not the
  one mkdocs runs under.
- `overrides/main.html`'s `'../' ~ base_url` was expected to break under
  directory URLs and does not — verified by reading the rendered href.

---

The RIDDL 2.0 documentation is **shipped and live**. Two older pieces of
follow-up work remain below.

### Where things stand

| Branch | State |
|--------|-------|
| `main` | RIDDL 2.0 docs, publishes as mike version `2.0` alias `next` |
| `docs/1.x` | RIDDL 1.31 docs, publishes as `1.31` alias `latest` |
| `gh-pages` | restructured and live; flat pre-versioning site removed |

All three pushed and in sync. Backup branch `gh-pages-preversioning` is on the
remote; rollback is
`git push --force origin gh-pages-preversioning:gh-pages`.

**Which compiler to use** — this bites immediately:

```bash
# 2.0 work (main / release/2)
riddlc                                          # PATH = riddlc-rc 2.0.0-rc.1
# 1.x work (docs/1.x)
/opt/homebrew/Cellar/riddlc/1.31.0/bin/riddlc   # NOT $(which riddlc)
```

`riddlc-rc` declares `conflicts_with "riddlc"`, so installing the RC took over
the PATH symlink. Validating 1.x docs with the PATH binary reports false
failures (3 on that Quickstart, all correct-for-1.31 deprecations).

---

### TASK A — mermaid DAG + per-scope mini-diagrams

**Decided 2026-07-30:** do both.

1. ✅ **DONE** — the ASCII hierarchy diagram on `docs/riddl/concepts/index.md`
   is replaced with mermaid.
2. ⬜ On each definition's concept page, replace the prose `## Contains` list
   with a **small per-scope mermaid mini-diagram**. 45 pages carry one.

**Stage 1, as built.** The mermaid fence is registered in `mkdocs.yml` under
`pymdownx.superfences.custom_fences`. Three things learned doing it:

- **One diagram was unreadable.** All 13 relations plus leaf bundles in a single
  flowchart renders as a wide, squished hairball — it *builds* and *renders*,
  it just cannot be read. It is now three: *where definitions live*, *what every
  processor may contain*, *behaviour and stories*. The diagram carries shape;
  the table below it carries completeness.
- **The containment table was wrong too.** It omitted `Relationship` from the
  *Processor contents* list, though `riddl-grammar.ebnf:102` includes it — so
  error #13 below had survived the `e4cda9d` correction. Fixed.
- **mermaid loads from a CDN** (`https://unpkg.com/mermaid@11/…`); Material does
  not bundle it. Verified by grepping the built `assets/javascripts/bundle.*.js`.
  Diagrams therefore need a real browser to verify, and would not have rendered
  under the `offline` plugin — which is one reason that plugin is being dropped.

**Stage 2 is a correctness pass, not just a rendering one.** Spot checks show
the prose lists have drifted the same way the diagram had: `entity.md` omits
Constant, Connector, Relationship and nested Processor; `saga.md` omits Inlet,
Outlet, Function and Include. Build each from the grammar, not from the list.

**Why a DAG, not a tree.** Saga and Connector occur at *two* scopes (Domain and
Context), processors nest, Groups nest. A tree cannot state containment
honestly — which is part of how the ASCII diagram drifted. Use dashed edges for
conditionally-scoped placements (Repository and Connector at Domain scope only
when they span contexts).

**The 13 errors in the old diagram** (all now fixed), each verified against
`docs/riddl/references/riddl-grammar.ebnf`:

| # | Wrong | Correct |
|---|-------|---------|
| 1 | Case → Statement | Case → **Interaction** |
| 2 | "Processor" *and* "Streamlet" separately | one concept — show **Processor** |
| 3 | Repository absent from Context | `context_definition` includes it |
| 4 | Repository/Connector absent at Domain | `domain_content` includes both (conditional) |
| 5 | Domain shows only Context, Epic, Type | + nested Domain, user, saga, author, version, copyright, import, include |
| 6 | Root shows only Domain | + module, author, version, copyright, import, include |
| 7 | Module absent | top-level container, unit of reuse |
| 8 | State → Handler only | + **Invariant** |
| 9 | Inlet/Outlet absent | every processor bears ports — **and so does a Saga** |
| 10 | Version/Copyright absent | nine scopes; **not** saga, **not** function |
| 11 | Connector absent | `domain_content` *and* `processor_definition_contents` |
| 12 | Saga only under Context | also `domain_content` |
| 13 | Relationship absent | `processor_definition_contents` |

**Verify against the GRAMMAR, never against the old picture.** Note this applies
to the containment *table* as well — `e4cda9d` corrected it but left error #13
in place, so it is not the oracle either. The grammar is.

Grammar rules to read: `root_content`, `root_definition`, `module_content`,
`domain_content`, `context_definition`, `entity_content`, `state_content`,
`processor_definition_contents`, `vital_definition_contents`,
`saga_definitions`, `epic_definitions`, `use_case`, `interactions`,
`group_definitions`, `function_definitions`, `repository_definitions`,
`projector_definitions`, `adaptor_contents`.

Confirm the mermaid actually *renders* — build, serve, and look at the page in a
browser. Two distinct failures hide from `--strict`: a missing fence
registration shows the block as a code block, and a registered fence can still
render an unreadable diagram. Check the built HTML for `class="mermaid"` to
tell those two apart.

---

### TASK B — the last 60 example fences (best effort)

Current baseline, from `main`:

```
137 validated, 145 skipped, 60 failed
```

By page: `guides/authors/index.md` 18, `introduction/what-conventions-does-riddl-use.md`
8, `guides/authors/design/ui-modeling.md` 5, `concepts/user.md` 4, then ones and
twos.

The automatable classes are exhausted. Each remaining fence needs its own
judgement: a page-prelude entry of the right *kind*, a split, or a `skip` with
a reason.

**Tooling** (all in `scripts/`, all take the riddlc path as argv[1]):

| Script | Does |
|--------|------|
| `validate-riddl-examples.py` | the gate. Uses each fence's declared directive — **most reliable error messages** |
| `annotate-riddl-examples.py` | tries every wrapper, writes the first that validates |
| `triage-riddl-examples.py` | three-way split; `--apply` auto-skips resolution-only failures |
| `suggest-riddl-prelude.py` | lists missing names |
| `check-riddl-blocks.py` | advisory scan for retired 1.x constructs |

Ten wrappers exist: `standalone`, `in-domain`, `in-context`, `in-entity`,
`in-handler`, `in-clauses`, `in-usecase`, `in-application`, `in-function`,
`in-record`.

**Traps, all learned the hard way:**

- `suggest-riddl-prelude.py` guesses *kinds* badly — riddlc says "should refer
  to a Type" for messages too, so `OrderPlaced` must be declared an `event`.
  Take the names, supply the kinds yourself.
- A page prelude must be **self-contained**. Never reference a
  wrapper-synthetic name (`ExampleEntity`, `ExampleCommand`) — every fence then
  fails *on the prelude*, and the errors point at lines that look fine.
- A prelude is **not** injected into `standalone` fences: context-level
  definitions are illegal at root and would break the fences needing no help.
- `mkdocs build --strict` does **not** fail on dangling intra-page anchors. Always
  `mkdocs build --strict 2>&1 | grep -E 'anchor|WARNING|ERROR'`.

Not a merge blocker: prose and syntax are correct and separately checked.
The CI gate stays off until this reaches zero.

---

### Also open

- **When 2.0 ships final:** `scripts/promote-2.0-to-latest.md`. Do not
  improvise — there is a silent-revert hazard if both branches declare
  `latest`.
- `sbt extractGrammar` still resolves the *published* riddl library and would
  overwrite the 2.0 grammar. `build.sbt` warns at the task.

---

## Current Status

Documentation site is deployed at https://ossum.tech. All major
sections are documented with proper RIDDL syntax highlighting.

**In progress — RIDDL 2.0 docs on `release/2` (2026-07-28):**

Documentation is being versioned with `mike`, one entry per RIDDL
MINOR version. Nothing is pushed yet; all work is local.

| branch | publishes as | role |
|--------|--------------|------|
| `docs/1.x` | `1.31` `[latest]` | 1.x maintenance line, live not frozen |
| `release/2` → `main` | `2.0` `[next]` | becomes `[latest]` when 2.0 ships |

Key facts to carry forward:

- `docs-version.yml` on each branch declares what it publishes.
  The release-time flip is a one-line edit there, not a workflow
  change.
- CI publishes only from `main` and `docs/1.x`, so `release/2`
  cannot refresh production.
- The `gh-pages` restructure is **not done** — it is supervised
  and happens at merge time. Runbook:
  `scripts/migrate-gh-pages-to-mike.md`, with backup branch and
  rollback.
- Live URLs are `.html`-style (the `offline` plugin sets
  `use_directory_urls: false`), and mike preserves that. Only a
  version prefix is added. `scripts/gh-pages-404.html` rewrites
  legacy links.
- Rehearsed against a clone of real `gh-pages`: mike leaves
  `CNAME`/`.nojekyll` alone and does not conflict with `offline`.

**Remaining before merge:** the RBBQ tutorial re-sync (blocked on
`riddl-models`, see below), and a final read-through.

### Traps found while doing this work

- **`mkdocs build --strict` does NOT fail on dangling intra-page
  anchors.** It reports them at INFO and exits 0. Always also run
  `mkdocs build --strict 2>&1 | grep -E 'anchor|WARNING|ERROR'`.
- **`sbt extractGrammar` would overwrite the 2.0 grammar.** It
  resolves the *published* riddl library, still 1.29.0. `build.sbt`
  carries a warning at the task. Bump the library version to 2.0.0
  before running it again.
- The local machine has mkdocs-material **Insiders**; CI installs
  the community edition. Do not use Insiders-only features.

### Incoming tasks cleared (2026-07-28)

All four `task/` files closed to `task/done/`.

- **document-code-statement** — added a Code Statement section to the language
  reference (it had none) and extended `concepts/statement.md` with the
  escape-hatch semantics. Claims re-verified against the compiler.
- **migration-guide-gaps** — findings real, **premise wrong**. All four
  reported breakages fail identically under 1.31 *and* 2.0, and the grammars
  are identical on each point, so none is a 1.x→2.0 change. Documented in the
  language reference under a new "Common Parse Errors" section instead of the
  migration guide, where they would have misled anyone upgrading from 1.31.
  Item 4 routed to riddl.
- **upgrade-riddl-1.13.1 / 1.13.3** — obsolete; `build.sbt` is on 1.29.0.

Two things worth remembering from that work:

- A user type named after a **parameterized** predefined (`Currency`,
  `Decimal`, `Pattern`, `Id`) gives `Expected ("(")` at the **use site**,
  arbitrarily far from the declaration. A **bare** one (`Location`) gives a
  clear error at the declaration. That asymmetry is why `Currency` was hard to
  diagnose.
- The `code` statement's language tag is matched by **prefix**, so `javafoo`
  and `pythonic` parse. Only `scala`/`java`/`python`/`mojo` are supported.

Filed against riddl: `riddl/task/2026-07-28-grammar-questions-from-docs.md`
(comment-with-`???`, and `command X()` leniency).

### Deployment: live and versioned (2026-07-30)

The mike migration is **done**. Both versions are live:

| URL | Serves |
|-----|--------|
| `ossum.tech/` | redirects to `latest/` |
| `/latest/`, `/1.31/` | RIDDL 1.31 |
| `/next/`, `/2.0/` | RIDDL 2.0 (release candidate) |

`gh-pages` was restructured: the flat pre-versioning site was removed (it was
shadowing the versioned content — `/riddl/...` was still serving pages built
2026-07-21), and `scripts/gh-pages-404.html` now redirects legacy unversioned
links. Backup branch `gh-pages-preversioning` is on the remote; rollback is
`git push --force origin gh-pages-preversioning:gh-pages`.

**Next deployment action — when RIDDL 2.0 ships final:** follow
`scripts/promote-2.0-to-latest.md`. Do not improvise it; there is a silent
revert hazard if both branches declare `latest`.

Two traps learned here, both recorded in CLAUDE.md:

- **mike aliases must be `--alias-type copy`.** The default is `symlink` and
  GitHub Pages does not serve symlinked content, so `/latest/...` 404s in
  production — while a local `python -m http.server` rehearsal follows symlinks
  and shows 200. A passing local preview proves nothing about aliases.
- **`mike` refuses to act on a stale local `gh-pages`** ("gh-pages is unrelated
  to origin/gh-pages"). Sync the branch; never reach for
  `--ignore-remote-status`, which clobbers the remote.

### Concepts hierarchy diagram

Superseded — see **TASK A** in the RESUME HERE section at the top of this
file, which carries the decision (mermaid DAG + per-scope mini-diagrams) and
the full list of errors.

### Cross-repo dependency

`riddl-models/task/2026-07-26-release2-syntax-migration.md` has an
appended section for re-syncing the RBBQ tutorial. The tutorial
deliberately still shows 1.x syntax, with a note saying so, because
its 30 pages quote that repo verbatim.

**Completed (2026-07-21):**

- **riddlg docs brought current to 0.6.0** (were pinned at 0.4.0; 0.5.0 and
  0.6.0 had shipped). Facts sourced from `../riddl-generator` at tag `0.6.0`,
  not from the release blog post alone.
  - **New** `docs/riddl/tools/riddlg/generators.md` — catalog of every output
    format, what each contains, Free/Pro, and the model options each reads
    (`sql_dialect`, `backstage_owner`, `confluence_space`, …).
  - **New** `docs/riddl/tools/riddlg/release-notes.md` — 0.2.0 → 0.6.0, with
    the two breaking changes called out (`OSSUM_GEN_*` → `RIDDLG_*` in 0.5.0;
    license files removed in 0.4.0).
  - Corrected errors the site was actively serving: `gen` documented as **4**
    subcommands (it has **9**); `-f hugo` labeled "coming Q3 2026" (shipped in
    0.5.0); Pro tier listed as **2** features (it is **4**); five
    `/generate/*` endpoints undocumented; install URLs at 0.4.0; a Client Note
    claiming "there is no streaming endpoint" (0.5.0 added SSE on
    `/ai/messages`).
  - `coming-soon/index.md` generation tables rebuilt — Hugo moved from roadmap
    to available; AsyncAPI/JSON Schema/SQL/DBML added; new Catalog Generators
    table for Backstage + EventCatalog.
  - Verified with `mkdocs build --strict` — zero broken links, zero broken
    anchors.
  - No local mkdocs on this machine — used a venv in the session scratchpad.
  - **Upstream drift found, owned by Reid (not this repo):**
    `riddl-generator`'s own `README.md` and `CLAUDE.md` are stale the same way
    this site was — riddl-lib 1.28.0/1.29.0 vs actual 1.31.0, no mention of
    the nine 0.6.0 generators, config table missing `token-param`/`auth`. Also
    a real inconsistency: `scripts/fetch-default-model.sh` defaults to the
    **bartowski** HF repo while `riddlg.model.url` defaults to the **official
    Qwen** repo — two sources for the same ~23 GB model.

- **Anchor validation is now permanent.** `mkdocs build --strict` promotes
  warnings to errors but does **not** check heading anchors by default, so a
  link to `page.md#renamed-heading` built clean and 404'd in the browser.
  Added a `validation.links` block to `mkdocs.yml` (`anchors: warn`,
  `not_found: warn`, `unrecognized_links: warn`). Proved it works by injecting
  a link to a non-existent anchor and confirming the build aborts. The whole
  site passes, so there was no pre-existing anchor rot.

- **The site has no PWA and no service worker** — `CLAUDE.md` claimed
  "Service worker caches pages for offline access"; the build output contains
  no `sw.js`, no web manifest, nothing. Material's `offline` plugin only
  (a) forces `use_directory_urls = False`, (b) adds an iframe-worker polyfill,
  and (c) inlines the search index so the *built* site can be copied to disk
  and browsed over `file://`. Visitors get zero offline caching. Claim
  corrected; a future session won't go hunting for a broken service worker.

- **Page URLs end in `.html`, not `/`.** Consequence of the above — both Reid
  and Claude independently hit a 404 assuming `.../generators/`. The real URL
  is `.../generators.html`. `use_directory_urls: true` in `mkdocs.yml` is
  silently overridden by the plugin (`plugin.py`, `on_config`), so switching
  URL style means dropping `offline` entirely, which would 404 every indexed
  URL. **Decision: keep `.html`** — directory URLs are cosmetic, the breakage
  is real. Documented in `CLAUDE.md` so it isn't re-litigated.

**Resolved this session (no longer open):**

- ~~`unset GITHUB_TOKEN` breaks `gh` here~~ — `gh` has no keychain auth on
  this machine, so `GITHUB_TOKEN` is its only credential. Fixed at source:
  ossuminc `CLAUDE.md` commit `6f76baa` reverses the guidance for all 17
  repos.
- ~~`main` had PR-required branch protection~~ — contradicted the ossuminc
  commit-directly-to-`main` convention and pushes were logging
  `Bypassed rule violations`. Reid removed it (confirmed: the final push
  logged no bypass).

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
| ~~Keep `.html` page URLs~~ | ~~`offline` plugin forces it; directory URLs are cosmetic and would 404 every indexed URL~~ | 2026-07-21 |
| **REVERSED**: directory-style URLs, `offline` dropped | The reasoning stood on its own, but the cost was about to be paid anyway: the per-product split moves every URL regardless, so the choice was one breakage or two. `offline` also bought nothing real — it advertised offline support the site never had (no service worker, no manifest) while blocking `navigation.instant` and preventing mermaid, which loads from a CDN, from ever rendering | 2026-07-30 |
| One MkDocs project per product | `mike` versions a whole project, so one project stamped RIDDL's version on everything — the privacy policy existed once per RIDDL version and had to be fixed on two branches | 2026-07-30 |
| MCP guides ship with riddlg, not RIDDL | 21 of their 22 outbound links point at riddlg; they document the server riddlg drives | 2026-07-30 |
| Licenses page URL is version-pinned | Notices must describe the artifact the reader is holding; a `/latest/` URL would show a riddlc 2.0.0 user some future release's dependencies | 2026-07-30 |
| Cross-site search deferred | Material's index is per-build. Pagefind indexes built HTML and would work, but keeping a search-UI change separate from a URL migration keeps both revertible | 2026-07-30 |
| Anchor validation in CI | `--strict` alone misses broken `#anchors`; they 404 silently in the browser | 2026-07-21 |
| riddlg gets its own Generators + Release Notes pages | Output surface outgrew the command reference; releases ship ~weekly and need a landing place | 2026-07-21 |

---

## Resolved Questions

| Question | Answer | Date |
|----------|--------|------|
| ~~MCP Server public URL~~ | ~~`https://mcp.ossuminc.com/mcp/v1/`~~ — **obsolete**: that hosted server was retired 2026-07-16 in favor of local `riddlg mcp` (stdio) / `riddlg serve` (`POST /mcp`, port 8910) | 2026-01-28 |
| Synapify beta availability | March 1, 2026 | 2026-01-28 |
