# Promoting RIDDL 2.0 to `latest`

Run this when RIDDL **2.0 final** ships. Until then, `latest` points at 1.31 —
which is correct, because `latest` must name the newest *released* version and
2.0 has been a release candidate.

Current state (as of the 2026-07-30 migration):

```
2.0  [next]      published from main
1.31 [latest]    published from docs/1.x
```

Target state:

```
2.0  [latest]    published from main
1.31             published from docs/1.x, no alias
```

---

## Read this first: the silent revert

**Two branches must never both declare `latest`.** The workflow deploys with
`--update-aliases`, which *moves* an alias to whatever version was deployed
most recently. So if `docs/1.x` still declares `latest` after you promote 2.0:

```
flip main            ->  2.0 [latest, next]   1.31
someone fixes a typo
   on docs/1.x       ->  2.0 [next]           1.31 [latest]   <-- reverted
```

The site silently goes back to serving 1.x as its default, months later,
triggered by an unrelated change. There is no error and nothing fails.

**Therefore: remove `latest` from `docs/1.x` BEFORE adding it to `main`.**

---

## Procedure

### 1. Take `latest` off docs/1.x — do this first

```bash
git checkout docs/1.x
```

Edit `docs-version.yml` to publish 1.31 with **no** alias:

```yaml
version: "1.31"
aliases: []
```

```bash
git commit -am "Release 1.31's claim on the latest alias, ahead of promoting 2.0"
git push origin docs/1.x
```

CI redeploys 1.31 without the alias. `latest` still exists and still points at
1.31 at this moment — nothing breaks, because removing a declaration does not
delete the alias.

### 2. Give `latest` to main

```bash
git checkout main
```

Edit `docs-version.yml`:

```yaml
version: "2.0"
aliases:
  - latest
```

```bash
git commit -am "Promote RIDDL 2.0 to the latest alias"
git push origin main
```

CI moves `latest` to 2.0. **The site's default is now 2.0.**

### 3. Retire the `next` alias

`next` meant "unreleased preview". Once 2.0 is final it is misleading, and it
will still be sitting in the version selector.

```bash
git fetch origin
git branch -f gh-pages "$(git rev-parse origin/gh-pages)"   # mike refuses if stale
mike delete --push next
```

### 4. Reword the outdated banner on main

`overrides/main.html` on `main` currently reads *"This is a preview of the
RIDDL 2.0 documentation. RIDDL 2.0 has not been released yet."*

Material shows that banner only when the build is **not** `latest`, so it
vanishes on its own the moment 2.0 is promoted — but it is baked into the
build, so it will reappear, wrong, the day 2.1 takes `latest`. Fix it now
while you are here:

```jinja
{% block outdated %}
  You are reading documentation for an older release of RIDDL.
  <a href="{{ '../' ~ base_url }}">
    <strong>Go to the latest version.</strong>
  </a>
{% endblock %}
```

### 5. Update the release-candidate install section

`docs/riddl/tools/riddlc/installation.md` says *"RIDDL 2.0 is being released
through a series of release candidates."* Keep the section — there will be
2.1 candidates — but reword the opening so it is not specific to 2.0, and
check that the "Once RIDDL 2.0 ships as a final release…" paragraph still
reads correctly.

---

## Verify

```bash
curl -sS https://ossum.tech/versions.json                       # 2.0 [latest], 1.31 bare
curl -sS https://ossum.tech/ | grep -o 'replace' -A2            # root -> latest/
curl -sSo /dev/null -w '%{http_code}\n' https://ossum.tech/latest/riddl/quickstart.html
curl -sSo /dev/null -w '%{http_code}\n' https://ossum.tech/next/riddl/quickstart.html   # expect 404
```

Then in a browser, confirm the selector lists `2.0 latest` and `1.31`, that
`/latest/` serves 2.0 content (`yield`, `initial state`), and that the 1.31
pages show the "older release" banner.

GitHub Pages rebuilds `gh-pages` in roughly 30 seconds; there is no long wait.

---

## Rollback

The pre-versioning backup is still on the remote:

```bash
git push --force origin gh-pages-preversioning:gh-pages
```

To undo only the promotion, reverse steps 1 and 2 — put `latest` back on
`docs/1.x`, remove it from `main`, and push `docs/1.x` **last** so it wins the
alias.

---

## Notes for later versions

The same procedure generalises. When 2.1 ships:

1. Remove `latest` from `main`'s `docs-version.yml` if 2.1 publishes from a
   different branch; otherwise just bump `version:` and keep the alias.
2. One mike version per RIDDL **minor** release, never per patch.
3. Whichever branch publishes the newest release owns `latest`, and **only**
   that branch may declare it.

Related: `scripts/migrate-gh-pages-to-mike.md` (the one-time restructure,
already done) and the Documentation Versioning section of `CLAUDE.md`.
