# Promoting RIDDL 2.0 to `latest`

Run this when RIDDL **2.0 final** ships. Until then, `latest` points at 1.31 —
which is correct, because `latest` must name the newest *released* version and
2.0 has been a release candidate.

Current state (since TASK G, 2026-07-31 — everything publishes from `main`):

```
riddl/2.0  [next]      sites/riddl/       docs-version.yml entry 1
riddl/1.31 [latest]    sites/riddl-1x/    docs-version.yml entry 2
```

Target state:

```
riddl/2.0  [latest]    sites/riddl/       entry 2  <- note the swap
riddl/1.31             sites/riddl-1x/    entry 1, no alias
```

Only the **riddl** prefix is involved. riddlg and Synapify have their own
version axes and their own `latest`; nothing here touches them.

---

## This used to be dangerous. It is not any more.

**Historical note, so nobody reintroduces the old dance.** When 1.31 published
from a `docs/1.x` branch, the two branches could both declare `latest`, and
because the workflow deploys with `--update-aliases` — which *moves* an alias
to whatever was deployed most recently — a later push to the wrong branch would
silently revert the site default months afterwards, with no error. The old
procedure therefore had a mandatory ordering: strip the alias from one branch,
push, then add it to the other.

Both entries now live in one file on one branch, so **there is no ordering
constraint and no race.** The promotion is a single commit.

**The one rule that survives:** `mike set-default` runs once per entry, so the
**last `riddl` entry** in `docs-version.yml` decides where `/riddl/` redirects.
Swap the order of the two entries as well as the alias, or `/riddl/` will keep
redirecting to whatever the last entry names.

---

## Procedure

### 1. Move the alias — one commit

Edit `docs-version.yml`: move `latest` from the 1.31 entry to the 2.0 entry,
**and put the 2.0 entry last**. Leave riddlg and synapify alone.

```yaml
sites:
  - prefix: riddl
    config: sites/riddl-1x/mkdocs.yml
    version: "1.31"
    aliases: []

  # Last riddl entry wins `mike set-default`, so /riddl/ -> latest -> 2.0
  - prefix: riddl
    config: sites/riddl/mkdocs.yml
    version: "2.0"
    aliases:
      - latest
```

Update `VERSION_SOURCE` in `scripts/check-cross-site-links.py` in the same
commit, so `latest` resolves against `sites/riddl/` rather than
`sites/riddl-1x/`:

```python
"1.31": "riddl-1x",
"latest": "riddl",     # was riddl-1x
```

```bash
git commit -am "Promote RIDDL 2.0 to the latest alias"
git push origin main
```

CI moves `latest` to 2.0 and redeploys 1.31 without an alias. **The site's
default is now 2.0.**

### 3. Retire the `next` alias

`next` meant "unreleased preview". Once 2.0 is final it is misleading, and it
will still be sitting in the version selector.

```bash
git fetch origin
git branch -f gh-pages "$(git rev-parse origin/gh-pages)"   # mike refuses if stale
# --deploy-prefix picks the right versions.json; -F is needed too, because
# mike reads mkdocs.yml from the working directory to resolve the branch and
# there is no config at the repo root any more.
mike delete --push --deploy-prefix riddl -F sites/riddl/mkdocs.yml next
```

### 4. Reword the outdated banner on main

`sites/riddl/mkdocs.yml` on `main` currently declares *"This is a preview of
the RIDDL 2.0 documentation. RIDDL 2.0 has not been released yet."*

Material shows that banner only when the build is **not** `latest`, so it
vanishes on its own the moment 2.0 is promoted — but it is baked into the
build, so it will reappear, wrong, the day 2.1 takes `latest`. Fix it now
while you are here:

```yaml
extra:
  outdated_banner: >-
    You are reading documentation for an older release of RIDDL.
```

It belongs in the site's own config, **not** in `overrides/main.html`: that
directory is `custom_dir` for every sub-site, so a message hard-coded there
appears on Synapify and riddlg too.

### 5. Update the release-candidate install section

`sites/riddl/docs/tools/riddlc/installation.md` says *"RIDDL 2.0 is being released
through a series of release candidates."* Keep the section — there will be
2.1 candidates — but reword the opening so it is not specific to 2.0, and
check that the "Once RIDDL 2.0 ships as a final release…" paragraph still
reads correctly.

---

## Verify

```bash
curl -sS https://ossum.tech/riddl/versions.json                  # 2.0 [latest], 1.31 bare
curl -sS https://ossum.tech/riddl/ | grep -o 'replace' -A2       # prefix root -> latest/
curl -sSo /dev/null -w '%{http_code}\n' https://ossum.tech/riddl/latest/quickstart/
curl -sSo /dev/null -w '%{http_code}\n' https://ossum.tech/riddl/next/quickstart/   # expect 404

# The other products must be untouched by this.
curl -sS https://ossum.tech/riddlg/versions.json                 # unchanged
curl -sS https://ossum.tech/synapify/versions.json               # unchanged
```

Then in a browser, confirm the RIDDL selector lists `2.0 latest` and `1.31`,
that `/riddl/latest/` serves 2.0 content (`yield`, `initial state`), and that
the 1.31 pages show the "older release" banner.

GitHub Pages rebuilds `gh-pages` in roughly 30 seconds; there is no long wait.

---

## Rollback

The pre-versioning backup is still on the remote:

```bash
git push --force origin gh-pages-preversioning:gh-pages
```

To undo only the promotion, revert the single commit and push. There is no
branch ordering to get right any more.

---

## Notes for later versions

The same procedure generalises. When 2.1 ships:

1. Add a `sites/riddl-2x/`-style entry only if 2.0 must stay maintained
   separately; otherwise bump `version:` on the existing entry and keep the
   alias.
2. One mike version per RIDDL **minor** release, never per patch.
3. Whichever entry names the newest release owns `latest`, and it must be the
   **last** entry for its prefix so `set-default` lands on it.
4. Keep `VERSION_SOURCE` in `scripts/check-cross-site-links.py` in step with
   this file — it maps each version and alias to the source tree that builds
   it, and nothing else enforces the correspondence.
5. Aliases belong to ONE prefix. `riddl/latest` and `riddlg/latest` are
   different aliases in different `versions.json` files and never interact.

Related: `scripts/migrate-to-per-product-versioning.md` (the current layout)
and the Documentation Versioning section of `CLAUDE.md`.
`scripts/migrate-gh-pages-to-mike.md` describes the earlier flat-to-versioned
move and is kept only for the record.
