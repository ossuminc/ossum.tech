---
title: "Command Reference"
description: "Complete reference for riddlc commands and options"
---

# Command Reference

`riddlc` uses a subcommand structure. The general syntax is:

```bash
riddlc [common-options] command [command-options]
```

## Available Commands

| Command | Description |
|---------|-------------|
| `about` | Print out information about RIDDL |
| `advise` | Report remediation advice for a model |
| `bastify` | Convert a RIDDL file to BAST (Binary AST) format |
| `dump` | Dump the AST, or with `--json` a machine-readable projection |
| `find` | Search a model for definitions, in the manner of Unix `find` |
| `flatten` | Flatten all includes into a single file |
| `from` | Load options from a configuration file |
| `help` | Print usage information |
| `info` | Print build information |
| `onchange` | Watch a directory and run a command on changes |
| `parse` | Parse the input file and report syntax errors |
| `prettify` | Reformat RIDDL source to a standard layout |
| `repeat` | Repeatedly run a command for edit-build-check cycles |
| `stats` | Generate statistics about a RIDDL model |
| `unbastify` | Convert a BAST file back to RIDDL source |
| `validate` | Parse and validate; reports a one-line summary of what it checked |
| `version` | Print the version and exit |

!!! info
    Hugo documentation generation and diagram generation have been moved to
    the [riddl-gen](https://github.com/ossuminc/riddl-gen) repository.

## Common Options

These options apply to all commands:

| Option | Description |
|--------|-------------|
| `-t`, `--show-times` | Show parsing phase execution times |
| `-I`, `--show-include-times` | Show parsing of included files times |
| `-d`, `--dry-run` | Go through the motions but don't write changes |
| `-v`, `--verbose` | Provide verbose output |
| `-D`, `--debug` | Enable debug output (for developers) |
| `-q`, `--quiet` | No output, just execute the command |
| `-a`, `--no-ansi-messages` | Disable ANSI formatting in messages |
| `--no-msg-ids` | Do not print the stable rule id beside each message |
| `-w`, `--show-warnings` | Control warning message display |
| `-m`, `--show-missing-warnings` | Control missing definition warnings |
| `-s`, `--show-style-warnings` | Control style warning display |
| `-u`, `--show-usage-warnings` | Control usage warning display |
| `-i`, `--show-info-messages` | Control info message display |
| `-S`, `--sort-messages-by-location` | Sort messages by file and line |
| `-G`, `--group-messages-by-kind` | Group messages by severity |
| `-x`, `--max-parallel-parsing` | Max parallel include file parsing |
| `--max-include-wait` | Max time to wait for include parsing |
| `-c`, `--show-completeness-warnings` | Control completeness warning display |
| `--warnings-are-fatal` | Treat warnings as errors |
| `-B`, `--auto-generate-bast` | Auto-generate .bast files after parsing |
| `-P`, `--provide-tips` | Include a remediation suggestion with each message that has one, for AI-assisted fixing |
| `--check-figma-drift` | Check `figma` references against the Figma REST API |

### Completeness Warnings

`--show-completeness-warnings` (default: on) controls severity-4 messages —
models that parse and validate but lack detail needed for a complete,
implementable specification.

When it is on, `validate` additionally runs the message-flow, entity-lifecycle
and use-case analyses, so epic and use-case completeness warnings surface here
rather than only through the analysis API. When it is off, those passes are
skipped entirely and cost nothing.

### Figma Drift Checking

`--check-figma-drift` is **off by default** and verifies that each
`figma "<file>" node "<id>"` reference in the model still resolves:

```bash
export FIGMA_TOKEN=figd_...
riddlc --check-figma-drift validate model.riddl
```

A node the API does not know about is an **Error**; a frame whose name no
longer corresponds to the annotated definition's name is a **Warning**.

An offline or token-less build cannot be affected. No token means no client at
all, and every failure to reach or understand the API produces nothing —
**only a successful API answer can produce a message**. With the flag on but
no client available, one informational message says so, and that is the whole
consequence.

The HOCON equivalent for a `from` configuration file is `check-figma-drift`.

### Every message carries a rule id

Every diagnostic riddlc emits is prefixed with its **severity** and a **stable
rule id**:

```
[missing] [stream-no-error-sink] model.riddl(1:1->12):
Domain 'Shop' declares no 'error-sink' inlet, so hard errors have no destination:
domain Shop is {
```

**The id is the durable handle; the wording is not.** Message text is free to
change between releases — the id is not. Anything that needs to name a
particular diagnostic (a CI filter, a suppression list, a docs cross-reference,
a spreadsheet of what a model still owes) should key on the id.

`--no-msg-ids` turns the prefix off, for output meant only for human reading:

```bash
riddlc --no-msg-ids validate model.riddl
```

!!! tip "Count by id, not by message text"
    Grouping a large model's diagnostics by rule id tells you what kind of work
    is outstanding; grouping by message text splits one rule across every
    definition name it mentions.

    ```bash
    riddlc validate model.riddl --json | jq -r '.[].rule' | sort | uniq -c | sort -rn
    ```

### Deprecation Messages

RIDDL 2.0 gives deprecations their own `[deprecated]` label rather than
rendering them as ordinary warnings, so a model can be checked for zero
deprecations independently of zero warnings:

```bash
riddlc validate model.riddl 2>&1 | grep '\[deprecated\]'
```

They also surface under **every** command that parses — `parse`, `stats`,
`bastify`, `prettify` and the generation commands — not only `validate`. In
1.x a successful parse that accumulated any message discarded the result, so
parse-time warnings never reached the user at all.

## Command Details

### parse

Parse a RIDDL file for syntactic correctness without semantic validation:

```bash
riddlc parse input-file.riddl
```

This is useful for quickly checking if a file is syntactically valid.

### validate

Parse and semantically validate a RIDDL file:

```bash
riddlc validate input-file.riddl
```

This performs full validation including:

- Reference resolution (all referenced definitions exist)
- Type checking
- Containment rules
- Style checks (optional)

It finishes with a one-line summary of **what it checked**, so a silent run is
distinguishable from a run that examined nothing.

| Option | Description |
|--------|-------------|
| `--fail-on <severity>` | Exit non-zero if any message is at or above `info`, `warning`, `error` or `severe` |
| `--json` | Emit diagnostics as a JSON array on stdout instead of the human summary |
| `--fix` | Apply every rule that carries a mechanical fix, then re-validate |
| `--fix-rule <id>` | Apply only this rule's fix (implies `--fix`) |
| `--fix-dry-run` | Show the diff `--fix` would apply and write nothing (implies `--fix`) |

#### `--fail-on` is the CI lever

Without it, `validate` exits 0 for anything short of a hard error, so a build
gate has to parse output to decide. `--fail-on` moves that decision into the
exit status:

```bash
riddlc validate model.riddl --fail-on warning
```

!!! warning "Check `$?` directly, never through a pipe"
    `riddlc validate … | tail` reports **`tail`'s** status, not riddlc's, so a
    red run reads green. Redirect to a file, check `$?`, then read the file:

    ```bash
    riddlc validate model.riddl --fail-on warning > report.txt 2>&1
    echo "EXIT=$?"
    ```

#### `--json` for tooling

Each element separates **severity** from **class**, and keeps riddl's raw
`kind` beside them so a consumer that already reads it is unaffected:

```json
{
  "rule": "stream-no-error-sink",
  "severity": "warning",
  "class": "missing",
  "kind": "Missing",
  "message": "Domain 'Shop' declares no 'error-sink' inlet, so hard errors have no destination",
  "file": "model.riddl",
  "line": 1,
  "col": 1
}
```

Before this split, a consumer handed `"kind": "MissingWarning"` had to know
riddl's taxonomy to work out that it was a warning.

#### `--fix` applies only mechanical rules

Most diagnostics have no mechanical fix — they need a judgement call, or a
rewrite outside the span that was reported. `--fix` applies the ones that do,
and **says what it did not fix and why**, grouped by reason with the rules
named:

```
validate --fix: 31 not fixed:
  31 x no mechanical fix: needs a judgement call, or a rewrite outside the
      reported span [doc-no-description, entity-no-id-type, name-too-short, …]
```

`--fix-rule <id>` narrows it to one rule, and naming a rule that has no
mechanical fix reports which rules do. Use `--fix-dry-run` first: it prints the
diff and writes nothing.

### prettify

Reformat RIDDL source to a standard layout:

```bash
riddlc prettify input-file.riddl -o output-dir
```

Options:

| Option | Description |
|--------|-------------|
| `-o`, `--output-dir` | Required output directory |
| `--project-name` | Project name for the output |
| `--check` | Report files not in canonical form and exit non-zero; write nothing |
| `-s`, `--single-file` | Merge all includes into a single file |

`--check` is the CI form: it asserts that a model is already formatted, the way
`scalafmtCheck` or `gofmt -l` do, without rewriting anything.

```bash
riddlc prettify model.riddl --check
```

### bastify

Convert RIDDL to Binary AST (BAST) format for faster loading:

```bash
riddlc bastify input-file.riddl
```

Creates a `.bast` file next to the input file. BAST files can be loaded
significantly faster than parsing RIDDL source, making them useful for
large models.

### unbastify

Convert a BAST file back to RIDDL source:

```bash
riddlc unbastify input-file.bast -o output-dir
```

Options:

| Option | Description |
|--------|-------------|
| `-o`, `--output-dir` | **Required.** Output directory |
| `-s`, `--single-file` | Resolve all includes and write one flattened file |

!!! warning "`-o` has no default, deliberately"
    It used to default to the input's own directory — which **silently
    overwrote the very sources the `.bast` was generated from**. Omitting it
    now fails with a non-zero exit rather than destroying anything.

    (riddlc's own `--help` still advertises the old default. The runtime is the
    authority; it rejects the call.)

### dump

Print the model's AST. With `--json`, print a flat, machine-readable
**projection** of it instead — one record per definition, which is what makes
a model scriptable:

```bash
riddlc dump model.riddl --json
```

```json
{
  "kind": "domain",
  "id": "Shop",
  "path": "Shop",
  "file": "model.riddl",
  "span": { "start": { "line": 1, "col": 1, "offset": 0 },
            "end":   { "line": 24, "offset": 610 } },
  "brief": "p"
}
```

| Option | Description |
|--------|-------------|
| `--json` | Emit the flat projection instead of the indented AST |
| `--jsonl` | One record per line, for streaming a large corpus |
| `--include-spans <bool>` | Include source spans (default: true) |
| `--resolve <bool>` | Resolve references, emitting `null` for ones that do not (default: true) |
| `-o`, `--output` | Write to this file instead of stdout |

Use `--jsonl` when piping a whole corpus through `jq` or a script: it streams
rather than requiring the entire array to be parsed at once.

```bash
# --json is one ARRAY, so jq needs `.[]` to iterate it
riddlc dump model.riddl --json  | jq -r '.[] | select(.kind=="entity") | .path'

# --jsonl is one record per line, so it does not
riddlc dump model.riddl --jsonl | jq -r 'select(.kind=="entity") | .path'
```

!!! tip "`dump --json` versus `find`"
    They answer different questions. `find` asks *"which definitions match?"*
    and can act on the answer; `dump --json` hands you **everything** and lets
    a script decide. Reach for `find` for a query, `dump --json` for an
    inventory or a report.

### find

Search a model for definitions, in the manner of Unix `find`. The expression
follows a `--` separator, which keeps riddlc's own options from competing with
the expression's:

```bash
riddlc find model.riddl -- -type entity -name 'Order*'
```

```
model.riddl:7:5: entity Order is {
[info] 1 matched
```

`find` operates on the **resolved model**, not on the text, so it sees what the
compiler sees: a definition's kind, its path, what it carries, whether it is a
stub. That is the difference between it and `grep`.

#### Predicates

| Predicate | Matches |
|---|---|
| `-type <kind>` | definitions of that kind — `entity`, `context`, `command`, `handler`, … |
| `-name <glob>` | identifier matches the glob; `-iname` is the case-insensitive form |
| `-path <glob>` | full path matches the glob; `-ipath` case-insensitive |
| `-regex <re>` | identifier matches the regex; `-iregex` case-insensitive |
| `-source-regex <re>` | the definition's **source text** matches |
| `-under-name <id>` | contained anywhere beneath a definition with that name |
| `-under-a <kind>` | contained anywhere beneath a definition of that kind |
| `-in <path>` | declared within that path |
| `-mindepth <n>` / `-maxdepth <n>` | bound the containment depth |
| `-intention <i>` | carries that intention — `event-sourced`, `application`, … |
| `-option <o>` | carries that option |
| `-shape <s>` | the streamlet shape: `flow`, `sink`, `source`, `merge`, … |
| `-arity <n>` | that port arity |
| `-cardinality <c>` | that cardinality |
| `-carries <type>` | a portlet carrying that type |
| `-operand-kind <k>` | a statement whose operand is of that kind |
| `-reads-state` | reads state |
| `-stub` | the body is `???` |
| `-empty` | the body is empty |
| `-unresolved` | holds a reference that does not resolve |

#### Combining them

Predicates juxtaposed are **and**-ed. `-o` (or `-or`) is disjunction, `!` (or
`-not`) negates, and parentheses group — quoted, so the shell does not eat
them:

```bash
riddlc find model.riddl -- -type command -o -type event
riddlc find model.riddl -- '(' -type entity -o -type context ')' -stub
riddlc find model.riddl -- -type entity '!' -name 'Test*'
```

#### Actions

| Action | Does |
|---|---|
| `-print` | print the match (the default) |
| `-location` | print `file:line:col` only |
| `-path` | print the definition's full path |
| `-printpath` | print the path, one per line |
| `-printf <fmt>` | print a format string — `%n` name, `%l` line, and friends |
| `-list` | list matches |
| `-quit` | stop at the first match |
| `-expect-min <n>` | **exit non-zero if fewer than `n` matched** |
| `-exec <cmd> ;` | run a command per match; `{}` is the match, `+` batches |
| `-replace <cmd> ;` | replace each match with the command's stdout |
| `-delete` | delete each match |

`-expect-min` is the one worth knowing for CI. It turns a search into an
assertion:

```bash
riddlc find model.riddl -- -type entity -expect-min 3
echo "EXIT=$?"     # 7 if fewer than three entities exist
```

!!! warning "Check `$?` directly"
    As everywhere else, a pipe replaces riddlc's exit status with the last
    command's. `riddlc find … | head` always looks successful.

#### Editing actions rewrite your model

`-replace`, `-delete` and `-exec` **mutate the source**. They exist for
codemods — renaming a construct across a corpus, stripping a retired option —
and they carry their own safety options:

| Option | Effect |
|---|---|
| `-dry-run` | show what would change, write nothing |
| `-keep-going` | continue after a failed edit rather than stopping |
| `-allow-empty` | permit an edit that produces an empty result |

```bash
# See what it would do, first
riddlc find model.riddl -- -type entity -name 'Legacy*' -delete -dry-run
```

!!! danger "Run `-dry-run` first, and have the file in version control"
    These actions edit files in place. `-dry-run` is not the default.

### flatten

Collapse a multi-file model into a single file:

```bash
riddlc flatten input-file.riddl -o output-file.riddl
```

This removes every `include` and `import` node, promoting its children into
the enclosing container. In RIDDL 2.0 it covers **both**: `import` nodes from
`.bast` modules are flattened alongside `include` nodes from source files.

!!! warning "Flattening is lossy, and is not a prerequisite for anything"
    An `include` or `import` is a **node** in the model whose children are the
    definitions it brought in. Passes traverse through it, so those definitions
    already resolve, validate and generate exactly as if written in place. You
    do **not** need to flatten to make a multi-file model work.

    What flattening removes is the **origin**: after it, nothing records which
    file or module a definition came from. That costs you the file attribution
    in diagnostics and the ability to tell your own model apart from what it
    imported.

    Use it only when a single self-contained file is the actual goal — handing
    one file to a tool that cannot follow includes, for instance — and keep the
    unflattened model as the source of truth.

### stats

Generate statistics about a RIDDL model:

```bash
riddlc stats -I input-file.riddl
```

Reports counts of domains, contexts, entities, types, and other definitions.

### from

Load options from a HOCON configuration file:

```bash
riddlc from config-file.conf target-command
```

See [Configuration](configuration.md) for details on the configuration format.

### repeat

Support edit-build-check cycles by repeating a command:

```bash
riddlc repeat config-file.conf target-command [refresh-rate] [max-cycles]
```

Options:

| Option | Description |
|--------|-------------|
| `refresh-rate` | How often to check for changes |
| `max-cycles` | Maximum number of cycles |
| `-n`, `--interactive` | Exit on EOF from stdin |

### onchange

Watch a directory and run a command when changes occur:

```bash
riddlc onchange config-file.conf watch-directory target-command
```

### info

Display build information:

```bash
riddlc info
```

Example output:

```
[info] About riddlc:
[info]            name: riddlc
[info]         version: 2.0.0-rc.1
[info]      git commit: ebce6ba945739bef06907445e5a570b2d030591b
[info]   documentation: https://ossum.tech/riddl
[info]       copyright: © 2019-2026 Ossum Inc.
[info]        licenses: Apache License, Version 2.0
[info]    organization: Ossum Inc.
[info]   scala version: 3.9.0
```

`git commit` is new in RIDDL 2.0: the full source SHA the binary was built
from. It lets a model repository locate the exact compiler changes a given
`riddlc` embodies — useful when a validation message appears that an older
build did not produce. Outside a git checkout it reads `unknown`.

### advise

Report remediation advice for a model. Pairs with `--provide-tips`, which
attaches a suggested fix to each message that has one — intended for
AI-assisted correction.

```bash
riddlc advise model.riddl
```

### help

Display usage information:

```bash
riddlc help
riddlc help validate  # Help for specific command
```

### version

Display the version number:

```bash
riddlc version
```
