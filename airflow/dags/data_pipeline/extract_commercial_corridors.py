from pipeline_tools import http_to_gcs

def main(ds):
    http_to_gcs(
        request_method='get',
        request_url='https://opendata.arcgis.com/datasets/f43e5f92d34e41249e7a11f269792d11_0.geojson',
        gcs_bucket_name='mjumbewu_cloudservices',
        gcs_blob_name=f'commercial_corridors/{ds}/phl_commercial_corridors.geojson',
    )

if __name__ == '__main__':
    import datetime as dt
    main(ds=dt.date.today())
