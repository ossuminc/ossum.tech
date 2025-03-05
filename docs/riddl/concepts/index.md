---
title: "Overview"
---

# Overview 
In this section we will explore the concepts and ideas that RIDDL uses. This is
not about the RIDDL language syntax, but about the concepts that the
language uses and how they relate to each other.

## Definitions
RIDDL consists only of [definitions](definition.md) that define the design of the desired system.  

## Definitional Hierarchy

Definitions in RIDDL are arranged in a hierarchy. Definitions that contain other
definitions are known as *branches*. Definitions that do not
contain other definitions are known as *leaves*.

This is done simply by having an attribute that lists the contents of any 
definition:

* _contents_: The contained definitions that define the container. Not all 
  definitions can contain other ones so sometimes this is empty.

### Simplifications
The valid hierarchy structure is shown below, but to make this hierarchy 
easier to comprehend, we've taken some short-cuts :

1. All the [common attributes](definition.md#common-attributes) 
   have been omitted for brevity but are implied on each line of the 
   hierarchy.
2. We only descend as far as a [Type](type.md) definition. 
   Whenever you see one, you should infer this hierarchy: 
  * [Types](type.md)
    * [Fields](field.md)

### Hierarchy
With those clarifying simplifications, here's the hierarchy:
* [Root](root.md)
  * [Domain](domain.md)
    * [Type](type.md)
    * [Epic](epic.md)
      * [Case](case.md)
        * [Statement](statement.md)
    * [Context](context.md)
      * [Type](type.md)
      * [Group](element.md#group)
        * [Output](output.md)
        * [Input](input.md)
      * [Entity](entity.md)
        * [Type](type.md)
        * [Function](function.md)
          * [Statement](statement.md)
        * [State](state.md)
          * [Type](type.md)
          * [Field](field.md)
          * [Handler](handler.md)
            * [On Clause](onclause.md)
              * [Statement](statement.md)
        * [Invariant](invariant.md)
          * [Conditional](conditional.md)
        * [Handler](handler.md)
          * [On Clause](onclause.md)
            * [Statement](statement.md)
      * [Handler](handler.md)
        * [On Clause](onclause.md)
          * [Statement](statement.md)
      * [Projector](projector.md)
        * [Type](type.md)
        * [Field](field.md)
        * [Handler](handler.md)
          * [On Clause](onclause.md)
            * [Statement](statement.md)
      * [Saga](saga.md)
        * [Type](type.md)
        * [SagaStep](sagastep.md)
          * [Statement](statement.md)
      * [Adaptor](adaptor.md)
        * [Type](type.md)
        * [Handler](handler.md)
          * [On Clause](onclause.md)
            * [Statement](statement.md)
      * [Processor](processor.md)
        * [Type](type.md)
        * [Inlet](inlet.md) 
        * [Outlet](outlet.md)
        * [Statement](statement.md)
      * [Function](function.md)
        * [Statement](statement.md)
      * [Streamlet](streamlet.md)
        * [Type](type.md)
        * [Inlet](inlet.md)
        * [Outlet](outlet.md)
        * [Connector](connector.md)

## Next
When you're done exploring all the concepts, check out our 
[guides](../guides/index.md) next.

## Full Index

{{< toc-tree >}}
