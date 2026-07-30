with avod_impressions as (
    select * from {{ ref('stg_ad_spots_avod') }}
),

campaigns as (
    select * from {{ ref('stg_ad_campaigns') }}
),

advertisers as (
    select * from {{ ref('stg_advertisers') }}
),

-- Aggregate to daily grain (confirmed by user — not impression-level)
daily_avod as (
    select
        programme_id,
        campaign_id,
        cast(served_at as date)                         as broadcast_date,
        count(impression_id) / 1000.0                   as impressions_thousands,
        sum(revenue_gbp)                                as actual_revenue_gbp
    from avod_impressions
    group by 1, 2, 3
),

-- Add campaign duration for pro-rata booked impression estimate
with_campaign as (
    select
        daily_avod.programme_id,
        daily_avod.campaign_id,
        daily_avod.broadcast_date,
        daily_avod.impressions_thousands,
        daily_avod.actual_revenue_gbp,
        campaigns.advertiser_id,
        campaigns.total_budget_gbp,
        campaigns.start_date,
        campaigns.end_date,
        datediff('day', campaigns.start_date, campaigns.end_date) + 1 as campaign_duration_days
    from daily_avod
    left join campaigns
        on daily_avod.campaign_id = campaigns.campaign_id
),

enriched as (
    select
        with_campaign.programme_id,
        with_campaign.campaign_id,
        with_campaign.broadcast_date,
        with_campaign.advertiser_id,
        'streaming'                                          as channel_id,
        'avod'                                          as platform,
        cast(null as varchar)                           as daypart_id,
        cast(null as numeric(8,2))                      as rate_card_cpm_gbp,

        with_campaign.impressions_thousands,
        with_campaign.actual_revenue_gbp,

        -- Pro-rata booked impressions from campaign budget
        -- Simplified demo formula: budget / days / 30 (avg CPM) * 1000
        -- This is a demo simplification — documented in YAML
        (with_campaign.total_budget_gbp
            / nullif(with_campaign.campaign_duration_days, 0)
            / 30.0)                                     as booked_impressions_thousands,

        with_campaign.actual_revenue_gbp
            / nullif(with_campaign.impressions_thousands, 0)  as realised_cpm_gbp,

        with_campaign.impressions_thousands
            / nullif(
                (with_campaign.total_budget_gbp
                    / nullif(with_campaign.campaign_duration_days, 0)
                    / 30.0),
                0
            )                                           as spot_delivery_ratio,

        advertisers.advertiser_name,
        advertisers.sector,
        advertisers.agency

    from with_campaign
    left join advertisers
        on with_campaign.advertiser_id = advertisers.advertiser_id
)

select * from enriched
