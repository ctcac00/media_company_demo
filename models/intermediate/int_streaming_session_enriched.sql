with sessions as (
    select * from {{ ref('stg_streaming_sessions') }}
),

users as (
    select * from {{ ref('stg_streaming_users') }}
),

demographics as (
    select * from {{ ref('stg_demographics') }}
),

-- Aggregate play events per session × programme
play_event_agg as (
    select
        session_id,
        programme_id,
        count(case when event_type = 'start'    then 1 end) as video_starts,
        count(case when event_type = 'complete' then 1 end) as video_completes,
        min(event_timestamp)                                 as first_event_ts,
        max(event_timestamp)                                 as last_event_ts
    from {{ ref('stg_streaming_play_events') }}
    group by 1, 2
),

-- Get programme duration for CA-09 filter
programme_durations as (
    select
        programme_id,
        duration_min
    from {{ ref('stg_programmes') }}
),

enriched as (
    select
        sessions.session_id,
        sessions.user_id,
        play_event_agg.programme_id,
        sessions.platform,
        sessions.device_type,
        sessions.is_new_user,
        cast(play_event_agg.first_event_ts as date)         as broadcast_date,

        -- Session engagement metrics
        play_event_agg.video_starts,
        play_event_agg.video_completes,
        datediff(
            'minute',
            play_event_agg.first_event_ts,
            play_event_agg.last_event_ts
        )                                                    as session_duration_min,

        play_event_agg.video_completes
            / nullif(play_event_agg.video_starts, 0)        as completion_rate,

        -- Demographic info
        demographics.age_band,
        demographics.gender,
        demographics.social_grade

    from sessions
    inner join play_event_agg
        on sessions.session_id = play_event_agg.session_id
    left join users
        on sessions.user_id = users.user_id
    left join demographics
        on users.demographic_id = demographics.demographic_id
    left join programme_durations
        on play_event_agg.programme_id = programme_durations.programme_id
    -- CA-09: exclude programmes shorter than 5 minutes (trailers/promos)
    where programme_durations.duration_min >= 5
       or programme_durations.duration_min is null
)

select * from enriched
