# BACKLOG

The single place for open work on ossum.tech. If it is not here, it is not
tracked. Completed items leave this file: what they taught goes to NOTEBOOK.md,
what is durably true goes to CLAUDE.md.

---

## 1. Annotate the RIDDL fences in the remaining doc trees

**What:** `concepts/`, `quickstart.md` and `references/language-reference.md`
are **fully gated** — 84 validated, 127 skipped, 0 failed, exit 0 against
2.0.0-rc.10-43. Not yet gated: `tutorials/rbbq/` (30 pages), `guides/`,
`tools/`, and the `riddlg`/`synapify`/`shell` sites.

**Verified 2026-08-08** against rc.10. Re-run:
```bash
python3 scripts/validate-riddl-examples.py ../bin/riddlc \
  sites/riddl/docs/concepts/*.md sites/riddl/docs/quickstart.md \
  sites/riddl/docs/references/language-reference.md
```

**Also open:** `check-riddl-blocks.py` flags two items in
`tutorials/rbbq/restaurant/online-ordering.md` (`state ... of O` without a
record; a `prompt "` statement). Advisory, and inside the ungated tree above.

**Order:** Independent. `tutorials/rbbq/` is the biggest and the most read.

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
