---
title: "Group"
draft: "false"
---

A group is the abstract structuring concept for an application. Groups can be 
nested which allows them to form a hierarchy that defines the structure of a 
user interface. Each group can also contain UI elements such as 
[inputs](input.md) and
[outputs](output.md) as well as [types](type.md).
To make this more tangible, groups could be used to model the following 
implementation concepts:
* HTML forms, pages, containers, and sections
* mobile application screens, pages, forms and containers
* accordions (vertically stacked list of items with show/hide functionality)

A UI designer is free to arrange the contained
elements in any fashion, but presumably in a way that is consistent with
their overall UI design theme.

## Occurs In
* [Application](application.md)
* [Group](group.md)

## Contains
* [Group](group.md) :material-recycle:
* [Type](type.md)
* [Input](input.md)
* [Output](output.md)
