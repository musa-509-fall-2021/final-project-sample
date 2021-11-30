WITH

place_visit_counts_with_geog AS (
    SELECT
        placekey,
        visit_date,
        visit_count,
        geog
    FROM staging.place_visit_counts
    JOIN staging.place_geographies USING (placekey)
),

corridor_visit_counts AS (
    SELECT
        cor.corridorkey,
        pl.visit_date,
        SUM(pl.visit_count) AS visit_count
    FROM staging.corridor_base AS cor
    JOIN place_visit_counts_with_geog AS pl ON ST_CONTAINS(cor.geog, pl.geog)
    GROUP BY cor.corridorkey, pl.visit_date
)

SELECT * FROM corridor_visit_counts
