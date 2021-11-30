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
        prop.year_built,
        prop.taxable_building AS internal_sqft,
        ST_GEOGFROMWKB(prop.geometry) AS geog
    FROM city_of_phl.properties AS prop
    JOIN staging.corridor_base AS cor ON ST_CONTAINS(cor.geog, ST_GEOGFROMWKB(prop.geometry))
),

most_recent_permits AS (
    SELECT
        perm.opa_account_num AS buildingkey,
        MAX(perm.permitissuedate) AS most_recent_permit_issue_date
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
    most_recent_permit_issue_date,
    geog
FROM corridor_buildings
JOIN most_recent_permits USING (buildingkey)
