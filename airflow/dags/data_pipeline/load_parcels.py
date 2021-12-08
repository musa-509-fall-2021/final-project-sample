from pipeline_tools import gcs_to_local_file, geopandas_to_gbq
import geopandas as gpd
import pandas as pd

def main(ds):
    local_path = gcs_to_local_file(
        gcs_bucket_name='mjumbewu_cloudservices',
        gcs_blob_name=f'parcels/{ds}/phl_parcels.zip',
    )

    print(f'Loading file {local_path} into a GeoDataFrame...')
    gdf = gpd.read_file(local_path)

    # Because there's an issue with the orientation of some of the parcel
    # geometries, we need to load the geometry as text, and re-convert it to a
    # correctly-oriented geometry in BigQuery.
    df = pd.DataFrame(gdf)
    df['geometry'] = gdf.geometry.apply(str)
    del gdf

    df.to_gbq('city_of_phl.parcels')

    print('Done.')

if __name__ == '__main__':
    import datetime as dt
    main(ds=dt.date.today())
