# BACKLOG

The single place for open work on ossum.tech. If it is not here, it is not
tracked. Completed items leave this file: what they taught goes to NOTEBOOK.md,
what is durably true goes to CLAUDE.md.

---

## 1g. Upgrade to riddl 2.0.0-rc.26 — the gate is RED at 6  ← START HERE

**The staged binary moved under us.** `../bin/riddlc` is now **2.0.0-rc.26**
while `build.sbt` still pins `2.0.0-rc.25-1-76cb9eab`. Nothing is wrong with
the docs — the last commit was verified green at 366/51/0 against rc.25-1.
**These six are an un-started upgrade, not a regression.**

Measured 2026-08-26 against the restaged binary: **360 validated / 51 skipped /
6 failed**. Three families, all from `5c377b9fd` *"[1.13] Type-check put,
return and require — and give literals a type"*:

**A. `put` now type-checks against the output's declared record (3 sites)**

```
'put' value is declared 'record { confirmationNumber: String }'
but the value is 'String'
```

- `concepts/output.md:59` · `concepts/statement.md:339` ·
  `references/language-reference.md:1949`

All three are `put order.confirmationNumber to output X`. The output is
declared `shows record ExampleOrder`, so `put` now wants the **record**, not a
field of it. Either pass the whole record, or declare an output that shows a
`String`. **Decide which the docs should teach before editing three pages** —
they are illustrating `put`, not record-vs-field.

**B. String literals no longer satisfy a `UUID` field (2 sites)**

```
Field 'cartId' of Command 'CreateOrder' is declared 'UUID'
but the value is 'String'
```

- `guides/authors/design/ui-modeling.md:220` · `guides/authors/index.md:200`

Same family already hit in the rc.24 migration, where the fix was to declare
the id alias as `String` because UUID-vs-String was not what the fence taught.
The same reasoning likely applies here; check what each page is demonstrating.

**C. A `when` condition must be Boolean (1 site)**

```
A 'when' condition must be a Boolean value; 'isValid' has type string
```

- `concepts/conditional.md:41`

Some `isValid` in scope is a String where the fence needs a Boolean. Check
whether it is the page prelude or the shared wrapper — the `in-handler`
wrapper's `ExampleData` does carry `isValid is Boolean`, so this is probably
page vocabulary shadowing it.

**Do the pin and the grammar together**, and regenerate the grammar **last** —
see the trap in CLAUDE.md, which this repo has already been bitten by once.

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
