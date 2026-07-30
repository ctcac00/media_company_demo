{{ config(
    materialized='table',
    cluster_by=['broadcast_date', 'channel_id']
) }}

with audience as (
    select * from {{ ref('int_barb_audience_with_demographics') }}
),

consolidated as (
    select * from {{ ref('stg_barb_consolidated_audience') }}
),

population as (
    select * from {{ ref('stg_uk_population_baseline') }}
),

schedule as (
    select distinct
        programme_id,
        channel_id,
        broadcast_date
    from {{ ref('int_programme_schedule_enriched') }}
),

-- Join population baseline
with_population as (
    select
        audience.*,
        population.population_thousands
    from audience
    left join population
        on audience.demographic_id = population.demographic_id
        and year(audience.broadcast_date) = population.year
),

-- Join consolidated audience (overnight + C7)
with_consolidated as (
    select
        wp.*,
        consolidated.overnight_viewers_thousands,
        consolidated.c7_viewers_thousands,
        consolidated.c7_viewers_thousands is not null  as is_c7_consolidated
    from with_population wp
    left join consolidated
        on wp.programme_id = consolidated.programme_id
        and wp.channel_id = consolidated.channel_id
        and wp.broadcast_date = consolidated.broadcast_date
),

-- Compute share of viewing: channel's viewers / total viewers across all channels on that date
viewing_totals as (
    select
        broadcast_date,
        demographic_id,
        sum(programme_viewers_thousands) as total_uk_viewing_thousands
    from audience
    group by 1, 2
),

final as (
    select
        {{ dbt_utils.generate_surrogate_key([
            'wc.programme_id',
            'wc.channel_id',
            'wc.broadcast_date',
            'wc.demographic_id'
        ]) }}                                                                   as programme_audience_daily_id,

        wc.programme_id,
        wc.channel_id,
        wc.broadcast_date,
        wc.demographic_id,

        -- TVR: viewers / population * 100 (CA-01)
        wc.programme_viewers_thousands
            / nullif(wc.population_thousands, 0) * 100                         as tvr_pct,

        wc.overnight_viewers_thousands,
        wc.c7_viewers_thousands,
        wc.is_c7_consolidated,

        -- Share of viewing: channel viewers / total UK viewers on that date (CA-03)
        wc.programme_viewers_thousands
            / nullif(vt.total_uk_viewing_thousands, 0) * 100                   as share_of_viewing_pct,

        -- Reach: consecutive 15-min approximation (hourly grain, CA-04)
        wc.consecutive_15min_viewers_thousands                                  as reach_15min_thousands,

        current_timestamp()                                                     as _dbt_updated_at

    from with_consolidated wc
    left join viewing_totals vt
        on wc.broadcast_date = vt.broadcast_date
        and wc.demographic_id = vt.demographic_id
)

select * from final
