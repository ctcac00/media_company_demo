{{ config(materialized='table') }}

with channels as (
    select * from {{ ref('stg_channels') }}
),

-- Ensure 'streaming' AVOD sentinel exists (may already be in seed)
streaming_sentinel as (
    select
        'streaming'          as channel_id,
        'MediaCo Streaming (AVOD)'  as channel_name,
        'MediaCo'     as broadcaster,
        true            as is_media_company_portfolio,
        true            as is_psb,
        current_timestamp() as _loaded_at
),

combined as (
    select * from channels
    union all
    -- Only add sentinel if not already present
    select * from streaming_sentinel
    where 'streaming' not in (select channel_id from channels)
)

select
    channel_id,
    channel_name,
    broadcaster,
    is_media_company_portfolio,
    is_psb,
    current_timestamp() as _dbt_updated_at
from combined
