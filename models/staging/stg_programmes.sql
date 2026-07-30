with source as (
    select * from {{ source('media_raw', 'programmes') }}
),

renamed as (
    select
        cast(programme_id as varchar)            as programme_id,
        cast(title as varchar)                   as title,
        cast(genre as varchar)                   as genre,
        cast(sub_genre as varchar)               as sub_genre,
        cast(is_original_uk as boolean)          as is_original_uk,
        cast(is_news_current_affairs as boolean) as is_news_current_affairs,
        cast(duration_min as integer)            as duration_min,
        current_timestamp()                      as _loaded_at
    from source
)

select * from renamed
