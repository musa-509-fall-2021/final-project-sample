WITH

corridor_visit_counts_past_year AS (
    SELECT
        corridorkey,
        visit_count
    FROM staging.corridor_visit_counts
    WHERE visit_date > DATE_SUB(CURRENT_DATE('US/Eastern'), INTERVAL 1 YEAR)
),

corridor_health_past_year AS (
    SELECT
        corridorkey,
        SUM(visit_count) / ST_AREA(ANY_VALUE(geog)) as health
    FROM staging.corridor_base
    JOIN corridor_visit_counts_past_year USING (corridorkey)
    GROUP BY corridorkey
)

SELECT * FROM corridor_health_past_year
