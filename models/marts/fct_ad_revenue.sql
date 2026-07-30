{{ config(
    materialized='table',
    cluster_by=['broadcast_date', 'advertiser_id']
) }}

with linear as (
    select
        channel_id,
        advertiser_id,
        campaign_id,
        daypart_id,
        broadcast_date,
        platform,
        delivered_impressions_thousands     as impressions_thousands,
        booked_impressions_thousands,
        actual_revenue_gbp,
        rate_card_cpm_gbp
    from {{ ref('int_ad_spot_enriched_linear') }}
),

avod as (
    select
        channel_id,
        advertiser_id,
        campaign_id,
        daypart_id,
        broadcast_date,
        platform,
        impressions_thousands,
        booked_impressions_thousands,
        actual_revenue_gbp,
        rate_card_cpm_gbp
    from {{ ref('int_ad_spot_enriched_avod') }}
),

combined as (
    select * from linear
    union all
    select * from avod
),

aggregated as (
    select
        {{ dbt_utils.generate_surrogate_key([
            'channel_id',
            'advertiser_id',
            'campaign_id',
            "coalesce(daypart_id, 'all_day')",
            'broadcast_date',
            'platform'
        ]) }}                                                               as ad_revenue_id,

        channel_id,
        advertiser_id,
        campaign_id,
        daypart_id,
        broadcast_date,
        platform,

        sum(impressions_thousands)                                          as impressions_thousands,
        sum(booked_impressions_thousands)                                   as booked_impressions_thousands,
        sum(actual_revenue_gbp)                                             as actual_revenue_gbp,
        avg(rate_card_cpm_gbp)                                              as rate_card_cpm_gbp,

        sum(actual_revenue_gbp)
            / nullif(sum(impressions_thousands), 0)                         as realised_cpm_gbp,

        sum(impressions_thousands)
            / nullif(sum(booked_impressions_thousands), 0)                  as spot_delivery_ratio,

        case
            when sum(impressions_thousands)
                 / nullif(sum(booked_impressions_thousands), 0)
                 < {{ var('underdelivery_threshold') }}
            then true
            else false
        end                                                                 as is_under_delivered,

        current_timestamp()                                                 as _dbt_updated_at

    from combined
    group by 1, 2, 3, 4, 5, 6, 7
)

select * from aggregated
