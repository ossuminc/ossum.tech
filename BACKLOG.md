# BACKLOG

The single place for open work on ossum.tech. If it is not here, it is not
tracked. Completed items leave this file: what they taught goes to NOTEBOOK.md,
what is durably true goes to CLAUDE.md.

---

## 1. Annotate the concept pages with fence directives

**What:** The ~50 pages under `sites/riddl/docs/concepts/` carry no per-fence
`<!-- riddl: ... -->` directives, so `validate-riddl-examples.py` cannot gate
them. Under `--auto`, 26 fences fail site-wide against rc.9.

**Why it is not urgent:** No file is above three failures, which is the agreed
threshold, and the failures are dominated by fragments that reference
definitions the page deliberately does not show — those need a per-page
`<!-- riddl-prelude ... -->`, not a correction.

**Verified:** Counted this session; `quickstart.md` is fully annotated and
validates clean on both 2.0 and 1.31. See CLAUDE.md § "Compiling RIDDL
examples" for the directive table.

**Order:** Independent. Pick pages with the most fences first.

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
