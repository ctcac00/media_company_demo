with consolidated as (
    select * from {{ ref('stg_barb_consolidated_audience') }}
),

schedule as (
    select * from {{ ref('int_programme_schedule_enriched') }}
),

-- Only rows where C7 data is available (TX+8 days rule per CA-02)
c7_ready as (
    select *
    from consolidated
    where datediff('day', broadcast_date, current_date()) >= 8
      and c7_viewers_thousands is not null
),

-- Latest broadcast per programme
latest_broadcast as (
    select *
    from c7_ready
    qualify row_number() over (
        partition by programme_id
        order by broadcast_date desc
    ) = 1
),

-- Get genre from schedule
programme_genres as (
    select distinct
        programme_id,
        genre,
        sub_genre,
        is_original_uk,
        is_news_current_affairs
    from schedule
    qualify row_number() over (
        partition by programme_id
        order by broadcast_date desc
    ) = 1
),

enriched as (
    select
        latest_broadcast.programme_id,
        latest_broadcast.channel_id,
        latest_broadcast.broadcast_date,
        latest_broadcast.overnight_viewers_thousands,
        latest_broadcast.c7_viewers_thousands,
        latest_broadcast.c7_reach_thousands,

        -- C7 uplift calculation (CA-02)
        (latest_broadcast.c7_viewers_thousands - latest_broadcast.overnight_viewers_thousands)
            / nullif(latest_broadcast.overnight_viewers_thousands, 0) as c7_uplift_pct,

        -- CA-02 consolidation flag
        latest_broadcast.c7_viewers_thousands is not null             as is_c7_consolidated,

        -- Genre context for BQ-12 analysis
        programme_genres.genre,
        programme_genres.sub_genre,
        programme_genres.is_original_uk,
        programme_genres.is_news_current_affairs

    from latest_broadcast
    left join programme_genres
        on latest_broadcast.programme_id = programme_genres.programme_id
)

select * from enriched
