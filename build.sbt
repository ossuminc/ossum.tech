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
  With.Scala3.configure(version = Some("3.8.4")),
  With.Riddl.library(version = "1.29.0", nonJVMDependency = false)
).settings(
  resolvers += "GitHub Package Registry" at "https://maven.pkg.github.com/ossuminc/riddl",

  // Extract RIDDL grammar by compiling and running ExtractGrammar.
  //
  // CAUTION on this branch: the grammar in docs/ is RIDDL 2.0's, taken
  // directly from riddl's release/2 branch at
  //   language/src/main/resources/riddl/grammar/ebnf-grammar.ebnf
  // because RIDDL 2.0 is not published yet and `With.Riddl.library` above
  // still resolves 1.29.0. Running this task now would silently overwrite the
  // 2.0 grammar with a 1.x one. Bump the library version to 2.0.0 first, then
  // this task is once again the way to keep the grammar in sync.
  extractGrammar := {
    (Compile / compile).value
    val log = streams.value.log
    val cp = (Runtime / fullClasspathAsJars).value
      .map(_.data.getAbsolutePath)
      .mkString(java.io.File.pathSeparator)
    val target = baseDirectory.value / "docs" / "riddl" / "references" / "riddl-grammar.ebnf"
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
