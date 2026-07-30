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
    <!-- riddl: in-entity -->         wrap in a domain, context AND entity
    <!-- riddl: in-handler -->        wrap deep enough to be inside an on-clause
    <!-- riddl: in-clauses -->        wrap in a handler (for `on ...` clause fragments)
    <!-- riddl: in-usecase -->        wrap in an epic + use case (for interaction steps)
    <!-- riddl: in-application -->    as in-handler, but an `application` context (for `put`)
    <!-- riddl: in-function -->       wrap in a function body (for `return`)
    <!-- riddl: in-record -->         wrap in a record (for a bare field declaration)
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
    """Nest a fragment deep enough to be a whole model.

    The prelude always lands at CONTEXT level, whatever the depth, because
    that is where a page's shared vocabulary belongs -- a fragment nested in
    a handler still needs to see the types the page defined around it.
    """
    body = body.rstrip()

    def ind(txt: str, n: int) -> str:
        pad = " " * n
        return "\n".join(pad + ln if ln.strip() else ln for ln in txt.split("\n"))

    pre = ind(prelude.strip(), 4) if prelude.strip() else ""
    # An author may only be DEFINED in a Module or Domain, so a context-level
    # page prelude cannot supply one -- yet `by author X` appears on many
    # pages. Every wrapper therefore defines one at domain level.
    AUTHOR = '  author Reid is { name is "Reid Spencer" email is "reid@ossuminc.com" }\n'

    if kind == "in-function":
        # `return` is legal only in a function body.
        return (
            "domain Example is {\n" + AUTHOR + "  context Example is {\n" + pre + "\n"
            "    record FnInput is { note is String }\n"
            "    function ExampleFunction is {\n"
            "      requires FnInput returns FnInput\n"
            + ind(body, 6) + "\n"
            "    }\n  }\n}\n"
        )
    if kind == "in-application":
        # `put ... to output` is legal only in an application/context handler.
        return (
            "domain Example is {\n" + AUTHOR + "  application context Example is {\n" + pre + "\n"
            "    record ExampleData is { note is String }\n"
            "    command ExampleCommand is { note is String }\n"
            "    page ExamplePage is {\n"
            "      document ExampleOutput shows type String\n"
            "      form ExampleInput accepts type String\n"
            "    }\n"
            "    handler ExampleHandler is {\n"
            "      on command ExampleCommand {\n"
            + ind(body, 8) + "\n"
            "      }\n    }\n  }\n}\n"
        )
    if kind == "in-record":
        # A bare field declaration, e.g. `items is many Item`.
        return (
            "domain Example is {\n" + AUTHOR + "  context Example is {\n" + pre + "\n"
            "    record ExampleRecord is {\n" + ind(body, 6) + "\n"
            "    }\n  }\n}\n"
        )
    if kind == "in-usecase":
        # An interaction step lives in a use case, inside an epic, inside a
        # domain -- three levels no other wrapper provides.
        return (
            "domain Example is {\n" + AUTHOR +
            "  user Customer is \"a customer\"\n"
            "  context Example is {\n" + pre + "\n"
            "    record ExampleData is { note is String }\n"
            "    entity Cart is { ??? }\n"
            "  }\n"
            "  epic ExampleEpic is {\n"
            "    user Customer wants to \"do a thing\" so that \"a benefit follows\"\n"
            "    case ExampleCase is {\n"
            "      user Customer wants to \"do a thing\" so that \"a benefit follows\"\n"
            + ind(body, 6) + "\n"
            "    }\n  }\n}\n"
        )
    if kind == "in-clauses":
        # An `on ...` clause fragment: give it a handler to sit in.
        return (
            "domain Example is {\n" + AUTHOR + "  context Example is {\n" + pre + "\n"
            "    record ExampleData is { note is String }\n"
            "    command ExampleCommand is { note is String }\n"
            "    entity ExampleEntity is {\n"
            "      state ExampleState of record ExampleData is {\n"
            "        handler ExampleHandler is {\n"
            + ind(body, 10) + "\n"
            "        }\n      }\n    }\n  }\n}\n"
        )
    if kind == "in-handler":
        # Statement-level fragment: give it an on-clause to live in.
        return (
            "domain Example is {\n" + AUTHOR + "  context Example is {\n" + pre + "\n"
            "    record ExampleData is { note is String }\n"
            "    command ExampleCommand is { note is String }\n"
            "    entity ExampleEntity is {\n"
            "      state ExampleState of record ExampleData is {\n"
            "        handler ExampleHandler is {\n"
            "          on command ExampleCommand {\n"
            + ind(body, 12) + "\n"
            "          }\n        }\n      }\n    }\n  }\n}\n"
        )
    if kind == "in-entity":
        return (
            "domain Example is {\n" + AUTHOR + "  context Example is {\n" + pre + "\n"
            "    entity ExampleEntity is {\n" + ind(body, 6) + "\n"
            "    }\n  }\n}\n"
        )
    if kind == "in-context":
        return (
            "domain Example is {\n" + AUTHOR + "  context Example is {\n" + pre + "\n"
            + ind(body, 4) + "\n  }\n}\n"
        )
    if kind == "in-domain":
        return "domain Example is {\n" + AUTHOR + ind(body, 2) + "\n}\n"
    # standalone: complete by definition, so the prelude is NOT injected --
    # a page prelude holds context-level definitions, and those are illegal at
    # root, which would break the very fences that need no help.
    return body + "\n"


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
    args = [a for a in sys.argv[1:] if a != "--auto"]
    auto = "--auto" in sys.argv
    riddlc, files = args[0], args[1:]

    total = skipped = failed = 0
    for f in files:
        md = Path(f)
        text = md.read_text(encoding="utf-8")
        prelude = "\n".join(m.group("body") for m in PRELUDE.finditer(text))

        for fm in FENCE.finditer(text):
            line = text[: fm.start()].count("\n") + 1
            kind, rest = directive_for(text, fm.start())
            if auto and kind == "standalone":
                kind = "auto"
            if kind == "skip":
                skipped += 1
                continue
            total += 1
            if kind == "auto":
                # Try each wrapping; a fence that fits ANY of them is a
                # fragment needing context, not a broken example. Used to
                # measure how many fences are genuinely wrong on pages that
                # do not yet carry directives.
                ok, detail = False, ""
                for attempt in ("standalone", "in-domain", "in-context", "in-entity", "in-handler", "in-application", "in-function", "in-record", "in-clauses", "in-usecase"):
                    ok, detail = validate(riddlc, wrap(attempt, fm.group("body"), prelude))
                    if ok:
                        break
            else:
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
