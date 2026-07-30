with source as (
    select * from {{ source('media_raw', 'channels') }}
),

renamed as (
    select
        cast(channel_id as varchar)      as channel_id,
        cast(channel_name as varchar)    as channel_name,
        cast(broadcaster as varchar)     as broadcaster,
        cast(is_media_company_portfolio as boolean) as is_media_company_portfolio,
        cast(is_psb as boolean)          as is_psb,
        current_timestamp()              as _loaded_at
    from source
)

select * from renamed
