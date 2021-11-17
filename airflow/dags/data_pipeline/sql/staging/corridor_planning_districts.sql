-- Some corridors (one in particular -- 31st & Norris) have a NULL p_dist value.
-- We deal with any exceptions here.

SELECT
    name,
    CASE
        WHEN p_dist IS NOT NULL THEN p_dist
        WHEN name = '31st and Norris' THEN 'North'
    END AS planning_district_name,
FROM `city_of_phl.commercial_corridors`
