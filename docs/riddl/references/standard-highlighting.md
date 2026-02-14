---
description: >-
  Standard token types and color scheme used for RIDDL syntax
  highlighting across all editors and documentation tools.
---

# Standard Highlighting

All RIDDL-aware tools—the IntelliJ plugin, VS Code extension,
Synapify editor, ossum.ai playground, and this documentation
site—share a common tokenization scheme for syntax highlighting.
This page documents the standard token types and their associated
colors.

## Token Types

The RIDDL lexer classifies every span of source text into one of
eleven token types, defined in the compiler's AST:

```scala
enum Token(at: At):
  case Punctuation(at: At)
  case QuotedString(at: At)
  case Readability(at: At)
  case Predefined(at: At)
  case Keyword(at: At)
  case Comment(at: At)
  case LiteralCode(at: At)
  case MarkdownLine(at: At)
  case Identifier(at: At)
  case Numeric(at: At)
  case Other(at: At)
```

Each token type has a specific semantic meaning:

| Token Type | What It Covers | Examples |
|------------|----------------|----------|
| **Keyword** | Definition and statement keywords | `domain`, `context`, `entity`, `handler`, `send`, `tell` |
| **Readability** | Connecting words that aid readability | `is`, `of`, `to`, `with`, `by`, `from` |
| **Predefined** | Built-in type names | `String`, `Integer`, `UUID`, `Timestamp`, `Boolean` |
| **Identifier** | User-defined names | `MyEntity`, `OrderPlaced`, `customerId` |
| **QuotedString** | Double-quoted string literals | `"Hello world"`, `"application/json"` |
| **Numeric** | Number literals | `42`, `3.14`, `100` |
| **Punctuation** | Structural delimiters and operators | `{`, `}`, `(`, `)`, `,`, `:`, `=` |
| **Comment** | Line and block comments | `// comment`, `/* block */` |
| **MarkdownLine** | Pipe-prefixed documentation lines | `\|## Heading`, `\|Some description text` |
| **LiteralCode** | Triple-quoted code blocks | ` ```scala ... ``` ` |
| **Other** | Anything not classified above | Placeholder `???`, unrecognized text |

## Standard Color Scheme

The standard RIDDL color scheme uses a dark theme as the primary
palette. Each implementation adapts these colors to its platform
while preserving the semantic intent.

### Dark Theme

| Token Type | Color | Hex | Swatch |
|------------|-------|-----|--------|
| **Keyword** | Burnt orange | `#fa8b61` | <span style="background:#fa8b61;color:#000;padding:2px 12px;border-radius:3px;font-weight:bold">#fa8b61</span> |
| **Readability** | Yellow-olive | `#b3ae60` | <span style="background:#b3ae60;color:#000;padding:2px 12px;border-radius:3px;font-weight:bold">#b3ae60</span> |
| **Predefined** | Teal | `#19c4bf` | <span style="background:#19c4bf;color:#000;padding:2px 12px;border-radius:3px;font-weight:bold">#19c4bf</span> |
| **Identifier** | Light gray | `#a9b7c6` | <span style="background:#a9b7c6;color:#000;padding:2px 12px;border-radius:3px;font-weight:bold">#a9b7c6</span> |
| **QuotedString** | Bright green | `#98c379` | <span style="background:#98c379;color:#000;padding:2px 12px;border-radius:3px;font-weight:bold">#98c379</span> |
| **Numeric** | Steel blue | `#6897bb` | <span style="background:#6897bb;color:#000;padding:2px 12px;border-radius:3px;font-weight:bold">#6897bb</span> |
| **Punctuation** | Teal | `#0da19e` | <span style="background:#0da19e;color:#000;padding:2px 12px;border-radius:3px;font-weight:bold">#0da19e</span> |
| **Comment** | Gray *(italic)* | `#808080` | <span style="background:#808080;color:#000;padding:2px 12px;border-radius:3px;font-weight:bold">#808080</span> |
| **MarkdownLine** | Dim green *(italic)* | `#629755` | <span style="background:#629755;color:#000;padding:2px 12px;border-radius:3px;font-weight:bold">#629755</span> |
| **LiteralCode** | Dim green | `#629755` | <span style="background:#629755;color:#000;padding:2px 12px;border-radius:3px;font-weight:bold">#629755</span> |
| **Other** | Light gray | `#a9b7c6` | <span style="background:#a9b7c6;color:#000;padding:2px 12px;border-radius:3px;font-weight:bold">#a9b7c6</span> |

### Light Theme

| Token Type | Color | Hex | Swatch |
|------------|-------|-----|--------|
| **Keyword** | Dark orange | `#c75a20` | <span style="background:#c75a20;color:#fff;padding:2px 12px;border-radius:3px;font-weight:bold">#c75a20</span> |
| **Readability** | Olive | `#7a7a30` | <span style="background:#7a7a30;color:#fff;padding:2px 12px;border-radius:3px;font-weight:bold">#7a7a30</span> |
| **Predefined** | Teal | `#0d8a85` | <span style="background:#0d8a85;color:#fff;padding:2px 12px;border-radius:3px;font-weight:bold">#0d8a85</span> |
| **Identifier** | Near black | `#2b2b2b` | <span style="background:#2b2b2b;color:#fff;padding:2px 12px;border-radius:3px;font-weight:bold">#2b2b2b</span> |
| **QuotedString** | Forest green | `#50873a` | <span style="background:#50873a;color:#fff;padding:2px 12px;border-radius:3px;font-weight:bold">#50873a</span> |
| **Numeric** | Muted blue | `#4a6a9a` | <span style="background:#4a6a9a;color:#fff;padding:2px 12px;border-radius:3px;font-weight:bold">#4a6a9a</span> |
| **Punctuation** | Teal | `#0a7a75` | <span style="background:#0a7a75;color:#fff;padding:2px 12px;border-radius:3px;font-weight:bold">#0a7a75</span> |
| **Comment** | Gray *(italic)* | `#707070` | <span style="background:#707070;color:#fff;padding:2px 12px;border-radius:3px;font-weight:bold">#707070</span> |
| **MarkdownLine** | Dark green *(italic)* | `#3d6a30` | <span style="background:#3d6a30;color:#fff;padding:2px 12px;border-radius:3px;font-weight:bold">#3d6a30</span> |
| **LiteralCode** | Dark green | `#3d6a30` | <span style="background:#3d6a30;color:#fff;padding:2px 12px;border-radius:3px;font-weight:bold">#3d6a30</span> |
| **Other** | Near black | `#2b2b2b` | <span style="background:#2b2b2b;color:#fff;padding:2px 12px;border-radius:3px;font-weight:bold">#2b2b2b</span> |

## Implementation Notes

### Platform Variations

The standard colors above are the canonical reference. Individual
tools may adapt them to fit their platform's conventions:

- **IntelliJ IDEA Plugin** — Maps token types to IntelliJ's
  `TextAttributesKey` system. Actual colors come from the user's
  selected theme (e.g., Darcula, IntelliJ Light) so they blend
  with the rest of the IDE.

- **VS Code Extension** — Uses TextMate scopes (e.g.,
  `keyword.control.riddl`, `support.type.riddl`). Colors are
  determined by the active VS Code color theme.

- **Synapify / ossum.ai Playground** — These Monaco-based editors
  use a Catppuccin-inspired palette and split the `Keyword` token
  into semantic sub-categories (definition keywords, statement
  keywords, modifier keywords, etc.) for finer-grained coloring.

- **This Documentation Site** — Uses a custom Pygments lexer
  (`riddl_lexer/`) with CSS overrides in `extra.css`. The colors
  in the tables above are taken directly from this implementation.

### Design Principles

The color scheme follows these principles:

1. **Semantic grouping** — Related tokens share color families
   (e.g., teal for types and punctuation, green for strings and
   documentation).

2. **Keywords stand out** — Burnt orange makes structural keywords
   immediately visible against a dark background.

3. **Comments recede** — Gray and italic styling keeps comments
   present but unobtrusive.

4. **Light/dark parity** — Each dark theme color has a
   corresponding light theme variant that maintains the same
   semantic associations at appropriate contrast levels.

### Adding RIDDL Highlighting to a New Tool

To implement RIDDL syntax highlighting in a new editor or tool:

1. **Tokenize** using the eleven `Token` types from the enum above
2. **Map** each token type to your platform's highlighting system
3. **Apply** the standard hex colors (or your platform's closest
   semantic equivalent)
4. **Test** with both light and dark themes

The RIDDL compiler's `Lexer` produces these tokens directly—see
`com.ossuminc.riddl.language.AST.Token` in the
[riddl](https://github.com/ossuminc/riddl) repository.
