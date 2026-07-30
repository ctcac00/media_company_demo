{% macro load_demo_source_data(demo_case='engagement', demo_batch_id=none) %}
    {% set batch_id = demo_batch_id if demo_batch_id is not none else invocation_id %}
    {% set batch_id_sql = batch_id | replace("'", "''") %}

    {% if demo_case != 'engagement' %}
        {{ exceptions.raise_compiler_error("Unsupported demo_case '" ~ demo_case ~ "'. Supported values: engagement.") }}
    {% endif %}

    {% set merge_users_sql %}
        merge into {{ source('media_raw', 'streaming_users') }} as target
        using (
            with demo_rows as (
                select
                    '{{ batch_id_sql }}' as demo_batch_id,
                    1 as row_number,
                    'D006' as demographic_id
                union all
                select
                    '{{ batch_id_sql }}' as demo_batch_id,
                    2 as row_number,
                    'D012' as demographic_id
                union all
                select
                    '{{ batch_id_sql }}' as demo_batch_id,
                    3 as row_number,
                    'D015' as demographic_id
            )

            select
                'DEMO_U_' || abs(hash(demo_batch_id))::varchar || '_' || row_number::varchar as user_id,
                '2026-07-01'::date as registration_date,
                demographic_id,
                true as is_active
            from demo_rows
        ) as source
            on target.user_id = source.user_id
        when matched then update set
            target.registration_date = source.registration_date,
            target.demographic_id = source.demographic_id,
            target.is_active = source.is_active
        when not matched then insert (
            user_id,
            registration_date,
            demographic_id,
            is_active
        ) values (
            source.user_id,
            source.registration_date,
            source.demographic_id,
            source.is_active
        )
    {% endset %}

    {% set merge_sessions_sql %}
        merge into {{ source('media_raw', 'streaming_sessions') }} as target
        using (
            with demo_rows as (
                select
                    '{{ batch_id_sql }}' as demo_batch_id,
                    1 as row_number,
                    'P005' as programme_id,
                    'ios' as platform,
                    'mobile' as device_type,
                    '2026-07-30 19:00:00'::timestamp_ntz as session_start,
                    '2026-07-30 19:45:00'::timestamp_ntz as session_end,
                    true as is_new_user
                union all
                select
                    '{{ batch_id_sql }}' as demo_batch_id,
                    2 as row_number,
                    'P029' as programme_id,
                    'ctv' as platform,
                    'smart_tv' as device_type,
                    '2026-07-30 20:00:00'::timestamp_ntz as session_start,
                    '2026-07-30 20:58:00'::timestamp_ntz as session_end,
                    false as is_new_user
                union all
                select
                    '{{ batch_id_sql }}' as demo_batch_id,
                    3 as row_number,
                    'P046' as programme_id,
                    'web' as platform,
                    'desktop' as device_type,
                    '2026-07-30 21:00:00'::timestamp_ntz as session_start,
                    '2026-07-30 21:30:00'::timestamp_ntz as session_end,
                    false as is_new_user
            )

            select
                'DEMO_S_' || abs(hash(demo_batch_id))::varchar || '_' || row_number::varchar as session_id,
                'DEMO_U_' || abs(hash(demo_batch_id))::varchar || '_' || row_number::varchar as user_id,
                session_start,
                session_end,
                platform,
                device_type,
                'GB' as country,
                is_new_user
            from demo_rows
        ) as source
            on target.session_id = source.session_id
        when matched then update set
            target.user_id = source.user_id,
            target.session_start = source.session_start,
            target.session_end = source.session_end,
            target.platform = source.platform,
            target.device_type = source.device_type,
            target.country = source.country,
            target.is_new_user = source.is_new_user
        when not matched then insert (
            session_id,
            user_id,
            session_start,
            session_end,
            platform,
            device_type,
            country,
            is_new_user
        ) values (
            source.session_id,
            source.user_id,
            source.session_start,
            source.session_end,
            source.platform,
            source.device_type,
            source.country,
            source.is_new_user
        )
    {% endset %}

    {% set merge_events_sql %}
        merge into {{ source('media_raw', 'streaming_play_events') }} as target
        using (
            with demo_sessions as (
                select
                    '{{ batch_id_sql }}' as demo_batch_id,
                    1 as session_number,
                    'P005' as programme_id,
                    'E00052' as episode_id,
                    'ios' as platform,
                    '2026-07-30 19:00:00'::timestamp_ntz as session_start,
                    2700 as complete_position_sec
                union all
                select
                    '{{ batch_id_sql }}' as demo_batch_id,
                    2 as session_number,
                    'P029' as programme_id,
                    'E00292' as episode_id,
                    'ctv' as platform,
                    '2026-07-30 20:00:00'::timestamp_ntz as session_start,
                    3480 as complete_position_sec
                union all
                select
                    '{{ batch_id_sql }}' as demo_batch_id,
                    3 as session_number,
                    'P046' as programme_id,
                    'E00418' as episode_id,
                    'web' as platform,
                    '2026-07-30 21:00:00'::timestamp_ntz as session_start,
                    1800 as complete_position_sec
            ),

            event_steps as (
                select 'start' as event_type, 0.00 as position_multiplier, 1 as event_number
                union all
                select '25pct' as event_type, 0.25 as position_multiplier, 2 as event_number
                union all
                select '50pct' as event_type, 0.50 as position_multiplier, 3 as event_number
                union all
                select '75pct' as event_type, 0.75 as position_multiplier, 4 as event_number
                union all
                select 'complete' as event_type, 1.00 as position_multiplier, 5 as event_number
            )

            select
                'DEMO_EV_' || abs(hash(demo_sessions.demo_batch_id))::varchar || '_' || demo_sessions.session_number::varchar || '_' || event_steps.event_number::varchar as event_id,
                dateadd(
                    second,
                    (demo_sessions.complete_position_sec * event_steps.position_multiplier)::integer,
                    demo_sessions.session_start
                ) as event_timestamp,
                'DEMO_U_' || abs(hash(demo_sessions.demo_batch_id))::varchar || '_' || demo_sessions.session_number::varchar as user_id,
                'DEMO_S_' || abs(hash(demo_sessions.demo_batch_id))::varchar || '_' || demo_sessions.session_number::varchar as session_id,
                demo_sessions.programme_id,
                demo_sessions.episode_id,
                event_steps.event_type,
                (demo_sessions.complete_position_sec * event_steps.position_multiplier)::integer as position_sec,
                demo_sessions.platform
            from demo_sessions
            cross join event_steps
        ) as source
            on target.event_id = source.event_id
        when matched then update set
            target.event_timestamp = source.event_timestamp,
            target.user_id = source.user_id,
            target.session_id = source.session_id,
            target.programme_id = source.programme_id,
            target.episode_id = source.episode_id,
            target.event_type = source.event_type,
            target.position_sec = source.position_sec,
            target.platform = source.platform
        when not matched then insert (
            event_id,
            event_timestamp,
            user_id,
            session_id,
            programme_id,
            episode_id,
            event_type,
            position_sec,
            platform
        ) values (
            source.event_id,
            source.event_timestamp,
            source.user_id,
            source.session_id,
            source.programme_id,
            source.episode_id,
            source.event_type,
            source.position_sec,
            source.platform
        )
    {% endset %}

    {% do run_query(merge_users_sql) %}
    {% do run_query(merge_sessions_sql) %}
    {% do run_query(merge_events_sql) %}
    {% do log("Loaded demo source data for demo_case='" ~ demo_case ~ "' and demo_batch_id='" ~ batch_id ~ "'.", info=true) %}
{% endmacro %}
