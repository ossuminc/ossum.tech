#!/usr/bin/env python3
"""Diff riddl_lexer's vocabulary against riddl's Keyword.allKeywords.

The Pygments lexer duplicates a list that lives in riddl, and NOTHING keeps
them in step. When they drift the failure is silent and cosmetic-looking:
every code sample on the site renders the missing words as plain identifiers,
which reads as a styling quirk rather than as a stale vocabulary. Measured
2026-09-09, fifteen keywords were missing this way -- `prompt` and `forward`
among them, both common in real models.

riddl has the same hazard internally and guards it with a drift TEST
(KeywordTableDriftTest); this is the same idea across the repo boundary.

Usage:
    python3 scripts/check-lexer-keywords.py [path-to-riddl-checkout]

Exits 1 if riddl has keywords the lexer does not. Words the LEXER has but
riddl does not are reported separately and are NOT failures: the lexer also
carries option values, predefined type names and UI aliases, none of which
are parser keywords.
"""
import re
import subprocess
import sys
from pathlib import Path

KEYWORDS_SCALA = (
    "language/src/main/scala/com/ossuminc/riddl/language/parsing/Keywords.scala"
)


def riddl_keywords(riddl_root: Path) -> set[str]:
    """Resolve Keyword.allKeywords to its string values.

    The Seq lists `final val` identifiers, not literals, so each has to be
    looked up. Reading the file from the working tree is fine here -- unlike
    the grammar, this is a cross-check, not content we ship.
    """
    src = (riddl_root / KEYWORDS_SCALA).read_text(encoding="utf-8")
    vals = dict(re.findall(r'final val (\w+)\s*=\s*"([^"]+)"', src))

    i = src.index("def allKeywords: Seq[String] = Seq(")
    start = src.index("(", i)
    depth = 0
    for j in range(start, len(src)):
        if src[j] == "(":
            depth += 1
        elif src[j] == ")":
            depth -= 1
            if depth == 0:
                end = j
                break
    body = re.sub(r"//[^\n]*", "", src[start + 1 : end])

    out, unresolved = set(), []
    for name in (n.strip() for n in body.split(",")):
        if not name:
            continue
        if name.startswith('"'):
            out.add(name.strip('"'))
        elif name in vals:
            out.add(vals[name])
        else:
            unresolved.append(name)
    if unresolved:
        sys.exit(f"cannot resolve {len(unresolved)} entries, e.g. {unresolved[:5]}")
    # `final value` is one two-word keyword; the lexer matches word by word.
    return {w for kw in out for w in kw.split()}


def lexer_words() -> set[str]:
    """Every word in every UPPER_CASE tuple in the lexer.

    The tuples are indented inside the class, so the pattern must not anchor
    at column zero -- an earlier version of this diff did, matched nothing,
    and reported all 168 keywords as missing.
    """
    src = (Path(__file__).parent.parent / "riddl_lexer" / "lexer.py").read_text(
        encoding="utf-8"
    )
    words = set()
    for m in re.finditer(r"^\s*[A-Z][A-Z_]+\s*=\s*\(\s*\n(.*?)\n\s*\)", src, re.S | re.M):
        words |= set(re.findall(r"'([^']+)'", m.group(1)))
    return words


def main() -> int:
    root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("../riddl")
    if not (root / KEYWORDS_SCALA).exists():
        sys.exit(f"no riddl checkout at {root} (pass one as the first argument)")

    riddl, lexer = riddl_keywords(root), lexer_words()

    # Controls: if these are absent the extraction is broken, not the lexer.
    for control in ("domain", "entity", "let"):
        if control not in lexer:
            sys.exit(f"extraction is broken: control word {control!r} not found")

    describe = subprocess.run(
        ["git", "-C", str(root), "describe", "--tags"],
        capture_output=True, text=True,
    ).stdout.strip() or "unknown"
    print(f"riddl {describe}: {len(riddl)} keywords; lexer: {len(lexer)} words")

    missing = sorted(riddl - lexer)
    if missing:
        print(f"\nMISSING from riddl_lexer ({len(missing)}):")
        for i in range(0, len(missing), 8):
            print("  " + "  ".join(missing[i : i + 8]))
        print("\nAdd each to the list that matches how the lexer groups it.")
        return 1

    print("no missing keywords")
    return 0


if __name__ == "__main__":
    sys.exit(main())
