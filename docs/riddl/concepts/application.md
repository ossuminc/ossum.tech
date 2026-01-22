---
title: "Application"
draft: false
---

An application in RIDDL is represented by a [Context](context.md) that has
[Group](group.md)s in its definition. represents an interface 
portion of a system where an 
user (human or machine) initiates an action on the system. Applications 
only define the net result of the interaction between the user and the 
application. They are abstract on purpose. That is, there is nothing in RIDDL 
that defines how information is provided to a user nor received from a user. 
This gives free latitude to the user interface 
designer to manage the entire interaction between human and machine. 

There are also no assumptions about the technology used for the 
implementation of an application. RIDDL's notion of an application is general
and abstract, but they can be implemented as any of the following:

* Mobile Application On Any Platform
* Web Application
* Native Operating System Application (graphical or command line)
* Interactive Voice Recognition
* Virtual Reality with Haptics
* and other things yet to be invented. 

This means a RIDDL application specification can be used as the basis for 
creating multiple implementations of the specification using a variety of 
technologies.     

## Groups
Applications abstractly design a user interface by containing a set of 
[groups](group.md). Groups can be nested which allows them
to define the structure of a user interface. 

## Handlers
Applications have message [handlers](handler.md) like many other RIDDL definitions. 
However, application handlers only receive their messages from [actors](user.md), 
unlike other handlers. Typically, the handling of messages in handlers will 
ultimately send further messages to other components, like a [context](context.md) or
[entity](entity.md)

## Occurs In
* [Domain](domain.md)

## Contains
* [Type](type.md)
* [Group](element.md)
* [Handler](handler.md)
