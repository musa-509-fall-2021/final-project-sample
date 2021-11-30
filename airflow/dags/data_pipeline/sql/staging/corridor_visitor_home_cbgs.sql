WITH

place_visitor_home_cbgs_with_geog AS (
    SELECT
        placekey,
        visitor_month,
        visitor_home_geo_id,
        visitor_count,
        geog
    FROM staging.place_visitor_home_cbgs
    JOIN staging.place_geographies USING (placekey)
),

corridor_visitor_home_cbgs AS (
    SELECT
        cor.corridorkey,
        pl.visitor_month,
        pl.visitor_home_geo_id,
        SUM(pl.visitor_count) AS visitor_count
    FROM staging.corridor_base AS cor
    JOIN place_visitor_home_cbgs_with_geog AS pl ON ST_CONTAINS(cor.geog, pl.geog)
    GROUP BY cor.corridorkey, pl.visitor_month, pl.visitor_home_geo_id
)

SELECT * FROM corridor_visitor_home_cbgs
