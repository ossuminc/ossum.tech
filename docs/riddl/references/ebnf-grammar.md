# Formal EBNF Grammar

Below is the formal Extended Backus-Naur Form (EBNF) grammar for RIDDL.
This grammar provides a precise definition of RIDDL syntax and can be used as a
reference when constructing valid RIDDL expressions. This grammar is
automatically extracted from the `riddl-language` library and kept in sync
with the reference grammar written in Scala/fastparse form.

!!! info "RIDDL 2.0"
    This is the grammar for RIDDL 2.0. Notable additions over 1.x include the
    generic `processor` rule with `as <shape>` ascription, the context
    `intention` prefix, the `value` and `boolean_expression` sub-languages, the
    `foreach`/`put`/`return`/`yield` statements, the `version` and `copyright`
    definitions, and the `figma` metadata reference. Rules that are retained
    only for backward compatibility carry a comment saying so.

    One rule is worth finding first: **`undefined = {comment} "???"`**. It
    replaces what used to be 23 separate inline `"???"` sites, and it is why a
    comment may introduce a stub — see
    [Undefined Bodies](language-reference.md#undefined-bodies). Each body tries
    `undefined` *before* its content alternative, because a PEG would otherwise
    consume the comments as content and never reach the marker.

```ebnf
--8<-- "riddl/references/riddl-grammar.ebnf"
```
