---
title: "Reactive BBQ Case Study"
description: "A comprehensive RIDDL tutorial using a restaurant chain domain"
---

Some people can learn RIDDL faster by looking at examples than by reading
the informal definitions in the
[language reference](../../references/language-reference.md) or the
formal definitions in the
[EBNF grammar](../../references/ebnf-grammar.md). To support
that mode of learning, this section decomposes the domain of a restaurant,
Reactive BBQ.

## About Reactive BBQ

The Reactive BBQ domain is a familiar one for those who have taken the
Lightbend Reactive Architecture Professional (LRA-P) course which uses
this example throughout the course to good effect in the workshops. The same
premises apply in this domain, but we have chosen to fully specify it in RIDDL.

As you might guess from the name, Reactive BBQ is a restaurant chain that
serves spicy (reactive!) BBQ dishes. It doesn't exist of course, even if some
people may or may not have mistaken
[R&R BBQ in Salt Lake City](https://randrbbq.com/) for the _Reactive_
version in 2018.

The Reactive BBQ case study in the LRA-P course included interviews with
several fictitious employees. Those interviews and the case study material
have been replicated in the [scenario description](scenario.md)
with thanks to Lightbend; we recommend that you read that scenario first.

## Domain Structure

The RIDDL files for Reactive BBQ are arranged into a directory structure,
each with an explanation page as follows:

- [Reactive BBQ Domain](reactive-bbq.md) - The top-level domain
    - [Restaurant](restaurant/index.md) - Restaurant operations context
    - [BackOffice](backoffice/index.md) - Back office administration context
    - [Corporate](corporate/index.md) - Corporate headquarters context

## Personas

The case study includes interviews with key personnel that inform the
domain model:

- [CEO](personas/ceo.md) - Overall business challenges and vision
- [Corporate Head Chef](personas/head-chef.md) - Menu and recipe management
- [Host](personas/host.md) - Reservations and seating
- [Server](personas/server.md) - Order taking and delivery
- [Bartender](personas/bartender.md) - Drink orders and bar service
- [Chef](personas/chef.md) - Kitchen operations
- [Cook](personas/cook.md) - Food preparation
- [Delivery Driver](personas/delivery-driver.md) - Delivery operations
- [Online Customer](personas/online-customer.md) - Online ordering experience
