#!/usr/bin/env python3
"""Validate ```riddl code fences in documentation against a real riddlc.

Most fences are FRAGMENTS -- a `context` with no enclosing `domain`, an
`entity` with no enclosing context -- so they cannot be validated as written.
Each fence therefore declares how to make it whole, via an HTML comment
immediately above it. HTML comments do not render, so this is invisible to
readers.

    <!-- riddl: standalone -->        a complete model; validate as-is (default)
    <!-- riddl: in-domain -->         wrap in `domain Example is { ... }`
    <!-- riddl: in-context -->        wrap in a domain AND a context
    <!-- riddl: skip -->              not RIDDL, or deliberately invalid
    <!-- riddl: skip reason=... -->   same, with the reason recorded

A page may also declare a PRELUDE: definitions that fragments reference but
do not show. It is injected into the wrapper alongside the fence body.

    <!-- riddl-prelude
    record Thing is { a is String }
    -->

Usage:
    scripts/validate-riddl-examples.py <riddlc> <file.md> [file.md ...]

Exit status is non-zero if any fence fails to validate, so this is usable as
a gate -- unlike check-riddl-blocks.py, which is advisory.
"""

from __future__ import annotations

import re
import subprocess
import sys
import tempfile
from pathlib import Path

FENCE = re.compile(
    r"^(?P<indent>[ \t]*)```+riddl[^\n]*\n(?P<body>.*?)^(?P=indent)```+",
    re.MULTILINE | re.DOTALL,
)
DIRECTIVE = re.compile(r"<!--\s*riddl:\s*(?P<what>[a-z-]+)(?P<rest>[^>]*)-->", re.IGNORECASE)
PRELUDE = re.compile(r"<!--\s*riddl-prelude\s*\n(?P<body>.*?)-->", re.DOTALL | re.IGNORECASE)


def directive_for(text: str, fence_start: int) -> tuple[str, str]:
    """The directive in the comment closest above this fence, if any."""
    head = text[:fence_start]
    # Only look at the last few lines, so a directive cannot leak across prose.
    tail = "\n".join(head.rstrip("\n").split("\n")[-4:])
    m = None
    for m in DIRECTIVE.finditer(tail):
        pass  # take the last one
    if not m:
        return "standalone", ""
    return m.group("what").lower(), m.group("rest").strip()


def wrap(kind: str, body: str, prelude: str) -> str:
    body = body.rstrip()
    if kind == "in-context":
        inner = "\n".join("    " + ln if ln.strip() else ln for ln in body.split("\n"))
        pre = "\n".join("    " + ln for ln in prelude.strip().split("\n")) if prelude.strip() else ""
        return f"domain Example is {{\n  context Example is {{\n{pre}\n{inner}\n  }}\n}}\n"
    if kind == "in-domain":
        inner = "\n".join("  " + ln if ln.strip() else ln for ln in body.split("\n"))
        pre = "\n".join("  " + ln for ln in prelude.strip().split("\n")) if prelude.strip() else ""
        return f"domain Example is {{\n{pre}\n{inner}\n}}\n"
    # standalone: a prelude, if any, sits beside the model at top level
    return (prelude.rstrip() + "\n\n" if prelude.strip() else "") + body + "\n"


def validate(riddlc: str, source: str) -> tuple[bool, str]:
    with tempfile.NamedTemporaryFile("w", suffix=".riddl", delete=False) as fh:
        fh.write(source)
        path = fh.name
    try:
        proc = subprocess.run(
            [riddlc, "validate", path],
            capture_output=True, text=True, timeout=120,
        )
        out = proc.stdout + proc.stderr
        # Strip ANSI so the report is readable when redirected to a file.
        out = re.sub(r"\x1b\[[0-9;]*m", "", out)
        bad = [
            ln for ln in out.split("\n")
            if "[error]" in ln or "[severe]" in ln or "[deprecated]" in ln
        ]
        detail = "\n".join(
            ln for ln in out.split("\n")
            if any(k in ln for k in ("[error]", "[severe]", "[deprecated]"))
            or ln.startswith(("Expected", "Context:"))
        )
        return (proc.returncode == 0 and not bad), detail.strip()
    finally:
        Path(path).unlink(missing_ok=True)


def main() -> int:
    if len(sys.argv) < 3:
        print(__doc__)
        return 2
    riddlc, files = sys.argv[1], sys.argv[2:]

    total = skipped = failed = 0
    for f in files:
        md = Path(f)
        text = md.read_text(encoding="utf-8")
        prelude = "\n".join(m.group("body") for m in PRELUDE.finditer(text))

        for fm in FENCE.finditer(text):
            line = text[: fm.start()].count("\n") + 1
            kind, rest = directive_for(text, fm.start())
            if kind == "skip":
                skipped += 1
                continue
            total += 1
            ok, detail = validate(riddlc, wrap(kind, fm.group("body"), prelude))
            if not ok:
                failed += 1
                print(f"\nFAIL {md}:{line}  (riddl: {kind})")
                for ln in detail.split("\n")[:8]:
                    print("    " + ln)

    print(f"\n{total} fence(s) validated, {skipped} skipped, {failed} failed")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
