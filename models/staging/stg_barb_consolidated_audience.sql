with source as (
    select * from {{ source('media_raw', 'barb_consolidated_audience') }}
),

renamed as (
    select
        cast(broadcast_date as date)                       as broadcast_date,
        cast(programme_id as varchar)                      as programme_id,
        cast(channel_id as varchar)                        as channel_id,
        cast(overnight_viewers_thousands as numeric(12,2)) as overnight_viewers_thousands,
        cast(c7_viewers_thousands as numeric(12,2))        as c7_viewers_thousands,
        cast(c7_reach_thousands as numeric(12,2))          as c7_reach_thousands,
        current_timestamp()                                as _loaded_at
    from source
)

select * from renamed
