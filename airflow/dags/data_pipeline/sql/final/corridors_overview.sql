WITH

least_healthy_corridor AS (
    SELECT name
    FROM staging.corridor_health
    ORDER BY health ASC
    LIMIT 1
),

most_healthy_corridor AS (
    SELECT name
    FROM staging.corridor_health
    ORDER BY health DESC
    LIMIT 1
)

SELECT
    l.name AS least_healthy_corridor_name,
    m.name AS most_healthy_corridor_name
FROM least_healthy_corridor AS l
CROSS JOIN most_healthy_corridor AS m
