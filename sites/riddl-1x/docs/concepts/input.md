---
title: "Input"
draft: "false"
---

An Input is the abstract notion of some information provided to an
application by its [user](user.md). To make this more tangible, inputs could
be implemented as any of the following:
* the submission of a typical HTML form a user could fill in,
* the tap of a button on a mobile device,
* the selection of items from a list on a native application, 
* a voice response providing information via any
  [IVR](https://wikipedia.com/en/IVR) system,
* a thought interpreted by a neural link,
* a physical movement interpreted by a motion-detection device,
* a retinal scan,
* picking items from lists of information by looking and blinking
* or any other system by which a human may provide information to a machine

The nature of the implementation for an input is up to the UI Designer.
RIDDL's concept of it is based on the net result: the data type received by
the application. 

An input is a named component of an [application](application.md)
that receives data of a specific [type](type.md) from a
[user](user.md) of the application. Each input can define 
data [types](type.md) and declares a 
[command message](message.md#command) as the data received
by the application's input.

## Occurs In
* [Group](group.md)

## Contains
* [Type](type.md)
* [Message](message.md)

