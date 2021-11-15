from pipeline_tools import http_to_gcs

def main(ds):
    http_to_gcs(
        request_method='get',
        request_url='https://phl.carto.com/api/v2/sql?filename=permits&format=gpkg&skipfields=cartodb_id&q=SELECT%20*%20FROM%20permits%20WHERE%20permitissuedate%20%3E=%20%272007-01-01%27%20AND%20permitissuedate%20%3C%20%272016-01-01%27',
        gcs_bucket_name='mjumbewu_cloudservices',
        gcs_blob_name=f'permits/{ds}/phl_permits_2007_to_2015.gpkg',
    )
    http_to_gcs(
        request_method='get',
        request_url='https://phl.carto.com/api/v2/sql?filename=permits&format=gpkg&skipfields=cartodb_id&q=SELECT%20*%20FROM%20permits%20WHERE%20permitissuedate%20%3E=%20%272016-01-01%27',
        gcs_bucket_name='mjumbewu_cloudservices',
        gcs_blob_name=f'permits/{ds}/phl_permits_2016_to_present.gpkg',
    )

if __name__ == '__main__':
    import datetime as dt
    main(ds=dt.date.today())
