#!/usr/bin/env python3
"""Report retired RIDDL 1.x constructs in ```riddl code fences.

This is ADVISORY, not a gate. Many fences are deliberate fragments, and the
version-specific pages legitimately show deprecated syntax in order to explain
it. So the script reports and exits 0 unless --strict is passed.

Three kinds of false positive are suppressed automatically:

  * a fence on a page that is ABOUT the deprecation (the migration guide, the
    RBBQ tutorial, and so on) -- see EXEMPT_PATHS
  * a fence immediately preceded by a line marking it as the "before" side of
    a before/after comparison -- see BEFORE_MARKERS
  * an individual LINE carrying a trailing comment that marks it as a
    deliberate counter-example -- see COUNTEREXAMPLE. Documentation that
    teaches a rule usually has to show the thing the rule forbids, so this is
    a recurring and legitimate pattern:

        when count > 5 then ??? end        // fails to parse

Usage:
    python3 scripts/check-riddl-blocks.py [--strict] [docs_dir]
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

# Retired or deprecated constructs, with what to use instead.
CHECKS: list[tuple[str, re.Pattern[str], str]] = [
    ("reply-statement", re.compile(r"\breply\s+(command|event|query|result)\b"),
     "use `yield`"),
    ("prompt-statement", re.compile(r'(?<!\()\bprompt\s+"'),
     "use `do \"...\"` (the `prompt(...)` VALUE, with parens, is fine)"),
    ("abstract-type", re.compile(r"\bAbstract\b"),
     "use `Anything`"),
    ("state-without-record", re.compile(r"\bstate\s+\w+\s+of\s+(?!record\b)\w"),
     "a state is typed by a `record`"),
    ("shape-keyword", re.compile(r"^\s*(source|sink|flow|merge|split|router)\s+[A-Z]\w*\s+is\b",
                                 re.MULTILINE),
     "use `processor <id> as <shape>`"),
    ("send-to-inlet", re.compile(r"\bsend\b[^\n]*\bto\s+inlet\b"),
     "send to an `outlet`, or use `tell`"),
    ("application-definition", re.compile(r"^\s*application\s+\w+\s+is\b", re.MULTILINE),
     "use `application context <id> is`"),
    ("ui-outside-application", re.compile(r"^\s*context\s+\w+\s+is\s*\{[^\n]*\b(page|group|dialog|pane)\b",
                                          re.MULTILINE),
     "UI requires an `application` context"),
    ("literal-comparison", re.compile(r"\b(when|require)\s+[\w.]+\s*(==|!=|<=|>=|<|>)\s*(\d|\")"),
     "comparison operands must be references or named constants"),
    ("nebula", re.compile(r"^\s*nebula\b", re.MULTILINE),
     "use `module <Name> is { ... }`"),
]

# Pages whose PURPOSE is to show the old syntax. Reporting them is noise.
EXEMPT_PATHS = {
    "riddl/migration/1.x-to-2.0.md",
    # The RBBQ tutorial quotes riddl-models verbatim and migrates with it.
    # See riddl-models/task/2026-07-26-release2-syntax-migration.md.
    "riddl/tutorials/rbbq/",
}

# A fence preceded by one of these is the "before" half of a comparison.
BEFORE_MARKERS = re.compile(r"^\s*(//\s*)?(1\.x|before|deprecated|old)\b", re.IGNORECASE)

# A line ending in one of these comments is showing what NOT to write.
COUNTEREXAMPLE = re.compile(
    r"//\s*.*\b(fails?\s+to\s+parse|does\s+not\s+parse|invalid|deprecated|"
    r"wrong|error|1\.x)\b",
    re.IGNORECASE,
)

FENCE = re.compile(r"^([ \t]*)```+riddl[^\n]*\n(.*?)^\1```+", re.MULTILINE | re.DOTALL)


def exempt(rel: str) -> bool:
    return any(rel == e or rel.startswith(e) for e in EXEMPT_PATHS)


def preceded_by_before_marker(text: str, fence_start: int) -> bool:
    """True if the two lines above the fence mark it as a 'before' example."""
    head = text[:fence_start].rstrip("\n").split("\n")
    return any(BEFORE_MARKERS.match(line) for line in head[-2:])


def main() -> int:
    args = [a for a in sys.argv[1:] if not a.startswith("-")]
    strict = "--strict" in sys.argv
    docs = Path(args[0]) if args else Path("docs")

    if not docs.is_dir():
        print(f"error: {docs} is not a directory", file=sys.stderr)
        return 2

    findings: list[str] = []
    fences = 0

    for md in sorted(docs.rglob("*.md")):
        rel = md.relative_to(docs).as_posix()
        if exempt(rel):
            continue
        text = md.read_text(encoding="utf-8")
        for m in FENCE.finditer(text):
            fences += 1
            body = m.group(2)
            if preceded_by_before_marker(text, m.start()):
                continue
            fence_line = text[: m.start()].count("\n") + 1
            for name, pattern, advice in CHECKS:
                for hit in pattern.finditer(body):
                    # Which line of the fence body did this land on?
                    offset = body[: hit.start()].count("\n")
                    line = body.split("\n")[offset]
                    if COUNTEREXAMPLE.search(line):
                        continue
                    snippet = hit.group(0).strip().replace("\n", " ")[:60]
                    findings.append(
                        f"{rel}:{fence_line + offset + 1}: {name}: "
                        f"{snippet!r} -- {advice}"
                    )
                    break  # one report per check per fence is enough

    print(f"Scanned {fences} riddl code fences under {docs}/")
    if findings:
        print(f"\n{len(findings)} possible 1.x construct(s):\n")
        for f in findings:
            print("  " + f)
        print("\nAdvisory only. Fences that deliberately show old syntax can be")
        print("exempted via EXEMPT_PATHS, or preceded by a `// 1.x` comment.")
        return 1 if strict else 0

    print("No retired 1.x constructs found.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
