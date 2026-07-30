# Migrating to per-product versioning

A one-time, supervised procedure. It splits the single MkDocs project into an
unversioned shell plus three independently-versioned sub-sites, and drops the
`offline` plugin so URLs go back to directory style.

Rehearse against a throwaway clone before running any of it for real. That is
how `CNAME`/`.nojekyll` survival was confirmed rather than assumed during the
previous migration, and this one is strictly larger.

## Why

`mike` versions a whole MkDocs *project*, not part of one. With one project,
RIDDL's version number ends up stamped on everything:

```
1.31/about/privacy-policy.html      2.0/about/privacy-policy.html
1.31/synapify/index.html            2.0/synapify/index.html
```

The privacy policy exists twice and must be fixed on two branches to be fixed
at both URLs. The Synapify docs carry a RIDDL version. riddlg is a third
independently-released product buried under `riddl/tools/`.

## Starting state

```
gh-pages/
  .nojekyll  404.html  CNAME  index.html  versions.json
  1.31/  latest/     <- RIDDL 1.31, from docs/1.x
  2.0/   next/       <- RIDDL 2.0,  from main
```

URLs are `.html`-style because `material/plugins/offline/plugin.py:41` forces
`use_directory_urls = False`. `mkdocs.yml` never sets it.

## Ending state

```
gh-pages/
  .nojekyll  404.html  CNAME  index.html  about/  coming-soon/  assets/
  riddl/     versions.json  1.31/ 2.0/ latest/ next/
  riddlg/    versions.json  0.6/  latest/
  synapify/  versions.json  0.2/  latest/
```

| Deployed at | Source | From |
|---|---|---|
| `/` | `sites/shell/` | `main`, unversioned |
| `/riddl/<ver>/` | `sites/riddl/` — riddl minus riddlg, plus OSS | `main`, `docs/1.x` |
| `/riddlg/<ver>/` | `sites/riddlg/` — riddlg plus MCP | `main` |
| `/synapify/<ver>/` | `sites/synapify/` | `main` |

MCP travels with riddlg because 21 of its 22 outbound links point at riddlg.

Example URL change:

```
before  /latest/riddl/concepts/entity.html
after   /riddl/latest/concepts/entity/
```

## Landmines

Read these before starting. Each has cost time before.

1. **`--alias-type copy` is required, per sub-site.** mike's default is
   `symlink` and **GitHub Pages does not serve symlinked content**, so
   `/riddl/latest/…` would 404 in production while working perfectly under a
   local `python -m http.server`, which *does* follow symlinks. A passing local
   rehearsal proves nothing about aliases.

2. **Never run `mike set-default` without `--deploy-prefix`.** Without one it
   writes a redirect to `gh-pages/index.html` — which now belongs to the shell.
   With one it writes `/<prefix>/index.html`, which is what you want.

3. **Two branches must never both declare the same prefix+alias.** The workflow
   deploys with `--update-aliases`, which *moves* an alias to the most recent
   deploy. If `docs/1.x` and `main` both declare `riddl`/`latest`, a later push
   to either silently drags the default. This is the same hazard
   `promote-2.0-to-latest.md` documents, now multiplied by the number of
   prefixes.

4. **`mike` refuses to act on a stale local `gh-pages`** ("gh-pages is unrelated
   to origin/gh-pages"). Sync the branch. Never reach for
   `--ignore-remote-status`, which clobbers the remote.

5. **`overrides/main.html:14` builds a URL by hand** — `{{ '../' ~ base_url }}`.
   That assumes the version segment sits one level below the site root.
   `use_directory_urls: True` puts every non-index page one level deeper, so
   this will point one level too high. Re-test it **on a deep page**, not the
   home page.

6. **`navigation.instant` is currently inert** — Material documents it as
   incompatible with `offline`. Removing the plugin makes it live for the first
   time, changing runtime navigation. Test it.

7. **mermaid loads from `unpkg.com`**; Material does not bundle it. Diagrams
   need a real browser to verify, never a build check.

## Procedure

### 1. Rehearse

```bash
git fetch origin gh-pages
SCRATCH=$(mktemp -d)
git clone --no-hardlinks . "$SCRATCH"
cd "$SCRATCH"
git branch -f gh-pages <sha-of-origin/gh-pages>   # a plain clone copies the
git remote remove origin                          # source repo's LOCAL refs,
                                                  # which may be stale
```

Run steps 3–7 there, drop `--push` from every mike command, and inspect.

### 2. Back up

```bash
git branch gh-pages-2026-07-preprefix origin/gh-pages
git push origin gh-pages-2026-07-preprefix
```

A **fresh** backup. `gh-pages-preversioning` predates the mike migration and
restoring it would discard everything deployed since.

### 3. Restructure sources on `main`

`git mv` into `sites/`. Depth must be preserved within each product or intra-
site relative links break; the only intended depth changes are riddlg
(`tools/riddlg/x.md` → `x.md`) and OSS/MCP, which gain a level.

```
sites/
  common.yml                 <- shared theme, extensions, palette
  shell/mkdocs.yml     docs/ <- index.md, about/, coming-soon/, CNAME
  riddl/mkdocs.yml     docs/ <- concepts/ guides/ … tools/ (no riddlg), OSS/
  riddlg/mkdocs.yml    docs/ <- index.md installation.md … , MCP/
  synapify/mkdocs.yml  docs/
```

Each `mkdocs.yml` starts `INHERIT: ../common.yml` (MkDocs 1.6). Shared assets
live once in `common/` and are copied into each site's `docs/` by
`scripts/sync-shared-assets.sh`; the copies are gitignored.

Remove `- offline` from the plugin list. Do **not** set `use_directory_urls` —
the MkDocs default is already `True`.

### 4. Rewrite cross-site links

79 cross-section relative links across ~30 files become cross-*site* and need
absolute URLs. Densest: `riddl/tools/riddl-mcp-server/index.md` (8),
`MCP/index.md` (6), `coming-soon/index.md` (6), `synapify/index.md` (5),
`about/index.md` (5). The seven `MCP/*` client guides follow a regular pattern
and script cleanly.

`validation.links` is already `warn`, so `--strict` turns every one that is
still relative into a build failure. **That is the completeness proof** — do not
hand-audit.

```bash
for s in shell riddl riddlg synapify; do
  echo "== $s"; mkdocs build --strict -f sites/$s/mkdocs.yml 2>&1 \
    | grep -E 'anchor|WARNING|ERROR'
done
```

### 5. Deploy the versioned sub-sites

```bash
git checkout docs/1.x
mike deploy --push --update-aliases --alias-type copy \
  --deploy-prefix riddl -F sites/riddl/mkdocs.yml 1.31 latest

git checkout main
mike deploy --push --update-aliases --alias-type copy \
  --deploy-prefix riddl -F sites/riddl/mkdocs.yml 2.0 next
mike deploy --push --update-aliases --alias-type copy \
  --deploy-prefix riddlg -F sites/riddlg/mkdocs.yml 0.6 latest
mike deploy --push --update-aliases --alias-type copy \
  --deploy-prefix synapify -F sites/synapify/mkdocs.yml 0.2 latest

mike set-default --push --deploy-prefix riddl     latest
mike set-default --push --deploy-prefix riddlg    latest
mike set-default --push --deploy-prefix synapify  latest
```

`riddl`'s `latest` stays on 1.31 until RIDDL 2.0 ships; see
`promote-2.0-to-latest.md`.

### 6. Deploy the shell and the 404 handler

The shell is not versioned, so mike is not involved. Build it and commit the
output to the `gh-pages` root, touching only the paths the shell owns — never
`riddl/`, `riddlg/`, `synapify/` or their `versions.json`.

```bash
mkdocs build -f sites/shell/mkdocs.yml -d /tmp/shell
git checkout gh-pages
cp -r /tmp/shell/{index.html,about,coming-soon,assets,stylesheets,search} .
cp -r /tmp/shell/{sitemap.xml,sitemap.xml.gz,CNAME} .
cp <repo>/scripts/gh-pages-404.html 404.html   # AFTER the copy: overwrites
git add -A && git commit -m "Deploy the unversioned shell"
git push origin gh-pages
```

`404.html` is copied last on purpose — the shell build emits its own and it
must lose. `.nojekyll` is never touched; nothing regenerates it, and losing it
breaks every underscore-prefixed asset silently.

### 7. Update the publishing workflow

`.github/workflows/publish.yaml` currently reads a flat `version`/`aliases`
pair and runs one `mike deploy` (`:37-53`). It becomes a loop over the sites
declared in `docs-version.yml`, plus the shell step. New schema:

```yaml
sites:
  - prefix: riddl
    config: sites/riddl/mkdocs.yml
    version: "2.0"
    aliases: [next]
  - prefix: riddlg
    config: sites/riddlg/mkdocs.yml
    version: "0.6"
    aliases: [latest]
shell:
  config: sites/shell/mkdocs.yml
```

On `docs/1.x` the file declares **only** the `riddl` site and no shell — the
shell and the non-RIDDL products publish from `main` alone.

## Verify

Build-level, before deploying:

```bash
for s in shell riddl riddlg synapify; do
  mkdocs build --strict -f sites/$s/mkdocs.yml 2>&1 | grep -E 'anchor|WARNING|ERROR'
done
```

On the rehearsal `gh-pages`, confirm root `CNAME` and `.nojekyll` survived all
four deploys, and that the three `versions.json` files are distinct:

```bash
git show gh-pages:CNAME
git ls-tree gh-pages --name-only
for p in riddl riddlg synapify; do git show gh-pages:$p/versions.json; done
```

After deploying, every row must be a 200:

```bash
for u in / /about/ /riddl/latest/concepts/entity/ /riddl/2.0/concepts/entity/ \
         /riddlg/latest/installation/ /synapify/latest/; do
  printf '%-42s ' "$u"; curl -sSo /dev/null -w '%{http_code}\n' "https://ossum.tech$u"
done
```

Then confirm the privacy policy exists **once**, not once per RIDDL version:

```bash
curl -sSo /dev/null -w '%{http_code}\n' https://ossum.tech/about/privacy-policy/       # 200
curl -sSo /dev/null -w '%{http_code}\n' https://ossum.tech/riddl/2.0/about/privacy-policy/  # 404
```

In a browser, which is the only way to check the rest:

- Redirect table in `gh-pages-404.html`, every row — the JS runs from a 404
  page, so `curl` sees 404 and cannot verify it.
- The version selector on each product lists **only that product's** versions.
- The outdated banner links correctly **from a deep page** (landmine 5).
- `navigation.instant` still navigates (landmine 6).
- Diagrams render (landmine 7).

## Rollback

```bash
git push --force origin gh-pages-2026-07-preprefix:gh-pages
```

Then revert the `publish.yaml` and `docs-version.yml` changes on `main` and
`docs/1.x`, or the next push re-runs the migration.
