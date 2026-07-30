---
title: "Installation"
description: "How to install the RIDDL compiler"
---

# Installing riddlc

This guide covers the various ways to install `riddlc` on your system.

## Download a Release

The easiest way to get started is to download a pre-built release:

1. Go to [GitHub Releases](https://github.com/ossuminc/riddl/releases)
2. Download the `.zip` asset for your platform (under "Assets")
3. Unpack the archive:
   ```bash
   unzip riddlc-*.zip
   ```
4. Add the `bin` directory to your PATH:
   ```bash
   export PATH="$PATH:$(pwd)/riddlc-*/bin"
   ```
5. Verify installation:
   ```bash
   riddlc version
   ```

!!! note
    Not all releases include pre-built assets. If no asset is available for
    your desired version, you'll need to build from source.

## Homebrew (macOS)

On macOS, the easiest installation method is via Homebrew:

```bash
brew install ossuminc/tap/riddlc
```

This installs the latest release and manages updates automatically. To upgrade
later:

```bash
brew upgrade riddlc
```

## Release Candidates

RIDDL 2.0 is being released through a series of **release candidates**, which
ship from a separate formula so they can never reach anyone who did not ask for
them.

```bash
brew unlink riddlc && brew install ossuminc/tap/riddlc-rc
```

To go back to the stable line:

```bash
brew unlink riddlc-rc && brew link riddlc
```

The `unlink` step is not optional. Both formulae install a binary called
`riddlc`, and the RC formula declares `conflicts_with "riddlc"`, so only one of
them can own the name at a time. The stable version stays installed while
unlinked — reverting does not re-download anything.

Confirm which one you are running:

```bash
riddlc info | grep version
```

Once RIDDL 2.0 ships as a final release, `brew upgrade riddlc` on the stable
formula is all you need, and the RC formula can be removed:

```bash
brew uninstall riddlc-rc && brew link riddlc && brew upgrade riddlc
```

!!! info "Why a separate formula rather than a flag"
    Homebrew has no prerelease flag, and its `devel` block was deprecated and
    removed. A separately named formula that you opt into is the supported
    pattern — the name itself is the experimental marking.

!!! warning "An RC is not for production models"
    A release candidate may still change language behaviour before the final
    release. Expect to re-validate models against the final 2.0, and see
    [Migrating from 1.x](../../migration/1.x-to-2.0.md) for what changed.

## Build from Source

Building RIDDL 2.0 from source requires JDK 25 and **sbt 2.0.2 or later**.

!!! warning "sbt 2 is required for RIDDL 2.0"
    RIDDL 2.0 migrated to sbt 2 and the `projectMatrix` build layout, so an
    sbt 1.x installation will not build it. The version is pinned in
    `project/build.properties`, and sbt's launcher will fetch the right one —
    but the launcher itself must be recent enough to understand it.

    Credentials for sbt 2 live in `~/.sbt/2/`, not `~/.sbt/1.0/`.

### Prerequisites

**Install JDK 25:**

=== "macOS"
    ```bash
    brew install --cask temurin
    ```

=== "Linux"
    Follow [Adoptium installation instructions](https://adoptium.net/installation/)

=== "Windows"
    Download from [Adoptium](https://adoptium.net/) and run the installer

**Install sbt:**

=== "macOS"
    ```bash
    brew install sbt
    ```

=== "Linux/Windows"
    Follow [sbt setup instructions](https://www.scala-sbt.org/1.x/docs/Setup.html)

### Build Steps

```bash
# Clone the repository
git clone https://github.com/ossuminc/riddl.git
cd riddl

# Compile and stage the executable
sbt "riddlc/stage"

# The executable is now at:
# riddlc/jvm/target/universal/stage/bin/riddlc
```

### Add to PATH

Add the staged executable to your PATH:

```bash
export PATH="$PATH:$(pwd)/riddlc/jvm/target/universal/stage/bin"
```

For permanent installation, add this to your shell profile (`.bashrc`, `.zshrc`,
etc.).

## Create Universal Package

To create a portable package you can distribute:

```bash
sbt "project riddlc" "universal:packageBin"
```

This creates a `.zip` file in `riddlc/target/universal/` that can be unpacked
on any system with a compatible JVM.

## Verify Installation

After installation, verify that riddlc is working:

```bash
riddlc info
```

You should see output like:

```
[info] About RIDDL:
[info]            name: utils
[info]         version: 2.0.0
[info]      git commit: 4af86d6712c9f0b1a3e5d8c47b2f6a90de13c8b5
[info]   documentation: https://ossum.tech/riddl
[info]       copyright: © 2019-2026 Ossum, Inc.
[info]        built at: 2026-07-27 11:04:12.117-0400
[info]        licenses: Apache-2.0
[info]    organization: Ossum, Inc.
[info]   scala version: 3.9.0
[info]     sbt version: 2.0.2
[info]        jvm name: OpenJDK 64-Bit Server VM
[info]     jvm version: 25.0.1
[info]   operating sys: Mac OS X
```

## Next Steps

- [Command Reference](command-reference.md) - Learn available commands
- [Configuration](configuration.md) - Configure riddlc options
- [GitHub Actions](github-actions.md) - Set up CI/CD validation
