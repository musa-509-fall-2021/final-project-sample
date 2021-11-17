SELECT
    name,
    filename,
    planning_district_name,
    health,
    geog
FROM `city_of_phl.commercial_corridors`
JOIN staging.corridor_health USING (name)
JOIN staging.corridor_filenames USING (name)
JOIN staging.corridor_planning_districts USING (name)
JOIN staging.corridor_geographies USING (name)
ORDER BY planning_district_name, name
