#!/usr/bin/env python3
"""Split failing fences into "illustrative" and "possibly wrong".

A fence can fail validation for two very different reasons:

  RESOLUTION ONLY -- it parses fine under some wrapper, but references names
      the page never defines (`send event ItemAdded to outlet CartEvents` on a
      page about statements). That is a legitimate documentation fragment. It
      gets `<!-- riddl: skip reason="illustrative fragment" -->`.

  PARSE FAILURE -- no wrapper can even parse it. That is either a deliberate
      counter-example or a genuinely wrong example, and a human must decide
      which. These are REPORTED, never auto-skipped, because silently skipping
      a broken example is how the sagastep.md and use-case.md errors survived
      for so long.

    scripts/triage-riddl-examples.py <riddlc> <file.md> ...          # report
    scripts/triage-riddl-examples.py --apply <riddlc> <file.md> ...  # write skips
"""

from __future__ import annotations

import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path

_ns: dict = {}
exec((Path(__file__).parent / "validate-riddl-examples.py").read_text(), _ns)  # noqa: S102
FENCE, PRELUDE, wrap, directive_for = (
    _ns["FENCE"], _ns["PRELUDE"], _ns["wrap"], _ns["directive_for"]
)

ATTEMPTS = ("standalone", "in-domain", "in-context", "in-entity", "in-handler",
            "in-application", "in-function", "in-record", "in-clauses")


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
    apply = "--apply" in sys.argv
    if len(args) < 2:
        print(__doc__)
        return 2
    riddlc, files = args[0], args[1:]

    skipped = passing = review = 0
    to_review: list[tuple[str, int, str, str]] = []

    for f in files:
        md = Path(f)
        text = md.read_text(encoding="utf-8")
        pre = "\n".join(m.group("body") for m in PRELUDE.finditer(text))
        edits: list[tuple[int, str]] = []

        for fm in list(FENCE.finditer(text))[::-1]:
            kind, _ = directive_for(text, fm.start())
            if kind == "skip":
                skipped += 1
                continue
            outs = []
            ok = False
            for attempt in (kind,) + tuple(a for a in ATTEMPTS if a != kind):
                ok, out = run(riddlc, wrap(attempt, fm.group("body"), pre))
                if ok:
                    break
                outs.append(out)
            if ok:
                passing += 1
                continue

            # Three outcomes, not two. A fence that PARSES but fails
            # validation for a reason other than a missing name is where real
            # documentation bugs live -- that is how the gateway/service
            # intention-shape error was found -- so it must be reviewed, never
            # auto-skipped.
            line = text[: fm.start()].count("\n") + 1
            parsed = [o for o in outs if "Expected" not in o]
            if parsed:
                non_resolution = [
                    ln.strip() for o in parsed for ln in o.split("\n")
                    if "[error]" not in ln and ln.strip()
                    and "was not resolved" not in ln
                    and ("must have" in ln or "is already" in ln
                         or "only allowed" in ln or "redefines" in ln)
                ]
                if non_resolution:
                    review += 1
                    to_review.append((str(md), line,
                                      fm.group("body").strip().split("\n")[0][:48],
                                      "VALIDATION: " + non_resolution[0][:64]))
                    continue
            if parsed:
                indent = fm.group("indent")
                edits.append((
                    fm.start(),
                    f'{indent}<!-- riddl: skip reason="illustrative fragment; '
                    f'references vocabulary this page does not define" -->\n',
                ))
                skipped += 1
            else:
                review += 1
                first = next(
                    (ln.strip() for o in outs for ln in o.split("\n")
                     if ln.startswith("Expected")), "(no Expected line)")
                to_review.append(
                    (str(md), line, fm.group("body").strip().split("\n")[0][:48], first[:76]))

        if edits and apply:
            for pos, ins in edits:
                text = text[:pos] + ins + text[pos:]
            md.write_text(text, encoding="utf-8")

    verb = "skipped" if apply else "would skip"
    print(f"{passing} passing, {verb} {skipped}, {review} need review\n")
    if to_review:
        print("NEEDS A HUMAN -- cannot parse under any wrapper:")
        for f, ln, head, why in to_review:
            print(f"  {f}:{ln}  {head}")
            print(f"      {why}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
