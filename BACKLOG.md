# BACKLOG

The single place for open work on ossum.tech. If it is not here, it is not
tracked. Completed items leave this file: what they taught goes to NOTEBOOK.md,
what is durably true goes to CLAUDE.md.

---

## 1a-remnant. `repository CartRepository` cannot be gated as written

**What:** One fence on `references/language-reference.md` still carries a
skip that is *not* a content bug. Its schema names `record Cart`, while the
page prelude must supply `entity Cart` for other fences on the page. One
context cannot hold both names, and `no-prelude=Cart` withdraws the entity
without providing the record.

**Fixing it** means renaming the prelude's `entity Cart` and every fence that
reaches it — bigger than it looks, and worth doing only if that page's
vocabulary is being reworked anyway. Everything else 1a-followup listed is
fixed (commit `470b436`).

**Not urgent:** the fence is a skip with an honest reason, so nothing is red.

---

## 1d. Finish the rc.16 migration — THE GATE IS RED  ← START HERE

**State:** 219 validated / 123 skipped / **35 failed**, exit 1, at commit
`11ee4da`. This is the only red gate in the project's history and it is
deliberate: skipping the 35 would hide real incompatibilities.

**Do not re-derive the analysis.** 109 failures were reduced to 35 by fixing
root causes; what remains is per-fence authoring, not investigation. The
grouped tally, measured 2026-08-18 against rc.16:

| n | Cause | Fix |
|---|---|---|
| ~24 | *"'X' in this 'send'/'tell'/'yield' names a message type, not a value, so nothing says where its N field(s) come from"* | give the message a constructor with values from scope: `send event Ev to outlet O` → `send event Ev(field = ...) to outlet O` |
| 4 | *"Value reference 'orderId' is not a 'let'-local, an 'on init'/'on term' parameter, …"* | saga/sagastep steps referencing `requires` fields that are no longer ambient |
| 3 | *"Context 'X' has duplicate content names"* | `guides/authors/authoring-riddl.md` fences colliding with the page prelude — needs `no-prelude=` |
| 2 | *"'set' is not allowed in Context 'X', which owns no state to write"* | rc.13's rule, two sites still on the old shape |
| 1 | record type named where a value is required | same as the 24, for a `morph` operand |

**Failures by file:** `references/language-reference.md` 9,
`guides/authors/index.md` 6, `guides/authors/authoring-riddl.md` 4,
`concepts/statement.md` 4, `quickstart.md` 3,
`guides/authors/design/ui-modeling.md` 2, and one each in
`introduction/why-is-riddl-needed.md`, `concepts/{sagastep,saga,projector,
processor,invariant,adaptor}.md`.

**The rule behind the big group is worth stating in the docs, not just
obeying:** a message named without a constructor says nothing about where its
field values come from, so RIDDL now requires the constructor. That belongs in
`concepts/message.md` and `concepts/statement.md` once the fences are fixed.

**Two facts to keep:** `Natural` excludes 0 — use `Whole`; and numeric
constants take bare literals (`= 100`), not strings.

---

## 1e. Document rc.16's new language features

None of these are documented anywhere yet. Each is in the generated grammar,
so the syntax is settled; the semantics for several are in
`../RIDDL-Computational-Model.md`.

- **`terminate <value> [with (args)]`** — ends an instance, invoking its
  `on term`. Target is a value typed `Id(entity E)`, not a processor ref.
- **`self` / `self.<field>`** — the executing instance; synthesized record
  (`id`, `version`).
- **`initiate`** — a value form; the creation counterpart to `terminate`.
- **Numeric literals** as first-class values, and in `constant` declarations.
- **Indexed lookup**: `value_ref at <index> {, <index>}`.
- **`on init` / `on term` take parameters**, making them invocable.
- **Connector intentions**: `at-least-once`, `at-most-once`, `exactly-once`,
  `persistent`, written before `connector`. Absent delivery means
  at-least-once; `at-most-once` is the knowing downgrade.
- **`Id(<processor-kind> Path)`** — adaptor/context/entity/projector/
  repository/streamlet, not just entity.
- **`prompt("...") as <type>`**.
- **`tell ... to X by <identifier>`**.
- **A38: a refusal step may name an invariant** rather than prose —
  `refuses user U <invariant-ref>`.
- **`!` and `not` are synonyms everywhere** (2026-08-14 ruling); `!` is no
  longer a separate `when`-only form. `concepts/conditional.md` says
  "Identifiers can be negated", which is now too narrow.
- **New UI aliases**: groups gain `scene`/`space`/`zone`; outputs gain
  `sound`/`speech`/`haptic`; inputs gain `voice`/`gesture`/`gaze`;
  presentation verbs gain `plays`/`speaks`/`announces`/`vibrates`/`pulses`/
  `nudges`/`diffuses`/`serve`/`offer`/`taste`. This is a deliberate widening
  past the screen — worth prose in `concepts/group.md`, not just a table row.

**Order:** 1d before 1e. A red gate first.

---

## 1c. The RBBQ tutorial is 73 skips and 0 validated

**What:** `tutorials/rbbq/` is the most-read tree and contributes **nothing**
to the gate: all 73 of its fences carry one identical skip — *"quoted verbatim
from riddl-models, which is still RIDDL 1.x"*. Everything else in
`sites/riddl/docs` is gated now, so this is the last blind spot.

**That reason has never been checked fence by fence, and it is the same shape
as the blanket skip 1a spent four passes retiring.** Measured 2026-08-10:
stripping it and running `--auto` with no prelude places **4 of 76**. That
number means very little on its own — `concepts/` scored 21 of 120 at the same
stage and finished fully gated, because most failures were missing page
vocabulary, not wrong RIDDL. At least one tutorial fence
(`external-contexts.md`, the `context HRSystem` one) validates clean under
`in-domain` today.

**So the open question is genuinely open:** how much of the tutorial is
actually 1.x, and how much merely needs a prelude? Answer it by gating two or
three pages the way `concepts/` was done, then extrapolate.

**Why it matters beyond coverage:** if a real part of it *is* 1.x, then the 2.0
documentation's flagship tutorial is teaching retired syntax. That is a content
problem, not a tooling one, and it is invisible today because the skip reason
sounds like a decision rather than an assumption.

**Prerequisite to check first:** the pages are transcribed from
`riddl-models`, which still builds against riddl 1.13.1. If that repo has not
migrated, fixing the tutorial means either diverging from its source or
migrating the models — a cross-project call. See the parent `CLAUDE.md`
dependency table.

**Also open:** `check-riddl-blocks.py` flags 33 advisory items, all in
`migration/` (which shows 1.x deliberately — arguably belongs in EXEMPT_PATHS)
and `tutorials/rbbq/`.

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
