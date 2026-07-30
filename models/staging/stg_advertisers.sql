with source as (
    select * from {{ source('media_raw', 'advertisers') }}
),
renamed as (
    select
        cast(advertiser_id as varchar)              as advertiser_id,
        trim(cast(advertiser_name as varchar))      as advertiser_name,
        lower(trim(cast(sector as varchar)))        as sector,
        trim(cast(agency as varchar))               as agency,
        current_timestamp()                         as _loaded_at
    from source
)
select * from renamed
