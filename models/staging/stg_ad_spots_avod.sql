with source as (
    select * from {{ source('media_raw', 'ad_spots_avod') }}
),
renamed as (
    select
        cast(impression_id as varchar)          as impression_id,
        cast(campaign_id as varchar)            as campaign_id,
        cast(play_event_id as varchar)          as play_event_id,
        cast(served_at as timestamp_ntz)        as served_at,
        cast(programme_id as varchar)           as programme_id,
        cast(ad_position as varchar)            as ad_position,
        cast(device_type as varchar)            as device_type,
        cast(revenue_gbp as numeric(14,4))      as revenue_gbp,
        current_timestamp()                     as _loaded_at
    from source
)
select * from renamed
