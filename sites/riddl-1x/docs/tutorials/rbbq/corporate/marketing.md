---
title: "Marketing Context"
description: "Multi-channel campaign management and promotions"
---

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

```riddl
type CampaignId is Id(Marketing.Campaign) with {
  briefly "Campaign identifier"
  described by "Unique identifier for a marketing campaign."
}

type CampaignStatus is any of {
  CampaignDraftStatus,
  CampaignScheduledStatus,
  CampaignLiveStatus,
  CampaignPausedStatus,
  CampaignEndedStatus
} with {
  briefly "Campaign status"
  described by "Current status of a marketing campaign."
}

type CampaignChannel is any of {
  Email,
  SocialMedia,
  InStore,
  MobileApp,
  Website
} with {
  briefly "Campaign channel"
  described by "Marketing channel for the campaign."
}

type PromotionType is any of {
  PercentDiscount,
  FixedDiscount,
  BuyOneGetOne,
  FreeItem,
  LoyaltyBonus
} with {
  briefly "Promotion type"
  described by "Type of promotional offer."
}

type CampaignPromotion is {
  promotionType is PromotionType
  promotionValue is optional Decimal(8, 2)
  promotionDescription is String(1, 500)
  applicableItems is many optional String(1, 50)
} with {
  briefly "Campaign promotion"
  described by "A promotional offer within a campaign."
}
```

The `CampaignChannel` enumeration captures the five channels
a campaign can target. The `CampaignPromotion` record type
bundles the promotion details, including which menu items it
applies to.

## Entity: Campaign

The `Campaign` entity has a 5-command lifecycle:

```riddl
entity Campaign is {

  command CreateCampaign is {
    campaignId is CampaignId
    campaignName is String(1, 200)
    campaignDescription is String(1, 2000)
    campaignChannels is many CampaignChannel
    campaignPromotion is optional CampaignPromotion
  }

  command ScheduleCampaign is {
    campaignId is CampaignId
    campaignStartDate is Date
    campaignEndDate is Date
  }

  command LaunchCampaign is {
    campaignId is CampaignId
    launchedAt is TimeStamp
  }

  command PauseCampaign is {
    campaignId is CampaignId
    pauseReason is String(1, 500)
  }

  command EndCampaign is {
    campaignId is CampaignId
    endedAt is TimeStamp
  }

  // Events: CampaignCreated, CampaignScheduled, CampaignLaunched,
  //         CampaignPaused, CampaignEnded

  state ActiveCampaign of Campaign.CampaignStateData

  handler CampaignHandler is {
    on command CreateCampaign {
      morph entity Marketing.Campaign to state
        Marketing.Campaign.ActiveCampaign
        with command CreateCampaign
      tell event CampaignCreated to
        entity Marketing.Campaign
    }
    on command ScheduleCampaign {
      tell event CampaignScheduled to
        entity Marketing.Campaign
    }
    on command LaunchCampaign {
      tell event CampaignLaunched to
        entity Marketing.Campaign
    }
    on command PauseCampaign {
      tell event CampaignPaused to
        entity Marketing.Campaign
    }
    on command EndCampaign {
      tell event CampaignEnded to
        entity Marketing.Campaign
    }
  }
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

```riddl
repository CampaignRepository is {
  schema CampaignData is relational
    of campaigns as Campaign
    index on field Campaign.campaignId
    index on field Campaign.campaignStatus
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
