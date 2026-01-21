---
title: "Duties -- Domain Expert's Guide"
description: "A description of the duties a Domain Expert brings to system specification"
draft: false
weight: 20
---

The duties of the domain expert in the context or making a system specification with
RIDDL are to, simply, provide their expertise. Although helpful, it is not necessary
to understand all the details of RIDDL in order to collaborate with 
[authors](../authors/index.md) and [implementors](../implementors/index.md)
on the system model's definition.

## Know Your Domain
Whatever it is that you know as an expert, that domain knowledge is essential to
the correct construction of a system model. Make sure that you do know it backwards,
upside down, and inside out. Your knowledge from direct experience with the domain
will be most helpful.  For example, if you only know rocket science from the 
perspective of theoretical physics text books, your expertise will be theoretically 
correct but practically useless without hands on experience of building rockets that
successfully reach their objectives.

## Communicate Your Domain

Your knowledge only becomes valuable when shared. As a domain expert, you must
articulate concepts clearly enough that others—whether authors, implementors, or
AI assistants—can translate them into precise specifications.

Effective communication involves:

- **Using precise terminology**: Every domain has specific terms with specific
  meanings. Use them consistently and define them when introducing them.
  RIDDL captures these in `term` definitions that become the project glossary.

- **Providing examples**: Abstract concepts become concrete through examples.
  When describing a business rule, walk through scenarios. When explaining
  a workflow, describe actual cases from your experience.

- **Explaining the "why"**: Don't just state rules—explain the reasoning behind
  them. Understanding intent helps authors make good decisions when the
  specification needs to evolve.

- **Drawing diagrams**: Visual representations often communicate relationships
  more effectively than words. Sketch entity relationships, workflow sequences,
  or state transitions to complement verbal descriptions.

## Be Consistent

Inconsistency creates confusion and errors. Maintain consistency in:

- **Terminology**: Use the same word for the same concept throughout. If you
  call it an "order" in one conversation, don't switch to "purchase request"
  in another without acknowledging the equivalence.

- **Rules**: Business rules should be stated the same way each time. If you
  realize a rule needs refinement, explicitly note the change rather than
  simply stating a different version.

- **Boundaries**: Be consistent about what belongs in your domain versus
  adjacent domains. If inventory management is separate from order processing
  in one discussion, maintain that boundary throughout.

When you notice inconsistencies in your own explanations, point them out.
It's better to acknowledge "I said X before, but I now realize Y is more
accurate" than to leave conflicting information in the specification.

## Respect The Expertise Of Others

RIDDL projects involve multiple disciplines. Authors understand specification
structure. Implementors understand technical constraints. Each brings essential
knowledge.

Respecting expertise means:

- **Listening to concerns**: When an author says "this doesn't fit RIDDL's
  model well" or an implementor says "this will be difficult to scale,"
  take those concerns seriously rather than insisting on your vision.

- **Accepting translation**: Your domain concepts will be expressed in RIDDL's
  abstractions. Trust that authors know how to capture business semantics in
  technical structures, even if the result looks different from how you'd
  describe it informally.

- **Collaborating on trade-offs**: Real systems involve compromises. Work with
  the team to find solutions that honor domain requirements while remaining
  technically feasible.

## Be Open To New Ideas

The process of formalizing domain knowledge often reveals insights. Be open to:

- **Discovering hidden assumptions**: When an author asks "what happens if X
  isn't true?" you may realize you've been assuming something that isn't
  always valid.

- **Finding simplifications**: Sometimes complex business rules, when analyzed
  carefully, can be expressed more simply. Don't cling to complexity for its
  own sake.

- **Considering alternatives**: The way things have always been done isn't
  necessarily the best way. If the specification process reveals opportunities
  for improvement, consider them.

- **Learning from AI suggestions**: AI assistants working with RIDDL may
  propose patterns from other domains that could apply to yours. Evaluate
  these suggestions on their merits.

## Be Patient With Non-Experts

Authors, implementors, and AI assistants are not experts in your domain—that's
why they need you. Patience is essential:

- **Expect repeated questions**: People may need to ask the same thing multiple
  ways to truly understand it. Each question is an opportunity to refine the
  specification.

- **Explain without condescension**: What seems obvious to you may be genuinely
  confusing to others. Explain fundamentals as clearly as advanced concepts.

- **Tolerate approximations**: Early drafts of specifications may not capture
  your domain perfectly. Guide refinement rather than criticizing imprecision.

- **Celebrate progress**: Acknowledge when concepts are captured correctly.
  Positive feedback helps the team know they're on the right track.

The goal is a specification that accurately captures your domain knowledge in
a form that can be validated, documented, and implemented. Your patience in
the process makes that outcome possible.
