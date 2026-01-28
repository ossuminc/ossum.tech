---
title: "On Clauses"
draft: false
---

# On Clause 

An On Clause specifies how to handle a particular kind of message or situation
as part of the definition of a [handler](handler.md). 
An On Clause is associated with a specific message definition and contains 
[statements](statement.md) that define the handling of that 
message by the handler's parent. The containing [Processor](processor.md) is the
recipient of the message and the sender of any statements that send messages.

There are fours kinds of On Clauses:
* _Initialization_ - when the definition is created and initialized
* _Termination_ - when the definition is terminated 
* _Message_ - when the definition receives a specific kind of message
* _Other_ - when the definition receives a message not otherwise handled

## Occurs In

* [Handlers](handler.md) - the handler to which the On 
  clause is applied

## Contains
* [Statement](statement.md) - specifies what should happen 
  when the event occurs
