with source as (
    select * from {{ source('media_raw', 'ad_spots_linear') }}
),
renamed as (
    select
        cast(spot_id as varchar)                              as spot_id,
        cast(campaign_id as varchar)                          as campaign_id,
        cast(broadcast_date as date)                          as broadcast_date,
        cast(airing_time as timestamp_ntz)                    as airing_time,
        cast(channel_id as varchar)                           as channel_id,
        cast(daypart as varchar)                              as daypart,
        cast(duration_sec as integer)                         as duration_sec,
        cast(booked_impressions_thousands as numeric(14,2))   as booked_impressions_thousands,
        cast(delivered_impressions_thousands as numeric(14,2)) as delivered_impressions_thousands,
        cast(rate_card_cpm_gbp as numeric(8,2))               as rate_card_cpm_gbp,
        cast(actual_revenue_gbp as numeric(14,2))             as actual_revenue_gbp,
        current_timestamp()                                   as _loaded_at
    from source
)
select * from renamed
