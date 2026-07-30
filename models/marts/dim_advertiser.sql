{{ config(materialized='table') }}

select
    advertiser_id,
    advertiser_name,
    sector,
    agency,
    current_timestamp() as _dbt_updated_at
from {{ ref('stg_advertisers') }}
