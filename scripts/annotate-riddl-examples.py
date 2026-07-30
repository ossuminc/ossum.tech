#!/usr/bin/env python3
"""Insert `<!-- riddl: … -->` directives above code fences, by trying them.

`validate-riddl-examples.py` needs each fence to declare how it should be
wrapped. Writing ~126 of those by hand is slow and gets them wrong; this tries
each wrapper against a real riddlc and writes in the first that validates.

A fence that no wrapper satisfies is left ALONE and reported. Those are the
interesting ones: either a genuinely broken example, or a fragment needing a
page prelude that only a human can supply.

Idempotent: a fence that already carries a directive is skipped, so this can
be re-run after hand-fixing.

Usage:
    scripts/annotate-riddl-examples.py <riddlc> <file.md> [file.md ...]
    scripts/annotate-riddl-examples.py --dry-run <riddlc> <file.md>
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from importlib import import_module

_v = import_module("validate-riddl-examples".replace("-", "_")) if False else None

# validate-riddl-examples.py is not importable by that name, so reuse its
# pieces by exec'ing it in a throwaway namespace. Keeps ONE definition of the
# fence regex and the wrappers rather than a second copy that can drift.
_ns: dict = {}
exec(  # noqa: S102 - deliberate, see comment above
    (Path(__file__).parent / "validate-riddl-examples.py").read_text(),
    _ns,
)
FENCE = _ns["FENCE"]
PRELUDE = _ns["PRELUDE"]
directive_for = _ns["directive_for"]
wrap = _ns["wrap"]
validate = _ns["validate"]

ATTEMPTS = ("standalone", "in-domain", "in-context", "in-entity", "in-handler",
            "in-application", "in-function", "in-record", "in-clauses")


def main() -> int:
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    dry = "--dry-run" in sys.argv
    if len(args) < 2:
        print(__doc__)
        return 2
    riddlc, files = args[0], args[1:]

    annotated = already = unresolved = 0
    problems: list[str] = []

    for f in files:
        md = Path(f)
        text = md.read_text(encoding="utf-8")
        prelude = "\n".join(m.group("body") for m in PRELUDE.finditer(text))

        # Work back-to-front so earlier offsets stay valid as we insert.
        edits: list[tuple[int, str]] = []
        for fm in list(FENCE.finditer(text))[::-1]:
            line = text[: fm.start()].count("\n") + 1
            kind, _ = directive_for(text, fm.start())
            if kind != "standalone" or "<!-- riddl:" in text[max(0, fm.start() - 200): fm.start()]:
                already += 1
                continue

            chosen = None
            for attempt in ATTEMPTS:
                ok, _ = validate(riddlc, wrap(attempt, fm.group("body"), prelude))
                if ok:
                    chosen = attempt
                    break

            if chosen is None:
                unresolved += 1
                problems.append(f"{md}:{line}")
                continue
            if chosen == "standalone":
                already += 1  # validates as-is; the default is already right
                continue

            indent = fm.group("indent")
            edits.append((fm.start(), f"{indent}<!-- riddl: {chosen} -->\n"))
            annotated += 1

        if edits and not dry:
            for pos, ins in edits:
                text = text[:pos] + ins + text[pos:]
            md.write_text(text, encoding="utf-8")

    print(f"annotated {annotated}, already fine {already}, unresolved {unresolved}")
    if problems:
        print("\nNeeds a human (broken, or wants a page prelude):")
        for p in problems:
            print("  " + p)
    return 0


if __name__ == "__main__":
    sys.exit(main())
