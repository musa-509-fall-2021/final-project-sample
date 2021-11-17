-- For each yyyy-mm-dd, Create a row with the total visit count.
-- Depends on staging.dated_safegraph_patterns

SELECT
    placekey,
    year,
    month,
    day,
    CAST(visit_count AS INTEGER) AS visit_count
FROM staging.dated_safegraph_patterns
CROSS JOIN UNNEST(JSON_EXTRACT_ARRAY(visits_by_day)) AS visit_count WITH OFFSET day
