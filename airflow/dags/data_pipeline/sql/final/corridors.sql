SELECT
    name,
    LOWER(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(name, '.', ''), ' / ', ''), '/', ''), ' - ', ' '), ' & ', ' '), ' ', '-')) as filename,
    CASE
        WHEN p_dist IS NOT NULL THEN p_dist
        WHEN name = '31st and Norris' THEN 'North'
    END AS planning_district_name,
    geometry AS geog
FROM `city_of_phl.commercial_corridors`
ORDER BY planning_district_name, name
