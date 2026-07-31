---
title: "Projectors"
draft: false
---

Projectors get their name from
[Euclidean Geometry](https://en.wikipedia.org/wiki/Projection_(mathematics))
but are probably more analogous to a
[relational database view](https://en.wikipedia.org/wiki/View_(SQL)). The
concept is very simple in RIDDL: projectors gather data from entities and
other sources, transform that data into a specific record type, and support
querying that data arbitrarily.

Projectors transform update events from entities into a data set that can
be more easily queried. Projectors have handlers that specify both how to
apply updates to the projector's state and satisfy queries against that state.
A projector's data is always a duplicate and not the system of record for the
data. Typically persistent entities are the system of record.



## Occurs In
* [Contexts](context.md)

## Contains
* [Fields](field.md)
* [Handlers](handler.md)
* [Includes](include.md)
