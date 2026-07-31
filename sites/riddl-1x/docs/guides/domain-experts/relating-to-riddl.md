---
title: "Relating To RIDDL -- Domain Expert's Guide"
description: "How a domain expert should think of RIDDL"
date: 2022-08-06T10:50:32-07:00
draft: false
weight: 10
---

Understanding RIDDL is a complex domain on its own. RIDDL uses a variety of
very abstract concepts that are adept at describing the design and architecture
of computing systems. This section helps you understand just enough RIDDL to
collaborate effectively without becoming a RIDDL expert yourself.

It is up to the [authors](../authors/index.md)
working with you to translate your expertise into a 
system model that uses RIDDL. You could do that even if they
weren't using RIDDL. However, since you're reading this, 
we'll assume they are using RIDDL. Consequently, it
will be beneficial to you and your project to be informed
of the essential concepts in RIDDL. The subsections that
follow will provide that for you.

### Message Passing Systems
The essential tenet of a large distributed system is the
passing of messages between system components. Unlike 
RPCs, APIs or function calls, messages are, essentially, 
the codification of invocations of behavior on the 
component to which they are sent. Even a user clicking
a button implicitly delivers a "you have been clicked"
message to the button. RIDDL models these things directly. 

### Processor

A processor in RIDDL is any component that receives messages and acts on them.
Think of processors as the "actors" in your system—the things that do work.
In your domain, processors might be:

- **People**: A customer service representative who handles complaints
- **Departments**: An accounting department that processes invoices
- **Systems**: A payment gateway that authorizes transactions
- **Devices**: A sensor that reports temperature readings

RIDDL has several kinds of processors, each suited to different purposes:

- **Entity**: Something with identity and persistent state (a customer account,
  an order, an inventory item)
- **Projector**: Something that builds a view from events (a dashboard, a report)
- **Adaptor**: Something that translates between systems
- **Streamlet**: Something that processes flowing data

You don't need to know which type is appropriate—that's the author's job. But
understanding that your domain has distinct "things that do work" helps you
describe them clearly.

### Message

Messages are how processors communicate. Unlike direct function calls, messages
represent complete units of communication that travel between components.
In your domain, messages might be:

- **Commands**: "Place an order", "Cancel subscription", "Update address"
- **Events**: "Order was placed", "Payment received", "Item shipped"
- **Queries**: "What is the account balance?", "Show order history"
- **Results**: The response to a query

When describing your domain, think about what information flows between
different actors. These become the messages in your RIDDL specification.

### Effects (Statements)

When a processor receives a message, it does something—these are effects.
Effects are described using statements like:

- **send**: Emit a message to another processor
- **tell**: Direct a command to a specific entity
- **set**: Change state values
- **morph**: Transform an entity from one state to another
- **become**: Switch to a different handler

As a domain expert, you describe effects in natural language: "When we receive
a payment, we mark the invoice as paid and notify the customer." Authors
translate these descriptions into RIDDL statements.

### Domain

A domain in RIDDL corresponds directly to the DDD concept—a sphere of knowledge
and activity. Your expertise likely centers on one or more domains:

- **E-commerce**: Orders, products, customers, payments
- **Healthcare**: Patients, appointments, treatments, records
- **Finance**: Accounts, transactions, portfolios, regulations

Domains contain contexts (see below) and can reference other domains. When
you describe "what your system does," you're describing domains.

### Context

A context is a bounded area within a domain where specific terms have specific
meanings. This maps to DDD's "bounded context." Within a context:

- Terms have precise definitions
- Rules apply consistently
- A coherent model operates

For example, within an "Order Management" context, an "order" has a specific
meaning and lifecycle. In a "Fulfillment" context, that same concept might be
called a "shipment request" with different attributes.

Identifying context boundaries is crucial. When you notice that the same word
means different things in different situations, you've likely found a context
boundary.

## Concepts

While you could spend a few days wading through the scores of entries in the
[Concepts](../../concepts/index.md) section, you don't really need all that
complexity. Here are the essential ideas:

- **Definition**: Everything in RIDDL is a definition with a name and
  description. Domains, contexts, entities, messages—all are definitions.

- **Type**: Types describe the shape of data. A customer has a name (string),
  age (number), and email (string). Types ensure data consistency.

- **Handler**: Handlers describe what happens when messages arrive. "When
  we receive X, do Y" is the pattern.

- **State**: Entities have state—the data they remember between messages.
  A customer's account balance is state.

- **Epic/Case**: User journeys through the system. These capture how users
  accomplish goals through sequences of interactions.

For deeper understanding, explore the [Concepts](../../concepts/index.md)
section. But for collaborating with authors, these fundamentals are sufficient.
