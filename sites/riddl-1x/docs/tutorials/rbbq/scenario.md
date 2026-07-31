---
title: "Case Study Scenario"
description: "Overview of the Reactive BBQ case study and personnel interviews"
---

# Reactive BBQ Case Study

The Reactive BBQ restaurant chain has determined that their existing restaurant
operations system is not suitably meeting their needs. They have hired a high
technology consulting company to provide guidance on how they can improve their
customer service, tracking, and reliability.

## The Challenge

The original system was designed for a single restaurant. As the chain expanded
to 500+ locations across 20 countries, they moved to the cloud. However, the
monolithic architecture hasn't scaled well:

- **Performance degradation** during peak hours
- **Cascading failures** that affect multiple or all locations
- **Deployment difficulties** requiring system-wide downtime
- **Resistance to change** - new features require "major refactors"

## Personnel Interviews

To understand the domain and identify requirements, interviews were conducted
with key personnel at Reactive BBQ. Each interview reveals challenges and
requirements that inform the RIDDL model.

### Executive & Corporate

| Role | Key Challenges |
|------|----------------|
| [CEO](personas/ceo.md) | System reliability, scaling, feature additions |
| [Corporate Head Chef](personas/head-chef.md) | Menu distribution, supply chain coordination |

### Front of House

| Role | Key Challenges |
|------|----------------|
| [Host](personas/host.md) | Slow reservations system, frequent failures |
| [Server](personas/server.md) | Order entry bottlenecks, terminal contention |
| [Bartender](personas/bartender.md) | Server notification for ready drinks |

### Kitchen

| Role | Key Challenges |
|------|----------------|
| [Chef](personas/chef.md) | Lost orders when system fails, handwritten fallback |
| [Cook](personas/cook.md) | Illegible handwritten tickets, frustrated servers |

### Delivery & Online

| Role | Key Challenges |
|------|----------------|
| [Delivery Driver](personas/delivery-driver.md) | App connectivity, payment collection |
| [Online Customer](personas/online-customer.md) | Website/app unreliability |

## Common Themes

Across all interviews, several themes emerge:

1. **Reliability** - The system fails too often, forcing manual workarounds
2. **Responsiveness** - Performance degrades under load
3. **Isolation** - Failures cascade across the entire system
4. **Flexibility** - New features are difficult and risky to add

These themes directly inform the reactive architecture principles that RIDDL
helps model: resilience, elasticity, message-driven communication, and
bounded contexts.

## Next Steps

After reviewing the interviews, proceed to the domain model:

- [Reactive BBQ Domain](reactive-bbq.md) - The top-level domain structure
- [Restaurant Context](restaurant/index.md) - Core restaurant operations
- [BackOffice Context](backoffice/index.md) - Administrative operations
- [Corporate Context](corporate/index.md) - Corporate headquarters functions
