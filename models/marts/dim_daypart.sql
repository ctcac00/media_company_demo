{{ config(materialized='table') }}

select
    daypart_id,
    daypart_name,
    start_hour,
    end_hour,
    (daypart_name = 'peak') as is_peak,
    current_timestamp()     as _dbt_updated_at
from {{ ref('stg_dayparts') }}
