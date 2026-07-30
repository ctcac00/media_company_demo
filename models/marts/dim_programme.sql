{{ config(materialized='table') }}

with programmes as (
    select * from {{ ref('stg_programmes') }}
),

episode_stats as (
    select
        programme_id,
        max(series_number)   as latest_series_number,
        count(episode_id)    as episode_count
    from {{ ref('stg_episodes') }}
    group by 1
)

select
    programmes.programme_id,
    programmes.title,
    programmes.genre,
    programmes.sub_genre,
    programmes.is_original_uk,
    programmes.is_news_current_affairs,
    programmes.duration_min,
    coalesce(episode_stats.latest_series_number, 0) as latest_series_number,
    coalesce(episode_stats.episode_count, 0)        as episode_count,
    current_timestamp()                             as _dbt_updated_at
from programmes
left join episode_stats
    on programmes.programme_id = episode_stats.programme_id
