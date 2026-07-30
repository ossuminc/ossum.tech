---
title: "Application"
draft: false
---

An application in RIDDL is not a separate definition type—it is a
[Context](context.md) declared with the `application`
[intention](context.md#intention), which is the only place
[Group](group.md)s, and therefore user interface, may be modeled. It
represents the interface portion of a system where a user (human or machine)
initiates actions.

<!-- riddl: skip reason="illustrative fragment; references vocabulary this page does not define" -->
```riddl
application context Storefront is {
  page ProductDetails is { ??? }
  page ShoppingCart is {
    button Checkout activates type Boolean
  }
}
```

!!! warning "UI outside an application context is an Error"
    In RIDDL 1.x, any context that happened to contain groups was an
    application. In 2.0 the intention must be declared: a context holding a
    group without the `application` prefix is a hard **Error**.

    This is what makes the application boundary checkable. Because the
    boundary is now explicit, RIDDL can also enforce that a
    [user](user.md) interacts only *at* it — an interaction step putting a
    user opposite something that is neither a UI element nor a definition
    inside an application context is an Error too.

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

Handlers in an application context may also use the `put` statement to publish
a value to an [output](output.md), and read one with `get from input`:

<!-- riddl: skip reason="illustrative fragment; references vocabulary this page does not define" -->
```riddl
handler Checkout is {
  on command PlaceOrder {
    let email = get from input SignupForm
    put email to output ConfirmationPanel
  }
}
```

## Design References

An application context, and the groups, inputs and outputs inside it, may carry
a `figma` reference linking the model element to the exact frame that depicts
it:

<!-- riddl: skip reason="illustrative fragment; references vocabulary this page does not define" -->
```riddl
page Checkout is { ??? } with {
  figma "aBcD1234" node "42:1337"
}
```

See [Metadata](metadata.md#figma-references) for the optional drift validation.

## See Also

* [Context](context.md) — The definition type used to model applications
* [Group](group.md) — UI structure within application contexts
* [Input](input.md) and [Output](output.md) — the data-flow endpoints
* [User](user.md) — who interacts at the application boundary