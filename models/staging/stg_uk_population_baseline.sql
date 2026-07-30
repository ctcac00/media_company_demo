with source as (
    select * from {{ source('media_raw', 'uk_population_baseline') }}
),
renamed as (
    select
        cast(year as integer)                      as year,
        cast(demographic_id as varchar)            as demographic_id,
        cast(population_thousands as integer)      as population_thousands,
        current_timestamp()                        as _loaded_at
    from source
)
select * from renamed
