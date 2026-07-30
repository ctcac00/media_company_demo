{{ config(materialized='table') }}

select
    demographic_id,
    age_band,
    gender,
    social_grade,
    current_timestamp() as _dbt_updated_at
from {{ ref('stg_demographics') }}
