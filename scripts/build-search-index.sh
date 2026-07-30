#!/usr/bin/env bash
#
# Build the cross-site Pagefind search index over a deployed site tree.
#
# Why this exists
# ---------------
# The documentation is four separate MkDocs projects. Material builds one
# search index per project, so each site's search box can only ever find that
# site -- a reader in the RIDDL docs searching "Synapify" gets nothing.
#
# Pagefind indexes BUILT HTML rather than MkDocs sources, so it does not care
# how many projects produced the tree. It runs last, over the assembled
# gh-pages content, and writes /pagefind/ at the root. The /find/ page loads it.
#
# Usage:
#   scripts/build-search-index.sh <site-root>
#
set -euo pipefail

ROOT="${1:?usage: build-search-index.sh <site-root>}"
[ -d "$ROOT" ] || { echo "no such directory: $ROOT" >&2; exit 1; }

# Use the interpreter mkdocs is installed under -- the `python3` first on PATH
# is often a different install without pagefind (see preview-versioned-site.sh).
PY="$(sed -n '1s|^#!||p' "$(command -v mkdocs)")"
[ -x "$PY" ] || PY=python3

# Index each product's DEFAULT ALIAS only, plus the unversioned shell pages.
#
# Not the whole tree: mike deploys aliases as full COPIES, so /riddl/latest/ is
# a byte-for-byte duplicate of /riddl/1.31/. Indexing everything would return
# the same page three or four times, once per version and once per alias.
#
# Following the alias rather than a pinned version means this needs no edit
# when RIDDL 2.0 is promoted -- `latest` moves and the index follows.
GLOB='{index.html,about/**/*.html,coming-soon/**/*.html,riddl/latest/**/*.html,riddlg/latest/**/*.html,synapify/latest/**/*.html}'

# Material renders a pilcrow anchor after every heading (`toc.permalink: true`).
# Pagefind treats it as heading text, so sub-results read "Purpose¶" and a
# search for a heading word can match the anchor rather than the prose.
EXCLUDE='.headerlink,.md-skip,.md-source__repository,.md-version'

echo "==> Indexing $ROOT"
"$PY" -m pagefind --site "$ROOT" --glob "$GLOB" --exclude-selectors "$EXCLUDE"

# A Pagefind run over a tree where nothing matched still exits 0 and writes an
# empty index, which looks exactly like success and fails silently in the
# browser. Assert every source actually contributed.
echo "==> Verifying the index spans all four sources"
missing=0
for want in riddl/latest riddlg/latest synapify/latest; do
  if ! find "$ROOT/$want" -name '*.html' -print -quit 2>/dev/null | grep -q .; then
    echo "  MISSING SOURCE: $want has no HTML -- was it deployed?" >&2
    missing=1
  fi
done
if [ ! -f "$ROOT/pagefind/pagefind.js" ]; then
  echo "  pagefind.js was not produced" >&2
  missing=1
fi
[ "$missing" -eq 0 ] || { echo "search index is incomplete" >&2; exit 1; }

echo "==> Search index written to $ROOT/pagefind/"
