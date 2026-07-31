---
title: "Application"
draft: false
---

An application in RIDDL is not a separate definition type—it is simply a
[Context](context.md) that contains [Group](group.md)s. When a context has
groups, it represents an interface portion of a system where a user (human
or machine) initiates actions.

Applications only define the net result of the interaction between the user
and the system. They are abstract on purpose. There is nothing in RIDDL that
defines how information is provided to a user or received from a user. This
gives free latitude to the user interface designer to manage the entire
interaction between human and machine.

There are also no assumptions about the technology used for implementation.
RIDDL's notion of an application is general and abstract, but can be
implemented as any of the following:

* Mobile Application On Any Platform
* Web Application
* Native Operating System Application (graphical or command line)
* Interactive Voice Recognition
* Virtual Reality with Haptics
* and other things yet to be invented

This means a RIDDL application specification can be used as the basis for
creating multiple implementations using a variety of technologies.

## Groups

Applications abstractly design a user interface by containing a set of
[groups](group.md). Groups can be nested, which allows them to define the
hierarchical structure of a user interface.

## Handlers

Application contexts have message [handlers](handler.md) like other contexts.
These handlers receive messages from [users](user.md) and typically forward
messages to other components like [entities](entity.md).

## See Also

* [Context](context.md) — The definition type used to model applications
* [Group](group.md) — UI structure within application contexts