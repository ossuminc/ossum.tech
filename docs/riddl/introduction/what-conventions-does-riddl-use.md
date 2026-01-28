---
title: "What Conventions Does RIDDL Use?"
date: 2022-02-25T10:07:32-07:00
draft: false
weight: 70
---


## Introduction

RIDDL is a language and therefore adopts some syntax and semantic conventions.
RIDDL tries to keep its syntax and semantics very simple and tolerant of user
omissions and formatting. It is intentionally simple and readable for author
and reader comprehension. The following language conventions are adhered to 
throughout the language for ease of use because special cases and rule 
contraventions may cause confusion.

## Freely Formatted
The language is free in its formatting. Indentation is not required and its
various definitions can be arranged on any line with any amount of white 
space. 

## DDD & UML Orientation
RIDDL supports the definition of a variety of concepts (domain, bounded 
context, entity, message, repository, etc.) taken directly from Domain Driven Design
and the Unified Modeling Language.

## Language Consistency
Most things in RIDDL are consistent throughout the language. We believe this
makes learning the language easier since there are no exceptions to fundamental 
constructs and syntax. The sections below define the consistent language features.

## Declarative Definitions
The language is based on declarative definitions. All that means, 
syntactically, is that you name something of a given type, like this:
```riddl
domain Engineering is { ??? }
```
In this example the type is `domain` and the name is `Engineering`. The
rest of the definition, `???`, contains more definitions specific to the
`domain` kind of definition. You don't say how to do something, you specify
the end result you want. The language aims to capture a detailed and
concise definition of the abstractions that a complex system will require. It
does not specify how those abstractions should be built. RIDDL is not a
programming language, but its compiler can generate structurally sound code
that can be completed by a software engineer or AI.

## Definitions May Be Empty On Purpose
You may have noticed in the preceding example, the use of a special sequence, `???`.
This is a language operator that says *"this definition is empty and that's okay"*.
The alternative, `{ }`, is not permitted. The three question marks indicate that the
definition is a work in progress. Modelling a domain can be hard work. New ideas
come up that must be flushed out at a later time.  Sometimes things get left
undefined. That's okay! This operator can be used as the body of
any definition.

## Branches
Branches are definitions that contain other, nested, definitions. Between the
`{` and the `}` that define the boundaries of a definition, you may place other
definitions. Such nested definitions are deemed to be **contained**.
Not every definition is a container.

## Leaves
Definitions that have no content (nested definitions) are referred to
as `leaf definitions` or `leaves` because, like tree leaves, they occur at the
extremities of the hierarchy of definitions.

## Hierarchy Of Definitions
Definitions are specified in a
[strict containment hierarchy](../concepts/index.md#hierarchy). Definitions
that can contain other definitions are known as _containers_. For example,
a domain definition is a recursively nested definition, as follows:
```riddl
domain root is {
  domain branch is {
    domain leaf is { ??? }
  }
}
```
That is, domains are definitions that can contain the definition of (sub)
domains. Similarly `context` can define `entity`
```riddl
context foo is {
  entity bar is { ??? }
}
```

## Every Definition Should Be Documented
Every thing you can define can optionally be documented in a variety of
ways. Documentation should conform to the  
[syntax of the Common Markdown](https://commonmark.org/help/) format.  
We call these
**descriptions** or **explanations** because this is the text that is
used to describe or explain the RIDDL definition, and it is used to generate
documentation for the definition.  A description occurs directly after the
definition's closing curly bracket and is preceded using keywords as
detailed in the subsections below

### Single Literal String
Pretty simple, like this:
```riddl
domain Engineering is { ??? } described by "Stuff about engineering"
domain SomeDomain is { ??? } explained as "Too vague to have a good name"
```

### Documentation Block
Allowing markdown syntax, like this:
```riddl
domain SomeDomain is { ??? } explained as {
  |## Overview
  |This domain is rather vague, it has no content.
  |## Utility
  |The utility of this domain is dubious because:
  |* It has no content
  |* Its name is not useful
  |* It is only an example of RIDDL syntax
}
```
### File Reference

```riddl
domain Engineering is { ??? } described in file "engineering.md"
```

### URL
or
```riddl
domain Engineering is { ??? } described at https://en.wikipedia.org/wiki/Engineering
```

## Definitions May Have Brief Descriptions
Every definition in RIDDL can have a `briefly` or `brief` suffix that in one
short string describes the definition, such as:
```riddl
domain Engineering is { ??? } briefly "The discipline of using natural science, mathematics,
 and design processes to create or improve systems that solve technical problems, 
 or increase efficiency and productivity." 
```

Brief descriptions should be short and concise, like a dictionary, and useful
in a glossary of terms. Brief descriptions must precede the other kinds of descriptions,
like this:

```riddl
domain Engineering is { ??? } briefly "The discipline of using natural science, mathematics,
 and design processes to create or improve systems that solve technical problems, 
 or increase efficiency and productivity." described at https://en.wikipedia.org/wiki/Engineering 
```


### Definitions And References
A definition introduces a named instance of some RIDDL concept (such as `domain`, 
`context` or `entity` as we have seen previously). Sometimes, we need to refer 
to our definitions when defining something else. 

For example, if RIDDL supported the concepts of a Cat and a Person, then you
might specify a cat named "Smudge" with an owner named "Reid" like this:
```text
person Reid is { ??? }
cat Smudge {
  owner: person Reid
}
```
Here is an explanation of each of these tokens:
* `person` is the concept of a human being, intrinsic to RIDDL (its not, this is just an example)
* `Reid` is the name (identifier) of the person being defined
* `is` is an optional keyword for readability to introduce a definition
* `{` is a required token that starts the definition of `Reid` the `person`
* `???` is syntactic sugar meaning "the details of this definition will be determined later"
* `}` is a required token that finishes the definition of `Reid` the `person`
* `cat` is the concept of a feline being, if it were intrinsic to RIDDL
* `Smudge` is the name the author wants to give to this `cat` concept
* `{` is a required token that starts the definition of Smudge the cat
* `owner` is the name of a property that all "cat" concepts have
* `:` is a required token to separate the property name from its value
* `person Reid` is a reference to an instance of a concept, a `person`, with name `Reid`.
* `}` completes the definition of Smudge the cat.

References to every kind of RIDDL concepts are made in this way, by stating
the name of the concept (`cat` or `person` here) followed by the specific instance of
that concept's name.  This is a simple convention used throughout the language for all
concept types and references to them.

## File Inclusion

RIDDL allows source input to be included, inline, from other files. The
`include` keyword specifies a file path (relative to the current file) whose
contents will be parsed as if they appeared at that location. This allows you
to organize large specifications into multiple files.

!!! note "Syntax"
    The `include` keyword takes a literal string path: `include "path/to/file"`

Include statements are only permitted within container definitions. This
prevents fragments of definitions from being separated across files.

For example, this is allowed:

```riddl
domain ThingAmaJig is {
  include "thingamajig/thing-context.riddl"
  include "thingamajig/ama-topic.riddl"
  include "thingamajig/jig-context.riddl"
}
```

While this is **not** allowed:

```riddl
domain
include "ThingAmaJig-domain.riddl"  // ERROR: include inside definition name
```

The domain needs a name before its body begins. As a rule, you can use
`include` right after the opening curly brace of any container definition.

### Organizing Large Models

A typical organization for a large model:

```
myproject/
├── main.riddl              # Top-level file
├── catalog/
│   ├── catalog-context.riddl
│   └── product-entity.riddl
├── shopping/
│   ├── shopping-context.riddl
│   └── cart-entity.riddl
└── fulfillment/
    └── fulfillment-context.riddl
```

With `main.riddl` containing:

```riddl
domain OnlineRetail is {
  include "catalog/catalog-context.riddl"
  include "shopping/shopping-context.riddl"
  include "fulfillment/fulfillment-context.riddl"
}
```

## Future: Directives and Substitutions

!!! warning "Not Yet Implemented"
    The following features are planned but not yet available in RIDDL.

**Directives** will allow preprocessor-style commands:

```riddl
#define COMPANY_NAME = "Acme Corp"
```

**Substitutions** will allow variable replacement:

```riddl
author Company is { name: $COMPANY_NAME }
```

These features may be added in future versions of RIDDL.


 

