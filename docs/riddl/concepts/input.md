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

## Syntax

An input is written as an alias, an identifier, an acquisition verb, and the
type it takes in:

<!-- riddl: skip reason="illustrative fragment; references vocabulary this page does not define" -->
```riddl
form  Signup   accepts type SignupDetails
button Checkout activates type Boolean
picklist Country selects type CountryCode
```

**Aliases**: `input`, `form`, `text`, `button`, `picklist`, `selector`, `item`

**Acquisition verbs**: `acquires`, `reads`, `takes`, `accepts`, `admits`,
`enters`, `provides`, `selects`, `chooses`, `picks`, `initiates`, `submits`,
`triggers`, `activates`, `starts`

The verbs `selects`, `chooses`, `picks`, `enters` and `provides` were added in
RIDDL 2.0; the rest are unchanged.

!!! warning "Selection verbs expect a choice type"
    An input using a **selection** verb — `selects`, `chooses` or `picks` —
    whose type is not a choice among options draws a **StyleWarning**. A
    selection widget should take an
    [Enumeration or Alternation](type.md#compounds); a `String` or an
    `Integer` is almost certainly not what was meant.

    This is never an Error: a predefined type is treated as resolved-but-not-a-
    choice, and a genuinely unresolved reference is skipped so the warning does
    not pile onto the real error.

## Reading an Input

A [handler](handler.md) reads an input's value with the `get from` value
expression:

<!-- riddl: skip reason="illustrative fragment; references vocabulary this page does not define" -->
```riddl
on command Register {
  let details = get from input Signup
  tell command CreateAccount(details) to entity Account
}
```

## Design References

An input may carry a [figma reference](metadata.md#figma-references) linking it
to the frame that depicts it.

## Occurs In
* [Group](group.md)

## Contains
* [Type](type.md)
* [Message](message.md)

