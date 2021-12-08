from pipeline_tools import http_to_gcs

def main(ds):
    http_to_gcs(
        request_method='get',
        request_url='https://opendata.arcgis.com/datasets/84baed491de44f539889f2af178ad85c_0.zip',
        gcs_bucket_name='mjumbewu_cloudservices',
        gcs_blob_name=f'parcels/{ds}/phl_parcels.zip',
    )

if __name__ == '__main__':
    import datetime as dt
    main(ds=dt.date.today())
