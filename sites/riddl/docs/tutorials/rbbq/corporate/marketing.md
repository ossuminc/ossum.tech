---
title: "Marketing Context"
description: "Multi-channel campaign management and promotions"
---


<!-- riddl-prelude
type CampaignId is Id(Campaign)
type CampaignName is String(1,120)
record StoredCampaign is { campaignId: CampaignId }
event CampaignCreated is { campaignId: CampaignId }
event CampaignLaunched is { campaignId: CampaignId }
event LaunchCampaignRejected is { campaignId: CampaignId, rejectionReason: String(1,500) }
type CampaignEvent is CampaignCreated | CampaignLaunched | LaunchCampaignRejected
entity Campaign is { ??? }
repository CampaignRepository is { ??? }
-->

# Marketing Context

The Marketing context manages marketing campaigns, promotions,
and advertising across multiple channels. It integrates with
the Loyalty context for loyalty-bonus promotions.

## Purpose

A 500-location restaurant chain runs promotional campaigns
across email, social media, in-store signage, the mobile app,
and the website. The Marketing context provides a structured
workflow for creating, scheduling, launching, pausing, and
ending campaigns — with built-in support for promotional
offers.

## Interview Connection

From the [CEO's interview](../personas/ceo.md):

> "I tried to get them to build a loyalty program a couple of
> years ago."

The Marketing context works alongside the
[Loyalty](../restaurant/loyalty.md) context. Campaigns can
include `LoyaltyBonus` promotions that offer bonus points,
connecting marketing efforts directly to customer retention.

## Types

<!-- riddl: in-context no-prelude=CampaignId,CampaignName -->
```riddl
type CampaignId is Id(Campaign)

type CampaignName is String(1,120)
```

The `CampaignChannel` enumeration captures the five channels
a campaign can target. The `CampaignPromotion` record type
bundles the promotion details, including which menu items it
applies to.

## Entity: Campaign

The `Campaign` entity has a 5-command lifecycle:

<!-- riddl: in-context no-prelude=Campaign,CampaignCreated,CampaignLaunched,LaunchCampaignRejected,CampaignCommand,CampaignEvent -->
```riddl
event-sourced entity Campaign as flow is {

  // An event-sourced entity OWNS the commands and events that change it, so
  // they are declared INSIDE it, and every command names the event it yields.
  command CreateCampaign yields event CampaignCreated is { campaignId: CampaignId }
  command LaunchCampaign yields event CampaignLaunched is { campaignId: CampaignId }

  event CampaignCreated is { campaignId: CampaignId }
  event CampaignLaunched is { campaignId: CampaignId }
  event LaunchCampaignRejected is { campaignId: CampaignId, rejectionReason: String(1,500) }

  record CampaignData is { campaignId: CampaignId }

  // Lifecycle phases are named STATES, not a status field: each state
  // declares the commands it accepts, so the compiler knows the machine.
  initial state ActiveCampaign of record CampaignData is {
    handler ActiveCampaignHandler is {
      on cmd: command LaunchCampaign is {
        yield event CampaignLaunched(campaignId = cmd.campaignId)
      }
      // `set` and `morph` may appear ONLY in an `on event` clause here:
      // replay has to re-apply exactly the same change.
      on evt: event CampaignLaunched is {
        morph entity Campaign to state Launched
          with record CampaignData(campaignId = evt.campaignId)
      }
    }
  }

  state Launched of record CampaignData is {
    handler LaunchedHandler is {
      // A command this state does not accept is refused -- and the refusal
      // is PUBLISHED before it is raised, so the attempt is recorded.
      on cmd: command LaunchCampaign is {
        send event LaunchCampaignRejected(campaignId = cmd.campaignId,
          rejectionReason = "Campaign does not accept LaunchCampaign in this state")
          to outlet CampaignEvents
        error "Campaign does not accept LaunchCampaign in this state"
      }
    }
  }

  // A processor receives on its OWN inlet and publishes on its OWN outlet,
  // and a portlet's type must ADMIT everything that travels on it.
  type CampaignCommand is CreateCampaign | LaunchCampaign
  type CampaignEvent is CampaignCreated | CampaignLaunched | LaunchCampaignRejected

  inlet CampaignCommands is type CampaignCommand
  outlet CampaignEvents is type CampaignEvent
}
```

The lifecycle: **Create → Schedule → Launch → (optional Pause)
→ End**.

Note that `campaignChannels` uses `many CampaignChannel` — a
single campaign can target multiple channels simultaneously.
The `campaignPromotion` is `optional` because not every
campaign includes a promotional offer; some are purely
awareness campaigns.

## Repository

<!-- riddl: in-context no-prelude=CampaignRepository,StoredCampaign -->
```riddl
repository CampaignRepository as flow is {
  inlet CampaignRepositoryFromCampaign is type CampaignEvent
  outlet CampaignRepositoryResponses is type CampaignEvent

  record StoredCampaign is { campaignId: CampaignId }

  // A repository that answers queries and declares NO index at all is a
  // sequential scan by construction, and draws a warning saying so.
  schema CampaignSchema is relational
    of rows as type StoredCampaign
      index on field StoredCampaign.campaignId

  command PersistCampaignLaunched is { campaignId: CampaignId }

  handler CampaignPersistence is {
    on command PersistCampaignLaunched is {
      do "update the stored campaign row for this campaignId"
    }
  }
}
```

## Design Decisions

**Why separate from Menu Management?** Marketing campaigns
and menu releases operate on different timelines, involve
different stakeholders, and have different lifecycles. A
marketing campaign might promote existing menu items without
any menu changes. Keeping them separate means the marketing
team doesn't need to coordinate with the menu workflow.

**Why include `LoyaltyBonus` in PromotionType?** This connects
marketing campaigns directly to the loyalty program. A campaign
can offer "Double Points Weekend" by specifying a `LoyaltyBonus`
promotion type. The Loyalty context processes the bonus points
independently.

**Multi-channel support:** The `many CampaignChannel` field
means a campaign targets specific channels. This enables
channel-specific analytics and allows campaigns to be launched
on some channels before others (e.g., email first, then
social media).

## Source

- [`MarketingContext.riddl`](https://github.com/ossuminc/riddl-models/tree/main/hospitality/food-service/reactive-bbq/corporate/MarketingContext.riddl)
- [`marketing-types.riddl`](https://github.com/ossuminc/riddl-models/tree/main/hospitality/food-service/reactive-bbq/corporate/marketing-types.riddl)
- [`Campaign.riddl`](https://github.com/ossuminc/riddl-models/tree/main/hospitality/food-service/reactive-bbq/corporate/Campaign.riddl)
