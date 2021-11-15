SELECT
    LEFT(_TABLE_SUFFIX, 4) AS year,
    RIGHT(_TABLE_SUFFIX, 2) AS month,
    *
FROM safegraph.safegraph_patterns_*
