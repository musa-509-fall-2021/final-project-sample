-- For each yyyy-mm and block group, create a row with the total visit count.
-- Depends on staging.dated_safegraph_patterns.

SELECT
    placekey,
    DATE(year, month, 1) as visitor_month,
    JSON_EXTRACT_SCALAR(visitor_home_cbg, '$.geo_id') AS visitor_home_geo_id,
    CAST(JSON_EXTRACT_SCALAR(visitor_home_cbg, '$.count') AS INTEGER) AS visitor_count
FROM staging.dated_safegraph_patterns
CROSS JOIN UNNEST(JSON_EXTRACT_ARRAY(visitor_home_cbgs)) AS visitor_home_cbg
