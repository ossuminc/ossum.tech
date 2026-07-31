---
title: "GitHub Actions"
description: "Using riddlc in GitHub Actions workflows"
---

# GitHub Actions Integration

Automate RIDDL validation in your GitHub repositories using GitHub Actions.
This ensures all pull requests and merges maintain model validity.

## Quick Start

Create `.github/workflows/validate-riddl.yml`:

```yaml
name: Validate RIDDL

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]
  workflow_dispatch:

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Set Up JDK 25
        uses: actions/setup-java@v4
        with:
          java-version: '25'
          distribution: 'temurin'

      - name: Get riddlc
        uses: ossuminc/riddl/actions/get-riddlc@main

      - name: Validate RIDDL model
        run: |
          riddlc validate src/main/riddl/MyModel.riddl
```

## Using Configuration Files

For more complex setups, use a configuration file:

```yaml
- name: Validate with config
  run: |
    riddlc from src/main/riddl/riddl.conf validate
```

With a `riddl.conf` file:

```hocon
command = validate

common {
  show-times = true
  verbose = true
}

validate {
  input-file = "MyModel.riddl"
}
```

## The get-riddlc Action

The `ossuminc/riddl/actions/get-riddlc@main` action:

- Downloads the latest `riddlc` release
- Adds it to the PATH
- Sets the `RIDDLC` environment variable

### Specifying a Version

```yaml
- name: Get specific riddlc version
  uses: ossuminc/riddl/actions/get-riddlc@main
  with:
    version: '1.0.0'
```

## Complete Workflow Example

A comprehensive workflow with caching and multiple checks:

```yaml
name: RIDDL CI

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  validate:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v4

      - name: Set Up JDK 25
        uses: actions/setup-java@v4
        with:
          java-version: '25'
          distribution: 'temurin'

      - name: Get riddlc
        uses: ossuminc/riddl/actions/get-riddlc@main

      - name: Validate model
        run: |
          riddlc validate \
            --warnings-are-fatal true \
            --show-times true \
            src/main/riddl/MyModel.riddl

      - name: Generate statistics
        run: |
          riddlc stats -I src/main/riddl/MyModel.riddl

  style-check:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v4

      - name: Set Up JDK 25
        uses: actions/setup-java@v4
        with:
          java-version: '25'
          distribution: 'temurin'

      - name: Get riddlc
        uses: ossuminc/riddl/actions/get-riddlc@main

      - name: Check style
        run: |
          riddlc validate \
            --show-style-warnings true \
            src/main/riddl/MyModel.riddl
```

## Caching for Speed

Cache the riddlc download for faster runs:

```yaml
- name: Cache riddlc
  uses: actions/cache@v4
  with:
    path: ~/.riddlc
    key: riddlc-${{ runner.os }}-${{ hashFiles('.riddlc-version') }}

- name: Get riddlc
  uses: ossuminc/riddl/actions/get-riddlc@main
```

## Pull Request Comments

Add validation results as PR comments:

```yaml
- name: Validate and capture output
  id: validate
  run: |
    OUTPUT=$(riddlc validate src/main/riddl/MyModel.riddl 2>&1) || true
    echo "output<<EOF" >> $GITHUB_OUTPUT
    echo "$OUTPUT" >> $GITHUB_OUTPUT
    echo "EOF" >> $GITHUB_OUTPUT
  continue-on-error: true

- name: Comment on PR
  if: github.event_name == 'pull_request'
  uses: actions/github-script@v7
  with:
    script: |
      github.rest.issues.createComment({
        issue_number: context.issue.number,
        owner: context.repo.owner,
        repo: context.repo.repo,
        body: `## RIDDL Validation Results\n\n\`\`\`\n${{ steps.validate.outputs.output }}\n\`\`\``
      })
```

## Triggering on RIDDL File Changes

Only run when RIDDL files change:

```yaml
on:
  push:
    paths:
      - '**/*.riddl'
      - '**/riddl.conf'
  pull_request:
    paths:
      - '**/*.riddl'
      - '**/riddl.conf'
```

## Matrix Testing

Test against multiple riddlc versions:

```yaml
jobs:
  test:
    strategy:
      matrix:
        riddlc-version: ['1.0.0', '1.1.0', 'latest']

    steps:
      - uses: actions/checkout@v4

      - name: Get riddlc ${{ matrix.riddlc-version }}
        uses: ossuminc/riddl/actions/get-riddlc@main
        with:
          version: ${{ matrix.riddlc-version }}

      - name: Validate
        run: riddlc validate src/main/riddl/MyModel.riddl
```

## Troubleshooting

### Common Issues

| Issue | Solution |
|-------|----------|
| "riddlc not found" | Verify get-riddlc action succeeded |
| JDK version mismatch | Use JDK 25 (temurin) |
| Validation timeout | Add `timeout-minutes: 30` |
| Permission denied | Check file permissions in repo |

### Debug Mode

Enable verbose output:

```yaml
- name: Validate (debug)
  run: |
    riddlc validate --debug --verbose src/main/riddl/MyModel.riddl
```

## Next Steps

- [Configuration](configuration.md) - Create config files for CI
- [Command Reference](command-reference.md) - Available commands
