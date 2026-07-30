with source as (
    select * from {{ source('media_raw', 'schedule') }}
),

renamed as (
    select
        cast(broadcast_date as date)      as broadcast_date,
        cast(channel_id as varchar)       as channel_id,
        cast(start_time as timestamp_ntz) as start_time,
        cast(end_time as timestamp_ntz)   as end_time,
        cast(programme_id as varchar)     as programme_id,
        cast(episode_id as varchar)       as episode_id,
        current_timestamp()               as _loaded_at
    from source
)

select * from renamed
