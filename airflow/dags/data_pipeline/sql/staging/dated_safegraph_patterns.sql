SELECT
    CAST(LEFT(_TABLE_SUFFIX, 4) AS INT) AS year,
    CAST(RIGHT(_TABLE_SUFFIX, 2) AS INT) AS month,
    *
FROM `safegraph.safegraph_patterns_*`
