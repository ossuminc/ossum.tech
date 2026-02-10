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

```riddl
entity Customer is { ??? } with {
  briefly "A person or organization that purchases products"
}
```

## Extended Description

Longer documentation using `described by` (or `described as`,
`explained by`, `explained as`):

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

```riddl
entity Order is {
  ???
} with {
  option is event-sourced
  option is aggregate
  option is technology("Akka")
  option is kind("core")
}
```

See [Options](option.md) for the full list of available options
per definition type.

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

## Attachments

Attachments associate external files (diagrams, spreadsheets,
images) with a definition:

```riddl
entity Order is {
  ???
} with {
  attachment StateChart is "diagrams/order-states.png"
    as "image/png"
}
```

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
* Attachments
* Comments
