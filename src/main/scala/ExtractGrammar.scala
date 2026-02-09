import com.ossuminc.riddl.language.Grammar
import java.nio.file.{Files, Path}

@main def extractGrammar(outputPath: String): Unit =
  val ebnf = Grammar.loadEbnfGrammarOrThrow
  Files.writeString(Path.of(outputPath), ebnf)
  println(s"Wrote ${ebnf.length} chars to $outputPath")
