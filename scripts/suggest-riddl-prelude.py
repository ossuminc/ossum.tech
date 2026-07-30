#!/usr/bin/env python3
"""Report, per page, what a `riddl-prelude` block still needs.

Most remaining validation failures are fragments referencing a shared
vocabulary the page never shows. riddlc's errors say both the missing NAME and
the KIND it should be ("and it should refer to a Type"), which is enough to
propose a definition rather than guess.

    scripts/suggest-riddl-prelude.py <riddlc> <file.md> [file.md ...]

Prints a ready-to-paste prelude per page, plus the fences that fail for some
OTHER reason -- those are the ones needing a human: a deliberate
counter-example to mark `skip`, or a genuinely wrong example to fix.
"""

from __future__ import annotations

import os
import re
import subprocess
import sys
import tempfile
from collections import OrderedDict
from pathlib import Path

_ns: dict = {}
exec(  # noqa: S102
    (Path(__file__).parent / "validate-riddl-examples.py").read_text(), _ns
)
FENCE, PRELUDE, wrap, directive_for = (
    _ns["FENCE"], _ns["PRELUDE"], _ns["wrap"], _ns["directive_for"]
)

ATTEMPTS = ("standalone", "in-domain", "in-context", "in-entity", "in-handler",
            "in-application", "in-function", "in-record", "in-clauses", "in-usecase")

UNRESOLVED = re.compile(
    r"Path '([^']+)' was not resolved.*?it should refer to (?:an?\s+)?(\w+)",
    re.S,
)

# How to spell a stub of each kind, at context level.
STUB = {
    "Type": "type {n} is String",
    "Entity": "entity {n} is {{ ??? }}",
    "Constant": 'constant {n} is Natural = "1"',
    "Function": "function {n} is {{ requires StubInput returns StubInput ??? }}",
    "Outlet": None,      # must live on a processor; not prelude-able
    "Inlet": None,
    "Input": None,       # must live in a group
    "Output": None,
    "Field": None,       # must live in a record
    "State": None,
    "Handler": None,
}


def run(riddlc: str, src: str) -> tuple[bool, str]:
    with tempfile.NamedTemporaryFile("w", suffix=".riddl", delete=False) as fh:
        fh.write(src)
        p = fh.name
    try:
        r = subprocess.run([riddlc, "validate", p], capture_output=True, text=True)
        o = re.sub(r"\x1b\[[0-9;]*m", "", r.stdout + r.stderr)
        bad = any(k in o for k in ("[error]", "[severe]", "[deprecated]"))
        return (r.returncode == 0 and not bad), o
    finally:
        os.unlink(p)


def main() -> int:
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    if len(args) < 2:
        print(__doc__)
        return 2
    riddlc, files = args[0], args[1:]

    for f in files:
        md = Path(f)
        text = md.read_text(encoding="utf-8")
        pre = "\n".join(m.group("body") for m in PRELUDE.finditer(text))

        wanted: OrderedDict[str, str] = OrderedDict()
        others: list[tuple[int, str, str]] = []

        for fm in FENCE.finditer(text):
            kind, _ = directive_for(text, fm.start())
            if kind == "skip":
                continue
            order = (kind,) + tuple(a for a in ATTEMPTS if a != kind)
            # Keep the attempt that got FURTHEST -- fewest errors -- rather
            # than whichever happened to run last. Reporting the last one
            # describes a wrapper nobody would have chosen for this fence.
            results = []
            ok = False
            for attempt in order:
                ok, out = run(riddlc, wrap(attempt, fm.group("body"), pre))
                if ok:
                    break
                results.append((out.count("[error]"), attempt, out))
            if not ok:
                # Prefer an attempt whose output says "was not resolved": that
                # means the WRAPPER worked structurally and only names are
                # missing, which is exactly what a prelude fixes. Counting
                # errors is the wrong signal -- an attempt that fails at the
                # first token reports fewest and teaches least.
                resolvable = [r for r in results if "was not resolved" in r[2]]
                pick = max(resolvable, key=lambda r: r[0]) if resolvable else results[-1]
                last = pick[2]
                found = UNRESOLVED.findall(last)
                if found:
                    for name, k in found:
                        base = name.split(".")[0]
                        if base not in wanted:
                            wanted[base] = k
                else:
                    line = text[: fm.start()].count("\n") + 1
                    why = next(
                        (ln.strip() for ln in last.split("\n")
                         if ln.startswith(("Expected", "Type ", "Identifier"))
                         or "is already" in ln or "only allowed" in ln),
                        "(unclear)",
                    )
                    others.append((line, fm.group("body").strip().split("\n")[0][:46], why[:78]))

        if not wanted and not others:
            print(f"\n{md}: nothing outstanding")
            continue

        print(f"\n=== {md} ===")
        if wanted:
            unstubbable = [n for n, k in wanted.items() if STUB.get(k) is None]
            print("  suggested prelude additions:")
            for n, k in wanted.items():
                tpl = STUB.get(k)
                if tpl:
                    print("    " + tpl.format(n=n))
            if unstubbable:
                print(f"  NOT prelude-able (must live inside something): {', '.join(unstubbable)}")
        for line, head, why in others:
            print(f"  L{line}: {head}")
            print(f"      {why}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
