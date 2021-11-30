from pipeline_tools import http_to_gcs

def main(ds):
    http_to_gcs(
        request_method='get',
        request_url='https://phl.carto.com/api/v2/sql?filename=opa_properties_public&format=gpkg&skipfields=cartodb_id&q=SELECT+*+FROM+opa_properties_public',
        gcs_bucket_name='mjumbewu_cloudservices',
        gcs_blob_name=f'properties/{ds}/phl_properties.gpkg',
    )

if __name__ == '__main__':
    import datetime as dt
    main(ds=dt.date.today())
