---
title: "Processors"
draft: false
---

A processor is a  [vital definition](vital.md) that
processes messages that it receives. There are many kinds of processors
in RIDDL:
* [Adaptor](adaptor.md)

some transformation of the data flowing in from
its [inlet](inlet.md), and produces different
data to its [outlet](outlet.md).


## Inlets
An [inlet](inlet.md) provides the name and data type for an 
input to the processor. There can be multiple inlets to the processor or none. 
A processor with no inlets defined is called a _source_ since it originates data
by itself. 

## Outlets

An [outlet](outlet.md) provides the name and data type for an 
output from the processor. There can be multiple outlets defined by the 
processor or none. A processor with no outlets is called a _sink_ since it 
terminates data flow.

## Kinds Of Processors

RIDDL supports six kinds of processors. The kind of processor depends solely
on the number of inlets and outlets that are defined by the processor, as 
shown in the table:

| # Inlets | # Outlets | Kind   | Description                                                 |
|----------|-----------|--------|-------------------------------------------------------------|
| 0        | any       | Source | Sources originate their data, and publish it to an outlet   |
| any      | 0         | Sink   | Sinks terminate their data, and consume it from their inlet |
| 1        | 1         | Flow   | Flows transform their data from inlet to outlet             |
| 1        | any       | Split  | Splits their data from one inlet to multiple outlets        |
| any      | 1         | Merge  | Merges their data from multiple intles to a single outlet   |
| any      | any       | Multi  | Any other combination is a many-to-many flow                |

## Handlers
A processor contains handlers that specify how the business logic should
proceed. For sources, sinks, and flows, this is trivial. But for splits,
merges and multis, there is a need to specify how the messages received on
inlets are processed (transformed) and then put out to the outlets.


## Occurs In
* [Contexts](domain.md)

# Contains
* [Inlets](inlet.md)
* [Outlets](outlet.md)
* [Handlers](handler.md)
