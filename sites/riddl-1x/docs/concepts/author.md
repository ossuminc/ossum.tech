---
title: "Author"
draft: false
---

An author definition describes one of the authors who wrote the
enclosing model. An author definition contains the usual profile
information for a human including:

* full name
* email address
* name of an organization (optional)
* title at that organization (optional)
* url for more information (optional)

## Syntax

```riddl
domain ECommerce is {
  author Reid is {
    name is "Reid Spencer"
    email is "reid@ossum.com"
  }

  // ... domain body definitions ...
}
```

## Author Definitions vs. Author References

**Author definitions** can only appear in the body of a **Module**
or a **Domain**. They are not permitted inside contexts, entities,
or other processors.

To associate an author with any other definition, use an **author
reference** in that definition's `with { }` metadata block:

```riddl
domain ECommerce is {
  author Reid is {
    name is "Reid Spencer"
    email is "reid@ossum.com"
  }

  context Catalog is {
    ???
  } with {
    by author Reid
  }
}
```

The `by author` reference uses a path identifier that resolves to
an author definition in an enclosing Module or Domain.

## Occurs In

Author **definitions** occur in:

* [Root](root.md) (via Module)
* [Domains](domain.md)

Author **references** (`by author`) occur in:

* [Metadata](metadata.md) blocks (`with { }`) on any definition

## Contains

No other definitions.
