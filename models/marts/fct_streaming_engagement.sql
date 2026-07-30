{{ config(
    materialized='table',
    cluster_by=['broadcast_date', 'platform']
) }}

select
    {{ dbt_utils.generate_surrogate_key([
        'session_id',
        'programme_id',
        'broadcast_date'
    ]) }}               as streaming_engagement_id,

    session_id,
    user_id,
    programme_id,
    broadcast_date,
    platform,
    device_type,
    session_duration_min,
    video_starts,
    video_completes,
    completion_rate,
    is_new_user,
    current_timestamp() as _dbt_updated_at

from {{ ref('int_streaming_session_enriched') }}
