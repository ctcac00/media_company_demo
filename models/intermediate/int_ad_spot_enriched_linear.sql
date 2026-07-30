with spots as (
    select * from {{ ref('stg_ad_spots_linear') }}
),

campaigns as (
    select * from {{ ref('stg_ad_campaigns') }}
),

advertisers as (
    select * from {{ ref('stg_advertisers') }}
),

dayparts as (
    select * from {{ ref('stg_dayparts') }}
),

enriched as (
    select
        spots.spot_id,
        spots.campaign_id,
        spots.broadcast_date,
        spots.airing_time,
        spots.channel_id,
        spots.duration_sec,
        spots.booked_impressions_thousands,
        spots.delivered_impressions_thousands,
        spots.rate_card_cpm_gbp,
        spots.actual_revenue_gbp,

        -- Campaign fields
        campaigns.advertiser_id,
        campaigns.campaign_name,

        -- Advertiser fields
        advertisers.advertiser_name,
        advertisers.sector,
        advertisers.agency,

        -- Resolve daypart from airing_time
        dayparts.daypart_id,
        dayparts.daypart_name,

        -- Computed metrics
        spots.delivered_impressions_thousands
            / nullif(spots.booked_impressions_thousands, 0)         as spot_delivery_ratio,

        spots.actual_revenue_gbp
            / nullif(spots.delivered_impressions_thousands, 0)      as realised_cpm_gbp,

        case
            when (spots.delivered_impressions_thousands
                  / nullif(spots.booked_impressions_thousands, 0))
                 < {{ var('underdelivery_threshold') }}
            then true
            else false
        end                                                         as is_under_delivered,

        'linear'                                                    as platform

    from spots
    left join campaigns
        on spots.campaign_id = campaigns.campaign_id
    left join advertisers
        on campaigns.advertiser_id = advertisers.advertiser_id
    left join dayparts
        on hour(spots.airing_time) >= dayparts.start_hour
        and hour(spots.airing_time) < dayparts.end_hour
)

select * from enriched
