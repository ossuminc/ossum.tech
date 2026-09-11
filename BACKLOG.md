# BACKLOG

The single place for open work on ossum.tech. If it is not here, it is not
tracked. Completed items leave this file: what they taught goes to NOTEBOOK.md,
what is durably true goes to CLAUDE.md.

---

## 1e-remnant. SUPERSEDED — riddl built the modality checks

**Closed 2026-08-26, by riddl, not by us.** The task filed that morning
(`riddl/task/done/2026-08-26-modality-aliases-parse-but-mean-nothing.md`) was
acted on the same day, and all three cases are settled:

| Case | Outcome | Rule id |
|---|---|---|
| 1. Verb inconsistent with output modality | **Built** — StyleWarning | `app-verb-modality-mismatch` |
| 2. Compound output mixing modalities | **DECLINED** — must not warn | — |
| 3a. A `menu` with no selectable input | **Built** — CompletenessWarning | `app-menu-has-no-choice` |
| 3b. An unreachable `popup`/`dialog` | **Built** — CompletenessWarning | `app-group-unreachable` |

Verified here: the four-defect fixture from that task now reports all four
against rc.26 — 2x `app-verb-modality-mismatch`, 1x `app-menu-has-no-choice`,
1x `app-group-unreachable`.

### What that leaves US, and it is a real correction

**`concepts/group.md:42` is now FALSE.** It says the aliases *"carry no
structural difference: they are directional heuristics for the reader and for a
generator's choice of representation."* That was true when written and is not
true now — three checks exist.

The replacement is not simply "they are checked", because the verb map is
**deliberately partial**, and riddl's reasoning is worth carrying:

- `presents` and `emits` are broad by meaning — a system may present through
  any channel — so mapping them would invent a rule the language never stated.
  **Silent, always.**
- `diffuses`, `serve`, `offer`, `taste` imply scent and taste, and **there is
  no scent or taste output kind at all**. Four verbs with no modality to
  contradict. Silent, and pinned by a test so nobody "completes" the map.
- `plays` maps to sound **and** animation, because both play.
- Mapped: `shows`/`displays`/`writes` visual · `plays` sound+animation ·
  `speaks`/`announces` speech · `vibrates`/`pulses`/`nudges` haptic.

Case 3's scoping also needs stating: `app-group-unreachable` covers **`popup`
and `dialog` only**, because those names promise something that appears in
response to an action. A `page` or `window` is a destination and may be entered
by means the model does not describe. A nested group is reached through its
parent and is never reported.

Do this **with or after 1g**, since it needs rc.26 to demonstrate.

### Upstream, not ours

Item 46 in `../RIDDL-Tools-To-Do-List.md` should be **struck**, not left open:
riddl ruled case 2 will not be built. Reid's framing, worth keeping: *a warning
must name something the author could plausibly want to change* — a model that
deliberately delivers through three modalities has nothing to fix, and a
diagnostic there trains people to ignore diagnostics.

---

## 1h. Upgrade to staged `2.1.1-33-dd3c2d80` — the gate is RED at 3  ← START HERE

**The staged binary moved under us again**, the second time in three days.
`../bin/riddlc` is **`2.1.1-33-dd3c2d80`**; `build.sbt:32` still pins
`2.1.1-26-4d17b1ef`. Verified 2026-09-11 by running `../bin/riddlc version`.

**Nothing is wrong with the docs.** The tree was verified green at
**376 / 52 / 0** against `-26`, which is what the last commit claims and what
was true. These three are an **un-started upgrade**, not a regression.

Measured against `-33`: **373 validated / 52 skipped / 3 failed**, 8 messages,
one rule:

```
[error] [saga-step-no-tell]
SagaStep 'PlaceTheOrder' do-statements contain no 'tell command' to effect
state changes:
      step PlaceTheOrder is {
```

- `guides/authors/authoring-riddl.md:668` (in-context)
- `guides/authors/index.md:606` (in-context)
- `references/language-reference.md:2500` (in-context)

8 messages over 3 fences because each saga has several steps — a ratio close to
1 per step, so this is **per-fence content, not a prelude or wrapper problem**
(cf. the 160-over-92 case that was). Fix the fences.

**The rule changed severity deliberately.** riddl `950d14804` — *"A saga step
that tells nothing is an ERROR, not a completeness warning"*. So this is not a
bug to report upstream; the examples genuinely describe saga steps that effect
nothing. Each needs a `tell command` in its `do` block, which is also better
teaching: a saga step whose body only narrates is not a step.

Related riddl commits in the same window, worth reading before editing:
`534f67290` (the saga rulings and the framing error behind them),
`56ebcc52a` (`saga-no-timeout` warns without blocking codegen),
`1037313f6` (a handler may declare at most one of each special on-clause —
may affect `on quiescence`, which this repo documents as one-per-handler).

**Do the pin and the grammar together**, and regenerate the grammar **last**.
Verify it by hash against riddl at whatever commit gets pinned.

---

## 1i. WATCH — implied adaptor ports are RULED ABOLISHED, and we document them

**Found during the 2026-09-11 handoff**, by reading `../riddl/task/` rather
than our own. Not actionable yet; it is here so nobody deepens the affected
section or is blindsided when it flips.

**`concepts/adaptor.md` documents implied adaptor ports as the design.** The
"Ports are implied, and declaring one overrides that side" subsection, and the
whole `adaptor-implied-outlet-ambiguous` explanation, rest on A103 giving a
port-less adaptor one implied inlet and one implied outlet. Written 2026-09-09,
gated green, and **correct against the compiler today**.

**Reid ruled on 2026-09-10 to abolish them** — riddl `e5b26745a`, *"implied
adaptor ports ruled, then paused on feasibility"*. The ruling stands; the
implementation stopped **before any code changed**, so nothing in our docs is
wrong yet.

**Why it is paused, which is also why it may stay paused a while:**
`Inlet.type_` is a TypeRef to a NAMED type, and of 411 port-less adaptors in
riddl-models only 165 handle exactly one type while 190 handle two to five,
with no single name to point at. Only 1 of 355 has a derivable outlet — the
rest are prose stubs (`do` + `error`, no `tell`). Generating the ports would
mean the compiler authoring user-facing alternation types. It is a feasibility
objection, not a corpus-cost one.

The open question sits in `riddl/task/2026-09-10-abolish-implied-adaptor-ports.md`.

**Do NOT pre-emptively rewrite the section.** The compiler still behaves this
way, the fences gate against it, and rewriting now would document a language
that does not exist — the exact failure the `cp`-the-grammar ban exists to
prevent. When the change lands:

- the "Ports are implied" subsection of `concepts/adaptor.md` goes
- `adaptor-implied-outlet-ambiguous` may disappear with it, so check before
  citing it
- the example's adaptors already declare their ports explicitly, so the FENCES
  should survive; it is the prose that moves

**Also unverified and worth checking in the same pass:** riddl `1037313f6`
("a handler may declare at most one of each SPECIAL on-clause") may or may not
bear on the one-`on quiescence`-per-handler rule we document in
`concepts/onclause.md` and the language reference.

---

## 2b. Retire `next`, `2.0` and `1.31` from gh-pages — manual, after the deploy

**Reid's decision, 2026-09-09:** RIDDL doc versions are **evolving lines**.
`2.x` is the live line and holds `latest`; `1.x` is maintenance. **`next` is
gone for good** — an evolving line has no use for an "unreleased preview",
because 2.x already is where unreleased work lands. A `3.x` line appears when
3.0.0 ships and becomes the evolving line then.

`docs-version.yml`, `VERSION_SOURCE` and the 404 handler are all updated and
committed. **What is left cannot be done by CI**, because mike only adds and
updates what the manifest declares and never removes what it stops declaring.

Three directories therefore keep serving until deleted by hand: `next` (an
alias, currently byte-identical to 2.0), and the retired `2.0` and `1.31`
version directories.

```bash
git fetch origin
git branch -f gh-pages "$(git rev-parse origin/gh-pages)"   # mike refuses if stale
mike delete --push --deploy-prefix riddl -F sites/riddl/mkdocs.yml next 2.0 1.31
```

`-F` is required: mike reads `mkdocs.yml` from the working directory to resolve
the branch, and there is no config at the repo root.

**The precondition is MET — verified 2026-09-11.** The deploy landed (run
`34377519216`, success, 57s). `gh-pages:riddl/versions.json` lists `2.x
[latest]`, `2.0 [next]`, `1.31` and `1.x`; `/riddl/index.html` redirects to
`latest/`; `latest` and `2.x` are byte-identical (`b67f1211…`); and `2.x`
carries the new A103 content while `2.0` does not (5 hits vs 0 for "The Adaptor
Is the Boundary"). **So this is runnable now, and has NOT been run** — all
three retired directories are still on `gh-pages`.

Until it runs the version selector offers **four** entries, which is the only
visible symptom.

The ordering rule that gated it is now satisfied, but keep it recorded: running
before the deploy would have deleted `2.0` while nothing had published `2.x`,
leaving the RIDDL docs with no live version at all.

**The stale `gh-pages` worktree that would have blocked `git branch -f` was
pruned on 2026-09-10.** `git worktree list` shows only the main tree; the
branch itself is intact at `417bd6a`.

**The URLs still in the wild are already handled.** `scripts/gh-pages-404.html`
maps `2.0`→`2.x`, `1.31`→`1.x` and `next`→`latest`, preserving the rest of the
path, so deleting the directories is what *activates* those redirects rather
than breaking anything. That is why deletion is right and leaving them is not:
a surviving `/riddl/2.0/` serves frozen content forever and never 404s, so the
handler never fires.

Verify from `gh-pages`, not a fresh curl of the live site — the CDN serves
stale for up to ten minutes and has produced three false alarms here:

```bash
git fetch origin gh-pages
git show origin/gh-pages:riddl/versions.json     # expect 2.x [latest] and 1.x only
git ls-tree origin/gh-pages riddl/ --name-only   # expect no next/2.0/1.31
node scripts/test-404-redirects.js               # 39 cases
```

---

## 2c. Keep the docs current with riddl 2.1.x — it is moving fast

**Not a defect; a standing condition.** riddl shipped 2.0.0 (2026-08-27),
2.1.0 (09-01) and 2.1.1 (09-04), and the work the docs now describe is **26
commits past 2.1.1** and in no release. Gating the tree against the staged
build on 2026-09-09 opened at **92 failures** against 0 the same morning on
2.0.0 — that is the delta over six weeks, and it will keep coming.

**What that means practically:**

- `build.sbt` pins a `git describe` version, not a tag, and will keep having to.
- The gate compiler is `../bin/riddlc` again. It has flipped three times; see
  the table in CLAUDE.md and **measure, never remember**.
- `python3 scripts/check-lexer-keywords.py` after every upgrade.
- Verify the grammar by hash against riddl at the pinned commit.

**When 2.1.x is released and Homebrew catches up, the authority flips back to
PATH.** That is the moment to re-read the CLAUDE.md table rather than assume.

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

The pin and the GATE COMPILER must name the same version, or the docs describe
a grammar the validated examples were never checked against. Since 2.0.0
shipped that compiler is the **`riddlc` on PATH** (Homebrew, `2.0.0`), NOT
`../bin/riddlc` — the staged binary is a post-release build and runs ahead of
the tag (`2.0.0-9-e895537f` on 2026-08-31). Bumping the pin may require bumping
`With.Scala3` to whatever riddl built with.

**Never `cp` it from `../riddl`.** That is a live working tree. Verified
2026-08-08: it held an uncommitted `yields`/`replies` split that exists in no
commit and no build, so a copy would have documented a language that does not
exist, and looked successful. See CLAUDE.md § "Things that will bite".

The file is generated wholesale, so partial syncs are not an option — expect
unrelated rules to come along.

**When:** Any time the gate compiler moves. Compare `riddlc version` against
the pin in `build.sbt` at session start, and check `../bin/riddlc version` too
— they are different builds and the staged one moves independently.

---

## 3b. The 1.31 gate has no compiler — `sites/riddl-1x/` is ungated

**Found 2026-08-31**, while verifying the 2.0.0 upgrade had not disturbed the
1.x tree. It had not; the gate simply cannot run any more.

Homebrew upgraded the `riddlc` formula to **2.0.0** and removed the 1.31.0
keg, so `/opt/homebrew/Cellar/riddlc/1.31.0/bin/riddlc` — the path CLAUDE.md
and this file both name — does not exist:

```
$ brew list --versions | grep riddl
riddlc 2.0.0
riddlc-rc 2.0.0-rc.5      # the stale RC formula; NOT a 1.x build either
```

`python3 scripts/validate-riddl-examples.py /opt/homebrew/.../1.31.0/bin/riddlc …`
now dies with `FileNotFoundError`, which at least fails loudly rather than
silently passing.

**Do NOT point it at a 2.0 binary.** 2.0 rejects constructs that are correct
1.x (the entity options, `one of`-only alternations, `state S of R` shapes),
so the run would report a pile of failures that are not defects in the 1.31
docs — the classic "confident nonsense from the wrong pairing".

**Options, in order of preference:**

1. Get a 1.31.0 binary back — a versioned Homebrew formula, a tarball from the
   riddl `1.31.0` release, or a local `sbt riddlc/stage` from that tag.
2. Pin the path in a variable so there is one place to fix.
3. Accept that the 1.x line is frozen and gate it only before a 1.x edit,
   recording that decision here.

**Why it matters:** `latest` still points at 1.31, so this is the tree most
readers currently land on. Its content is unchanged and was green when last
gated — the exposure is that nothing would catch a *future* edit to it.

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
