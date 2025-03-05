---
title: "States"
draft: false
---

A State defines the state of an [entity](entity.md). It is 
defined as a set of [fields](field.md) with a 
[handler](handler.md) that defines 
how messages cause changes to the value of those fields. 

An [entity](entity.md) can have multiple state definitions with
the implication that this entity would be considered a 
[Finite State Machine](https://en.wikipedia.org/wiki/Finite-state_machine). 
However, it would only be such if the entity used the 
[finite state machine](entity.md#finite-state-machine) 
[option](option.md).


## Occurs In
* [Entities](entity.md)

## Contains
* [Fields](field.md)
* [Handler](handler.md)
