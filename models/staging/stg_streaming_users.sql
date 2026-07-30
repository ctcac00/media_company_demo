with source as (
    select * from {{ source('media_raw', 'streaming_users') }}
),
renamed as (
    select
        cast(user_id as varchar)                 as user_id,
        cast(registration_date as date)          as registration_date,
        cast(demographic_id as varchar)          as demographic_id,
        cast(is_active as boolean)               as is_active,
        current_timestamp()                      as _loaded_at
    from source
)
select * from renamed
