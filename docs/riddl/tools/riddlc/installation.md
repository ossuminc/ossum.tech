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

## Build from Source

Building from source requires JDK 25 and sbt.

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
[info] About riddlc:
[info]            name: riddlc
[info]         version: 1.1.2
[info]   documentation: https://riddl.tech
[info]       copyright: © 2019-2026 Ossum Inc.
[info]        licenses: Apache License, Version 2.0
[info]    organization: Ossum Inc.
[info]   scala version: 3.3.7
```

## Next Steps

- [Command Reference](command-reference.md) - Learn available commands
- [Configuration](configuration.md) - Configure riddlc options
- [GitHub Actions](github-actions.md) - Set up CI/CD validation
