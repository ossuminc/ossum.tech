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
  With.Scala3.configure(version = Some("3.7.4")),
  With.Riddl.library(version = "1.13.1", nonJVMDependency = false)
).settings(
  resolvers += "GitHub Package Registry" at "https://maven.pkg.github.com/ossuminc/riddl",

  // Extract RIDDL grammar by compiling and running ExtractGrammar
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
