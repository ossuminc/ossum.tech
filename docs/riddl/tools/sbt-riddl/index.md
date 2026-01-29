---
title: "sbt-riddl Plugin"
description: "SBT plugin for RIDDL integration"
---

# sbt-riddl Plugin

The `sbt-riddl` plugin integrates RIDDL validation into your Scala/sbt build
process. This allows you to validate RIDDL models as part of your normal
compilation workflow.

## Installation

Add to your `project/plugins.sbt`:

```scala
addSbtPlugin("com.ossuminc" %% "sbt-riddl" % "1.0.0")
```

Replace `1.0.0` with the [latest version](https://github.com/ossuminc/riddl/releases).

## Configuration

In your `build.sbt`:

```scala
// Enable the plugin
enablePlugins(RiddlSbtPlugin)

// Specify riddlc options to run during compile
riddlcOptions := Seq(
  "--verbose",
  "from", "src/main/riddl/riddl.conf",
  "validate"
)

// Minimum riddlc version required
riddlcMinVersion := "1.0.0"
```

## Usage

Once configured, RIDDL validation runs automatically with `compile`:

```bash
sbt compile
```

To run validation explicitly:

```bash
sbt riddlValidate
```

## Configuration Options

### riddlcOptions

Command-line arguments passed to `riddlc`:

```scala
riddlcOptions := Seq(
  "--verbose",
  "--show-times",
  "from", "path/to/config.conf",
  "validate"
)
```

### riddlcMinVersion

Minimum `riddlc` version required for this project:

```scala
riddlcMinVersion := "1.0.0"
```

The plugin will fail if the installed `riddlc` is older than this version.

### riddlcPath

Override the path to the `riddlc` executable:

```scala
riddlcPath := file("/usr/local/bin/riddlc")
```

By default, the plugin searches the PATH.

## Example Project Setup

```scala
lazy val root = project
  .in(file("."))
  .enablePlugins(RiddlSbtPlugin)
  .settings(
    name := "my-riddl-project",
    riddlcOptions := Seq(
      "from", "src/main/riddl/model.conf",
      "validate"
    ),
    riddlcMinVersion := "1.0.0"
  )
```

With a configuration file at `src/main/riddl/model.conf`:

```hocon
common {
  verbose = true
  show-times = true
}

validate {
  input-file = "MyModel.riddl"
}
```

## Multi-Project Builds

For projects with multiple RIDDL models:

```scala
lazy val domainA = project
  .in(file("domain-a"))
  .enablePlugins(RiddlSbtPlugin)
  .settings(
    riddlcOptions := Seq(
      "validate", "src/main/riddl/DomainA.riddl"
    )
  )

lazy val domainB = project
  .in(file("domain-b"))
  .enablePlugins(RiddlSbtPlugin)
  .settings(
    riddlcOptions := Seq(
      "validate", "src/main/riddl/DomainB.riddl"
    )
  )
```

## CI Integration

The sbt-riddl plugin works seamlessly with CI systems:

```yaml
# GitHub Actions example
- name: Validate RIDDL models
  run: sbt compile
```

## Troubleshooting

### Plugin Not Found

Ensure you're using the correct Scala version for the plugin. The plugin
is published for Scala 2.12 (sbt 1.x default).

### riddlc Not Found

Either:
1. Install `riddlc` and add to PATH
2. Set `riddlcPath` explicitly in `build.sbt`

### Version Mismatch

If you see version errors, update your `riddlcMinVersion` or upgrade your
`riddlc` installation.

## Next Steps

- [riddlc Installation](../riddlc/installation.md) - Install the compiler
- [Configuration](../riddlc/configuration.md) - Config file format
