WITH

active_or_completed_permits AS (
    SELECT
        permitnumber,
    FROM city_of_phl.permits
    WHERE status in ('ISSUED', 'COMPLETED')
),

corridor_buildings AS (
    SELECT
        cor.corridorkey,
        prop.parcel_number AS buildingkey,
        CASE
            WHEN prop.year_built IS NULL THEN NULL
            WHEN prop.year_built IN ('0', '0000') THEN NULL
            ELSE CAST(prop.year_built AS INTEGER)
        END AS year_built,
        prop.total_livable_area AS internal_sqft,
        ST_GEOGFROMWKB(prop.geometry) AS geog
    FROM city_of_phl.properties AS prop
    JOIN staging.corridor_base AS cor ON ST_CONTAINS(cor.geog, ST_GEOGFROMWKB(prop.geometry))
),

most_recent_permits AS (
    SELECT
        perm.opa_account_num AS buildingkey,
        PARSE_TIMESTAMP('%Y-%m-%dT%H:%M:%S%Ez', MAX(perm.permitissuedate)) AS last_permit_date
    FROM city_of_phl.permits AS perm
    JOIN active_or_completed_permits USING (permitnumber)
    JOIN corridor_buildings ON perm.opa_account_num = buildingkey
    GROUP BY perm.opa_account_num
)

SELECT
    buildingkey,
    corridorkey,
    year_built,
    internal_sqft,
    last_permit_date,
    geog
FROM corridor_buildings
LEFT JOIN most_recent_permits USING (buildingkey)
