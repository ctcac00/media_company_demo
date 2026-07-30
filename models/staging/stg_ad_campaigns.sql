with source as (
    select * from {{ source('media_raw', 'ad_campaigns') }}
),

renamed as (
    select
        cast(campaign_id as varchar)            as campaign_id,
        cast(advertiser_id as varchar)          as advertiser_id,
        cast(campaign_name as varchar)          as campaign_name,
        cast(start_date as date)                as start_date,
        cast(end_date as date)                  as end_date,
        cast(total_budget_gbp as numeric(14,2)) as total_budget_gbp,
        cast(target_demographic_id as varchar)  as target_demographic_id,
        current_timestamp()                     as _loaded_at
    from source
)

select * from renamed
