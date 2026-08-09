# Engineering Notebook: ossum.tech

## Incoming Tasks

**At session start**, check the `task/` directory for pending
work requests from other projects. Each `.md` file describes a
task (e.g., dependency upgrade). Treat unresolved tasks as to-do
items unless already completed (verifiable from this notebook,
CLAUDE.md, or git log). After completing a task, append results
to the task file and note completion in this notebook.

---

## HANDOFF — as of 2026-08-08

**State:** branch `main`, clean. Through `aa33647` is pushed; the rc.10-46
upgrade on top of it is committed and **not yet pushed**.

**Compiler: `../bin/riddlc` is `2.0.0-rc.10-46-286ef815`** — run `riddlc
version`, it is restaged often. `build.sbt`'s `With.Riddl.library` pin must
name the SAME version, or the docs describe a grammar the examples were never
checked against.

**Refresh the grammar ONLY with `sbt extractGrammar`,** after bumping that pin.
**Never `cp` it from `../riddl`** — that is a live working tree, and on
2026-08-08 it held an uncommitted `yields`/`replies` split present in no commit
and no build. A copy would have documented a language that does not exist and
looked successful. CLAUDE.md § "Things that will bite" has the recipe.

**`task/` is empty.** Everything is in `task/done/`.

**Nothing is in flight.** Open work is in `BACKLOG.md`.

### What is now true

`concepts/`, `quickstart.md` and `references/language-reference.md` are **fully
gated** — 84 fences validated, 128 skipped, 0 failed, exit 0, against rc.10-46.

**rc.10-46 split `yield` and `reply`:** a command `yields`/`yield`s an EVENT, a
query `replies`/`reply`s a RESULT, `yield result` is an Error, and `reply` is
un-deprecated. `ask` is new — a VALUE (`let a = ask query Q of entity E`), not a
statement. Every doc that mentioned `reply` asserted the opposite of the truth
and was corrected; `check-riddl-blocks.py`'s rule did too. **If a doc rule and
the compiler disagree after an upgrade, suspect the rule.**
Re-run with:

```bash
python3 scripts/validate-riddl-examples.py ../bin/riddlc \
  sites/riddl/docs/concepts/*.md sites/riddl/docs/quickstart.md \
  sites/riddl/docs/references/language-reference.md
```

The 1.31 line is unaffected and still green under its own 1.31 compiler.
Remaining ungated trees — `tutorials/rbbq/` chief among them — are in BACKLOG 1.

**Baseline before blaming a wrapper change for a failure.** One command settles
whether a failure is yours or pre-existing:

```bash
git show <rev>:scripts/validate-riddl-examples.py > /tmp/base.py
python3 /tmp/base.py ../bin/riddlc <file.md>
```

### Traps this session paid for

- **A recorded warning can be stale; check its premise before obeying it.**
  Three places here said `sbt extractGrammar` resolves a *published 1.x*
  library and would clobber the 2.0 grammar. True when the pin was 1.29.0, and
  false for a long time since — `build.sbt`'s own comment said so. Acting on
  the note instead of reading the build produced a `cp` that was correct only
  by luck of timing. Same shape as the rc.9 lesson below about a failed
  compile: the note tells you what someone once found, not what is true now.
- **`--auto` reports the LAST wrapping it tried, not the relevant one.** All 15
  initial failures showed an identical `interactions` error, which looked like
  one systemic bug and was an artifact. It is a *measurement* mode; diagnose
  fences one at a time.
- **A green fence can mean nothing was checked.** `use-case.md:85` passed while
  referring to five definitions that did not exist — riddlc does not resolve
  references inside `sequence`/`parallel`/`optional`. Filed with riddl.
- **`check-riddl-blocks.py` is much weaker than it looks.** It reported all 129
  concept fences clean while two carried retired 1.x `then`-chains. Only
  compiling finds this class of error; do not read its "clean" as coverage.
- **A shared wrapper is load-bearing.** Injecting the ordinary prelude at domain
  level broke 4 fences in `language-reference.md`. Wrapper vocabulary may be
  ADDED but never renamed, and a change must be re-baselined against every page
  that uses that kind, not just the page in hand.
- **`[severe] empty(1:1->1)` means an exception was thrown in a pass**, not a
  language error — `Pass.scala` catches NonFatal and emits the stack trace,
  which can render empty. Bisect the model; do not read the message.
- **A markdown line swallows the rest of its line, including `}`.**
  `term SKU is { | text }` on ONE line consumes the closing brace as
  description text and unbalances the model. Put the `}` on its own line. The
  parse error lands at the END of the file, nowhere near the cause.
- **Do not trust an exit code read through a pipeline.** `riddlc ... | head;
  echo $?` reports `head`'s status. It made a failing compile look like a silent
  pass, and the wrong claim reached Reid before being corrected.

### Filed with riddl, and FIXED in rc.10

Both task files are closed by riddl commits `7c8c83ca0` (paths may descend into
a Function) and `acc11b274` (steps inside sequence/parallel/optional are
resolved and validated), plus `a466dab16`, which stops the in-pass exception
handler emitting an empty `[severe]`.

**The second fix had fallout here, as expected:** `use-case.md`'s grouped steps
referenced five definitions that did not exist and had been passing silently.
Anything else that leaned on grouped steps going unchecked will surface the
same way.

**Run `/ossuminc-skills:check-tasks` in the new session.**

The sections below are kept as the record of how the current state was reached.

---

### Invariant semantics and the `initial` handler ✅ **2026-08-04**

Task `2026-08-04-invariant-semantics-and-initial-handler.md` from riddl: RIDDL
2.0 invariants now apply **implicitly** across their declaring scope as a
precondition, rather than doing nothing until a clause writes `require invariant
X`. Six pages changed; details and the full verification log are in
`task/done/`.

Three things worth keeping:

- **The task file's own claims were the least reliable input.** It said the
  grammar had not landed (it had, one minute after the file was written — the
  sender later appended a correction); that `initial handler` was undocumented
  (it was documented, and the entity-level half was *wrong*, which is worse than
  a gap because it read as authoritative); and that the EBNF page needed no
  manual edit (it did — `sbt extractGrammar` resolves the **published** riddl
  library, so running it would have replaced the 2.0 grammar with a 1.x one).
- **Compile every example before writing prose around it.** Arithmetic in a
  block `let` (`balance - holdAmount`) is a parse error, and it came straight
  from the settled semantics — so "the computational model says so" is not
  evidence that the compiler accepts it.
  Two forms we *also* wrote up as errors were not: `when not invariant X`
  (spelling, see below) and `requires type T`, which is **valid** —
  `aggregate_use_case` includes `"type"`, and we misread
  `type_ref = [aggregate_use_case] path_identifier` as excluding the keyword.
  riddl corrected us. Both spellings work; the docs use the bare one.
- **A failed compile proves the spelling wrong, not the feature missing.**
  `when not invariant X` is a parse error, and we first wrote it up — in the
  docs *and* in a riddl task — as "invariants cannot be named in conditions,
  A17 unimplemented". Reid asked whether we were reporting real faults or
  misunderstandings. We were not: the **bare** `when not X` works, resolves to
  the invariant, and composes with `and`/`or`. Proof it resolves rather than
  being waved through: delete the invariant's declaration and the same line
  becomes an error. The real defect is a one-word inconsistency with `require
  invariant X` plus a diagnostic that points past the cause. **The negative
  test — does this fail for the reason I think? — was the one we skipped**,
  and it is cheap: try the other spellings before concluding the capability is
  absent.
- **The compiler is the authority over the model document where they differ**,
  and where they differ *is itself the finding* — both riddl follow-ups above
  came out of this gap, not out of the docs.

**Round trip completed the same evening.** riddl took all three files, fixed
both bugs, and shipped `2.0.0-rc.9-54-64b7b413`:

- `invariant X` and `invariant X with <expr>` are now boolean atoms
  (`InvariantCondition`), so **both** spellings work in conditions, and a
  condition never needs the argument. Reid's ruling dissolved our design
  question rather than picking one of its three options: a condition *asks*
  whether a rule holds, a `require` *applies* it and so must be handed what the
  rule reads.
- The `entity.states.sizeIs <= 1` guard is gone.
- Our report shook out **two latent bugs neither side was looking for**: BAST
  round-tripping of `require invariant X` was corrupting the stream (tag
  mismatch between writer and reader), and `defaultEntityInitials` counted
  states without seeing through `include` while validation did — so riddlc
  auto-marked a handler `initial` and then reported the *author's* handler as
  the duplicate. The old guard had been masking the second one, which is the
  strongest argument for removing it.

So three "not supported yet" notes we shipped in the afternoon were stale by
evening and are gone. **That is the standing hazard while 2.0 is an RC** —
see the HANDOFF section.

---

### Task-queue triage ✅ **2026-08-03**

Reid's point — *if it needs a change in riddl, drop a task there or it will
never happen* — turned out to apply to the tracking itself. All three files in
`task/` were reconciled:

- **`publish-riddl-license-page.md`** — needed **no** riddl task. riddl had
  already changed all three places in `733573373` (2026-07-30), the same day
  our "still outstanding" note was written. The note was stale from the moment
  it was filed and sat on the open list for four days because nobody re-checked
  the other repo. Verified end to end: `riddlc info` prints
  `/riddl/2.0/licenses/`, which returns 200.
  riddl's reason is better than ours, and worth keeping: notices describe the
  dependencies of **that** release, so a `/latest/` page would show a 2.0 user
  the notices of a future build. Version-pinning is right on its merits.
- **`activate-verb-now-parses.md`** — already done; `element.md` documents both
  spellings and carries no caveat.
- **`add-silent-breaking-changes-to-2.0-migration-guide.md`** — **genuinely
  outstanding**, and the one that would have been lost. Now done: the migration
  guide has a "Silent changes for tools that read the AST" section covering the
  `OnEventClause`/`OnMessageClause` split and `AST` companion shadowing. Both
  claims were re-verified against `AST.scala` rather than trusted — the shared
  parent is `OnMessageLikeClause` (line 3707), which the guide names, because
  "match on the common parent" is only actionable if the parent is named.

**Lesson:** two of three were already done and one was quietly rotting. Check
`task/` against the *other repo's* current state, not against what the task file
says about it.

### TASK K — AST / Finder / Pass API documentation ✅ **DONE 2026-08-03**

New page: `guides/developers/ast-api.md`. Nothing existed — the developer guide
was index, principles and releasing, and the whole programmatic surface lived
only in scaladoc, despite riddl-generator, riddlg and both IDE plugins being
consumers of it.

Written from `AST.scala`, `Finder.scala` and `Pass.scala` on `release/2`.

**The API change it exists to capture:** all 35 accessor declarations now use
`filterThroughWrappers` and descend **both** `Include` and `BASTImport`.
Previously `context.entities` was empty whenever the entity was written in an
included file while `context.repositories` in the same context worked — the
same model answering differently depending only on which file the author typed
into. riddl-generator emitted 582 files for reactive-bbq with no entity class
among them and *everything reported success*. The page tells consumers to
delete any hand-rolled include walk, or count twice.

**Three claims that did not survive checking, and are why the page is worth
trusting:**

- riddl says "35 accessors" and so did my first draft — but there are **34
  names**. `repositories` is declared twice with *different return types*:
  `Seq[Repository]` on `WithRepositories`, `Seq[RepositoryRef]` on `Projector`.
  A tool treating the latter as definitions gets refs, and it type-checks.
- `PassesResult.symbols`/`resolution`/`validation` are `lazy val`s, not `def`s,
  so a `def` grep says they do not exist. They do.
- The developer guide still required Scala 3.3.x LTS and sbt 1.10+; riddl is on
  **3.9.0-RC4 and sbt 2.0.2**, and the experimental-TASTy constraint is why
  consumers must match exactly.

Also documented, because the scaladoc argues them and the reasoning is the
useful part: `span` is character offsets (a definition needs start AND end),
`declaringFile` survives `FlattenPass` and is the supported way to ask "which
file do I edit?", `isEmpty` is semantic and comment-tolerant, and passes
**traverse** wrappers while accessors **see through** them — opposite by design,
since a symbol table cares about provenance and a reader does not.

### TASK J — riddl rc.9 language changes ✅ **DONE 2026-08-02**

Upgraded to **2.0.0-rc.9-12-0054a843** (`~/.ivy2/local`; Scala unchanged at
3.9.0-RC4) and regenerated the grammar. 35 riddl commits since rc.5; six
changed what the docs must say.

**Keep `build.sbt` in step with `../bin/riddlc`.** The staged compiler is what
validates the fences; if the library version drifts from it, the grammar in the
docs and the compiler enforcing it describe different languages. The staged
binary moved twice during this work (rc.9-6 then rc.9-12) and the version here
was bumped both times.

**The one that mattered: entity intentions.** `event-sourced`, `persistent`
(was `value`), `transient`, `aggregate`, `consistent` and `available` are now
keywords **before** `entity`. The option spellings still parse but emit
`[deprecated]` — **and the fence validator gates on `[deprecated]`**, so all 16
occurrences across 7 files had started failing. This was not a cosmetic rename.

**`event-sourced` is now enforced by four Errors** (R1–R4): commands declare
`yields`; every event so named has an `on event` clause; `set`/`morph`/`become`
only inside `on event` (no `on init` exemption); a foreign event may not touch
state. Several examples claimed event sourcing while being structurally
impossible to event-source. Each was rewritten — commands and events moved
*inside* their entity, since only an entity's own events may change its state.
Two structural examples in `authoring-riddl.md` went the other way and dropped
`event-sourced`, because forcing the four rules into a section about entity
*structure* would teach the wrong lesson.

Also documented: infix alternation `A | B` (identical to `one of { … }`;
prettify emits the words — and **predefined types are not valid alternatives**,
which the compiler caught in the first draft of the example), `option is
error-sink` with its three rules, adaptor uniqueness per direction, saga
`retry`/`undo-retry`/`failure-message`, and non-positive durations now being an
Error. The migration guide gained an entity-intentions section, since it is the
page a 1.x reader will look at.

**Late addition in rc.9-12: refusing a command discharges its `yields`.**
`checkYieldConformance` had required *every* `on command C` clause to yield C's
declared event, with no exemption for one that refuses it — which combined with
R1 made the most ordinary event-sourcing shape inexpressible: a command accepted
in one state and refused in the others, where each refusing clause was required
to record the state change it had just declined. Both `error` and `require`
count as refusals; yielding the *wrong* event is still an error. Documented
under Event Sourcing Rules. No grammar change — the regenerated EBNF was
byte-identical, which is the check that confirmed it.

**Compiler to use:** `../bin/riddlc` is 2.0 (rc.9). The Homebrew `riddlc` on
PATH is **rc.5** and does *not* report the deprecation, so validating the 2.0
docs with it silently passes examples the real compiler rejects. CLAUDE.md now
says so in both places it names a compiler.

**Site-wide: 144 fences validated, 26 failing, no file above three** — down from
28 before the upgrade, so the language change regressed nothing.

**IDE docs** corrected against the shipped plugins: IntelliJ needs **2025.3+**
(since-build 253) and **JDK 21+**, not the 2024.1/JDK 25 we claimed, and the
Community/Ultimate distinction is gone from 2025.3. VS Code gained Document
Outline, Breadcrumbs, Go to Symbol and handler-completeness diagnostics.

### TASK I — consent and theme asked once per VERSION ✅ **DONE 2026-08-01**

Reid noticed the cookie prompt returning every time he selected the RIDDL 2.0
`next` version. Cause: Material keys `localStorage` by the MkDocs project's base
URL —

```js
__md_scope = new URL("{{ base_url }}", location)
__md_get = k => JSON.parse(localStorage.getItem(__md_scope.pathname + "." + k))
```

— and under mike every version of every product is its own project, so the base
URL is the **version directory**. Accepting on `/riddl/latest/` wrote
`/riddl/latest/.__consent`; `/riddl/2.0/` looked for `/riddl/2.0/.__consent`,
found nothing, and asked again. One site, **up to six consents**.

The same scoping reset the light/dark choice — `__palette` is keyed identically,
which is why the theme sometimes flipped when changing product or version.

**Fixed** by reassigning `__md_scope` to `/` in `overrides/main.html`.

**The placement is the whole trick.** It must land after Material defines the
scope and before the first thing that reads it — the analytics gate,
`__md_get("__consent")`, which base.html emits in `{% block analytics %}`,
between the definition and `extrahead`. Putting it in `extrahead`, where the
rest of our head additions live, is **too late**: the gate would keep reading
the old key and analytics would never enable. Confirmed by byte offsets in the
built HTML:

```
__md_scope defined   11059
our reassignment     11369   <- inside {% block analytics %}
gate reads __consent 12594
extrahead            12997   <- would have been too late
```

`{{ super() }}` renders the stock block instead of a copy, so no Material
partial is named and nothing pins us to a release.

**Verified in a browser**, from cleared storage: prompt appears once, accepting
writes `/.__consent`, then `/riddl/2.0/` and `/` show no prompt; a dark theme
chosen on 2.0 carries to the landing page; `typeof __md_analytics !==
"undefined"` stays true, proving the gate still works. Storage drops from up to
twelve keys to two.

One-time cost: old per-version keys are orphaned, so everyone is asked once
more and pre-existing theme choices reset once. Unavoidable for any fix.

### TASK H — logo linked to the sub-site, not the site ✅ **DONE 2026-07-31**

Material links the logo to `nav.homepage.url`, the root of the MkDocs *project*
being built — so on `/riddl/latest/concepts/entity/` it rendered as
`href="../.."` and went to `/riddl/latest/`. With four projects under one
domain, a reader inside a product had no way back to the landing page except
the back button.

Fixed with `extra.homepage: /` in `sites/common.yml`. Points worth keeping:

- **Both** logo anchors read it — the header one and the drawer one in
  `partials/nav.html` — so no template copy is needed and the repo stays
  unpinned from a Material release. (Contrast the header and search partials,
  which have no such hook and are therefore handled by script.)
- Root-relative `/`, not `https://ossum.tech/`, so it is also right under
  `preview-versioned-site.sh`. Material passes the value through MkDocs' `url`
  filter, which leaves a root-relative path alone.
- It went in `common.yml`, so all five sites got it at once — TASK G paying off
  the same day.

### TASK G — fold `docs/1.x` into `main` as a directory ✅ **DONE 2026-07-31**

Deployed and verified live: `/riddl/1.31/` serves 1.x content with the new
chrome, its edit links point at `main/sites/riddl-1x/`, `versions.json` still
reads `2.0 [next]` + `1.31 [latest]`, and `/riddl/` still redirects to `latest`.

Rehearsed with `preview-versioned-site.sh` before pushing, which is how the two
same-prefix entries were confirmed to coexist.

**What changed beyond moving files:**

- `check-cross-site-links.py` became **version-aware**. It mapped a URL prefix
  to one source directory; `riddl` now has two, so `/riddl/1.31/…` links were
  being checked against the 2.0 sources. `VERSION_SOURCE` maps each version and
  alias to the tree that builds it, and an unmapped version is now a dead link
  rather than a silent pass. Coverage went 65 → 80 links.
- The workflow publishes from `main` only. The `concurrency` group **stays** —
  two pushes to `main` in quick succession still race for `gh-pages`.
- `preview-versioned-site.sh` no longer checks out a branch mid-run.
- `promote-2.0-to-latest.md` rewritten: promotion is now one commit.

**The one ordering rule that replaced the landmine:** `mike set-default` runs
once per entry, so the **last `riddl` entry** in `docs-version.yml` decides
where `/riddl/` redirects. The 1.31 entry holding `latest` is last on purpose.

**Proof the consolidation works:** `sites/riddl-1x/docs/stylesheets/extra.css`
picked up the clickable-row rules from the shared copy with no action at all,
and TASK H then reached all five sites from a single line.

The original proposal follows, kept for the reasoning.

#### The case, as argued before doing it

**The problem, measured (2026-07-31).** `docs/1.x` has 17 commits since the
merge base. **Twelve of them are pure replication** — "Carry the header Full
Search field onto the 1.x line", "Match the Full Search strip colour on the 1.x
line", "Apply the navigation rework to the 1.x line", "Carry robots.txt
generation onto docs/1.x", and so on. Only about four are real 1.31 content
work.

That tax is not theoretical: the clickable-search-row change (TASK E) shipped to
`main` and silently did **not** reach `/riddl/latest/`, which is 1.31 and is
where most readers land. It was caught only by checking the deployed site, not
by any build or link check. Nothing in CI can catch it, because each branch
builds correctly *on its own terms*.

**Why a branch is not actually required.** mike versions the **output**
directory in `gh-pages`; it has no opinion about the source and simply takes
`-F <config>`. The branch exists only because both lines build the same config
*path*, `sites/riddl/mkdocs.yml`, and one checkout cannot hold two contents at
one path. A second directory solves that just as well.

**The shape.** Move the 1.x content to `sites/riddl-1x/` on `main`, with its own
`mkdocs.yml`, and add an entry to `docs-version.yml`:

```yaml
  - prefix: riddl
    config: sites/riddl-1x/mkdocs.yml
    version: "1.31"
    aliases: [latest]
```

**What it buys:**

- The "carry onto the 1.x line" class of commit stops existing.
- `overrides/` and `common/stylesheets/` are already `custom_dir` and shared
  assets for every site, so chrome changes reach 1.31 automatically. Today's
  divergence becomes structurally impossible rather than merely noticed.
- **The two-branches-one-alias landmine disappears.** One branch declaring both
  entries cannot race itself, and promoting 2.0 becomes a one-file edit instead
  of an ordered cross-branch sequence.

**Cost:** `main` carries ~5,000 more lines of maintenance-line docs, and a fifth
entry under `sites/`.

**Genuine divergence, for scope.** 178 files exist on both branches; **89 differ**
(~5,000 lines). That is the RIDDL documentation itself — 1.31 and 2.0 are
different languages (`reply` vs `yield`, no `initial state`, and the rest). None
of that can be shared, and none of it needs to be: it just moves.

**Two things to get right, both already known traps:**

- `sites/riddl-1x/` must validate against the **1.31** compiler, not the 2.0 one
  on PATH — `/opt/homebrew/Cellar/riddlc/1.31.0/bin/riddlc`. `docs/1.x` already
  carries a commit fixing exactly this ("Stop telling this branch to validate
  with the wrong compiler"), and the RC formula has since taken over the PATH
  symlink.
- `scripts/check-cross-site-links.py` keys off tracked `mkdocs.yml` files to
  decide which sub-sites exist, so it needs to learn about the new one.

**Do not delete `docs/1.x` until the directory build is verified deployed.** It
is the only copy of the 1.31 content.

*(Done 2026-07-31, after the deploy was verified. The branch is gone, remote and
local. Its 18 commits are preserved by the annotated tag `archive/docs-1.x`,
which was pushed and confirmed to dereference to the branch tip BEFORE anything
was deleted. `git log archive/docs-1.x` still works, and so does
`git show archive/docs-1.x:<path>`.)*

**Do not restore that branch to publish from.** It carries its own copy of
`.github/workflows/publish.yaml`, which still lists `docs/1.x` as a trigger, so
a push would redeploy 1.31 with the pre-TASK-G chrome — and it would look like
an ordinary successful deploy while quietly undoing the consolidation. That
hazard is why the branch was retired rather than merely left alone.

### TASK F — build on sbt 2 / riddl 2.0.0-rc.5 ✅ **DONE 2026-07-31**

`build.sbt` was pinned at riddl **1.29.0**, which forced the 2.0 grammar to be
hand-copied out of riddl's `release/2`. Now on **sbt 2.0.2**, **sbt-ossuminc
3.1.0**, **riddl 2.0.0-rc.5**, and `sbt extractGrammar` works again — its first
run differed from the hand-copy by exactly one token (`activate`), which is the
evidence the extraction path is correct.

**Scala is 3.9.0-RC4 here, not the org-standard 3.8.4**, because that is what
riddl publishes 2.0.0-rc.5 with. An RC compiler emits *experimental* TASTy
(28.9-experimental-1), readable only by the exact compiler that produced it;
3.8.4 accepts 28.0–28.8 and failed to load every riddl class. The
`asTerm called on not-a-Term` crash that surfaced is dotty falling over after
those loads fail — **not** a source error, and a day-waster if read as one.
Keep the two versions in step when bumping riddl.

**This affects every riddl consumer**, and final 2.0.0 should not ship built on
an RC compiler — it would force all of them onto that exact RC. Not filed as a
riddl task (Reid's call, 2026-07-31); noted here so it is not rediscovered.

Two sbt 2 API breaks fixed in `extractGrammar`: `fullClasspathAsJars` yields
`HashedVirtualFileRef` (route through `fileConverter`), and sbt 2 caches task
results by hashing inputs, so a side-effecting task needs `Def.uncached`.
Its output path also still pointed at the pre-split `docs/riddl/references/`.

`release/2` in THIS repo was fully merged into `main` (0 commits ahead) and has
been **deleted**, locally and on the remote.

### TASK E — clickable search result rows ✅ **DONE 2026-07-31**

Delegated from the mount in `overrides/main.html`, not by restyling the anchor:
the excerpt is a *sibling* of `a.pagefind-ui__result-link`, so an anchor
stretched over the row would swallow the sub-results and their own links. The
listener is on the mount because Pagefind destroys and rebuilds the drawer on
every keystroke.

**Sub-results are tested before their parent** — they are nested inside it, so
checking `.pagefind-ui__result` first sends every sub-result to the top of the
page instead of its own anchor. That was the trap this task flagged in advance.

Three behaviours preserved on purpose: a click landing on a real anchor falls
through, a click that ends a text selection does not navigate, and cmd/ctrl-click
still opens a new tab.

**No row padding.** Pagefind writes its own as
`.pagefind-ui__result.svelte-XXXX.svelte-XXXX` — it repeats the hash to raise
specificity — and `pagefind-ui.css` loads from `extrahead`, i.e. *after*
`extra.css`. Beating it needs four classes including a build-specific hash, for
a cosmetic inset. Don't; the hover wash spans the row anyway. (The input-sizing
rules above it hit the same wall — this is a recurring trap, not a one-off.)

**Verifying this needs a browser** — no build check can see it. What worked:
build shell + riddl into a scratch tree (`-d <tmp>/riddl/latest`), run
`scripts/build-search-index.sh` over it, serve with `python3 -m http.server`.
`preview-versioned-site.sh` **clones the repo**, so it only ever sees *committed*
state — useless for checking work in progress. Two snags: `build-search-index.sh`
reports "no product contributed" because the scratch tree has no `versions.json`
(harmless), and Material's cookie-consent overlay intercepts clicks until
accepted.

---

### TASK A — concept `## Contains` diagrams ✅ **stage 2 done**

23 concept pages now carry a per-scope mermaid diagram plus a linked list. The
diagram gives the shape; the list stays because mermaid cannot carry links
without `click` directives, and losing them would make the pages harder to use.

Every entry was taken from `riddl-grammar.ebnf`, not from the prose it replaced
— those had drifted: `entity.md` omitted Constant, Connector, Relationship and
nested Processor; `saga.md` omitted Inlet, Outlet, Function and Include.

**Pages deliberately left as prose:** the 10 leaves that contain nothing, and
the ones whose "Contains" describes syntax rather than definitions
(`statement.md`, `value.md`, `option.md`, `metadata.md`, `description.md`,
`conditional.md`, `include.md`, `author.md`). `inlet.md`/`outlet.md` kept prose
too: the grammar has `inlet = "inlet" identifier is type_ref`, so a type is
**referenced**, not contained, and a diagram would assert something false.

**Both content problems resolved (2026-07-31, decided with Reid):**

- **`case.md` deleted**, `use-case.md` is the keeper. It was not merely a
  duplicate: its step table documented retired 1.x keywords (`publish`,
  `subscribe`, `arbitrary`, `provide`, `present`), none of which exist in the
  2.0 grammar. Old URLs redirect to `use-case`.
- **`element.md` kept** — "element" is **abstract**, a class name in the AST
  like *Node*, not a RIDDL keyword; Group, Input and Output are its concrete
  kinds. The page uses a mermaid `classDiagram` with an `<<abstract>>`
  stereotype, because the relation is *is-a* and a flowchart would have implied
  containment. Its `## Contains`
  now says so instead of claiming it holds Handlers. Its group-alias list was
  also wrong: it listed `row`, `stack`, `panel` and `form`, none of which are
  group aliases (`form` is an *input* alias).

**`element.md` fully corrected (2026-07-31).** Its "Element Types" table
invented four keywords that never existed — `Give`, `Select`, `View` and
`Activate` as *definitions*. It now documents the real input and output
aliases and their acquisition and presentation verbs, taken from the grammar.

Navigation is not a definition: it is an input whose verb conveys the action,
e.g. `button Checkout activates type Boolean`.

**Measured, not assumed:** against riddlc 2.0.0-rc.1, `activates` parses and
bare `activate` is **rejected** at the verb position. Reid asked for `activate`
to be allowed, so `riddl/task/add-activate-acquisition-verb.md` requests it and
the page carries a note saying only `activates` parses today. Remove that note
when riddl confirms.

---

### TASK B — RIDDL example fences ✅ **all three files at zero (2026-07-31)**

| File | Start | Now | Fences checked |
|---|---|---|---|
| `guides/authors/index.md` | 9 | **0** | 13 |
| `guides/authors/authoring-riddl.md` | 18 | **0** | 18 (was 15) |
| `guides/authors/design/ui-modeling.md` | 5 | **0** | 9 (was 7) |
| everything else | — | ≤3 | — |

**Site-wide: 142 fences validated, 28 failing, no file above 3.** Coverage rose
while the count fell — five fences that were `skip`ped to dodge harness
limitations are now genuinely under test.

**Two harness gaps fixed**, both of which had been papered over with `skip`:

- `no-prelude=<Name>` — a page prelude was injected into *every* fence, so a
  fence DEFINING one of those names collided with it. It now names what it
  owns and keeps the rest of the vocabulary. Selective on purpose: a bare
  `no-prelude` was tried first and traded one duplicate-name error for a pile
  of unresolved paths.
- `in-app-context` — groups/inputs/outputs are legal only in a context with the
  `application` intention. `in-context` gives a plain context (group = hard
  error) and `in-application`, despite the name, wraps in an *on-clause*.

**Two content faults worth remembering**, both cases of a page contradicting
itself:

- `authoring-riddl.md`'s Predefined Types table invented `Blob` and `Money`,
  kept the deprecated `Abstract`, misspelled `TimeStamp`, and listed `List`,
  `Set`, `Map`, `Sequence`, `Mapping` as type *names*. They are type
  **expressions** (`sequence of X`, `set of X`, `mapping from K to V`, `many X`).
  The fences using `List of X` were downstream of the table, so the table was
  corrected against the grammar rather than patched around.
- Both `ui-modeling.md` and `index.md` had epics running the user straight into
  domain contexts — the exact thing `ui-modeling.md` documents as an error 180
  lines further down. Both now route through an application context.

**Grammar facts that cost time** (all measured against riddlc 2.0.0-rc.5):

- `arbitrary_step` takes **one** literal string, *before* the target ref. Both
  pages supplied a second one after it.
- `put` takes a *value*; a bare message ref is not one, and neither is an
  integer literal — `put result R(f = R.f) to output O` is what validates.
- `option_name` is `/[a-z0-9_-]*/`: `option is finite state machine` must be
  `finite-state-machine`.
- A saga body admits only function/include/inlet/outlet/requires/returns/step
  — no `record`.
- Every state needs a handler, final states included (`handler H is { ??? }`).
- `in-domain` and `standalone` fences receive **no prelude** by design, so they
  must define what they use.

**Error classes swept site-wide earlier** (still zero outside the tutorial):
bare-string `when` conditions (use `when prompt("...")`), `if/then/else`,
`user X is { }`, `send ... to context X`, bare `option X` in a body, pre-2.0
trailing metadata, `state X is { fields }`.

**To see the exact failing line:** load `scripts/validate-riddl-examples.py` as
a module and reproduce `wrap()` with the fence's directive — reported positions
are into the *wrapped* source, not the markdown. Mirror the prelude logic too,
or the diagnosis will disagree with the validator.

**Two traps that cost time:**

- A fixer script that asserts *before* writing loses every earlier fix when a
  later assert fails. Write unconditionally, report misses.
- `re.subn` returns `(string, count)`. Getting them backwards writes an int and
  throws — silently discarding every edit in that script run.

---

### TASK D — navigation and content rework ✅ **DEPLOYED 2026-07-31**

Top menu carries RIDDL / riddlg / Synapify (root-relative, into each product's
`latest`) plus **IDE help** and About. The old "OSS" label is gone: the three
IDE-tool pages are now unversioned at `/ide-help/`, while `authoring-riddl.md`
stayed version-tracked and moved to the RIDDL author guides — it teaches the
language, not a tool. Coming Soon and `/find/` are deleted.

**Search is two fields, deliberately additive**, both in the header:

```
row 1   logo · title · version · [Material search] · repo
row 2   FULL SEARCH  [ cross-site input ]        <- purple band
row 3   tabs
```

Material's title-bar box still searches the current site *and version*; Full
Search queries Pagefind across all products. An earlier design replaced the
title-bar box, which would have cost version-scoped search; rejected.

Rendered into Material's `{% block hero %}` and then **moved into the header by
script**. It cannot be templated there: with `navigation.tabs.sticky` the tabs
are rendered inside `partials/header.html`, so no block exists between the title
row and the tabs, and reaching it would mean copying that partial and pinning
the repo to a Material release. If Material renames `.md-header`/`.md-tabs` the
move silently does not happen and the bar stays below the header — worse
looking, still working.

Two sizing gotchas: `pagefind-ui.css` loads from `extrahead`, i.e. **after**
`extra.css`, so at equal specificity Pagefind wins — the input needed an extra
selector level to shrink. And forcing the page text colour across the results
drawer also hit `mark`, giving light-on-yellow highlights in dark mode.

`extra.css` carries no content hash, so a returning visitor may see cached
styling until it expires. Pre-existing, not introduced here.

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

**Closed 2026-08-03:** `task/publish-riddl-license-page.md` is in `task/done/`.
The note that used to sit here said `riddlc info` still printed the unversioned
`/riddl/licenses/` and that riddl had to change three places. **riddl had
already changed all three** — commit `733573373`, 2026-07-30, the same day this
note was written. It was stale from the start and stayed on the open list for
four days because nobody re-checked the other repo.

Verified end to end: `riddlc info` prints `/riddl/2.0/licenses/`, and that URL
returns 200 with the notices. Bump the constant, its test and
`THIRD-PARTY-NOTICES.txt` together on each documented minor release.

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
