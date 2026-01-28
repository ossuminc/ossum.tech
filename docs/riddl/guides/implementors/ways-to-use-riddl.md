---
title: "Different Ways To Get/Use RIDDL"
description: "RIDDL documentation focused on implementors' usage"
date: 2022-08-06T10:50:32-07:00
draft: false
weight: 30
---

There are several ways to get riddl software on to your computer, depending 
on how you want to work.

## Download
This is the simplest way to get `riddlc`. It should run on Windows, Mac 
and Linux. Follow these steps:
* Go to [the riddlc downloads page](https://github.com/ossuminc/riddl/releases/)
* Click on the release title you want to install
* Scroll down to the "Assets" section
* Download the riddlc-{version}.zip file
* Unzip that file on your computer
* Place the riddlc-{version}/bin directory in your path

## Staged
To use `riddlc` locally and be able to update it with new changes without a 
large download, use this approach:
* `git clone https://github.com/ossuminc/riddl.git`
* `cd riddl`
* Put the `./riddlc/target/universal/stage/bin` directory in your PATH
  variable using a full path instead of "."
* Run `sbt riddlc/stage` to build the program
* To update, run `git pull` from the `riddl` cloned repository directory and
  rerun `sbt riddlc/stage` to rebuild.

This allows you to both make local changes and pull in changes from others to
keep your local copy of `riddlc` up to date.

## Integrate With SBT

For Scala projects, integrating RIDDL into your sbt build allows you to
validate RIDDL specifications as part of your normal compile cycle. There
are two approaches: using the SBT plugin (recommended) or invoking riddlc
directly.

The SBT plugin approach (described in the next section) is preferred because
it integrates seamlessly with sbt's task system, automatically running
validation before compilation.

If you need more control, you can invoke riddlc directly from sbt using a
custom task:

```scala
lazy val validateRiddl = taskKey[Unit]("Validate RIDDL specification")

validateRiddl := {
  import scala.sys.process._
  val result = "riddlc validate src/main/riddl/model.riddl".!
  if (result != 0) throw new RuntimeException("RIDDL validation failed")
}

(Compile / compile) := ((Compile / compile) dependsOn validateRiddl).value
```

## RiddlSbtPlugin

To use the sbt-plugin you must first have installed riddlc by one of the above
methods. This approach allows you to run `riddlc` commands from a sbt based
project. The command you configure will run first when you use the `compile`
command in sbt. Follow these steps:

* In your `plugins.sbt` file, add:
  `addSbtPlugin("com.ossuminc" % "sbt-riddl" % "{version}"). You can find 
  the [latest available version here](https://github.com/ossuminc/riddl/releases)
* In your `build.sbt` file, use `enablePlugins(SbtRiddlPlugin)` on your project
* Set the following sbt settings:
    * `riddlcPath := file("...")` This defaults to "riddlc" which is
      appropriate if the right version is in your path; otherwise specify the
      full path to the `riddlc` command
    * `riddlcOptions := Seq("from", "path/to/config/file", "validate")` This is
      just an example, you can put any command or options you want in that
      sequence. Use `riddlc help` to find out what commands you can use.
* To run validation this way, put a `riddlc.conf` file next to the top
  level `.riddl` file you want to validate. The content of that file can
  specify common options and the commands you want to support from
  `sbt-riddl`. These files use
  [HOCON (Human-Optimized Config Object Notation)](https://github.com/lightbend/config):

```hocon
common {
    show-times = true
    verbose = true
    quiet = false
    dry-run = false
    show-warnings = true
    show-missing-warnings = false
    show-style-warnings = false
}
validate {
    input-file = "MyModel.riddl"
}
```

## Next Steps

Once you have RIDDL integrated into your development workflow:

1. **Validate early and often**: Run validation as part of your CI pipeline
   to catch specification issues before they become implementation problems.

2. **Generate documentation**: Documentation generation will be available
   through [Synapify](../../../synapify/index.md).

3. **Explore code generation**: Code generation from RIDDL models will also
   be available through [Synapify](../../../synapify/index.md).

See the [riddlc documentation](../../tools/riddlc/index.md) for the full
command reference.
