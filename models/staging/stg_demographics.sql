with source as (
    select * from {{ source('media_raw', 'demographics') }}
),
renamed as (
    select
        cast(demographic_id as varchar)    as demographic_id,
        cast(age_band as varchar)          as age_band,
        cast(gender as varchar)            as gender,
        cast(social_grade as varchar)      as social_grade,
        current_timestamp()                as _loaded_at
    from source
)
select * from renamed
