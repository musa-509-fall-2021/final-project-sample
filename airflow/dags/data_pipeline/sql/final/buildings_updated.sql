SELECT
    corridorkey,
    buildingkey,
    internal_sqft,
    CAST(last_permit_date AS STRING) AS last_permit_date,
    NTILE(5) OVER (ORDER BY last_permit_date NULLS FIRST) AS last_permit_date_bin,
    geog
FROM staging.building_base
