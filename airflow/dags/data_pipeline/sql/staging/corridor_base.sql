/*
  Standardize the way we refer to corridor fields:
  - Add a unique key (based on the planning commission number)
  - Rename the `geometry` to `geog`
*/

SELECT
    pcpc_num as corridorkey,
    name,
    geometry AS geog
FROM `city_of_phl.commercial_corridors`
