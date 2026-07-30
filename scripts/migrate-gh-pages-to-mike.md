# Migrating gh-pages to mike

A one-time, supervised procedure. Run it when `release/2` merges to `main`, not
before. It restructures the `gh-pages` branch from a flat unversioned site into
mike's per-version layout.

Everything here was rehearsed against a throwaway clone of the real `gh-pages`
before being written down. Rehearse again before running it for real.

## Starting state

`gh-pages` holds a flat build at the root:

```
.nojekyll  404.html  CNAME  MCP  OSS  about  assets  coming-soon
index.html  riddl  search  sitemap.xml  sitemap.xml.gz  stylesheets  synapify
```

Live URLs are `.html`-style, not directory-style — the `offline` plugin in
`mkdocs.yml` sets `use_directory_urls: false`. For example
`https://ossum.tech/riddl/concepts/entity.html`. mike preserves this shape, so
the only thing that changes about a URL is the added version prefix.

## Ending state

```
.nojekyll  404.html  CNAME  versions.json  index.html
1.31/  latest/      <- RIDDL 1.x, built from docs/1.x
2.0/   next/        <- RIDDL 2.0, built from main
```

`index.html` is mike's redirect to the default version. `404.html` is
`scripts/gh-pages-404.html`, which rewrites legacy unversioned links.

## Procedure

### 1. Rehearse

```bash
git fetch origin gh-pages
SCRATCH=$(mktemp -d)
git clone --no-hardlinks . "$SCRATCH"
cd "$SCRATCH"
git branch gh-pages <sha-of-origin/gh-pages>   # a plain clone copies the
git remote remove origin                       # source repo's LOCAL refs,
                                               # which may be stale
```

Then run steps 2–5 there and inspect the result. Confirm `CNAME` and
`.nojekyll` survive — mike touches only version directories,
`versions.json`, and (on `set-default`) the root `index.html`.

### 2. Back up

```bash
git branch gh-pages-preversioning origin/gh-pages
git push origin gh-pages-preversioning
```

### 3. Clear the flat site, keeping the root files that must persist

```bash
git checkout gh-pages
git rm -r --quiet MCP OSS about assets coming-soon index.html riddl \
                  search sitemap.xml sitemap.xml.gz stylesheets synapify
git commit -m "Clear the flat unversioned site ahead of mike versioning"
```

Keep `CNAME` (custom domain — losing it takes the site down) and `.nojekyll`.
`404.html` is replaced in step 5.

### 4. Deploy both versions

!!! danger "`--alias-type copy` is required"
    mike's default alias type is **symlink**, and **GitHub Pages does not
    follow symlinks** — `/latest/…` would 404 in production while working
    perfectly under a local `python -m http.server`, which does follow them.
    A local rehearsal therefore cannot catch this; the flag must be passed.

```bash
git checkout docs/1.x && mike deploy --push --alias-type copy 1.31 latest
git checkout main     && mike deploy --push --alias-type copy 2.0  next
mike set-default --push latest
```

`latest` stays on 1.31 until RIDDL 2.0 actually ships. To flip it at release
time, change `aliases` in `docs-version.yml` on `main` from `next` to `latest`
and push; CI does the rest.

### 5. Install the legacy-link 404 handler

```bash
git checkout gh-pages
cp <repo>/scripts/gh-pages-404.html 404.html
git add 404.html
git commit -m "Redirect legacy unversioned links to the default version"
git push origin gh-pages
```

mike does not manage root files, so this survives every later deploy.

## Verify

```bash
curl -sSo /dev/null -w '%{http_code}\n' https://ossum.tech/                 # 200
curl -sS https://ossum.tech/versions.json                                    # both versions
curl -sSo /dev/null -w '%{http_code}\n' https://ossum.tech/latest/riddl/concepts/entity.html   # 200
curl -sSo /dev/null -w '%{http_code}\n' https://ossum.tech/next/riddl/concepts/entity.html     # 200
curl -sS https://ossum.tech/riddl/concepts/entity.html | grep -c DEFAULT_VERSION               # 404 handler served
```

In a browser: the version dropdown appears at the top of every page, lists both
versions, and the selection holds as you navigate — the version is part of the
path, so in-site links carry it.

## Rollback

```bash
git push --force origin gh-pages-preversioning:gh-pages
```

Then revert the `publish.yaml` change on `main` so CI goes back to
`mkdocs gh-deploy --force`.
