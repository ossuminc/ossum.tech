---
title: "Output"
draft: "false"
---

An Output definition is concerned with providing information to the
[user](user.md) without regard to the form of that information when
presented to the user. To make this more tangible, an 
Output could be implemented as any of the following:

* the text shown on a web page or mobile application
* the display of an interactive graphic, chart, etc. 
* the presentation of a video or audio recording
* haptic, olfactory or gustatory feedback
* any other way in which a human can receive information from a machine.

The nature of the implementation for an output is up to the UI Designer.
RIDDL's concept of it is based on the net result: the data type received by
the user.

An Output is a named component of an [application](application.md)
that sends data of a specific [type](type.md) from the application to its
[user](user.md). Each output can define data [types](type.md) and declares a
[result message](message.md#result) as the data sent to the 
user.

## Occurs In
* [Group](group.md)

## Contains
* [Type](type.md)
* [Message](message.md)
