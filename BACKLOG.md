# BACKLOG

The single place for open work on ossum.tech. If it is not here, it is not
tracked. Completed items leave this file: what they taught goes to NOTEBOOK.md,
what is durably true goes to CLAUDE.md.

---

## 1a. Retire the blanket "illustrative fragment" skips  ← START HERE

**What:** When filed, the gated pages reported 84 validated and **128 skipped**,
**118 of them carrying one identical reason**: `illustrative fragment;
references vocabulary this page does not define`. That is precisely what a
`<!-- riddl-prelude ... -->` exists to supply, so they were bulk-skipped rather
than annotated.

A skip is a legitimate outcome for a fence that genuinely cannot compile — a
deliberate counter-example, or an `include` resolved against a file that does
not exist. What 1a retires is the **blanket** reason applied without looking.
Each such fence keeps a skip, but with a reason that says which of those it is.

**Measured 2026-08-08**, not estimated: stripping that one reason from 8 sample
concept pages (14 such skips) and re-running with `--auto` — **4 of the 14
needed nothing but an existing wrapper** and were skipped for no reason at all.
The other 10 need a per-page prelude, which is the documented remedy, not a
correction to the examples.

**Method per page:**
```bash
# strip the blanket skip (WHOLE line, indentation included -- a leftover
# indent corrupts fence matching and silently changes the counts)
# then see which wrapper each fence fits:
python3 scripts/validate-riddl-examples.py --auto ../bin/riddlc <page>.md
```
Annotate the ones that place; write one page prelude for the rest.

**Progress:** `concepts/` and `introduction/` are **done** — not one blanket
skip remains in either. `language-reference.md` has had a first slice: 23
validated / 52 skipped → **35 / 40**. Gate-wide: **171 validated / 55 skipped
/ 0 failed**, from 84/128 when 1a was filed.

**49 blanket skips remain:**

| Where | Count | Note |
|---|---|---|
| `references/language-reference.md` | 32 | in scope; see below |
| `migration/1.x-to-2.0.md` | 6 | **outside the gate** — 1b territory |
| `guides/authors/design/command-event-patterns.md` | 6 | outside the gate |
| `guides/authors/design/ui-modeling.md` | 3 | outside the gate |
| `guides/authors/index.md` | 2 | outside the gate |

### What the remaining 32 need (measured, do not re-derive)

The page's prelude has been extended once and **compiles clean on its own** —
probe it with `wrap("in-context", "type ProbeOnly is String", prelude)` before
blaming a fence. What is left divides roughly into:

- **Statement fences** (`send`/`tell`/`set`/`let`/`match`/`foreach`/`become`)
  that want `in-handler`. The wrapper already supplies `order`, `cart` and
  their fields; what they lack is page vocabulary — outlets, events, target
  entities — some of which is now in the prelude and some not.
- **Whole-context fences** (adaptor, projector, pipeline, application, epic)
  that declare their own `context`. These want `in-domain` plus a
  **`riddl-domain-prelude`** holding the sibling contexts they name
  (`PaymentContext`, `OrderContext`, `Storefront`). The page has no domain
  prelude yet; that is the single biggest lever left.
- **Genuinely unskippable, needing a precise reason instead of the blanket
  one:** the two `import "commerce.bast"` fences, and the
  `on command DoIt from context Other` pair (two spellings of the same clause,
  which cannot share a handler — same fence as `onclause.md`).
- **Known content bugs to fix while there:** `button Checkout activates type
  Boolean` (fifth page with that line), and the `version` fence whose
  `entity Order` has no handler.

**Two traps this page taught, both costly:**

- **Never name a prelude entry `Tax`.** The `in-function` wrapper supplies a
  sibling `context Tax`, so a prelude `function Tax` makes every `Tax.…` path
  ambiguous and breaks the page's in-function fences. The prelude carries a
  comment saying so.
- **`annotate-riddl-examples.py` places a fence against the prelude AS IT
  WAS.** Extending the prelude afterwards can invalidate earlier placements —
  it silently invalidated 8. Annotate, then extend, then re-run the page.

**The gate's scope is a file list, not a directory.** The exact command is in
CLAUDE.md § "Compiling RIDDL examples". Compare numbers only within one scope.

**Rules the work established** (each earned by a regression):

- Wrapper-internal names keep the `Example` prefix. A record named `OrderData`
  collided with `language-reference.md`'s own prelude — a page prelude and the
  wrapper share one context — and broke two of its fences.
- Wrapper vocabulary is only ever ADDED, never renamed: an extra field cannot
  break a fence that ignores it.
- **Re-run the FULL gate after any wrapper edit**, never just the page in hand.
  Wrapper changes have regressed other pages three times in this work.
- A wrapper must satisfy the checks its own shape triggers: `in-entity` needs a
  state with a handler, or a fence contributing only invariants fails for the
  wrapper rather than for itself.

**Why this outranks 1b:** these pages are already gated, so the gate reports
green while checking barely 40% of their RIDDL. That is the same
"green-but-measured-nothing" failure recorded in NOTEBOOK.

---

## 1b. Gate the doc trees that have no directives at all

**What:** Not yet gated: `tutorials/rbbq/` (30 pages, the most-read tree),
`guides/`, `tools/`, and the `riddlg`/`synapify`/`shell` sites.

**Also open:** `check-riddl-blocks.py` flags 33 advisory items, all in
`migration/` (which shows 1.x deliberately — arguably belongs in EXEMPT_PATHS)
and `tutorials/rbbq/`.

**Order:** After 1a, which is smaller and buys more real coverage.

---

## 2. Promote RIDDL 2.0 to `latest` when it ships final

**What:** `latest` points at 1.31, which is correct while 2.0 is an RC.

**How:** `scripts/promote-2.0-to-latest.md`. Since TASK G it is **one commit** —
both RIDDL lines publish from `main`, so the old two-branches-one-alias landmine
is gone.

**The one rule left:** `mike set-default` runs once per entry, so the **last
`riddl` entry** in `docs-version.yml` decides where `/riddl/` redirects. Move
the entries, not just the alias.

**Blocked on:** RIDDL 2.0 final. `../bin/riddlc` is `2.0.0-rc.10-57-e012ebb9`
(verified 2026-08-10); do not trust a version written here, run it.

---

## 3. Re-sync the EBNF grammar whenever riddl's parser changes

**What:** `sites/riddl/docs/references/riddl-grammar.ebnf` is **generated** from
the riddl version pinned in `build.sbt`. It moves often while 2.0 is in RC.

**Do this, always:**
```bash
# 1. set build.sbt's With.Riddl.library(version = ...) to match `riddlc version`
# 2. then
sbt extractGrammar
```

The pin and `../bin/riddlc` must name the SAME version, or the docs describe a
grammar the validated examples were never checked against. Bumping the pin may
require bumping `With.Scala3` to whatever riddl built with.

**Never `cp` it from `../riddl`.** That is a live working tree. Verified
2026-08-08: it held an uncommitted `yields`/`replies` split that exists in no
commit and no build, so a copy would have documented a language that does not
exist, and looked successful. See CLAUDE.md § "Things that will bite".

The file is generated wholesale, so partial syncs are not an option — expect
unrelated rules to come along.

**When:** Any time riddl restages `../bin/riddlc`. Compare `riddlc version`
against the pin in `build.sbt` at session start.

---

## 4. Watch for `requires type T` in prose

**What:** Low priority, informational. `requires <type_ref>` accepts an
**optional** `type` keyword — `aggregate_use_case = "type" | "command" |
"query" | ...` (`ebnf-grammar.ebnf`), confirmed by riddl 2026-08-04 and by
compiling both spellings.

**Why it is here:** This session briefly believed `requires type T` was invalid,
having misread `type_ref = [aggregate_use_case] path_identifier` as excluding
the keyword. The docs use the bare form, which is correct — but do not "fix"
anyone who writes `requires type T`, and do not assert it is wrong.

---

## 5. Site and content roadmap (was buried in NOTEBOOK.md)

**What:** 18 site/content items that had been recorded in NOTEBOOK.md's
"Deferred Strategic Improvements" and "Lower Priority" tables. Moved here
2026-08-10 because NOTEBOOK is the narrative record and BACKLOG is the tracked
one — an item living only in NOTEBOOK is not tracked.

**Not verified.** Unlike items 1-4, these were carried over as written and none
was re-checked against the current site. Treat priorities as stale until
confirmed; several predate the per-product versioning migration.


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


**Lower priority**

| Task | File | Notes |
|------|------|-------|
| Type examples | `references/language-reference.md` | Add specialized examples |
| Synapify generation docs | `synapify/generation.md` | Use preserved config |
