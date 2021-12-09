WITH

total_sqft AS (
    SELECT
        corridorkey,
        SUM(internal_sqft) as total_internal_sqft
    FROM staging.building_base
    GROUP BY corridorkey
),

year_built_order AS (
    SELECT
        corridorkey,
        year_built,
        SUM(internal_sqft) OVER (
            PARTITION BY corridorkey
            ORDER BY year_built) AS cumulative_internal_sqft
    FROM staging.building_base
),

date_updated_order AS (
    SELECT
        corridorkey,
        last_permit_date,
        SUM(internal_sqft) OVER (
            PARTITION BY corridorkey
            ORDER BY last_permit_date) AS cumulative_internal_sqft
    FROM staging.building_base
),

median_year_built_order_sqft AS (
    SELECT
        corridorkey,
        cumulative_internal_sqft
    FROM year_built_order
    JOIN total_sqft USING (corridorkey)
    ORDER BY ABS(total_internal_sqft / 2 - cumulative_internal_sqft)
    LIMIT 1
),

median_date_updated_order_sqft AS (
    SELECT
        corridorkey,
        cumulative_internal_sqft
    FROM date_updated_order
    JOIN total_sqft USING (corridorkey)
    ORDER BY ABS(total_internal_sqft / 2 - cumulative_internal_sqft)
    LIMIT 1
),

median_year_built AS (
    SELECT
        corridorkey,
        ANY_VALUE(year_built) AS median_year_built
    FROM year_built_order
    JOIN median_year_built_order_sqft USING (corridorkey, cumulative_internal_sqft)
    GROUP BY corridorkey
),

median_date_updated AS (
    SELECT
        corridorkey,
        ANY_VALUE(last_permit_date) AS median_date_updated,
    FROM date_updated_order
    JOIN median_date_updated_order_sqft USING (corridorkey, cumulative_internal_sqft)
    GROUP BY corridorkey
)

SELECT
    corridorkey,
    median_date_updated,
    median_year_built,
    total_internal_sqft
FROM median_year_built
JOIN median_date_updated USING (corridorkey)
JOIN total_sqft USING (corridorkey)
