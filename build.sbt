// build.sbt

lazy val developers: List[Developer] = List(
  Developer(
    id = "reid-spencer",
    "Reid Spencer",
    "reid.spencer@ossuminc.com",
    url("https://github.com/reid-spencer")
  )
)

// Task to extract EBNF grammar from riddl-language jar
lazy val extractEbnf = taskKey[File]("Extract EBNF grammar from riddl-language jar if newer")

lazy val root = Root(
  ghRepoName = "ossum-tech",
  ghOrgName = "ossuminc",
  startYr = 2025,
  devs = developers
).configure(
  With.Scala3
).settings(
  resolvers += "GitHub Package Registry" at "https://maven.pkg.github.com/ossuminc/riddl",
  libraryDependencies += "com.ossuminc" %% "riddl-language" % "1.1.2+",

  // Define the extractEbnf task - automatically triggers update via dependencyClasspath
  extractEbnf := ExtractEbnf(
    baseDirectory.value,
    (Compile / dependencyClasspath).value.files,
    streams.value.log
  ),

  // Automatically extract EBNF after update resolves dependencies
  update := {
    val updateReport = update.value
    ExtractEbnf.fromUpdateReport(
      baseDirectory.value,
      updateReport,
      streams.value.log
    )
    updateReport
  }
)
