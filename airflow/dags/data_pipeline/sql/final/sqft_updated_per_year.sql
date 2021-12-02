WITH

permit_ages AS (
    SELECT
        corridorkey,
        buildingkey,
        internal_sqft,
        CURRENT_TIMESTAMP() - last_permit_date AS age
    FROM staging.building_base
    WHERE last_permit_date IS NOT NULL
),

permit_ages_in_years AS (
    SELECT
        corridorkey,
        buildingkey,
        internal_sqft,
        EXTRACT(YEAR FROM JUSTIFY_DAYS(JUSTIFY_HOURS(age))) AS age_in_years
    FROM permit_ages
),

sqft_updated_per_year AS (
    SELECT
        corridorkey,
        age_in_years,
        SUM(internal_sqft) AS total_internal_sqft
    FROM permit_ages_in_years
    GROUP BY corridorkey, age_in_years
    ORDER BY corridorkey, age_in_years
)

SELECT * FROM sqft_updated_per_year
