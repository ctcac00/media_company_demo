with source as (
    select * from {{ source('media_raw', 'streaming_play_events') }}
),
renamed as (
    select
        cast(event_id as varchar)                as event_id,
        cast(event_timestamp as timestamp_ntz)   as event_timestamp,
        cast(user_id as varchar)                 as user_id,
        cast(session_id as varchar)              as session_id,
        cast(programme_id as varchar)            as programme_id,
        cast(episode_id as varchar)              as episode_id,
        cast(event_type as varchar)              as event_type,
        cast(position_sec as integer)            as position_sec,
        cast(platform as varchar)                as platform,
        current_timestamp()                      as _loaded_at
    from source
)
select * from renamed
