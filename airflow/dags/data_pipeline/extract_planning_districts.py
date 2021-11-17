from pipeline_tools import http_to_gcs

def main(ds):
    http_to_gcs(
        request_method='get',
        request_url='https://opendata.arcgis.com/datasets/0960ea0f38f44146bb562f2b212075aa_0.geojson',
        gcs_bucket_name='mjumbewu_cloudservices',
        gcs_blob_name=f'planning_districts/{ds}/phl_planning_districts.geojson',
    )

if __name__ == '__main__':
    import datetime as dt
    main(ds=dt.date.today())
