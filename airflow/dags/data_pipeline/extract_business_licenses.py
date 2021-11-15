from pipeline_tools import http_to_gcs

def main(ds):
    http_to_gcs(
        request_method='get',
        request_url='https://phl.carto.com/api/v2/sql?q=SELECT+*+FROM+business_licenses&filename=business_licenses&format=gpkg&skipfields=cartodb_id',
        gcs_bucket_name='mjumbewu_cloudservices',
        gcs_blob_name=f'business_licenses/{ds}/phl_business_licenses.gpkg',
    )

if __name__ == '__main__':
    import datetime as dt
    main(ds=dt.date.today())
