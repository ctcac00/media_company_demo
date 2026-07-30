with source as (
    select * from {{ source('media_raw', 'barb_minute_ratings') }}
),

renamed as (
    select
        cast(broadcast_date as date)             as broadcast_date,
        cast(broadcast_hour as integer)          as broadcast_hour,
        cast(channel_id as varchar)              as channel_id,
        cast(programme_id as varchar)            as programme_id,
        cast(demographic_id as varchar)          as demographic_id,
        cast(viewers_thousands as numeric(12,2)) as viewers_thousands,
        cast(tvr_pct as numeric(6,3))            as tvr_pct,
        current_timestamp()                      as _loaded_at
    from source
)

select * from renamed
