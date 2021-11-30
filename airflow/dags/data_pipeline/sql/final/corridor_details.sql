SELECT
    name,
    visit_count,
    NTILE(5) OVER (ORDER BY visit_count) AS visit_count_bin
FROM staging.corridor_base
JOIN staging.corridor_visit_counts USING (corridorkey)
WHERE visit_date > DATE_SUB(CURRENT_DATE('US/Eastern'), INTERVAL 1 YEAR)
