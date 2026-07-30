#!/usr/bin/env bash
#
# Copy the shared logo/image/CSS assets into every sub-site's docs tree.
#
# The site is built as four separate MkDocs projects (see
# migrate-to-per-product-versioning.md). MkDocs can only serve files from
# inside a project's `docs_dir`, so shared assets have to exist once per
# project. They are stored once in `common/` and copied in here; the copies
# are gitignored so there is exactly one editable original.
#
# Run this before any `mkdocs build` or `mkdocs serve`. CI runs it too.
# It is idempotent.
set -euo pipefail

REPO="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$REPO"

# Discovered rather than listed, because the set of sites differs by branch:
# `main` publishes the shell plus three products, while docs/1.x publishes only
# the riddl sub-site.
shopt -s nullglob
SITES=(sites/*/docs)
if (( ${#SITES[@]} == 0 )); then
  echo "sync-shared-assets: no sites/*/docs found -- wrong directory?" >&2
  exit 1
fi

for dest in "${SITES[@]}"; do
  # --delete so a removed shared asset does not linger in the copies.
  rsync -a --delete common/assets/      "$dest/assets/"
  rsync -a --delete common/stylesheets/ "$dest/stylesheets/"
  echo "synced -> $dest"
done
