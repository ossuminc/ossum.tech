---
title: "Design Principles"
description: "Foundational principles guiding RIDDL's design"
---

# RIDDL Design Principles

RIDDL is a high-level system specification language. These principles guide
its design and evolution.

## 1. Declarative

RIDDL adopts a *what, not how* principle. It is not an implementation
language and does not pretend to be computationally complete.

Details are for software developers. The analyst or architect who writes
RIDDL specifications wants to describe *what* the system is while abstracting
away *how* to construct it. It is like city planning—defining what should
exist—not laying pipes, providing power, or paving roads.

A specification states what needs to be produced but not how it will be
realized (implemented). RIDDL specifications model large, complicated
knowledge domains. A RIDDL model must be complete enough that all parts are
recognizable and what it will do is discernable, without understanding how
it will be produced.

## 2. Both Data and Process

RIDDL models appreciate that the dichotomy between "doing" (process) and
"being" (data) is false. Modern computing systems that model reality must be
both.

Strictly data-oriented specification languages and strictly process-oriented
specification languages are insufficient. RIDDL must be both. As Kurt Vonnegut
wrote in "Deadeye Dick":

> Socrates: To be is to do
> Sartre: To do is to be
> Sinatra: Do be do be doooo

## 3. Completeness

The specification must provide implementors all the information they need to
complete the implementation of the system, *and no more*.

RIDDL specifications should be:

- **Sufficient** - All necessary information is present
- **Minimal** - No extraneous detail
- **Unambiguous** - One interpretation is possible

## 4. Sufficiently Formal

A RIDDL specification should be sufficiently formal that it can be tested for:

- Consistency
- Correctness
- Completeness
- Other desirable properties

The `riddlc` compiler aims to verify these properties automatically through
its validation passes.

## 5. Familiar Terms

The specification should discuss the system in terms that are normal and
common for users, implementors, and subject-matter experts.

While RIDDL introduces keywords that require explanation, Domain-Driven
Design (DDD) terminology is used as the primary model to reinforce this
principle. Terms like *domain*, *context*, *entity*, and *handler* should
be familiar to anyone with DDD experience.

## 6. Rapidly Translatable

RIDDL exists to reduce the burden on system architects, business analysts,
and others who must manage complexity and large volumes of concepts.

Without the ability to rapidly translate the specification into useful
artifacts, the language would not have high utility. RIDDL can produce:

- **Documentation websites** - Complete documentation for the specified model
- **Diagrams** - Visual comprehension of the model structure
- **Code artifacts** - Ease the software developer's burden
- **Other artifacts** - Through extension plugins

## Implications for Authors

These principles inform how you should write RIDDL specifications:

1. **Focus on *what*, not *how*** - Describe the business domain, not
   implementation details

2. **Define complete behavior** - Specify all relevant events, commands,
   and responses

3. **Use domain terminology** - Let your ubiquitous language shine through

4. **Keep it testable** - Write specifications that can be validated by tools

5. **Remember the readers** - Specifications should be readable by all
   stakeholders

## Related

- [Author's Guide](../authors/index.md) - Writing RIDDL specifications
- [Language Reference](../../references/language-reference.md) - Complete
  language documentation
