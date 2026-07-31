#!/usr/bin/env bash
#
# Build the whole site exactly as it will be deployed, and serve it locally.
#
# Why not `mike serve`? Because mike operates on THIS repository's gh-pages
# branch, so previewing would mutate it. This script clones into a scratch
# directory instead, so your working repository is never touched.
#
# What it produces is the real end state, not an approximation:
#   - every product deployed under its own prefix, with its own versions.json
#   - each product's aliases, created as COPIES (see the warning below)
#   - mike's <prefix>/index.html redirect to each product's default
#   - the unversioned shell at the root
#   - the legacy-link 404 handler from scripts/gh-pages-404.html
#
# Usage:
#   scripts/preview-versioned-site.sh [port]
#
set -euo pipefail

PORT="${1:-8800}"
REPO="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SCRATCH="${TMPDIR:-/tmp}/ossum-tech-preview"
SERVE="$SCRATCH/site"

command -v mike >/dev/null || { echo "mike not installed: pip install -r requirements.txt" >&2; exit 1; }

# Read docs-version.yml with the SAME interpreter mkdocs is installed under.
# The `python3` first on PATH is often a different install without pyyaml --
# on a Homebrew Mac mkdocs lives under python@3.9 while `python3` is 3.13.
PY="$(sed -n '1s|^#!||p' "$(command -v mkdocs)")"
[ -x "$PY" ] || PY=python3
"$PY" -c 'import yaml' 2>/dev/null || {
  echo "No python with pyyaml found (tried $PY)" >&2; exit 1; }

echo "==> Cloning $REPO into a scratch directory (your repo is not touched)"
rm -rf "$SCRATCH"
git clone --quiet --no-hardlinks "$REPO" "$SCRATCH/repo"
cd "$SCRATCH/repo"

# Detach first: a clone checks out the source repo's current branch, and git
# refuses to force-update a branch that a worktree has checked out.
git checkout --quiet --detach

# A plain clone copies the SOURCE repo's local refs, which may lag its
# remote-tracking refs. Prefer origin/ when it is ahead.
SRC_BRANCH="$(git -C "$REPO" rev-parse --abbrev-ref HEAD)"
git branch --quiet -f "$SRC_BRANCH" "$(git -C "$REPO" rev-parse HEAD)" 2>/dev/null || true
if git rev-parse --verify --quiet origin/gh-pages >/dev/null; then
  git branch --quiet -f gh-pages "$(git rev-parse origin/gh-pages)"
fi
git remote remove origin

echo "==> Clearing the previous layout from the gh-pages root"
if git rev-parse --verify --quiet gh-pages >/dev/null; then
  git checkout --quiet gh-pages
  for entry in $(git ls-tree --name-only gh-pages); do
    case "$entry" in
      CNAME|.nojekyll) ;;   # losing CNAME takes the site down
      *) git rm -rq --ignore-unmatch "$entry" ;;
    esac
  done
  git commit --quiet -m "preview: clear previous layout" 2>/dev/null || true
fi

git checkout --quiet "$SRC_BRANCH"
./scripts/sync-shared-assets.sh >/dev/null

# --alias-type copy is REQUIRED, not a preference. mike's default is `symlink`,
# and GitHub Pages does NOT serve symlinked content -- /riddl/latest/... would
# 404 in production. python's http.server DOES follow symlinks, so this
# preview would look perfect while production was broken. Keep the flag.
deploy() {  # prefix config version aliases...
  local prefix="$1" config="$2" version="$3"; shift 3
  echo "==> Deploying $prefix $version [$*]"
  # Output is captured rather than discarded: mike is chatty on success but its
  # failures are one line, and silencing both once hid a set-default error for
  # a full rehearsal cycle.
  local log; log="$(mktemp)"
  if ! DOCS_SITE_URL="https://ossum.tech/$prefix/$version/" \
       mike deploy --alias-type copy --deploy-prefix "$prefix" \
         -F "$config" "$version" "$@" >"$log" 2>&1; then
    echo "--- mike deploy failed for $prefix $version ---" >&2
    tail -20 "$log" >&2
    return 1
  fi
}

# RIDDL 1.31 no longer needs a branch checkout: it is sites/riddl-1x/ on this
# branch and comes through the ordinary loop below like every other entry
# (TASK G, 2026-07-31). The previous version of this script checked out
# docs/1.x here, deployed it, and switched back.

# Everything this branch declares.
while IFS='|' read -r prefix config version aliases; do
  [ -n "$prefix" ] || continue
  # shellcheck disable=SC2086
  deploy "$prefix" "$config" "$version" $aliases
  default="${aliases%% *}"; default="${default:-$version}"
  # -F is REQUIRED here, not just on deploy. set-default reads mkdocs.yml from
  # the working directory to resolve the remote and branch, and there is no
  # longer a config at the repo root -- it fails with "No such file or
  # directory: 'mkdocs.yml'".
  mike set-default --deploy-prefix "$prefix" -F "$config" "$default"
done < <("$PY" - <<'PY'
import yaml
cfg = yaml.safe_load(open("docs-version.yml"))
for s in cfg.get("sites") or []:
    print(f"{s['prefix']}|{s['config']}|{s['version']}|{' '.join(s.get('aliases') or [])}")
PY
)

echo "==> Building the unversioned shell"
SHELL_CFG=$("$PY" -c "import yaml;c=yaml.safe_load(open('docs-version.yml'));print((c.get('shell') or {}).get('config',''))")

echo "==> Extracting gh-pages and overlaying the shell + 404 handler"
rm -rf "$SERVE"; mkdir -p "$SERVE"
git archive gh-pages | tar -x -C "$SERVE"
if [ -n "$SHELL_CFG" ]; then
  DOCS_SITE_URL="https://ossum.tech/" mkdocs build -q -f "$SHELL_CFG" -d "$SCRATCH/shell"
  cp -r "$SCRATCH/shell/." "$SERVE/"
fi
# Copied last: the shell build emits its own 404.html and this one must win.
cp "$REPO/scripts/gh-pages-404.html" "$SERVE/404.html"

# Cross-site search, built exactly as CI builds it -- same script, so the
# preview exercises the real thing rather than an approximation.
"$REPO/scripts/build-search-index.sh" "$SERVE"

# robots.txt, generated from the deployed tree exactly as CI does it.
"$REPO/scripts/build-robots-txt.sh" "$SERVE"

echo
for p in riddl riddlg synapify; do
  [ -f "$SERVE/$p/versions.json" ] && printf '%-10s %s\n' "$p" "$(cat "$SERVE/$p/versions.json")"
done
cat <<EOF

==> Serving on http://localhost:$PORT/

  http://localhost:$PORT/                        the unversioned shell
  http://localhost:$PORT/about/privacy-policy/   exists ONCE, not per version
  http://localhost:$PORT/riddl/latest/           RIDDL
  http://localhost:$PORT/riddlg/latest/          riddlg
  http://localhost:$PORT/synapify/latest/        Synapify

Each product has its own version dropdown, listing only its own versions.

Note: python's http.server does not run the 404 handler, so a legacy URL
shows a plain 404 here rather than redirecting. GitHub Pages does serve it.
Check that mapping with: node scripts/test-404-redirects.js

Ctrl-C to stop.
EOF

cd "$SERVE"
exec python3 -m http.server "$PORT"
