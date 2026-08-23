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
  // 3.9.0-RC4, not the org-standard 3.8.4, because that is what riddl
  // publishes 2.0.x with. An RC compiler emits EXPERIMENTAL TASTy
  // (28.9-experimental-1), which only the exact compiler that produced it can
  // read -- 3.8.4 accepts 28.0 to 28.8 and fails to load every riddl class.
  // Keep these two lines in step: bumping the riddl version may require
  // bumping this one to whatever riddl built with.
  With.Scala3.configure(version = Some("3.9.0-RC4")),
  With.Riddl.library(version = "2.0.0-rc.21", nonJVMDependency = false)
).settings(
  resolvers += "GitHub Package Registry" at "https://maven.pkg.github.com/ossuminc/riddl",

  // Extract RIDDL grammar by compiling and running ExtractGrammar.
  //
  // The library above resolves a real 2.0 build, so this task produces the
  // grammar the docs actually describe -- the hand-copy from riddl's release/2
  // branch that the old 1.29.0 pin forced is no longer needed.
  //
  // Keep the version above in step with ../bin/riddlc, the STAGED 2.0
  // compiler that validates the fences. If they drift, the grammar in the
  // docs and the compiler enforcing it are describing different languages.
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
