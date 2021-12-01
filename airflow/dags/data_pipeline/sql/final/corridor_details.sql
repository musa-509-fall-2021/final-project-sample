WITH

building_stats AS (
    SELECT DISTINCT
        corridorkey,
        COUNT(*) OVER corridor_partition AS number_of_buildings,
        PERCENTILE_DISC(year_built, 0) OVER corridor_partition AS oldest_year_built,
        PERCENTILE_DISC(year_built, 0.1) OVER corridor_partition AS p10_year_built,
        PERCENTILE_DISC(year_built, 0.5) OVER corridor_partition AS p50_year_built,
        PERCENTILE_DISC(year_built, 0.9) OVER corridor_partition AS p90_year_built,
        PERCENTILE_DISC(year_built, 1) OVER corridor_partition AS newest_year_built,
        PERCENTILE_DISC(last_permit_date, 0) OVER corridor_partition AS oldest_last_permit_date,
        PERCENTILE_DISC(last_permit_date, 0.1) OVER corridor_partition AS p10_last_permit_date,
        PERCENTILE_DISC(last_permit_date, 0.5) OVER corridor_partition AS p50_last_permit_date,
        PERCENTILE_DISC(last_permit_date, 0.9) OVER corridor_partition AS p90_last_permit_date,
        PERCENTILE_DISC(last_permit_date, 1) OVER corridor_partition AS newest_last_permit_date
    FROM staging.building_base
    WINDOW corridor_partition AS (PARTITION BY corridorkey)
),

visit_count_stats AS (
    SELECT
        corridorkey,
        SUM(visit_count) AS visit_count
    FROM staging.corridor_visit_counts
    WHERE visit_date > DATE_SUB(CURRENT_DATE('US/Eastern'), INTERVAL 1 YEAR)
    GROUP BY corridorkey
)

SELECT
    name,
    filename,
    planning_district_name,

    -- Health fields
    health,
    NTILE(5) OVER (ORDER BY health) as health_bin,

    -- Visit count fields
    visit_count,
    NTILE(5) OVER (ORDER BY visit_count) AS visit_count_bin,

    -- Building fields
    number_of_buildings,
    oldest_year_built,
    p10_year_built,
    p50_year_built,
    p90_year_built,
    newest_year_built,
    NTILE(5) OVER (ORDER BY p50_year_built) AS median_year_built_bin,
    oldest_last_permit_date,
    p10_last_permit_date,
    p50_last_permit_date,
    p90_last_permit_date,
    newest_last_permit_date,
    NTILE(5) OVER (ORDER BY p50_last_permit_date) AS median_last_permit_date_bin,

    geog

FROM staging.corridor_base
JOIN visit_count_stats USING (corridorkey)
JOIN building_stats USING (corridorkey)
JOIN staging.corridor_health USING (corridorkey)
JOIN staging.corridor_filenames USING (corridorkey)
JOIN staging.corridor_planning_districts USING (corridorkey)
ORDER BY planning_district_name, name
