#!/usr/bin/env bash
#
# Build the versioned site exactly as it will be deployed, and serve it
# locally for review.
#
# Why not `mike serve`? Because mike operates on THIS repository's gh-pages
# branch, so previewing would mutate it. This script clones into a scratch
# directory instead, so your working repository is never touched.
#
# What it produces is the real end state, not an approximation:
#   - both versions deployed under their own paths
#   - the `latest` and `next` aliases
#   - mike's root index.html redirect to the default version
#   - the legacy-link 404 handler from scripts/gh-pages-404.html
#   - the old flat site cleared from the gh-pages root, as the migration
#     runbook does
#
# Usage:
#   scripts/preview-versioned-site.sh [port]
#
set -euo pipefail

PORT="${1:-8800}"
REPO="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SCRATCH="${TMPDIR:-/tmp}/ossum-tech-preview"
SERVE="$SCRATCH/site"

# Which branch supplies which version. Keep in step with docs-version.yml on
# each branch; this script cannot read both at once.
V1_BRANCH="docs/1.x";   V1_VERSION="1.31"; V1_ALIAS="latest"
V2_BRANCH="release/2";  V2_VERSION="2.0";  V2_ALIAS="next"
DEFAULT_ALIAS="latest"

command -v mike >/dev/null || { echo "mike not installed: pip install -r requirements.txt" >&2; exit 1; }

echo "==> Cloning $REPO into a scratch directory (your repo is not touched)"
rm -rf "$SCRATCH"
git clone --quiet --no-hardlinks "$REPO" "$SCRATCH/repo"
cd "$SCRATCH/repo"

# Detach first: a clone checks out the source repo's current branch, and git
# refuses to force-update a branch that a worktree has checked out.
git checkout --quiet --detach

# A plain clone copies the SOURCE repo's local refs, which may lag its
# remote-tracking refs. Prefer origin/gh-pages when it is ahead.
if git rev-parse --verify --quiet origin/gh-pages >/dev/null; then
  git branch --quiet -f gh-pages "$(git rev-parse origin/gh-pages)"
fi
for br in "$V1_BRANCH" "$V2_BRANCH"; do
  git rev-parse --verify --quiet "origin/$br" >/dev/null \
    && git branch --quiet -f "$br" "origin/$br"
done
git remote remove origin

echo "==> Clearing the old flat site from the gh-pages root"
if git rev-parse --verify --quiet gh-pages >/dev/null; then
  git checkout --quiet gh-pages
  # Keep only the files that must persist at the root.
  for entry in $(git ls-tree --name-only gh-pages); do
    case "$entry" in
      CNAME|.nojekyll) ;;
      *) git rm -rq --ignore-unmatch "$entry" ;;
    esac
  done
  git commit --quiet -m "preview: clear flat site" 2>/dev/null || true
fi

echo "==> Deploying $V1_VERSION [$V1_ALIAS] from $V1_BRANCH"
git checkout --quiet "$V1_BRANCH"
mike deploy --alias-type copy "$V1_VERSION" "$V1_ALIAS" >/dev/null 2>&1

echo "==> Deploying $V2_VERSION [$V2_ALIAS] from $V2_BRANCH"
git checkout --quiet "$V2_BRANCH"
mike deploy --alias-type copy "$V2_VERSION" "$V2_ALIAS" >/dev/null 2>&1

echo "==> Setting the default version to $DEFAULT_ALIAS"
mike set-default "$DEFAULT_ALIAS" >/dev/null 2>&1

echo "==> Extracting gh-pages and installing the legacy-link 404 handler"
rm -rf "$SERVE"; mkdir -p "$SERVE"
git archive gh-pages | tar -x -C "$SERVE"
cp "$REPO/scripts/gh-pages-404.html" "$SERVE/404.html"

echo
mike list
echo
cat <<EOF
==> Serving on http://localhost:$PORT/

  http://localhost:$PORT/                 redirects to the default version
  http://localhost:$PORT/latest/riddl/    RIDDL $V1_VERSION
  http://localhost:$PORT/next/riddl/      RIDDL $V2_VERSION (unreleased)

The version dropdown is in the header, left of the search box.

Note: python's http.server does not run the 404 handler, so a legacy
unversioned URL will show a plain 404 here rather than redirecting.
GitHub Pages does serve it.

Ctrl-C to stop.
EOF

cd "$SERVE"
exec python3 -m http.server "$PORT"
