WITH

place_visit_counts_past_year AS (
    SELECT
        placekey,
        visit_count,
        geog
    FROM staging.place_visit_counts
    JOIN staging.place_geographies USING (placekey)
    WHERE visit_date > DATE_SUB(CURRENT_DATE('US/Eastern'), INTERVAL 1 YEAR)
),

corridor_health_past_year AS (
    SELECT
        cor.corridorkey,
        SUM(pl.visit_count) / ST_AREA(ANY_VALUE(cor.geog)) as health
    FROM staging.corridor_base AS cor
    JOIN place_visit_counts_past_year AS pl ON ST_CONTAINS(cor.geog, pl.geog)
    GROUP BY cor.corridorkey
)

SELECT * FROM corridor_health_past_year
