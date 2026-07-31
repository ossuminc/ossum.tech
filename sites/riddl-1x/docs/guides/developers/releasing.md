---
title: "Releasing RIDDL"
description: "How to release new versions of RIDDL"
---

# Releasing RIDDL

This guide covers the release process for RIDDL maintainers.

## Prerequisites

Before releasing, ensure you have:

- Commit access to the main repository
- GPG key configured for signing
- Access to Maven Central (Sonatype)
- GitHub release permissions

## Pre-Release Checklist

### 1. Build and Test

Make sure everything tests correctly from a clean start:

```bash
cd riddl
sbt clean test
```

Run tests multiple times to expose any parallelism issues:

```bash
sbt test test test
```

If any tests fail, stop and fix the software before proceeding.

### 2. Stage the Build

```bash
sbt riddlc/stage
```

If this fails, fix the documentation—likely references between `[[` and `]]`
in ScalaDoc comments.

### 3. Test on a Large Project

Run `riddlc validate` on a large multi-file specification to expose any
language change issues:

```bash
./riddlc/jvm/target/universal/stage/bin/riddlc validate /path/to/large/model.riddl
```

If validation fails, go back and fix the software.

## Release Process

### 1. Commit Changes

Commit any changes to a branch and push to GitHub:

```bash
git checkout -b release/1.2.0
git add .
git commit -m "Prepare release 1.2.0"
git push -u origin release/1.2.0
```

### 2. Create Pull Request

Create a PR and wait for all workflows to pass. If any fail, fix the issues
and restart the release process.

### 3. Merge to Main

After workflows pass, merge the PR to the `main` branch.

### 4. Checkout and Verify Main

```bash
git checkout main
git pull
git status
```

Ensure you have a clean working tree:

```
On branch main
Your branch is up to date with 'origin/main'
nothing to commit, working tree clean
```

### 5. Determine Version Number

Follow [semantic versioning](https://semver.org/):

- **MAJOR** - Breaking changes to language syntax or semantics
- **MINOR** - New features, backward compatible
- **PATCH** - Bug fixes, backward compatible

Review changes since the last release to determine the appropriate increment.

### 6. Tag the Release

```bash
git tag -a 1.2.0 -m "Release 1.2.0: Brief description"
sbt show version  # Verify the version
git push --tags
```

!!! warning "No 'v' Prefix"
    Do not use a `v` prefix (like `v1.2.0`). sbt-dynver requires tags
    without the prefix.

### 7. Publish to Maven Central

```bash
sbt clean test publishSigned
```

Then:

1. Log in to [Sonatype OSS Repository](https://oss.sonatype.org/#stagingRepositories)
2. Check staged artifacts for sanity
3. Close the repository (add release number in notes)
4. Press **Release** to publish to Maven Central

### 8. Build Release Artifacts

```bash
sbt "project riddlc" "Universal/packageBin"
```

This creates:
- `riddlc/jvm/target/universal/riddlc-1.2.0.zip`

### 9. Create GitHub Release

1. Go to [GitHub Releases](https://github.com/ossuminc/riddl/releases/new)
2. Select the tag you just created
3. Write release notes summarizing changes
4. Upload artifacts:
   - `riddlc-1.2.0.zip`

### 10. Update get-riddlc Action

Edit `actions/get-riddlc/action.yaml` and update the version:

```yaml
inputs:
  version:
    default: '1.2.0'
```

Commit and push this change (not included in the release tag).

!!! important
    Do this step last. Other projects depend on this action, and the action
    depends on the uploaded artifacts.

## Post-Release

### Announce the Release

- Update documentation if needed
- Announce on relevant channels (Slack, mailing list, etc.)
- Update any dependent projects

### Verify the Release

Test that the release works:

```bash
# Test GitHub Action
# Create a test workflow using get-riddlc@main

# Test Maven artifact
sbt "show dependencyResolution"  # In a project using sbt-riddl
```

## Hotfix Releases

For urgent fixes to released versions:

1. Create a hotfix branch from the release tag:
   ```bash
   git checkout -b hotfix/1.2.1 1.2.0
   ```

2. Make the fix with tests

3. Follow the release process from step 1

4. Merge the hotfix back to `main` and `development`:
   ```bash
   git checkout development
   git merge hotfix/1.2.1
   ```

## Related

- [GitHub Actions](../../tools/riddlc/github-actions.md) - CI/CD integration
- [sbt-riddl](../../tools/sbt-riddl/index.md) - SBT plugin
