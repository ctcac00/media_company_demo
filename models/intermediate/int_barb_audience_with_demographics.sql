with barb as (
    select * from {{ ref('stg_barb_minute_ratings') }}
),

demographics as (
    select * from {{ ref('stg_demographics') }}
),

channels as (
    select * from {{ ref('stg_channels') }}
),

daily_aggregated as (
    select
        channel_id,
        programme_id,
        demographic_id,
        broadcast_date,
        avg(tvr_pct)                as tvr_pct,
        sum(viewers_thousands)      as programme_viewers_thousands,
        count(broadcast_hour)       as hours_in_programme
    from barb
    group by 1, 2, 3, 4
),

enriched as (
    select
        daily_aggregated.channel_id,
        daily_aggregated.programme_id,
        daily_aggregated.demographic_id,
        daily_aggregated.broadcast_date,
        daily_aggregated.tvr_pct,
        daily_aggregated.programme_viewers_thousands,
        daily_aggregated.hours_in_programme,

        -- Consecutive 15-min reach approximation at hourly grain
        -- True when viewers > 0 for at least 1 continuous hour (60+ minutes)
        -- Note: Exact 15-min window requires minute-level data per CA-04
        case
            when daily_aggregated.programme_viewers_thousands > 0
                 and daily_aggregated.hours_in_programme >= 1
            then true
            else false
        end                         as has_consecutive_15min,

        -- Approximate reach for hour-level grain
        case
            when daily_aggregated.programme_viewers_thousands > 0
                 and daily_aggregated.hours_in_programme >= 1
            then daily_aggregated.programme_viewers_thousands
            else 0
        end                         as consecutive_15min_viewers_thousands,

        -- Demographic attributes
        demographics.age_band,
        demographics.gender,
        demographics.social_grade,

        -- Channel attributes
        channels.channel_name,
        channels.broadcaster,
        channels.is_media_company_portfolio,
        channels.is_psb

    from daily_aggregated
    left join demographics
        on daily_aggregated.demographic_id = demographics.demographic_id
    left join channels
        on daily_aggregated.channel_id = channels.channel_id
)

select * from enriched
