-- Create a geography from the lng/lat in the safegraph tables for each place

SELECT
    placekey,
    ANY_VALUE(ST_GEOGPOINT(longitude, latitude)) as geog
FROM safegraph.safegraph_patterns_*
GROUP BY placekey
