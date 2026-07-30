with schedule as (
    select * from {{ ref('stg_schedule') }}
),

programmes as (
    select * from {{ ref('stg_programmes') }}
),

episodes as (
    select * from {{ ref('stg_episodes') }}
),

channels as (
    select * from {{ ref('stg_channels') }}
),

enriched as (
    select
        schedule.broadcast_date,
        schedule.channel_id,
        schedule.start_time,
        schedule.end_time,
        schedule.programme_id,
        schedule.episode_id,

        -- Programme metadata
        programmes.title,
        programmes.genre,
        programmes.sub_genre,
        programmes.is_original_uk,
        programmes.is_news_current_affairs,
        programmes.duration_min,

        -- Episode metadata
        episodes.series_number,
        episodes.episode_number,
        episodes.first_tx_date,

        -- Channel metadata
        channels.channel_name,
        channels.broadcaster,
        channels.is_media_company_portfolio,
        channels.is_psb,

        -- Derived columns
        datediff('minute', schedule.start_time, schedule.end_time) as slot_duration_min,
        hour(schedule.start_time)                                   as broadcast_hour,
        false                                                       as is_simulcast

    from schedule
    left join programmes
        on schedule.programme_id = programmes.programme_id
    left join episodes
        on schedule.episode_id = episodes.episode_id
    inner join channels
        on schedule.channel_id = channels.channel_id
)

select * from enriched
