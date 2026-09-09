// build.sbt

lazy val developers: List[Developer] = List(
  Developer(
    id = "reid-spencer",
    "Reid Spencer",
    "reid.spencer@ossuminc.com",
    url("https://github.com/reid-spencer")
  )
)

lazy val extractGrammar = taskKey[Unit]("Extract RIDDL grammar via Grammar API")

lazy val root = Root(
  ghRepoName = "ossum-tech",
  ghOrgName = "ossuminc",
  startYr = 2025,
  devs = developers
).configure(
  // 3.9.0, not the org-standard 3.8.4, because that is what riddl builds
  // 2.0.x AND 2.1.x with (checked at the pinned commit, not assumed), and
  // TASTy is not forward-compatible: 3.8.4 accepts 28.0 to 28.8 and fails to
  // load every riddl class.
  //
  // This is the FINAL 3.9.0, and it is an LTS line, so it is expected to hold
  // for a long time. The RC4 pin that stood here through the 2.0 release
  // candidates is gone -- with it goes the experimental-TASTy hazard, where
  // 28.9-experimental-1 could only be read by the exact compiler that emitted
  // it. Keep these two lines in step anyway: bumping the riddl version may
  // require bumping this one to whatever riddl built with.
  With.Scala3.configure(version = Some("3.9.0")),
  With.Riddl.library(version = "2.1.1-26-4d17b1ef", nonJVMDependency = false)
).settings(
  resolvers += "GitHub Package Registry" at "https://maven.pkg.github.com/ossuminc/riddl",

  // Extract RIDDL grammar by compiling and running ExtractGrammar.
  //
  // The library above resolves the STAGED build, not a release, because the
  // language work the docs describe (`on quiescence`, `send ... at`,
  // `streamlet`, the A103 adaptor-boundary rules) is in riddl `main` past the
  // 2.1.1 tag and in no published release. Its JVM `_3` artifacts are in
  // ~/.ivy2/local, which is what makes the exact `git describe` version
  // resolvable.
  //
  // Keep the version above in step with the riddlc that validates the fences.
  // WHICH BINARY THAT IS KEEPS CHANGING, so measure it rather than assuming:
  //   - during the 2.0 RCs it was ../bin/riddlc (PATH lagged by 20 releases)
  //   - when 2.0.0 shipped it flipped to PATH (Homebrew became the release)
  //   - now it is ../bin/riddlc again (riddl is developing past 2.1.1 while
  //     Homebrew still serves 2.0.0)
  // Run `riddlc version && ../bin/riddlc version` and decide from the output.
  // If the pin and the gate compiler drift, the grammar in the docs and the
  // compiler enforcing it are describing different languages.
  // Re-run this task whenever the riddl version here is bumped.
  // Def.uncached because sbt 2 caches task results by hashing their inputs,
  // and this task has no hashable result: it shells out and writes a file as
  // a side effect. Caching it would skip the extraction on a second run.
  extractGrammar := Def.uncached {
    (Compile / compile).value
    val log = streams.value.log
    // sbt 2 hands back HashedVirtualFileRef, not File, so the classpath has
    // to go through the build's FileConverter to become real paths.
    val converter = fileConverter.value
    val cp = (Runtime / fullClasspathAsJars).value
      .map(entry => converter.toPath(entry.data).toAbsolutePath.toString)
      .mkString(java.io.File.pathSeparator)
    // sites/riddl/ only. sites/riddl-1x/ has its own grammar file for the 1.31
    // language and must NOT be overwritten by a 2.x library.
    val target =
      baseDirectory.value / "sites" / "riddl" / "docs" / "references" / "riddl-grammar.ebnf"
    val script = baseDirectory.value / "tools" / "extract-grammar.sh"
    log.info("Extracting RIDDL grammar...")
    val exitCode = scala.sys.process.Process(
      Seq("bash", script.getAbsolutePath, target.getAbsolutePath),
      baseDirectory.value,
      "CLASSPATH" -> cp
    ).!
    if (exitCode != 0) {
      throw new MessageOnlyException("Grammar extraction failed")
    }
  }
)
