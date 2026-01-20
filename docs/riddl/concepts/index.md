---
title: "Overview"
---

# Overview 
In this section we will explore the concepts and ideas that RIDDL uses. This is
not about the RIDDL language syntax, just the concepts of the language.

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

1. [Root](root.md)
  1. [Domain](domain.md)
    1. [Type](type.md)
    2. [Epic](epic.md)
      1. [Case](case.md)
        1. [Statement](statement.md)
    3. [Context](context.md)
      1. [Type](type.md)
      2. [Group](element.md#group)
        1. [Output](output.md)
        2. [Input](input.md)
      3. [Entity](entity.md)
        1. [Type](type.md)
        2. [Function](function.md)
          1. [Statement](statement.md)
        3. [State](state.md)
          1. [Type](type.md)
          2. [Field](field.md)
          3. [Handler](handler.md)
            1. [On Clause](onclause.md)
              1. [Statement](statement.md)
        4. [Invariant](invariant.md)
          1. [Conditional](conditional.md)
        5. [Handler](handler.md)
          1. [On Clause](onclause.md)
            1. [Statement](statement.md)
      4. [Handler](handler.md)
        1. [On Clause](onclause.md)
          1. [Statement](statement.md)
      5. [Projector](projector.md)
        1. [Type](type.md)
        2. [Field](field.md)
        3. [Handler](handler.md)
          1. [On Clause](onclause.md)
            1. [Statement](statement.md)
      6. [Saga](saga.md)
        1. [Type](type.md)
        2. [SagaStep](sagastep.md)
          1. [Statement](statement.md)
      7. [Adaptor](adaptor.md)
        1. [Type](type.md)
        2. [Handler](handler.md)
          1. [On Clause](onclause.md)
            1. [Statement](statement.md)
      8. [Processor](processor.md)
        1. [Type](type.md)
        2. [Inlet](inlet.md) 
        3. [Outlet](outlet.md)
        4. [Statement](statement.md)
      9. [Function](function.md)
        2. [Statement](statement.md)
      10. [Streamlet](streamlet.md)
        1. [Type](type.md)
        2. [Inlet](inlet.md)
        3. [Outlet](outlet.md)
        4. [Connector](connector.md)

## Next
When you're done exploring all the concepts, check out our 
[guides](../guides/index.md) next.

## Full Index

{{< toc-tree >}}
