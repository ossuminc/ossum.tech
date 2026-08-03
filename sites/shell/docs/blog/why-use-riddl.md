---
title: "Why Use RIDDL?"
description: "Why a specification language beats English prompts once a system gets large: context without drift, one model that drives documentation, APIs, schemas and code."
---

# Why Use RIDDL?

!!! quote "About this article"
    By **Reid Spencer**, Ossum Inc. — originally published on LinkedIn,
    1 August 2026.
    [Read the original](https://www.linkedin.com/pulse/why-use-riddl-ossum-inc-wjswe/).

I'll admit that I'm unabashedly trying to drum up more developers and
architects using RIDDL to get more feedback so RIDDL can be perfected or made
useful for many purposes. However, at the core of that effort is one stubborn
question: "Why use RIDDL?" which leads to all the corollary questions:

- How is RIDDL better than simply "vibe coding" or AI-assisted development?
- What does RIDDL have that simple English prompts do not?
- What can RIDDL do that I can't do in a programming language?
- ...

So, let's answer all those questions, and the big one in the title of this
article. I'm hoping by the end you'll see the advantages of developing LARGE
systems with RIDDL.

## How is RIDDL better than simply "vibe coding" or AI-assisted development?

Using AI assistance when developing software has some caveats:

- Even million-token contexts aren't enough to grasp a mega-project

Think of a RIDDL specification as the AI context for your entire system: entire
domains and contexts, all the entities, the repositories and projectors, those
pernicious sagas, every type and message definition, your reactive streams,
.... all of it. Furthermore, RIDDL's syntax is consistent (with very few
special rules) and maps to a well-defined computational model; all the
generators were given that *exact* same model as their basis for generating
code.

Furthermore, you're not locked into the Qwen open-source model that we use by
default. You can use any GGUF model you want (including the not-yet-invented
ones), and you can still have the RIDDL generators use your AI system through
its API. So if you like Claude Code, trust Claude Code, then RIDDL generators
can use Claude Code. You do, of course, need to BYOK.

All this saves you time. If you don't like the way the Java/Quarkus output
works or hate reading Java, then try the Rust generator, or Scala/Pekko, or
Python, or ... Those will all be available soon. Maybe even by the time this is
published.

## What does RIDDL have that simple English prompts do not?

Software development has become increasingly complex. Modern systems are
distributed, event-driven, and must operate at scale. Yet the gap between
business requirements and technical implementation remains wide:

- Business experts understand what the system should do but struggle to
  communicate precise requirements
- Technical teams understand how to build systems but often misinterpret
  business intent
- Documentation becomes outdated the moment it's written
- Code generation from specifications has been limited to narrow domains

The result? Miscommunication, rework, and systems that don't meet business
needs. To combat that, RIDDL is a specification language that is:

- [business readable](/riddl/latest/introduction/why-is-riddl-needed/#1-business-readable-specifications)
- [formally structured](/riddl/latest/introduction/why-is-riddl-needed/#2-formally-structured)
- [designed for translation](/riddl/latest/introduction/why-is-riddl-needed/#3-designed-for-translation)
- [AI ready](/riddl/latest/introduction/why-is-riddl-needed/#4-ai-ready)
- [self documenting](/riddl/latest/introduction/why-is-riddl-needed/#5-self-documenting)
- [translatable to code](/riddlg/latest/)

Writing specifications for enterprises at the Fortune 500 scale requires far
more than simple English prompts. You can do an app and a script that way, but
not an ecosystem of dozens or even hundreds of cooperating services that:

- decompose complex knowledge domains
- are naturally event-driven, streaming and reactive throughout
- utilize CQRS and event-sourcing judiciously
- mind the limitations of the CAP theory
- understand eventual consistency and strong consistency and their tradeoffs
- can use the best (or even favored) technologies

## What can RIDDL do that I can't do in a programming language?

Honestly? Not much. But the question isn't "what", it's "how". Writing systems
in programming languages is now the task for competent AI LLMs: they can do it
faster, better, and cheaper than any human. Alan Turing would be amazed, and
right about his predictions. Since AI can code so well these days, the question
shifts to prompt engineering and context engineering. This is where RIDDL has
always been focused: context and complexity. Although highly readable by
humans, RIDDL is quite succinct and easily processed by AI. The "context" of a
system idea is readily transferable to AI to process as needed. Furthermore,
since we purposefully designed RIDDL around Eric Evans' DDD ("Tackling
Complexity in the Heart of Software" was the subtitle), we also aimed to make
that context representation deal with the inherent complexity of large systems.

Sure, your team of highly qualified software engineers and domain experts can
spend years developing a system full of bugs and misconceptions, OR, those same
domain experts can design a RIDDL model with AI assistance in a matter of
weeks; it can be refined by software engineers and made deployable in a few
more weeks, and then built and deployed in a few days. If you don't like it,
you can regenerate from the same model to a different technology platform.

So if I were to highlight the one thing that matters that a software system
can't easily do it would be this: a single specification can drive all these
things:

- Documentation (asciidoc, hugo, mkdocs, DocBook, Confluence pages)
- API specifications (Smithy, gRPC, OpenAPI, JSON Schema, and AsyncAPI 3.0)
- Schemas and catalogs — SQL DDL in five dialects, DBML, Backstage software
  catalogs, and EventCatalog sites
- Code generation — Java/Quarkus fully supported today, Scala/Pekko, and
  ecosystems around Go, Rust, TypeScript, and Python coming soon.

And that list is unbounded. We can easily add more as new technologies and
languages come to the forefront. Furthermore, generating RIDDL from plain
language is supported by any LLM and a helpful MCP server that knows all the
details of RIDDL.

## What is RIDDL based on?

The RIDDL specification language borrows concepts from all these previous works
developed by some amazing minds:

- [Domain Driven Design (DDD)](https://en.wikipedia.org/wiki/Domain-driven_design)
- [Reactive System Architecture (RSA)](https://www.reactivemanifesto.org/)
- [C4 Model Of Software Architecture](https://c4model.com/)
- [Akka](https://akka.io/)
- [Jacobsen Use Cases 2.0](https://www.ivarjacobson.com/publications/white-papers/use-case-20-e-book)
- [Agile User Stories](https://en.wikipedia.org/wiki/User_story)
- [Behavior Driven Development (BDD)](https://en.wikipedia.org/wiki/Behavior-driven_development)
- [Finite State Machines](https://en.wikipedia.org/wiki/Finite-state_machine)
- [Command/Query Separation](https://en.wikipedia.org/wiki/Command%E2%80%93query_separation)
- [CQRS](https://martinfowler.com/bliki/CQRS.html)
- [Event Sourcing](https://learn.microsoft.com/en-us/azure/architecture/patterns/event-sourcing)
- [Saga Pattern](https://microservices.io/patterns/data/saga.html)
- [Unified Modeling Language (UML)](https://en.wikipedia.org/wiki/Unified_Modeling_Language)

## So, Why Use RIDDL?

Because software architecture shouldn't be lost in translation—or lost in an
LLM's context window.

When enterprise systems reach real-world complexity, unstructured English
prompts fall apart, and manual coding becomes an expensive bottleneck. RIDDL
gives you the ultimate leverage point:

- **Complete AI Control Without Context Drift:** Stop feeding LLMs disjointed
  prompts and praying for cohesive code. RIDDL provides a clean, mathematically
  consistent blueprint of your entire domain, entities, and reactive streams
  that any AI model can process with absolute precision.
- **Write the Intent, Not the Boilerplate:** One specification automatically
  yields your documentation, API contracts, database schemas, and fully
  functional multi-language microservices. When your tech stack or cloud
  provider changes, you don't rewrite—you re-target.
- **Eliminate the Business-to-Code Telephone Game:** Bridge the gap between
  domain experts and software engineers in weeks instead of years. RIDDL turns
  complex domain architecture into an executable contract before a single line
  of production code is written.

You aren't just writing specs—you're building a deterministic, future-proof
engine for your entire enterprise ecosystem.

## Conclusion

RIDDL isn't just another specification language; it's the culmination of
decades spent solving the hardest problems in software engineering. We built
Ossum Inc. around RIDDL because we believe building complex, event-driven
architecture shouldn't feel like fighting your tooling. It should feel
effortless, precise, and—above all—ossum.

We are standing at a fundamental shift in how software is created. As AI takes
over the raw mechanical task of writing code, the real competitive advantage
lies in mastering context, intent, and architectural precision. RIDDL is
designed to be the definitive standard for that new paradigm: a single,
precise, and concise source of truth that turns enterprise-scale complexity
into a deterministic engine. It frees you from the endless churn of boilerplate
and framework lock-in, empowering domain experts and engineers to build what
actually matters without losing the vision along the way.

The future of architecture won't be written in thousands of lines of fragile
hand-coded glue, nor will it be left to unstructured prompts. If you're ready
to stop fighting context drift and build systems that last,
[see how it works](https://ossum.ai/how-it-works/), check out the
[RIDDL documentation](/riddl/latest/), explore our open-source tools on
[GitHub](https://github.com/ossuminc/riddl),
[join our newsletter](https://ossum.ai/#newsletter), and join the Ossum
community today to help shape the future of AI-driven software architecture.
