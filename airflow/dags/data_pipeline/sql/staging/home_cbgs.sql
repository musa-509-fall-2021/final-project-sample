-- CBG info for block groups listed as homes of visitors.

WITH

home_cbg_ids AS (
  SELECT DISTINCT visitor_home_geo_id AS geo_id
  FROM staging.place_visitor_home_cbgs
)

SELECT
    geo_id,
    state_fips_code,
    county_fips_code,
    internal_point_geom,
    blockgroup_geom,
    LEFT(geo_id, 5) = '42101' AS is_in_philadelphia
FROM `bigquery-public-data.geo_census_blockgroups.blockgroups_*`
JOIN home_cbg_ids USING (geo_id)
