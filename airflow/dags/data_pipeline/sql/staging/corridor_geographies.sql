-- The raw data refers what gets read into the geography field as `geometry`.
-- Here we just rename the field so that it's standardized to `geog`.
SELECT
    name,
    geometry AS geog
FROM `city_of_phl.commercial_corridors`
