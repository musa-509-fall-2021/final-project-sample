from pipeline_tools import gcs_to_local_file, geopandas_to_gbq
import geopandas as gpd
import pandas as pd

def main(ds):
    local_path = gcs_to_local_file(
        gcs_bucket_name='mjumbewu_cloudservices',
        gcs_blob_name=f'rcos/{ds}/phl_rcos.geojson',
    )

    print(f'Loading file {local_path} into a GeoDataFrame...')
    gdf = gpd.read_file(local_path)

    # Because there's an issue with the some of the geometries, we need to load
    # the geometry as text.
    #
    # Invalid polygon loop: Edge 0 has duplicate vertex with edge 3; in WKB geography
    df = pd.DataFrame(gdf)
    df['geometry'] = gdf.geometry.apply(str)
    del gdf

    df.to_gbq('city_of_phl.rcos', if_exists='replace')

    print('Done.')

if __name__ == '__main__':
    import datetime as dt
    main(ds=dt.date.today())
