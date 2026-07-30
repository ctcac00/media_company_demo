with source as (
    select * from {{ source('media_raw', 'streaming_sessions') }}
),
renamed as (
    select
        cast(session_id as varchar)              as session_id,
        cast(user_id as varchar)                 as user_id,
        cast(session_start as timestamp_ntz)     as session_start,
        cast(session_end as timestamp_ntz)       as session_end,
        cast(platform as varchar)                as platform,
        cast(device_type as varchar)             as device_type,
        cast(country as varchar)                 as country,
        cast(is_new_user as boolean)             as is_new_user,
        current_timestamp()                      as _loaded_at
    from source
)
select * from renamed
