#!/usr/bin/env bash
set -euo pipefail

# Extract the RIDDL grammar using Grammar.loadEbnfGrammarOrThrow().
#
# Usage:
#   CLASSPATH=<jars> ./tools/extract-grammar.sh <output-file>
#
# Called by `sbt extractGrammar` which sets CLASSPATH automatically.

OUTPUT="${1:?Usage: extract-grammar.sh <output-file>}"

if [ -z "${CLASSPATH:-}" ]; then
  echo "Error: CLASSPATH not set. Run via 'sbt extractGrammar' instead." >&2
  exit 1
fi

java -cp "$CLASSPATH" extractGrammar "$OUTPUT"
