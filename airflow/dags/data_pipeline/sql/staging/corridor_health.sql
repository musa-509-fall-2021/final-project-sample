SELECT
    name,
    SUM(vis.visit_count) as health
FROM `city_of_phl.commercial_corridors` AS cor
JOIN staging.place_geographies AS geo ON ST_CONTAINS(cor.geometry, geo.geog)
JOIN staging.place_visit_counts AS vis ON geo.placekey = vis.placekey
GROUP BY name
