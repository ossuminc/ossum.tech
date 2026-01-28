---
title: "What Can RIDDL Do?"
date: 2022-02-25T10:07:32-07:00
draft: false
weight: 20
---

RIDDL is a specification language, and like any language, it needs tools to
work with it. The primary tool is the open source compiler, `riddlc`.

## The RIDDL Compiler: `riddlc`

The `riddlc` compiler is RIDDL's validation workhorse. It reads your
specification files, checks them thoroughly, and reports any issues.

### Input

The compiler takes a single `.riddl` file as input. This top-level file can
include others hierarchically, letting you organize large specifications across
multiple files while keeping a single entry point.

### What It Validates

The compiler performs two levels of validation:

* **Syntax Validation** — Ensures your specification follows RIDDL's grammar.
  Catches typos, missing keywords, and structural errors.

* **Semantic Validation** — Checks that your specification makes sense as a
  whole. Verifies that references point to real definitions, types are used
  correctly, and the model is internally consistent.

Think of syntax validation as spell-checking and semantic validation as
grammar-checking—both are essential for a well-formed specification.

### Options

The `riddlc` program offers options to control:

* Configuration sources (load settings from config files)
* Logging verbosity (from terse error-only output to verbose debugging)
* Warning levels and error handling

For detailed usage information, see the [riddlc documentation](../tools/riddlc/index.md).