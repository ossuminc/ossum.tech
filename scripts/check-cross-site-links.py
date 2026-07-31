#!/usr/bin/env python3
"""Validate absolute cross-site links between the ossum.tech sub-sites.

Why this exists
---------------
The site is built as four separate MkDocs projects. A link from one to another
cannot be relative, so it is written as an absolute path such as
``/riddlg/latest/mcp-tools/``. MkDocs classifies those as external and does not
check them -- ``--strict`` proves every *intra*-site link resolves, and says
nothing at all about the cross-site ones.

Without this check the split would trade build-verified links for a class of
404 that nothing notices. Run it alongside the strict builds.

    python3 scripts/check-cross-site-links.py

Exits non-zero on the first broken link, and prints every one it found.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
SITES = {"riddl", "riddlg", "synapify"}  # prefixed sites; shell is at the root

# Aliases a link may legitimately point at. mike creates a directory per alias,
# so these are real paths on the deployed site, not just names.
ALIASES = {"latest", "next"}

# A URL prefix is not always one source directory. TWO trees publish under
# `riddl` -- sites/riddl is 2.0, sites/riddl-1x is the 1.31 maintenance line --
# so which tree a link resolves against depends on the VERSION segment.
# Without this, every /riddl/1.31/... link would be checked against the 2.0
# sources and reported broken wherever the two lines differ.
#
# Mirrors docs-version.yml; keep the two in step. When 2.0 is promoted,
# `latest` moves to "riddl" here in the same commit that moves it there.
VERSION_SOURCE = {
    "riddl": {
        "2.0": "riddl",
        "next": "riddl",
        "1.31": "riddl-1x",
        "latest": "riddl-1x",
    },
}

LINK = re.compile(r"\]\((/[^)\s]*?)(#[^)\s]*)?\)")


def doc_for(url: str) -> tuple[Path, str] | None:
    """Map an absolute site URL to the markdown file that should produce it."""
    parts = [p for p in url.split("/") if p]

    if parts and parts[0] in SITES:
        site = parts[0]
        rest = parts[1:]
        # a prefixed site URL must carry a version or alias segment
        if not rest:
            return None
        version = rest[0]
        if version not in ALIASES and not re.fullmatch(r"\d+(\.\d+)*", version):
            return None
        rest = rest[1:]
        # Resolve against the tree that actually publishes this version.
        # An unmapped version is a dead link, not a pass: it names a version
        # the site does not deploy.
        if site in VERSION_SOURCE:
            source = VERSION_SOURCE[site].get(version)
            if source is None:
                return None
            site = source
    else:
        site, rest = "shell", parts

    docs = REPO / "sites" / site / "docs"
    if not rest:
        return docs / "index.md", f"{site}:index.md"
    candidate = docs / ("/".join(rest) + "/index.md")
    if candidate.exists():
        return candidate, f"{site}:{'/'.join(rest)}/index.md"
    return docs / ("/".join(rest) + ".md"), f"{site}:{'/'.join(rest)}.md"


def main() -> int:
    problems: list[str] = []
    checked = 0
    unverifiable: dict[str, int] = {}

    for md in sorted((REPO / "sites").rglob("*.md")):
        if "/site/" in md.as_posix():
            continue
        for m in LINK.finditer(md.read_text()):
            url = m.group(1)
            rel = md.relative_to(REPO).as_posix()
            resolved = doc_for(url)
            if resolved is None:
                problems.append(f"{rel}: unroutable cross-site link {url!r}")
                continue
            path, label = resolved
            # Not every branch carries every sub-site: docs/1.x publishes only
            # `riddl`, and its links into riddlg or Synapify point at content
            # published from `main`. Those cannot be checked from here, and
            # calling them broken would be wrong.
            # Presence is judged by the site's mkdocs.yml, which is tracked and
            # therefore branch-accurate. NOT by its docs/ directory: shared
            # assets are copied into sites/*/docs/ and gitignored, so those
            # directories survive a branch switch and would make a sub-site
            # this branch does not build look present -- turning every link
            # into it into a false failure.
            tsite = label.split(":")[0]
            if not (REPO / "sites" / tsite / "mkdocs.yml").is_file():
                unverifiable[tsite] = unverifiable.get(tsite, 0) + 1
                continue
            checked += 1
            if not path.exists():
                problems.append(f"{rel}: {url!r} -> no such document ({label})")

    for p in problems:
        print(p, file=sys.stderr)
    for site, n in sorted(unverifiable.items()):
        print(f"note: {n} link(s) into '{site}', which this branch does not "
              f"build -- published from another branch, not checked")
    print(f"checked {checked} cross-site links, {len(problems)} broken")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
