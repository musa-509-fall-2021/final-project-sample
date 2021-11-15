from pipeline_tools import http_to_gcs

def main(ds):
    http_to_gcs(
        request_method='get',
        request_url='https://opendata.arcgis.com/datasets/efbff0359c3e43f190e8c35ce9fa71d6_0.geojson',
        gcs_bucket_name='mjumbewu_cloudservices',
        gcs_blob_name=f'rcos/{ds}/phl_rcos.geojson',
    )

if __name__ == '__main__':
    import datetime as dt
    main(ds=dt.date.today()-dt.timedelta(days=1))
