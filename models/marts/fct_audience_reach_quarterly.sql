{{ config(
    materialized='table',
    cluster_by=['broadcast_quarter', 'channel_id']
) }}

with audience as (
    select * from {{ ref('int_barb_audience_with_demographics') }}
),

population as (
    select * from {{ ref('stg_uk_population_baseline') }}
),

quarterly as (
    select
        channel_id,
        demographic_id,
        concat(
            cast(year(broadcast_date) as varchar),
            'Q',
            cast(quarter(broadcast_date) as varchar)
        )                                                           as broadcast_quarter,
        sum(case
            when has_consecutive_15min = true
            then consecutive_15min_viewers_thousands
            else 0
        end)                                                        as reach_thousands
    from audience
    group by 1, 2, 3
),

with_population as (
    select
        q.*,
        p.population_thousands
    from quarterly q
    left join population p
        on q.demographic_id = p.demographic_id
        and cast(left(q.broadcast_quarter, 4) as integer) = p.year
),

final as (
    select
        {{ dbt_utils.generate_surrogate_key([
            'channel_id',
            'demographic_id',
            'broadcast_quarter'
        ]) }}                                                       as audience_reach_quarterly_id,

        channel_id,
        demographic_id,
        broadcast_quarter,

        reach_thousands,

        reach_thousands
            / nullif(population_thousands, 0) * 100                as reach_pct_uk_population,

        true                                                        as is_15min_consecutive,

        current_timestamp()                                         as _dbt_updated_at

    from with_population
)

select * from final
