WITH

building_ages_in_years AS (
    SELECT
        corridorkey,
        buildingkey,
        internal_sqft,
        EXTRACT(YEAR FROM CURRENT_DATE('US/Eastern')) - year_built AS age_in_years
    FROM staging.building_base
    WHERE year_built IS NOT NULL
),

building_ages_in_decades AS (
    SELECT
        corridorkey,
        buildingkey,
        internal_sqft,
        FLOOR(age_in_years / 10) AS age_in_decades
    FROM building_ages_in_years
),

sqft_built_per_decade AS (
    SELECT
        corridorkey,
        age_in_decades,
        SUM(internal_sqft) AS total_internal_sqft
    FROM building_ages_in_decades
    GROUP BY corridorkey, age_in_decades
    ORDER BY corridorkey, age_in_decades
)

SELECT * FROM sqft_built_per_decade
