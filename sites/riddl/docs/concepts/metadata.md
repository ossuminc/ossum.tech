---
title: "Metadata"
draft: false
---

Metadata in RIDDL provides supplementary information about
definitions—documentation, terminology, attribution, and
implementation hints—without affecting core semantics. All metadata
lives in a `with { }` block that follows the definition's closing
brace.

## Placement

Metadata appears **after** a definition's body, not inside it:

<!-- riddl: in-domain -->
```riddl
context OrderManagement is {
  // body definitions go here (entities, types, handlers, etc.)
  ???
} with {
  // metadata goes here
  briefly "Manages the order lifecycle"
  term Fulfillment is {
    |The complete process of receiving, processing, and
    |delivering an order to the customer.
  }
  option is technology("Kafka")
}
```

## Brief Description

A short, one-line summary using `briefly`:

<!-- riddl: in-context -->
```riddl
entity Customer is { ??? } with {
  briefly "A person or organization that purchases products"
}
```

## Extended Description

Longer documentation using `described by` (or `described as`,
`explained by`, `explained as`):

<!-- riddl: in-context -->
```riddl
entity Customer is { ??? } with {
  described by {
    |Customers are the primary actors in our e-commerce system.
    |They can browse products, place orders, and manage their
    |account information.
  }
}
```

The `|` prefix indicates lines of documentation text in Markdown
format.

## Terms

Domain-specific terminology defined as glossary entries. The syntax
is `term` *identifier* `is` *doc_block*:

```riddl
domain ECommerce is {
  context Catalog is {
    ???
  } with {
    term Listing is {
      |A product's presence in the catalog, including its
      |description, images, pricing, and availability.
    }
  }
} with {
  term SKU is {
    |Stock Keeping Unit—a unique identifier for a specific
    |product variant, including size, color, and other
    |attributes.
  }
}
```

## Options

Options are instructions to translators about how a definition
should be implemented or interpreted. The syntax is `option is`
*option_name* with optional string arguments:

<!-- riddl: in-context -->
```riddl
entity Order is {
  ???
} with {
  option is technology("Akka")
  option is kind("core")
}
```

See [Options](option.md) for the full list of available options
per definition type.

!!! warning "Repeated single-valued metadata"
    `briefly` and `ulid` are single-valued: only the first occurrence is used,
    and repeating either draws a **StyleWarning**. `author`, `see`, `term`,
    `option`, `comment` and `described` may be repeated freely.

!!! warning "Inconsistent terms"
    Defining the same term name at two scopes with **different** definition
    text draws a **StyleWarning** at each conflicting definition. Identical
    redefinitions are fine and produce nothing.

## Scope-Wide Facts Are Definitions, Not Metadata

Facts that apply across a *scope* are definitions in RIDDL rather than metadata
options. [Author](author.md) was always one; RIDDL 2.0 completes the set with
[Version](version.md) and [Copyright](copyright.md).

```riddl
domain Shopping is {
  version 4
  copyright House is "© 2026 Ossum Inc."
  author Reid is { name is "Reid Spencer" email is "reid@ossuminc.com" }
} with {
  briefly as "metadata applies to the domain itself"
}
```

After this change the rule *"metadata options apply to the bearing definition
only"* holds without exception, which is why `version` and `copyright` go in
the body rather than in `with { }`.

## Author Definitions vs. Author References

RIDDL distinguishes between **author definitions** and **author
references**. They serve different purposes and appear in different
places.

### Author Definitions (Body)

Author definitions declare who created or maintains a model. They
can **only** appear in the body of a **Module** or **Domain**—not
in contexts, entities, or other definitions:

```riddl
domain ECommerce is {
  author Reid is {
    name is "Reid Spencer"
    email is "reid@ossum.com"
  }

  context Catalog is { ??? }
}
```

See [Author](author.md) for full details.

### Author References (Metadata)

Author references use `by author` to associate an existing author
definition with any definition's metadata:

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

## Figma References

A `figma` reference connects a model element to the exact frame in a Figma file
that depicts it:

<!-- riddl: in-domain -->
```riddl
application context Storefront is {
  page Checkout is { ??? } with {
    figma "aBcD1234" node "42:1337"
  }
}
```

The two strings are the **file key** and the **node id** — exactly the two
arguments the Figma REST API's nodes endpoint takes — so the reference resolves
to *one frame* rather than to a document a human has to go hunting through.
Before this existed, the only way to connect a design to a model was an opaque
URL in a `briefly`: unreadable by a machine and unverifiable by anything.

A figma reference is **metadata, not a definition**. It has no identifier,
nothing in the model can path-reference it, and it contributes nothing to the
definition hierarchy or the symbol table. It decorates a definition rather than
being one.

It is permitted on [Input](input.md), [Output](output.md), [Group](group.md),
and a [Context](context.md) whose intention is `application` — the definitions
that describe user interface, which is what a Figma frame depicts. The parser
accepts it in any `with` block, as it does every other metadata, and validation
confines it, so a misplaced reference gets a clear **Error** rather than a parse
failure.

### Drift Validation

Drift validation is **opt-in and off by default**. With
`riddlc --check-figma-drift` and a `FIGMA_TOKEN` in the environment:

- a node the API does not know about is an **Error**
- a frame whose name does not correspond to the annotated definition's name is
  a **Warning**
- a file the API cannot read — deleted, moved, or not visible to the token — is
  an **Error** reported as drift, since a missing file is an answer, not a
  failure to get one

Names are compared on **letters and digits only**, so `Payment Screen`,
`PaymentScreen` and `payment_screen` all correspond. The point is to catch a
renamed or repurposed frame, not to police house style.

!!! info "An offline build cannot be affected"
    The flag is off by default; no `FIGMA_TOKEN` means no client at all; and
    every failure to reach or understand the API yields nothing. **Only a
    successful API answer can produce a message.** When the flag is on but no
    client can be had, one informational message says so, and that is the whole
    consequence.

    The HTTP client is configured on the JVM only. Under Scala.js and Scala
    Native it is honestly absent — a browser has no environment to read a token
    from and would be blocked cross-origin anyway.

## Attachments

An attachment associates supplementary material — a diagram, a spreadsheet, an
image — with a definition. There are three forms, and the **MIME type comes
before the content**:

<!-- riddl: in-context -->
```riddl
entity Order is {
  ???
} with {
  // content held in a separate file
  attachment StateChart is image/png in file "diagrams/order-states.png"

  // content given inline
  attachment Note is text/plain as "reviewed 2026-07-29"

  // a ULID identifying the definition
  attachment ULID is "01ARZ3NDEKTSV4RRFFQ69G5FAV"
}
```

The order matters and is easy to get backwards. `attachment X is
"path" as "image/png"` — content first, type second — does **not** parse; the
parser is looking for a MIME type where the path appears.

!!! info "The ULID form became usable in 2.0"
    `attachment ULID is "…"` was documented syntax that could not actually be
    parsed: all three forms begin with the same `attachment` keyword, and
    because the keyword combinator commits, whichever rule came first won
    unconditionally — so the ULID branch was unreachable. The three forms now
    share one keyword match, and each is exercised by a fixture.

    An ordinary attachment merely *named* `ULID` still works: it fails the
    ULID branch at its literal string and falls through to the general form.

## Occurs In

Metadata (`with { }` blocks) can appear on any definition,
including:

* [Domains](domain.md)
* [Contexts](context.md)
* [Entities](entity.md)
* [Types](type.md)
* All other definitions

## Contains

Metadata blocks contain:

* Brief descriptions (`briefly`)
* Extended descriptions (`described by`)
* [Terms](term.md) — glossary entries
* [Options](option.md) — translator instructions
* Author references (`by author`)
* Figma references (`figma "..." node "..."`)
* Attachments
* Comments

Note that [Versions](version.md) and [Copyrights](copyright.md) are *not*
metadata — they are leaf definitions and go in the body.
