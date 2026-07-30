{{ config(materialized='table') }}

with date_spine as (
    {{ dbt_utils.date_spine(
        datepart="day",
        start_date="cast('2020-01-01' as date)",
        end_date="cast('2028-01-01' as date)"
    ) }}
),

dated as (
    select
        date_day,
        dayofweek(date_day)                                                     as day_of_week_num,
        dayname(date_day)                                                       as day_of_week_name,
        weekiso(date_day)                                                       as iso_week,
        month(date_day)                                                         as calendar_month,
        quarter(date_day)                                                       as calendar_quarter,
        year(date_day)                                                          as calendar_year,

        -- UK broadcast week starts Monday
        -- Snowflake: dayofweek returns 0=Sun, 1=Mon, ..., 6=Sat
        dateadd(
            'day',
            case
                when dayofweek(date_day) = 0 then -6   -- Sunday → back 6
                else -(dayofweek(date_day) - 1)         -- Mon=0, Tue=-1, ...
            end,
            date_day
        )                                                                       as broadcast_week_start,

        -- 4-4-5 broadcast month within quarter (CA-13)
        -- Weeks 1-4 of quarter = month 1, weeks 5-8 = month 2, weeks 9+ = month 3
        case
            when mod(weekiso(date_day), 13) between 1 and 4 then 1
            when mod(weekiso(date_day), 13) between 5 and 8 then 2
            else 3
        end                                                                     as broadcast_month_of_quarter,

        concat(
            cast(year(date_day) as varchar),
            'Q',
            cast(quarter(date_day) as varchar)
        )                                                                       as broadcast_quarter,

        (dayofweek(date_day) in (0, 6))                                         as is_weekend,

        -- Placeholder: extend with actual UK bank holiday dates as needed
        false                                                                   as is_uk_bank_holiday,

        current_timestamp()::timestamp_tz                                       as _dbt_updated_at

    from date_spine
)

select * from dated
