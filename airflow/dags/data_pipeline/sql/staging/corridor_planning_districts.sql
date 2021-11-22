-- Some corridors (one in particular -- 31st & Norris) have a NULL p_dist value.
-- We deal with any exceptions here.

SELECT
    corridorkey,
    CASE
        WHEN raw.p_dist IS NOT NULL THEN raw.p_dist
        WHEN cor.name = '31st and Norris' THEN 'North'
    END AS planning_district_name,
FROM staging.corridor_base AS cor
JOIN `city_of_phl.commercial_corridors` AS raw ON (cor.corridorkey = raw.pcpc_num)
