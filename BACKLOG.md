# BACKLOG

The single place for open work on ossum.tech. If it is not here, it is not
tracked. Completed items leave this file: what they taught goes to NOTEBOOK.md,
what is durably true goes to CLAUDE.md.

---

## 1. Annotate the remaining RIDDL fences outside `concepts/`

**What:** `sites/riddl/docs/concepts/` is now fully gated (56 validated, 76
skipped, 0 failed). `language-reference.md` is not: **3 fences fail** and are
pre-existing, unrelated to the concepts work.

**Verified 2026-08-08:** the 3 are `language-reference.md` at the fences on
lines 861 (`in-context`), 1549 and 2138 (both `standalone`). Baselined against
`git show HEAD:scripts/validate-riddl-examples.py` to confirm they predate the
new wrapper kinds — they are not a regression from that work.

**Also open:** `check-riddl-blocks.py` flags two items in
`tutorials/rbbq/restaurant/online-ordering.md` (`state ... of O` without a
record; a `prompt "` statement). Advisory, left alone as out of scope.

**Order:** Independent of everything else.

---

## 2. Promote RIDDL 2.0 to `latest` when it ships final

**What:** `latest` points at 1.31, which is correct while 2.0 is an RC.

**How:** `scripts/promote-2.0-to-latest.md`. Since TASK G it is **one commit** —
both RIDDL lines publish from `main`, so the old two-branches-one-alias landmine
is gone.

**The one rule left:** `mike set-default` runs once per entry, so the **last
`riddl` entry** in `docs-version.yml` decides where `/riddl/` redirects. Move
the entries, not just the alias.

**Blocked on:** RIDDL 2.0 final. Currently `2.0.0-rc.9-54`.

---

## 3. Re-sync the EBNF grammar whenever riddl's parser changes

**What:** `sites/riddl/docs/references/riddl-grammar.ebnf` is a **copy**. It
drifted twice in one day this session (invariant `requires` + block form, then
`invariant_test` as a boolean atom).

**The trap, verified:** `sbt extractGrammar` resolves the **published** riddl
library, which is 1.x. Running it would replace the 2.0 grammar with a 1.x one
and look like a successful sync. See the warning at the task in `build.sbt`.

**Do this instead:**
```bash
cp ../riddl/language/src/main/resources/riddl/grammar/ebnf-grammar.ebnf \
   sites/riddl/docs/references/riddl-grammar.ebnf
```
The file is generated wholesale, so partial syncs are not an option — expect
unrelated rules to come along.

**When:** Any time riddl reports a grammar change. Worth a diff at session
start while 2.0 is moving this fast.

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
