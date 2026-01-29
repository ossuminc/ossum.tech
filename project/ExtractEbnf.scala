import java.nio.file.{Files, StandardCopyOption}
import sbt._
import sbt.librarymanagement.UpdateReport
import sbt.util.Logger

/** Extract EBNF grammar from riddl-language jar.
  * This function copies the EBNF grammar resource from the riddl-language jar
  * to docs/riddl/references/ebnf-grammar.ebnf, but only if the jar version
  * is newer than the local copy.
  */
object ExtractEbnf {

  /** Extract from classpath (for manual task invocation) */
  def apply(
    baseDir: File,
    classpath: Seq[File],
    log: Logger
  ): File = {
    val riddlJar = classpath.find(_.getName.contains("riddl-language"))
    extractFromJar(baseDir, riddlJar, log)
  }

  /** Extract from UpdateReport (for post-update hook) */
  def fromUpdateReport(
    baseDir: File,
    updateReport: UpdateReport,
    log: Logger
  ): File = {
    val riddlJar = updateReport.allFiles.find(_.getName.contains("riddl-language"))
    extractFromJar(baseDir, riddlJar, log)
  }

  private def extractFromJar(
    baseDir: File,
    riddlJar: Option[File],
    log: Logger
  ): File = {
    val targetFile = baseDir / "docs" / "riddl" / "references" / "ebnf-grammar.ebnf"
    val resourcePath = "riddl/grammar/ebnf-grammar.ebnf"

    riddlJar match {
      case Some(jar) =>
        val jarFile = new java.util.jar.JarFile(jar)
        try {
          val entry = jarFile.getEntry(resourcePath)

          if (entry != null) {
            val jarEntryTime = entry.getTime
            val targetTime = if (targetFile.exists()) targetFile.lastModified() else 0L

            if (jarEntryTime > targetTime) {
              log.info(s"Extracting EBNF grammar from ${jar.getName}")
              val is = jarFile.getInputStream(entry)
              try {
                Files.copy(is, targetFile.toPath, StandardCopyOption.REPLACE_EXISTING)
                log.success(s"Updated ${targetFile.getName}")
              } finally {
                is.close()
              }
            } else {
              log.info("EBNF grammar is up to date")
            }
          } else {
            log.error(s"Resource $resourcePath not found in jar")
          }
        } finally {
          jarFile.close()
        }

      case None =>
        log.warn("riddl-language jar not found - EBNF extraction skipped")
    }
    targetFile
  }
}
