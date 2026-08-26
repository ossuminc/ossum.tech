# BACKLOG

The single place for open work on ossum.tech. If it is not here, it is not
tracked. Completed items leave this file: what they taught goes to NOTEBOOK.md,
what is durably true goes to CLAUDE.md.

---

## 1e-remnant. Alias-specific UI validations are unbuilt, by intent

**1e is otherwise DONE (2026-08-22).** Every feature it listed is now
documented on the site and gated against `../bin/riddlc`:

| Feature | Spec | Where |
|---|---|---|
| `Id(P)` over all six processor kinds, keyword form, truth-check | 71 | language-reference § Instance Identity; cheat-sheet types |
| `self` / `self.id` | 71 | language-reference § Instance Identity; `concepts/value.md` |
| `initiate` | 71 | same, plus both value-form tables |
| `terminate` | 71 | language-reference § Terminate Statement (2026-08-21) |
| Structural addressing and `tell … by` | 71 | language-reference § Tell → Addressing is structural |
| Message operand may name its VALUE | 72 | language-reference § Constructors |
| `set`/`get from state` need an OWNER | 75 | language-reference § Set Statement |
| Modality aliases | 43 | `concepts/group.md`, `element.md`, `input.md`, `output.md`, both references |
| Presentation verbs | 46 | `concepts/output.md`, `element.md`, cheat-sheet |
| Refusal citing an invariant | 38 | `concepts/interaction.md`; all three step tables |
| Ordering is an option, persistence an intention | 33 | `concepts/connector.md` |
| Connector scope and cross-context persistence | 34, 35 | `concepts/connector.md` (2026-08-21) |
| Correlations in projectors | 70 | documented 2026-08-13 |

**What remains is not documentation, and is now FILED UPSTREAM.** Items 43 and
46 both call for alias-specific validations that do not exist: that a `popup`
is reachable, that a `menu` contains selectable inputs, and noun/verb
consistency across a compound output's parts. Item 43 calls these "useful later
work"; item 46 wants them symmetric with item 44, whose input-side half IS
built.

Filed 2026-08-26 as
`riddl/task/2026-08-26-modality-aliases-parse-but-mean-nothing.md`, with the
three cases stated explicitly and a ready-made fixture — four deliberate
modality defects that riddlc validates with **zero errors, exit 0**, measured
against rc.25-1.

**Nothing here is blocked on it.** The docs describe the aliases as closed
lists carrying no structural difference, which is exactly what is true today;
when the checks land the docs need an addition, not a correction.

**Two spec notes in `../RIDDL-Tools-To-Do-List.md` are STALE and should be
corrected there.** Items 43 and 46 are marked *"NOT BUILT (verified
2026-08-14)"*. Re-verified against the **rc.20** grammar on 2026-08-22: every
alias is present — `group_aliases` carries `scene`/`space`/`zone`,
`output_aliases` carries `sound`/`speech`/`haptic`, `input_aliases` carries
`voice`/`gesture`/`gaze`, and `presentation_aliases` carries all ten verbs.
Item 43's own implementation note says SHIPPED `5072bad5b`, so the two halves
of that entry contradict each other. Trust the generated grammar.

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
