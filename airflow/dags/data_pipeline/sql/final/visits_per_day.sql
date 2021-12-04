WITH

comparative_visits_per_day AS (
    SELECT
        y1.corridorkey,
        CAST(y1.visit_date AS STRING) as visit_date,
        y1.visit_count AS y1_visit_count,
        y2.visit_count AS y2_visit_count,
        y3.visit_count AS y3_visit_count
    FROM staging.corridor_visit_counts AS y1
    LEFT JOIN staging.corridor_visit_counts AS y2
        ON y1.corridorkey = y2.corridorkey
        AND y1.visit_date = y2.visit_date + INTERVAL 52 WEEK
    LEFT JOIN staging.corridor_visit_counts AS y3
        ON y1.corridorkey = y3.corridorkey
        AND y1.visit_date = y3.visit_date + INTERVAL 104 WEEK
    WHERE y1.visit_date >= CURRENT_DATE('US/Eastern') - INTERVAL 1 YEAR
),

visits_with_trailing_averages AS (
    SELECT
        *,
        AVG(y1_visit_count) OVER window_7day y1_7day_visit_count,
        AVG(y2_visit_count) OVER window_7day y2_7day_visit_count,
        AVG(y3_visit_count) OVER window_7day y3_7day_visit_count,
    FROM comparative_visits_per_day
    WINDOW window_7day AS (
        PARTITION BY corridorkey
        ORDER BY visit_date
        ROWS BETWEEN 6 PRECEDING AND CURRENT ROW)
    ORDER BY corridorkey, visit_date
)

SELECT *
FROM visits_with_trailing_averages
