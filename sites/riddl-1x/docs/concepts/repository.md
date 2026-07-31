---
title: "Repository"
draft: false
---

A RIDDL repository is an abstraction for anything that can retain 
information (e.g. [messages](message.md)) for retrieval at a
later time. This might be a relational database, NoSQL database, a data lake, 
an API, or something not yet invented. There is no specific technology implied
other than the retention and retrieval of information. Thinking of repositories
only as a database is missing the mark. 

## Schemas
As part of their intrinsic definition, repositories have schemas. Schemas in 
implementation and leaves them unspecified. Repository schemas in RIDDL have
little relationship to SQL because they are not relational databases and indeed
must support the schema for any kind of data storage. The schema is specified
more like a graph database.  A set of types defines what can be placed in 
the database, an optional set of links defines how the fields of those types
are related, and a set of indices defines which fields the database indexes. 

A repository may define multiple schemas, each with its own _kind_. The kind of
schema may be: flat, relational, time-series, graphical, hierarchical, star, 
document, columnar, vector, or other. These are only suggestive of the kind of
storage layout the repository uses. 

## Handling Messages
A repository has a [handler](handler.md) that processes 
messages with respect to the repository's stored information.

[Query messages](message.md#query) sent to the repository 
are requests for retrieval of some information. The handler should define 
how the processing of that query should proceed and yield a 
[Result message](message.md#result).

[Command messages](message.md#command) sent to the
repository are updates to the repository. The handler should define how the
update works and may optionally yield an
[Event message](message.md#event) but generally that is
handled at a higher level of abstraction. 

## Occurs In
* [Context](context.md)

## Contains
* [Types](type.md)
* [Messages](message.md)
* [Handler](handler.md)

