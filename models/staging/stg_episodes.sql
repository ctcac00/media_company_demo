with source as (
    select * from {{ source('media_raw', 'episodes') }}
),

renamed as (
    select
        cast(episode_id as varchar)   as episode_id,
        cast(programme_id as varchar) as programme_id,
        cast(series_number as integer) as series_number,
        cast(episode_number as integer) as episode_number,
        cast(first_tx_date as date)   as first_tx_date,
        cast(synopsis as varchar)     as synopsis,
        current_timestamp()           as _loaded_at
    from source
)

select * from renamed
