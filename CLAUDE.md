# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with
code in this repository.

## Project Overview

**ossum.tech** is the technical documentation website for Ossum Inc., built
with [MkDocs Material](https://squidfunk.github.io/mkdocs-material/). The
primary focus is documenting the RIDDL language and its ecosystem of tools.

### Repository Structure

```
ossum.tech/
├── docs/                    # All documentation content (Markdown)
│   ├── riddl/               # RIDDL language documentation
│   │   ├── introduction/    # What is RIDDL, why it exists
│   │   ├── concepts/        # RIDDL language concepts (domain, context, etc.)
│   │   ├── guides/          # User guides by role (authors, domain experts, etc.)
│   │   ├── examples/        # Model gallery linking to riddl-models repo
│   │   ├── playground/      # Interactive RIDDL editor (coming soon)
│   │   ├── references/      # Language reference and EBNF grammar
│   │   ├── tools/           # Documentation for riddlc, IDE plugins, etc.
│   │   └── future-work/     # Planned features and roadmap
│   ├── MCP/                 # RIDDL MCP Server documentation
│   ├── OSS/                 # Open source tools documentation
│   ├── synapify/            # Synapify visual editor docs
│   ├── stylesheets/         # Custom CSS (includes RIDDL syntax colors)
│   └── about/               # Company info, privacy policy
├── riddl_lexer/             # Custom Pygments lexer for RIDDL syntax highlighting
│   ├── __init__.py          # Package exports
│   ├── lexer.py             # Token definitions and regex patterns
│   └── style.py             # Color scheme matching IDE tools
├── overrides/               # MkDocs theme customizations
├── mkdocs.yml               # MkDocs configuration
├── pyproject.toml           # Python package config for riddl_lexer
└── .github/workflows/       # CI/CD (publishes to GitHub Pages)
```

### Key Documentation Files

When working on RIDDL-related tasks, these files are essential context:

- **EBNF Grammar**: `docs/riddl/references/ebnf-grammar.md`
- **Language Reference**: `docs/riddl/references/language-reference.md`
- **Concepts Index**: `docs/riddl/concepts/index.md`

### Reactive BBQ Tutorial Structure

The tutorial at `docs/riddl/tutorials/rbbq/` is a comprehensive
case study with 30 pages based on the actual RIDDL model in
`riddl-models/hospitality/food-service/reactive-bbq/`. All RIDDL
code blocks are verbatim from the model source.

```
rbbq/
├── index.md              # Landing page
├── scenario.md           # Business challenge
├── reactive-bbq.md       # Top-level domain model
├── patterns.md           # 7 cross-cutting patterns
├── external-contexts.md  # 6 third-party integrations
├── restaurant/           # 6 context pages + index
├── backoffice/           # 3 context pages + index
├── corporate/            # 3 context pages + index
└── personas/             # 9 persona interviews + index
```

Each context page follows a consistent structure: Purpose,
Interview Connection, Types, Entity, Repository, Projector
(if applicable), Adaptors, Design Decisions, Source links.
The source links point to `riddl-models` (not `riddl-examples`).

---

## Build and Development

### Prerequisites

- Python 3.8+ with pip
- MkDocs Material: `pip install mkdocs-material`

### Local Development

```bash
# Install build dependencies (mkdocs-material, mike)
pip install -r requirements.txt

# Install the RIDDL lexer for syntax highlighting
pip install -e .

# Serve locally with hot reload
mkdocs serve

# Build static site
mkdocs build --strict

# Preview the versioned site as deployed
mike serve
```

The site will be available at `http://localhost:8000` when serving locally.

**Do not run `mkdocs gh-deploy`.** The site is versioned with `mike`; a
`gh-deploy` would flatten the version structure. CI runs
`mike deploy --push --update-aliases` instead.

---

## Documentation Versioning

**The site is four MkDocs projects, not one.** `mike` versions a whole project,
so a single project meant every product carried RIDDL's version number — the
privacy policy existed once per RIDDL version, and the Synapify docs were
stamped `2.0`. Each product now deploys under its own prefix with its own
`versions.json` and its own version selector.

| Deployed at | Source | Version |
|---|---|---|
| `/` | `sites/shell/` — landing, About, **IDE help** | **unversioned** |
| `/riddl/2.0/` | `sites/riddl/` — the 2.0 language docs | 2.0 · `next` |
| `/riddl/1.31/` | `sites/riddl-1x/` — the 1.x maintenance line | 1.31 · `latest` |
| `/riddlg/<ver>/` | `sites/riddlg/` — riddlg plus the `MCP/` guides | 0.6 · `latest` |
| `/synapify/<ver>/` | `sites/synapify/` | 0.17 · `latest` |

**Everything publishes from `main`.** Two source trees share the `riddl`
prefix, which is why the 1.x line is a *directory* and not a branch: as
`docs/1.x` it needed every change to the shared chrome replicated by hand, and
12 of that branch's 17 commits were exactly that. Forgetting was invisible —
each branch built correctly on its own terms, so nothing in CI could catch it.
See TASK G in NOTEBOOK.md.

That branch was deleted on 2026-07-31. **Do not restore it to publish from:** it
carries its own `publish.yaml` that still triggers on `docs/1.x`, so a push
would redeploy 1.31 with the pre-consolidation chrome and look like a perfectly
normal successful deploy.

### Branches, and where the deleted ones went

Only **`main`** and the `gh-pages` family remain. Retired branches were tagged
before deletion, so their history is still reachable: `git log archive/<name>`
and `git show archive/<name>:<path>` both work.

| Tag | Was | Superseded by |
|---|---|---|
| `archive/docs-1.x` | the RIDDL 1.x publishing branch | `sites/riddl-1x/` |
| `archive/riddl-guides-author` | 2025-03 Hugo-era author guide | `guides/authors/`, `references/` |
| `archive/riddl-guides-developers` | 2025-03 Hugo-era developer guide | the current guides |
| `archive/reid-spencer-patch-1` | one attribution commit | already in `main`, with its `$$$`/"SPencer" typos fixed |

**`gh-pages-2026-07-preprefix` is load-bearing — do not delete it.** It is not
an ancestor of `gh-pages`, so its state is unreachable from that history, and
it is the rollback target for the per-product versioning migration.
`gh-pages-preversioning` *is* an ancestor, so it is only a convenience marker.

Order in `docs-version.yml` matters for one thing: `mike set-default` runs per
entry, so the **last `riddl` entry decides where `/riddl/` redirects**. Keep
the entry holding `latest` last.

One documentation version per product **minor** version, never per patch.

The MCP guides live with riddlg, not with the language docs, because 21 of
their 22 outbound links point at riddlg — they document the server riddlg
drives, so they version with it.

`docs-version.yml` is where `main` declares what it publishes; the release-time
alias flip is an edit there, not a workflow change. **Only `main` publishes**,
so work branches can be pushed freely.

Shared theme config lives in `sites/common.yml`, pulled in with `INHERIT`.
Shared logos and CSS live once in `common/` and are copied into each site by
`scripts/sync-shared-assets.sh` — **run it before any build**, or every page
loses its stylesheet. The copies are gitignored.

### Search: two fields, on purpose

| Field | Covers | Built by |
|---|---|---|
| The box in the title bar | that site **and version** only | Material, per build |
| **Full Search**, directly below it | **all products at once** | Pagefind, `scripts/build-search-index.sh` |

The second is **additive** — Material's box is untouched, so version-scoped
search still works. An earlier design replaced it, which would have meant a
reader on the 1.31 pages getting 2.0 answers with no way to search 1.31.

Full Search is rendered from `overrides/main.html` into Material's
`{% block hero %}`. That block is empty and officially supported, and because
`navigation.tabs.sticky` is on, Material renders the tabs inside the header
partial and leaves `{% block tabs %}` emitting nothing — so `hero` lands
directly beneath the *whole* sticky header. Getting the same placement by
copying `partials/search.html` would pin this repo to one Material release.

The Pagefind loader lives in `extrahead`, not in `hero`, because there are two
mount points: the bar, and the About page's own copy which sits with the prose
explaining what each field covers. The bar is suppressed on About.

Material builds one search index per MkDocs project, so its search can never
span the four sites — a reader in the RIDDL docs searching "Synapify" gets
nothing. Pagefind indexes **built HTML** instead of sources, so it does not
care how many projects produced the tree. It runs last, over the assembled
`gh-pages` content, and writes `/pagefind/` at the root.

Two things about the index that are deliberate:

- **It covers each product's `latest` alias only**, plus the shell pages (Home,
  About, IDE help). mike
  deploys aliases as full *copies*, so indexing everything would return each
  page three or four times. Following the alias rather than a pinned version
  means no edit is needed when 2.0 is promoted.
- **Older versions are therefore not globally searchable.** That is the
  trade-off, not an oversight; each version's own search box still works.

Material's `toc.permalink` pilcrow is excluded, or every sub-result reads
"Purpose¶". The header link to `/find/` is injected from `overrides/main.html`
because Material has no block for adding a header item and copying
`partials/header.html` would pin the repo to one Material release.

### Crawlers and duplicate versions

`robots.txt` is **generated** at deploy time by `scripts/build-robots-txt.sh`,
because its job is to list the sitemaps and the set of them changes with every
release: each build writes its own `sitemap.xml` inside its own version
directory, and nothing at the root references them.

It blocks nothing except `/pagefind/`. Version/alias duplication is handled by
**`rel=canonical`**, not by hiding pages: each build is built once with its own
version's `site_url`, so the pages inside an alias copy carry a canonical
pointing at the real version directory — `/riddl/next/…` canonicalises to
`/riddl/2.0/…`. Alias sitemaps are skipped because a copied sitemap is
byte-identical to the one already listed.

This relies on `DOCS_SITE_URL` being set per deploy. Without it every build
would claim `https://ossum.tech/` as its canonical and the site would tell
crawlers that every version of every page is the same URL.

### Things that will bite

- **`mike` aliases must be `--alias-type copy`.** The default is `symlink`, and
  GitHub Pages does not serve symlinked content, so `/riddl/latest/…` 404s in
  production. A local `python -m http.server` rehearsal DOES follow symlinks
  and so cannot catch it. The workflow passes the flag; keep it.
- **Never run `mike set-default` without `--deploy-prefix`.** Without one it
  writes a redirect over `gh-pages/index.html`, which is the shell's landing
  page.
- **Two branches must never declare the same prefix AND alias.** See the
  release section below.
- **`mkdocs build --strict` does NOT fail on dangling intra-page anchors.** It
  reports them at INFO level and exits 0. Always verify with:
  ```bash
  mkdocs build --strict -f sites/<site>/mkdocs.yml 2>&1 | grep -E 'anchor|WARNING|ERROR'
  ```
- **`--strict` says nothing about cross-site links.** They are absolute, so
  MkDocs treats them as external and never checks them. `scripts/check-cross-site-links.py`
  covers them; run it alongside the strict builds.
- **`pagefind[bin]`, not `pagefind`.** The bare package is only the Python API
  wrapper and fails at run time with "Could not find pagefind binary".
- **A broken `--8<--` include renders as NOTHING, silently**, and `--strict`
  stays quiet. The EBNF grammar page shipped completely empty this way.
  `check_paths: true` in `sites/common.yml` makes it fail loudly — keep it on.
- **Live URLs are directory-style** (`/riddl/latest/concepts/entity/`). The
  `offline` plugin, which forced `use_directory_urls: false`, has been removed.
  `scripts/gh-pages-404.html` maps the two older URL shapes onto the current
  one; it lives at the `gh-pages` root, which mike does not manage.
- **The 404 handler cannot be verified with `curl`.** GitHub Pages serves it
  with a 404 status and the rewrite happens in the browser, so every legacy URL
  looks like a failure from the command line either way. Use
  `node scripts/test-404-redirects.js`.
- **Do not judge a deploy by `curl`ing the live site straight afterwards.**
  ossum.tech is served with `cache-control: max-age=600`, and the CDN routinely
  populates from the origin *before* Pages finishes publishing — so for up to
  ten minutes the old content comes back and the deploy looks like it silently
  failed. A `?cachebust=` query does **not** reliably defeat it, and neither do
  `Cache-Control: no-cache` request headers. This produced three false alarms in
  one session.
  **Check `gh-pages` instead — that is the authority:**
  ```bash
  git fetch origin gh-pages
  git show origin/gh-pages:riddl/2.0/index.html | grep -c 'the thing you changed'
  ```
  Then, if you want live confirmation, poll until it flips rather than
  concluding from one request:
  ```bash
  until curl -s https://ossum.tech/<path> | grep -q 'the thing'; do sleep 20; done
  ```
- **`overrides/` is `custom_dir` for all four sites.** Anything product-specific
  hard-coded there appears on every site — that is how the Synapify docs briefly
  announced themselves as a preview of RIDDL 2.0. The outdated banner's wording
  comes from `extra.outdated_banner` per site.
- **mermaid loads from a CDN** (`unpkg.com`); Material does not bundle it. A
  diagram can only be verified in a real browser, never by a build check.
- **A rendered mermaid diagram is INVISIBLE to page JavaScript.** Material puts
  the SVG in a *closed* shadow root (`r.attachShadow({mode:"closed"})`), so
  `document.querySelector(".mermaid svg")` returns null and `.textContent`
  returns `""` **even when the diagram is rendering perfectly**. Verify with a
  screenshot, or by the element's height — an unrendered block is ~0px. Do not
  conclude from an empty query that mermaid is broken; that reads as a
  site-wide regression and is not one.
- **This machine has mkdocs-material Insiders; CI installs the community
  edition.** Do not use Insiders-only features.
- **ALWAYS refresh the grammar with `sbt extractGrammar`. Never `cp` it.**
  The task resolves the riddl version pinned in `build.sbt`, so its output is
  reproducible and provably matches a real build:

  ```bash
  # 1. point build.sbt at the same version as ../bin/riddlc
  #    With.Riddl.library(version = "<what `riddlc version` prints>")
  # 2. then
  sbt extractGrammar
  ```

  Bumping the pin may require bumping `With.Scala3` to whatever riddl built
  with — the two lines in `build.sbt` are commented to stay in step.

  **Regenerate the grammar LAST, after the fences are green — or verify it
  again before committing.** `git checkout -- sites/riddl/docs` reverts the
  regenerated grammar along with everything else, and a fence migration
  routinely needs one. On 2026-08-25 the rc.24-33 upgrade did exactly that:
  two reverts during the migration undid `extractGrammar`, nothing re-ran it,
  and the commit shipped **rc.21's grammar** under a message claiming it was
  regenerated. Nothing caught it — the gate validates fences against the
  BINARY, never against the .ebnf, so a stale grammar is invisible to every
  check in this repo. Found only because the next upgrade's diff was
  suspiciously identical to the previous one's.

  Cheapest check, before any upgrade commit:

  ```bash
  git log --oneline -1 -- sites/riddl/docs/references/riddl-grammar.ebnf
  ```

  If that names an older upgrade than the one in flight, `extractGrammar` did
  not survive. Same family as every other trap here: the signal that something
  was skipped is ABSENT rather than wrong.

  **The sbt build exists only for this task** — it produces no site content
  and is on no CI publishing path. It is **sbt 2.0.6** (bumped from 2.0.2 on
  2026-08-10 to clear a critical vulnerability), sbt-ossuminc 3.1.0, and
  **Scala 3.9.0-RC4**. The RC compiler is required; see NOTEBOOK.md TASK F
  before "fixing" it to a release version.

  **`cp` from `../riddl/.../ebnf-grammar.ebnf` is NOT a fallback.** That path
  is a live working tree: on 2026-08-08 it held an uncommitted `yields`/
  `replies` split present in no commit and no build, so a copy would have
  documented a language that does not exist — and looked perfectly successful.
  A `cp` is right only by luck of timing.

  (Historical note, so this is not "corrected" back: a warning here used to say
  extractGrammar resolves a *published 1.x* library and would clobber the 2.0
  grammar. That was true when the pin was 1.29.0. The pin has been a real 2.0
  build for some time, snapshot builds land in the local cache via riddl's
  `publishLocal`, and the stale warning is what caused the `cp` above.)

### When RIDDL 2.0 ships final

`latest` currently points at **1.31**, which is correct while 2.0 is a release
candidate. Promoting it is a short procedure with one landmine, written up in
**`scripts/promote-2.0-to-latest.md`**.

**The old landmine is gone.** It used to be that two branches must never both
declare `latest`, because `--update-aliases` *moves* the alias to the most
recent deploy — so a later push to `docs/1.x` could silently drag the site's
default back to 1.x, months later, from an unrelated typo fix, with no error.
Since both RIDDL lines publish from `main` (TASK G), one branch cannot race
itself: promotion is moving `latest` from the 1.31 entry to the 2.0 entry in
`docs-version.yml`, in a single commit.

The one ordering rule that remains: `mike set-default` runs once per entry, so
the **last `riddl` entry** in that file decides where `/riddl/` redirects. Move
the entries, not just the alias, if you want `/riddl/` to follow.

### Migrating gh-pages

Two migrations, both one-time and supervised, both rehearsed against a
throwaway clone before being run — that is how `CNAME`/`.nojekyll` survival was
confirmed rather than assumed.

- `scripts/migrate-gh-pages-to-mike.md` — **historical, already executed.** It
  describes the flat-to-versioned move and still documents `.html` URLs. Do not
  follow it; it is kept for the record.
- `scripts/migrate-to-per-product-versioning.md` — the current layout. Read its
  landmines section before touching deployment.

### Verifying RIDDL code blocks

`scripts/check-riddl-blocks.py` scans every ` ```riddl ` fence for retired 1.x
constructs. It is advisory (exit 0 unless `--strict`), because many fences are
deliberate fragments.

```bash
python3 scripts/check-riddl-blocks.py docs
```

Counter-examples are suppressed by a trailing comment on the offending line —
`// fails to parse`, `// invalid`, `// deprecated` — so a page can teach a rule
by showing what it forbids.

### Compiling RIDDL examples

`scripts/validate-riddl-examples.py` runs each ` ```riddl ` fence through a
**real riddlc**, which is the only way to know an example works. Unlike the
checker above it is a **gate**: it exits non-zero on failure.

**Point each tree at its own compiler.** Both live on `main` now, so nothing
about the checkout tells you which one is meant — and the `riddlc` on PATH is
neither of them any more, so the wrong pairing reports confident nonsense.

**`../bin/riddlc` is the 2.0 compiler** — since 2026-08-12 a **native binary
installed directly at that path**; `../riddlc-dist/` is gone, so the old
symlink description no longer holds. The Homebrew `riddlc` on PATH lags it
badly — verified 2026-08-26: PATH is **2.0.0-rc.5** while `../bin` is
**2.0.0-rc.25-1-76cb9eab**, one commit PAST the rc.25 tag. rc.9
deprecated the entity options, so validating the 2.0 docs with the PATH binary
silently passes examples the real compiler rejects. Run both and compare;
never assume.

**The staged binary is USUALLY not a clean tag, and the clean tag usually does
not resolve.** rc.20, rc.24 and rc.25 were each staged one-to-thirty-three
commits past their tag, with only the staged version's JVM `_3` artifacts in
`~/.ivy2/local`. So `build.sbt` pins the exact `git describe` version — asking
for "rc.25" and pinning `2.0.0-rc.25` would fail to resolve AND describe a
different build than the gate runs. Check all three separately (tag, binary,
artifact) and pin what is staged.

**A tag in `riddl` means neither a staged binary nor a resolvable artifact.**
These three drift apart and must be checked separately: the tag, what
`../bin/riddlc version` prints, and what actually resolves from
`~/.ivy2/local`. On 2026-08-10 `2.0.0-rc.11` was tagged with only its JS and
Native artifacts published — the JVM `_3` ones were reachable nowhere, so
`With.Riddl.library(version = "2.0.0-rc.11")` failed to resolve and
`extractGrammar` could not run, while the staged binary was two commits *before*
the tag. All three were reconciled on 2026-08-11 and the pin is now
`2.0.0-rc.11` exactly. The lesson stands even though that instance is
resolved: an upgrade request is not evidence that any of the three has moved.

```bash
# 2.0 -- sites/riddl/, validated by the STAGED compiler, not the one on PATH
python3 scripts/validate-riddl-examples.py ../bin/riddlc \
  sites/riddl/docs/quickstart.md

# 1.31 -- sites/riddl-1x/, validated by the 1.31 build, NOT the one on PATH
python3 scripts/validate-riddl-examples.py \
  /opt/homebrew/Cellar/riddlc/1.31.0/bin/riddlc \
  sites/riddl-1x/docs/quickstart.md
```

Most fences are **fragments** and cannot validate as written, so each declares
how to be made whole with an HTML comment above it. HTML comments do not
render, so readers never see them:

| Directive | Wraps the fence in |
|-----------|--------------------|
| `<!-- riddl: standalone -->` | nothing — a complete model (the default) |
| `<!-- riddl: in-domain -->` | `domain Example is { … }` |
| `<!-- riddl: in-context -->` | a domain and a context |
| `<!-- riddl: in-entity -->` | a domain, context and entity |
| `<!-- riddl: skip -->` | not validated |

A page may declare a `<!-- riddl-prelude ... -->` block of definitions that its
fragments reference but do not show. It lands at **context** level whatever the
wrapper's depth.

Domain-level vocabulary is a **separate** `<!-- riddl-domain-prelude ... -->`
block, read only by `in-domain`. The two cannot be one block — a `user` is
legal only in a domain, a `record` only in a context. It is what makes
whole-`context` fences gateable: a domain body may hold type definitions, and a
bare name resolves upward and across sibling contexts, so a sibling context in
the domain prelude can supply outlets and events a fence names but never
declares.

A fence that defines a name a prelude also supplies must say
`no-prelude=Name`. This applies to **both** preludes by the same names.

`--auto` tries every wrapping and reports a fence only if none works. It is a
*measurement* mode for pages that do not yet carry directives — not a
substitute for them.

**The gate covers ALL of `sites/riddl/docs` as of 2026-08-10** — every page
carrying at least one `<!-- riddl: -->` directive, which is now every page that
has RIDDL in it. It takes files, not directories. Run it exactly like this, or
a reported number cannot be compared with the last one:

```bash
# 2.0 -- the WHOLE tree, not just annotated pages (see Status below for why)
python3 scripts/validate-riddl-examples.py ../bin/riddlc \
  $(find sites/riddl/docs -name '*.md' | sort) > /tmp/gate.txt 2>&1
echo "EXIT=$?"; tail -2 /tmp/gate.txt

# 1.31 -- same shape over sites/riddl-1x/docs, with the 1.31 compiler
```

**Do not pipe it into `tail`** — `$?` then reports `tail`'s status and a red
gate reads green. Redirect to a file, check `$?`, then read the file.

**Status** (2026-08-26, rc.25-1): the whole 2.0 tree is **366 validated / 51
skipped / 0 failed**, and **every blanket skip is gone** — both the 118
`"illustrative fragment"` ones and the 73 `tutorials/rbbq/` ones. Every
remaining skip states its own reason.

**Run the gate over the whole tree, not over "files with a directive".** The
old scope was `grep -rl '<!-- riddl:'`, which silently excluded any page that
had never been annotated — and three such pages existed while CLAUDE.md
claimed every RIDDL-bearing page was covered (`tutorials/basics.md`,
`guides/authors/design/contexts.md`,
`introduction/what-is-riddl-based-on.md`). All three failed the moment they
were included. A scope defined by "has an annotation" can never report a
missing annotation:

```bash
python3 scripts/validate-riddl-examples.py ../bin/riddlc \
  $(find sites/riddl/docs -name '*.md' | sort) > /tmp/gate.txt 2>&1
echo "EXIT=$?"; tail -2 /tmp/gate.txt
```

Gating `language-reference.md` found seven wrong examples that review had not
— including an adaptor that violated the isolation-seam rule warned about
immediately below it. All are fixed.

**The RBBQ tutorial is authored, not quoted** (2026-08-21). Its fences used to
be excused as "quoted verbatim from riddl-models, which is still RIDDL 1.x".
riddl-models is clean on rc.20, so that was false — but re-quoting was never
possible either: the model carries `briefly`/`described as` on nearly every
field and is **20,882 lines against the tutorial's 2,069**, roughly 10:1.
`KitchenTicket.riddl` alone is 901 lines where the fence is 70. Each fence is
now a condensed 2.0 excerpt whose structure comes from the source and whose
correctness comes from the gate. **When the model moves, re-derive the
excerpt; do not paste the source in.** `scripts/` has no tool for this; the
session used a throwaway metadata-stripper to read structure at a readable
size.

**Wrapper vocabulary is only ever ADDED — and that rule covers fields, NOT
enumerations.** An enumeration's enumerators join the enclosing namespace, so a
wrapper-level `any of { Pending, Shipped }` collides with any page naming a
state `Shipped`. Put enumerations in the page prelude. Likewise **no prelude
entry may depend on another that a fence might strip** with `no-prelude`, or
that fence loses both.

**More prelude rules, each found by a gate failure pointing somewhere else:**

- **A prelude entry must fit on ONE line.** `no-prelude` withholds an entry by
  removing its first line only, so a wrapped alternation leaves an orphan
  `| More | Members` behind and the parse error lands far from the cause.
- **A prelude may not declare an alternation over messages that live INSIDE an
  entity.** The prelude can only stub the entity, so the members do not
  resolve. Only the entity's own fence should declare that alternation.
- **A `projector X is { ??? }` stub is not valid at all** — a projector
  requires a record and exactly one handler. Entities and repositories stub
  fine; projectors cannot, so nothing may reference one from a prelude.
- **A prelude event redeclared inside an event-sourced entity is ambiguous**,
  and it surfaces as the *event-sourcing* rule — "handles an event declared
  outside it" — rather than as ambiguity. Withhold the prelude copy by name.
- **A `with { }` block's `described as { |… }` needs its content on its own
  lines.** The one-line form does not parse and the error points at the
  closing brace.
- **An `as <shape>` ascription is checked against real port arity**, so a
  condensed excerpt that drops an inlet fails on its *shape*, not its content:
  1-in/1-out is `flow`, 2-in/1-out `merge`, 1-in/0-out `sink`, 0-in/1-out
  `source`.

**The shared `in-handler` wrapper cannot declare `yields`.** Adding it turns
every fence that does NOT yield into an Error ("does not yield it on every
path") — verified by probe against rc.20-2. `in-yielding-handler` exists for
fences that do yield; it is otherwise identical.

**Regenerating a page that was already rebuilt inserts a SECOND prelude**, and
two preludes still validate, so the gate will not tell you. Restore the page
to its pre-rebuild commit first, and count preludes when in doubt.

**Three ways this gate can lie to you, all observed:**

- **`python3 scripts/validate-riddl-examples.py ... | tail` reports `tail`'s
  exit status.** Redirect to a file and check `$?`, or a red gate reads green.

- A **hand-rolled probe that filters only `[error]`/`[severe]` will call a
  fence clean that the gate rejects** — the gate also fails on `[deprecated]`.
  Filter exactly as `validate()` does, or use the gate itself.
- **A malformed directive silently degrades to `standalone`.** There is no
  warning for a directive that does not parse, so a deliberate skip can quietly
  become a validated fence. The `[^>]*` bug that caused this is fixed, but the
  failure mode is structural: if a fence's result surprises you, check that its
  directive actually parses before believing the result.

**Version differences that matter for examples** (verified against both
compilers):

| Construct | 1.31 | 2.0 |
|-----------|------|-----|
| `state S of record R` | ✅ | ✅ — use this in both |
| `do "..."` | ✅ | ✅ — use this in both |
| `option is X` in `with { }` | ✅ | ✅ — never in the body |
| `initial state` / `initial handler` | ❌ | ✅ |
| query response statement | `reply` | `reply` — un-deprecated in rc.10-46; `yield` is for a command's event, and `yield result` is an **Error** |
| query response declaration | ❌ | `query Q replies result R is …` — `yields` on a query is an Error |
| `ask` | ❌ | ✅ `let a = ask query Q of entity E` — a **value**, not a statement; requires Q to declare `replies`; an **Error anywhere inside a saga step**, at any nesting depth (rc.11) |
| `set` / `get from state` | unrestricted | only where the container **owns** state (rc.13) — a context handler and a saga step own none, and state is readable only inside its own entity |
| projector `correlation` | ❌ | ✅ rc.13 — keyed accumulation of events into one command; completion derived from the command's required fields; `times out after` mandatory |
| outlet on an entity | ❌ — put it on a `source` | ✅ |
| entity semantics | `option is event-sourced` | **`event-sourced entity X`** — the option form is `[deprecated]` |
| alternation | `one of { A, B }` | also `A \| B` (identical; `prettify` emits the words) |
| `command C yields event E is …` | ❌ | ✅ — **required** on every command an event-sourced entity handles. Goes between the name and `is`, and takes a **concrete Event** — an alternation is an Error |
| `forward` | ❌ | ✅ rc.18 — `forward m to outlet X` / `to entity Y`. Passes the handled message on and **discharges** its `yields`/`replies` obligation. Only in a clause handling a command with `yields` or a query with `replies`; an event or result cannot be forwarded; a `yield`/`reply` after it is an Error |
| what discharges a response | — | only `yield`/`reply`, `error`/`require`, `forward`. A `send` of the handled message does **not** (rc.18) |
| `error` / `terminate` | not terminal | **terminal** (rc.19, rc.20) — a statement after either is an Error. `require` is deliberately not terminal; `on term` is a separate list and unaffected |
| refusals-before-effects set | `set`,`morph`,`become`,`send`,`tell`,`yield`,`put` | **`set`, `morph`, `terminate` only** (rc.19) — local state change, not purity. Which is what makes "refuse AND publish a rejection event" legal |
| `option is snapshots` | ❌ | ✅ rc.19 — event-sourced entities only; an **Error** elsewhere. Whether, never how often; absence means "replay the whole log" and is a real choice |
| portlet type | unchecked | a `send`/`forward` naming a message the portlet does not **admit** is an Error (rc.18). Widen the portlet to an alternation |
| cross-context connector | any port | must land on each context's **OWN** portlet; reaching past the boundary is an Error (rc.18). Intra-context, anything may talk to anything |
| sink/source streamlet | required for messaging | not required — an **entity IS a streamlet**, a **context IS the sink**. Per-entity: handles messages → needs its own inlet; emits → its own outlet |
| adaptor direction | — | **inbound (`from`) handles the peer's OUTPUT** (events, results); **outbound (`to`) handles the target's INPUT** (commands). Backwards is an Error. One peer per adaptor — `from X to Y` does not parse |
| duplicate field / ctor arg | silent | **Error** (rc.18) — a repeated name makes the aggregate's shape ambiguous |
| repository with no index | — | CompletenessWarning if it answers queries (rc.17); it cannot name which field, because an `on query` body is prose |
| user interaction | — | only at the **application boundary** — steps name an app's group/input/output, never a context directly |

**`event-sourced` is not decoration in 2.0.** It turns on four Errors: every
handled command's type must declare `yields`; every event so named needs an
`on event` clause; `set`/`morph`/`become` may appear **only** in `on event`
clauses (no exemption for `on init`); and a foreign event may not touch state —
it must yield one of the entity's own first. In practice that means declaring
an event-sourced entity's commands and events **inside** it. Several examples
claimed event sourcing while being structurally impossible to event-source, and
rc.9 started rejecting them.

Since the entity options emit `[deprecated]`, and the fence validator gates on
that, they now **fail the gate** — so this is not a cosmetic migration.

### RIDDL Syntax Highlighting

The `riddl_lexer/` package provides custom Pygments syntax highlighting for
RIDDL code blocks. It's automatically installed in CI via `pip install -e .`
before building.

**Token categories and colors (dark theme):**

| Token Type | Color | Examples |
|------------|-------|----------|
| Keywords | Burnt orange `#fa8b61` | `domain`, `context`, `entity`, `handler` |
| Readability | Yellow `#b3ae60` | `is`, `of`, `to`, `with`, `by` |
| Predefined types | Teal `#19c4bf` | `String`, `Integer`, `UUID`, `Timestamp` |
| Option values | Green `#57d07c` | `event-sourced`, `aggregate` |
| Punctuation | Teal `#0da19e` | `{`, `}`, `(`, `)`, `,`, `:` |
| Comments | Gray `#808080` | `// comment`, `/* block */` |
| Strings | Bright green `#98c379` | `"quoted text"` |
| Markdown docs | Dim green `#629755` | `\|## Heading` |

CSS overrides in `docs/stylesheets/extra.css` apply these colors to both
dark and light themes.

### MkDocs Configuration

The site uses MkDocs Material theme with these notable features:
- Automatic light/dark mode with visible toggle
- Navigation tabs
- Search with highlighting
- Admonitions (info boxes, warnings, etc.)
- Code highlighting via Pygments with custom RIDDL lexer
- Custom CSS in `docs/stylesheets/`
- **Edit links** - Each page links to GitHub for community contributions
- **PWA/offline support** - Service worker caches pages for offline access
- **SEO meta descriptions** - Key pages have frontmatter descriptions

### Markdown Extensions

The following Python Markdown extensions are enabled:
- `admonition` - Info boxes, warnings, tips
- `pymdownx.details` - Collapsible sections
- `pymdownx.superfences` - Fenced code blocks with syntax highlighting
- `pymdownx.tabbed` - Tabbed content
- `pymdownx.tasklist` - Checkbox lists
- `pymdownx.keys` - Keyboard key styling (++ctrl+s++)
- `attr_list` - HTML attributes on elements
- `md_in_html` - Markdown inside HTML blocks

---

## Documentation Standards

### File Structure

- Use `index.md` for section landing pages
- Use descriptive filenames with hyphens: `what-is-riddl.md`
- Keep files focused on single topics
- Use front matter for titles and metadata

### Writing Style

- Write for domain experts who may not be programmers
- Explain concepts before showing syntax
- Use concrete examples from realistic domains
- Link to related concepts liberally
- Define jargon when first used

### Admonitions

Use MkDocs Material admonitions for callouts:

```markdown
!!! info "Title"
    Information content here.

!!! warning "Caution"
    Warning content here.

!!! tip "Pro Tip"
    Helpful tip here.
```

### Code Examples

Use fenced code blocks with the `riddl` language hint:

````markdown
```riddl
domain Example is {
  context MyContext is {
    // Context contents
  }
}
```
````

### Cross-References

Link to other documentation pages using relative paths:

```markdown
See [Domain concepts](../concepts/domain.md) for more details.
```

---

## Editorial Guidelines

These guidelines were established during documentation review sessions:

### Tooling Separation

**Important**: The RIDDL ecosystem has a clear separation of concerns:

- **`riddlc`** (open source): Syntax and semantic validation only. It reads
  RIDDL files, checks them, and reports errors. No code generation.
- **`riddlg`** (proprietary, freemium): The local generation CLI from the
  `riddl-generator` repo. Validates RIDDL and generates docs (AsciiDoc,
  MkDocs), API specs (Smithy, gRPC, OpenAPI), AI-generated RIDDL from
  natural language, and (Pro) Quarkus code. Docs:
  `docs/riddl/tools/riddlg/`.
- **Synapify** (commercial): Provides advanced features including code
  generation, documentation generation, and AI-assisted development
  (it drives `riddlg serve` for generation). These features are available
  via subscription.

When documenting capabilities, do NOT claim that `riddlc` generates code,
diagrams, Kubernetes manifests, etc. Those capabilities belong to `riddlg`
and Synapify. Note: `riddl-gen` (the deprecated generator repo behind
gen.ossuminc.com) is a DIFFERENT project from `riddl-generator`/`riddlg` —
don't conflate them.

### Outdated Technology References

Remove or generalize references to specific generation targets that are no
longer accurate:

- ~~Kalix~~ (no longer a target)
- ~~Kubernetes deployment descriptors~~ (not in OSS tooling)
- ~~Akka code generation~~ (not in OSS tooling)

Instead, describe RIDDL's *capability* to enable such translation without
claiming specific tool support.

### Hugo Remnants

This site migrated from Hugo to MkDocs Material. Remove any Hugo shortcodes:

- `{{< toc-tree >}}` — doesn't work in MkDocs
- `{{< icon "..." >}}` — use Font Awesome syntax or remove
- Any other `{{< ... >}}` patterns

### Capitalization

Always use **RIDDL** (all caps) in prose. It's an acronym. Not "Riddl" or
"riddl" except in code/filenames where lowercase is conventional.

### Metadata vs Body Definitions

RIDDL has a critical distinction between **body definitions**
(inside `{ }`) and **metadata** (in `with { }` after the body):

- **Body**: types, handlers, entities, states, functions, etc.
- **Metadata**: term, option, author_ref (`by author`), briefly,
  described by, attachment

**Author definitions** (not references) only occur in Module and
Domain bodies. All other definitions use `by author Name` in
their `with { }` block to reference an author.

**Option syntax** requires `is`: `option is event-sourced`,
`option is technology("Kafka")`.

**Term syntax**: `term SKU is { |Stock Keeping Unit... }` — not
`term "SKU" is described by "..."`.

### RIDDL Syntax in Examples

Code examples must match the EBNF grammar. Common issues to avoid:

1. **Enumerations vs Alternations**:
   - `any of { A, B, C }` — enumeration of constants
   - `one of { TypeA, TypeB }` — alternation of types

2. **User terminology**: Use "User" not "Actor" (per Use Cases 2.0)

3. **Hyphenation**: `event-sourced` (hyphenated as compound
   modifier)

4. **Version requirements**:
   - JDK 25 (current LTS)
   - Scala 3.3.x (current LTS)
   - `sbt riddlc/stage` (not `sbt stage`)

### Tone and Style

- Light, accessible, occasionally jovial
- Technical precision without being dry
- Explain concepts before showing syntax
- Use em-dashes for asides—they read more naturally
- Prefer active voice

---

## RIDDL Language Context

When editing RIDDL documentation, understand these core concepts:

### Definition Hierarchy

```
Root
└── Domain (knowledge domain boundary)
    └── Context (bounded context from DDD)
        ├── Entity (stateful business object)
        ├── Repository (persistent storage)
        ├── Projector (event projection)
        ├── Saga (multi-step process coordination)
        ├── Streamlet (stream processing)
        └── Adaptor (message translation)
```

### Key Patterns

- **Event Sourcing**: Entities can store state as event logs
- **CQRS**: Commands and queries are separate message types
- **Handlers**: Define behavior in response to messages
- **Statements**: Pseudocode for business logic (not Turing-complete)

### Target Audience

Documentation serves multiple audiences:
- **Authors**: Write RIDDL models, need syntax and semantics
- **Domain Experts**: Review models, need concept understanding
- **Implementors**: Generate code from models, need technical details
- **Developers**: Maintain RIDDL tooling, need architecture info

---

## Related Repositories

This documentation site covers tools from other Ossum Inc. repositories:

- **riddl**: The RIDDL compiler (`riddlc`) and language implementation
- **synapify**: Desktop application for visual RIDDL editing
- **riddl-idea-plugin**: IntelliJ IDEA plugin for RIDDL
- **riddl-vscode**: VS Code extension for RIDDL (source for lexer tokens)
- **riddl-mcp-server**: MCP server for AI-assisted RIDDL modeling
- **riddl-models**: Curated example models (linked from `docs/riddl/examples/`)

Refer to the parent `../CLAUDE.md` for cross-project coordination guidance.

---

## Quick Reference

There is **no `mkdocs.yml` at the repo root** — every command needs
`-f sites/<site>/mkdocs.yml`, where `<site>` is `shell`, `riddl`, `riddl-1x`,
`riddlg` or `synapify`. Run `sync-shared-assets.sh` first or pages build
without CSS.

| Task | Command |
|------|---------|
| Install deps | `pip install -r requirements.txt && pip install -e .` |
| **Sync shared assets** (before any build) | `./scripts/sync-shared-assets.sh` |
| Start dev server | `mkdocs serve -f sites/riddl/mkdocs.yml` |
| Build one site | `mkdocs build --strict -f sites/riddl/mkdocs.yml` |
| Check links **and anchors** | `mkdocs build --strict -f sites/riddl/mkdocs.yml 2>&1 \| grep -E 'anchor\|WARNING\|ERROR'` |
| Check **cross-site** links | `python3 scripts/check-cross-site-links.py` |
| Check the 404 redirect map | `node scripts/test-404-redirects.js` |
| Build the cross-site search index | `./scripts/build-search-index.sh <site-root>` |
| Generate robots.txt | `./scripts/build-robots-txt.sh <site-root>` |
| Check RIDDL code blocks | `python3 scripts/check-riddl-blocks.py sites/riddl/docs` |
| Compile RIDDL examples (2.0) | `python3 scripts/validate-riddl-examples.py ../bin/riddlc sites/riddl/docs/quickstart.md` |
| Compile RIDDL examples (1.31) | `python3 scripts/validate-riddl-examples.py /opt/homebrew/Cellar/riddlc/1.31.0/bin/riddlc sites/riddl-1x/docs/quickstart.md` |
| Run the **whole** 2.0 gate | see § "Compiling RIDDL examples" — the scope is a file list, not a directory |
| Preview the whole site | `scripts/preview-versioned-site.sh` |
| Deploy | push to `main`; CI loops over `docs-version.yml` |

Build every site before concluding a change is clean — a cross-site link edit
can only break the site at the *other* end:

```bash
./scripts/sync-shared-assets.sh
for s in shell riddl riddl-1x riddlg synapify; do
  mkdocs build --strict -f sites/$s/mkdocs.yml 2>&1 | grep -E 'anchor|WARNING|ERROR'
done
python3 scripts/check-cross-site-links.py
```

---

## Pending Updates

These items need updating when conditions are met:

| Item | Location | Update When |
|------|----------|-------------|
| "Coming Soon" warnings | All MCP guides | MCP server goes live (~early 2026) |
| Download links | Tool pages | Final releases published |
