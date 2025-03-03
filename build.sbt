// build.sbt

lazy val developers: List[Developer] = List(
  Developer(
    id = "reid-spencer",
    "Reid Spencer",
    "reid.spencer@ossuminc.com",
    url("https://github.com/reid-spencer")
  )
)

lazy val root = Root(
  "ossum-tech",
  "ossuminc",
  "com.ossum.doc",
  startYr = 2025,
  devs = developers
).settings(name := "ossum-tech")
