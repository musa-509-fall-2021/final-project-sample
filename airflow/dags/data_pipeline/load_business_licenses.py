from pipeline_tools import gcs_to_local_file, geopandas_to_gbq
import geopandas as gpd

def main(ds):
    local_path = gcs_to_local_file(
        gcs_bucket_name='mjumbewu_cloudservices',
        gcs_blob_name=f'business_licenses/{ds}/phl_business_licenses.gpkg',
    )

    print(f'Loading file {local_path} into a GeoDataFrame...')
    gdf = gpd.read_file(local_path)

    geopandas_to_gbq(
        geodataframe=gdf,
        dataset_name='city_of_phl',
        table_name='business_licenses'
    )

    print('Done.')

if __name__ == '__main__':
    import datetime as dt
    main(ds=dt.date.today())
