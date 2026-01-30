---
title: "Comment"
draft: false
---

Comments in RIDDL are semantic elements of the language—they're not simply
ignored by the parser like in most programming languages. RIDDL captures
comments and associates them with nearby definitions, making them available
for documentation generation and tooling.

## Syntax

RIDDL uses C-style comment notation:

```riddl
// Single-line comment extending to end of line

/* Multi-line comment
   that can span
   multiple lines */
```

## Placement Rules

Unlike general-purpose programming languages, RIDDL comments cannot appear
anywhere whitespace is allowed. Valid positions include:

- **Before definitions**: Comments immediately preceding a definition are
  associated with that definition
- **After definitions**: Comments following a definition's closing brace
- **At file scope**: Top-level comments in a file

```riddl
// This comment describes the domain below
domain Inventory is {

  // This comment describes the context
  context Warehouse is {

    // This describes the entity
    entity Product is {
      // ...
    } // End of Product entity

  }
}
```

## Comments vs. Descriptions

RIDDL provides two ways to document definitions:

| Feature | Comments | Descriptions |
|---------|----------|--------------|
| Syntax | `//` or `/* */` | Markdown in `|` blocks |
| Visibility | Captured but secondary | Primary documentation |
| Use case | Implementation notes | User-facing docs |

**Descriptions** are the preferred way to document definitions for end users:

```riddl
domain Inventory is {
  |## Inventory Domain
  |Manages product stock levels, warehouse locations,
  |and inventory movements.

  // Internal note: Consider splitting into sub-domains later
}
```

## Best Practices

1. **Use descriptions for documentation**: Put user-facing content in
   description blocks
2. **Use comments for implementation notes**: TODOs, technical decisions,
   temporary notes
3. **Keep comments concise**: Longer explanations belong in descriptions
4. **Don't duplicate**: If it's in the description, don't repeat in comments

## Occurs In

Comments can appear at file scope and around any definition.

## Contains

Nothing (comments are leaf elements)