SELECT
    name,
    filename,
    planning_district_name,
    health,
    geometry AS geog
FROM `city_of_phl.commercial_corridors`
JOIN staging.corridor_health USING (name)
JOIN staging.corridor_filenames USING (name)
JOIN staging.corridor_planning_districts (name)
ORDER BY planning_district_name, name
