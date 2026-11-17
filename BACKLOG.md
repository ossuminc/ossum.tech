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
# 2. then -- `--server`, or sbtn attaches to IntelliJ's sbt shell and hangs
sbt --server -batch extractGrammar
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

---

## 6. The language reference teaches `tell event … to entity`

Filed 2026-11-11 during the 2.6.0 upgrade. Three fences tell an **event** to an
entity, which riddl 2.5.0's release notes name as the usual cause of
`msg-tell-no-route-for-type` (an entity's inlets normally admit commands):

- `sites/riddl/docs/references/language-reference.md:1887`, the **first**
  `tell` example on the page, under "Tell Statement"
- the same file, lines 2551 and 2554 (`OrderPending`, `OrderShipped`)

**Verified:** they pass the gate on 2.6.0 only because the wrapper's target
declares no inlets, which is one of the rule's exemptions. The gate cannot see
the problem. The example is legal; the thing it shows readers is not.

**Wanted:** tell a command, or say why an event is right there and show the
inlet that admits it. Line numbers move; grep for `tell event`.


## 7. Language-docs audit against riddl 2.7.0 (task 2026-11-17)

Derived 2026-11-17 from riddl's own artifacts at tag `2.7.0`: the grammar
diffed release by release from 2.0.0, the 56 rule ids added to
`rule-ids.txt` since 2.0.0, every deprecation emitter in `*/src/main`, the
CM log since 2026-08-27, and the 2.7.0 release notes. Not derived from this
repo's own "documented" claims.

**Already done:** pin `2.7.0`; grammar regenerated with
`sbt --server -batch extractGrammar`, `cmp` identical to tag 2.7.0.

**Baseline gate on `../bin/riddlc` 2.7.0 (whole tree): 387 / 52 / 3 failed.**
All three failures are `[value-initiate-keyword]`: `concepts/value.md:311`,
`references/language-reference.md:1895` and `:2453`. Nothing else in the
fence corpus regressed. So everything below is PROSE or skipped fences,
which the gate cannot see.

Lexer check: clean, `create` was already a keyword.

### Stale — teaches something wrong

- **S1. `initiate` taught as current** (2.7.0). 17 lines outside the grammar:
  `concepts/value.md`, `concepts/onclause.md`,
  `references/language-reference.md`, `references/cheat-sheet.md`,
  `introduction/what-is-riddl-based-on.md`.
- **S2. Both deprecation tables recommend a deprecated spelling.**
  `language-reference.md` § Deprecated Constructs and
  `migration/1.x-to-2.0.md` § 2 say shape keywords → `processor <id> as
  <shape>`. `processor` itself is deprecated (`stream-processor-keyword`,
  2.1.0); the answer is `streamlet <id> as <shape>`. Same advice at
  `language-reference.md:306` and `concepts/streamlet.md:72`.
- **S3. WITHDRAWN (Reid, 2026-11-17).** "Slated for removal in 3.0" is
  CORRECT: a deprecated spelling lasts until the next major release, not
  forever. riddl's `CLAUDE.md` rule 3 ("deprecation is FOREVER from 3.0
  onward") is what is wrong, and the grammar/RuleId comments that repeat it
  ("keeps parsing forever", "goes on parsing indefinitely"). Reported to
  riddl as R4. Keep "removed in 3.0" wording when rewriting the tables (S4).
- **S4. Both deprecation tables are incomplete.** RuleId has 18 deprecation
  emitters. Missing from the language-reference table: `processor` →
  `streamlet`, `initiate` → `create`, `reference to entity X` →
  `Id(entity X)`, entity options → intentions, connector
  `option persistent`/`at-least-once`/`at-most-once`/`exactly-once` →
  intentions, `type X is command { … }` → `command X is { … }`, quoted
  numeric constant `"5"` → `5`, single-alternative `one of { A }`,
  `option is package` → `namespace`. The migration table lacks most of the
  same. Each row should name its rule id and whether `--fix` handles it.
- **S5. The RBBQ tutorial teaches `option is external`** as the current
  form (`opt-deprecated` since 2.0.0) in 6 places:
  `tutorials/rbbq/external-contexts.md:10,13,37`,
  `tutorials/rbbq/patterns.md:335,390`,
  `tutorials/rbbq/backoffice/index.md:86`. Its own fences already write
  `external context`, so prose contradicts the code beside it.
- **S6. `cheat-sheet.md:405`** gives streamlet syntax as
  `processor OrderEnricher as flow is { ... }`.
- **S7. = BACKLOG 6** (`tell event … to entity`, 2.5.0 routing).

### Missing — the language has it, the site does not

- **M1. `create`** (2.7.0): the value, `create entity Order(…)` yielding
  the new instance's `Id`, and that it runs `on init`. Language reference
  § values, `concepts/value.md`, cheat-sheet.
- **M2. Streamlet references** (2.7.0): `streamlet_ref` keyword set is
  `source | sink | merge | split | void | flow | router | streamlet`
  (+ deprecated `processor`); and the one exception: in an epic step's
  `send … from`, `flow X` is a GROUP (`flow_group_ref`) — write
  `streamlet X`. Nowhere on the site. Also re-read
  `language-reference.md:1900` ("every processor reference is keyword-led")
  in that light.
- **M3. A transmission before a refusal is delivered** (CM §0.3 ruling 3,
  2026-11-16): the refusal does not recall a prior `send`/`tell`/`yield`/
  `put`. Add to the "Refusals before effects" boxes (`cheat-sheet.md:787`,
  language reference) and `guides/authors/authoring-riddl.md:564`.
- **M4. Creation runs `on init`, never `on activate`** (CM §4.5/§13.7,
  2026-11-16). `language-reference.md:1059`, `concepts/onclause.md:41`.
- **M5. Both legs of an `ask` must be wired** (CM §40.7, 2026-09-10;
  `msg-ask-target-unreachable` Error, `msg-ask-reply-unreachable`, 2.2.0).
  Language reference § Ask says nothing about connectors. Probe severity of
  the reply-leg rule before writing it.
- **M6. Journal-shape diagnostics** (CM 2026-09-12, 2.2.0):
  `entity-event-sourced-unread-history`,
  `entity-crud-with-transitions-consumed`,
  `entity-event-sourced-snapshot-events`. When event sourcing buys nothing,
  and when a CRUD entity's history is being consumed. Event-sourcing
  section of the language reference / `concepts/entity.md`. Probe severity.
- **M7. Two authoring lints** (CM B6/B8, 2.3.0): `stmt-yield-argument-prompt`
  (Advisory — a yielded field is usually a value the handler already has)
  and `stmt-do-validates-a-range` (a `do` that validates a range in prose
  should be a range/enumeration/pattern TYPE). § yield and § do.
- **M8. `riddlc find`/`dump` select values** (2.7.0): `-type create`,
  `-type ask`, …; `tools/riddlc/command-reference.md:371` says definitions
  only.
- **M9. BAST revision 31** (2.7.0): `.bast` from 2.6.0 or earlier must be
  re-`bastify`'d. `command-reference.md` § bastify. Low.

### Deliberately deferred (proposed)

- **D1. Rule ids for behaviour already described.** The 2.3.0 repository
  Errors (`repo-*`, `stmt-store-*`, `stmt-update-*`, `stmt-upsert-needs-key`,
  `value-query-outside-repository`, `value-not-a-collection`,
  `value-membership-type-mismatch`) and 2.2.0
  `handler-duplicate-special-clause`: the RULES are in the prose; only the
  ids are absent. The site has never promised an id per rule.
- **D2. → now M10 (Reid, 2026-11-17: not deferred).**

- **M10. Rule ids for ten existing diagnostics** (2.7.0): add ONLY the id
  where the site already describes the diagnostic — `entity-empty-handlers`,
  `entity-fsm-too-few-states`, `entity-state-no-handlers`,
  `entity-no-handlers-or-states`, `field-method-should-be-lowercase`,
  `field-method-arg-should-be-lowercase`, `type-pattern-invalid-regex`,
  `saga-step-uncompensated`, `saga-step-too-many-fail-points`, and
  `field-should-be-lowercase` (which the field-name check now reports).
  Text and severity are unchanged per the release notes.

### Verified covered (no action)

Generic `streamlet` keyword; `on quiescence`; `send … at`; `append`/`remove`;
`log`; `store`/`upsert`/`update`/`delete`; `query [one]`; arithmetic and
result types; duration literals; collection predicates, `count of`,
`contains`; constant expressions; `key on`/`with history`; typed `empty`
(2.4.0); typed `tell` routing and duplicate-send (2.5.0); fold determinism
(2.6.0); `Id(entity …)`; adaptor targeting/ports; `stream-graph-cycle`;
`on other` as `case _`. Spot-checked by grep plus the gate, not re-read
line by line.

### Reported to riddl (`riddl/task/`)

- **R1.** `type-reference-to-is-id` and `opt-deprecated` are emitted as
  deprecations but lack `deprecates = true`, so `RuleId.deprecations`
  omits them — the exact failure mode `RuleId`'s doc comment says the enum
  exists to prevent.
- **R2.** `type-reference-to-is-id` is emitted `autoFixable = true`, but
  `riddlc validate --fix` reports it "no mechanical fix". Probed on 2.7.0.
- **R3.** `StreamingParser.scala:195` comment still names
  `processor <id> as <shape>` as the replacement.
- **R4. The never-delete rule is wrong (Reid, 2026-11-17).** A deprecated
  spelling lasts until the NEXT MAJOR release. riddl `CLAUDE.md` rule 3,
  `BACKLOG.md:128`, the grammar comments (`ebnf-grammar.ebnf:167,635`) and
  `RuleId.scala:207,213` / `StreamingParser.scala:269` say "forever". The
  diagnostics that say "removed in 3.0" (`send-to-inlet`) are the RIGHT ones;
  `state-is-record`'s "a future major version" should say 3.0 too.
