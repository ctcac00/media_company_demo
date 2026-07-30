with source as (
    select * from {{ source('media_raw', 'dayparts') }}
),
renamed as (
    select
        cast(daypart_id as varchar)        as daypart_id,
        cast(daypart_name as varchar)      as daypart_name,
        cast(start_hour as integer)        as start_hour,
        cast(end_hour as integer)          as end_hour,
        current_timestamp()                as _loaded_at
    from source
)
select * from renamed
