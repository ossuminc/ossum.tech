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

SITES=(shell riddl riddlg synapify)

for site in "${SITES[@]}"; do
  dest="sites/$site/docs"
  if [[ ! -d $dest ]]; then
    echo "sync-shared-assets: no such site: $dest" >&2
    exit 1
  fi
  # --delete so a removed shared asset does not linger in the copies.
  rsync -a --delete common/assets/      "$dest/assets/"
  rsync -a --delete common/stylesheets/ "$dest/stylesheets/"
  echo "synced -> $dest"
done
