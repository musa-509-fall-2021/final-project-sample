SELECT
    name,
    filename,
    planning_district_name,
    health,
    NTILE(5) OVER (ORDER BY health) as health_bin,
    geog
FROM staging.corridor_base
JOIN staging.corridor_health USING (corridorkey)
JOIN staging.corridor_filenames USING (corridorkey)
JOIN staging.corridor_planning_districts USING (corridorkey)
ORDER BY planning_district_name, name
