from google.cloud import bigquery
from google.cloud import storage
import pandas as pd
import geopandas as gpd
import pathlib
import requests
import tempfile


# PATCH THE GEODATAFRAME.TO_PARQUET FUNCTION.
original_to_parquet = None
def patched_to_parquet(self, path, index=None, compression="snappy", **kwargs):
    kwargs.pop('engine', None)
    return original_to_parquet(self, path, index=index, compression=compression, **kwargs)

if gpd.GeoDataFrame.to_parquet is not patched_to_parquet:
    original_to_parquet = gpd.GeoDataFrame.to_parquet
    gpd.GeoDataFrame.to_parquet = patched_to_parquet
# END PATCH


def http_to_gcs(request_method, request_url,
                gcs_bucket_name, gcs_blob_name,
                request_data=None, request_files=None):
    """
    This function makes a request to an HTTP resource and saves the response
    content to a file in Google Cloud Storage.
    """
    # 1. Download data from the specified URL
    print(f'Downloading from {request_url}...')

    response = requests.request(request_method, request_url,
                                data=request_data, files=request_files)

    # 2. Save retrieved data to a local file
    with tempfile.NamedTemporaryFile(delete=False) as local_file:
        local_file_name = local_file.name
        print(f'Saving downloaded content to {local_file_name}...')
        local_file.write(response.content)

    # 3. Upload local file of data to Google Cloud Storage
    print(f'Uploading to GCS file gs://{gcs_bucket_name}/{gcs_blob_name}...')

    storage_robot = storage.Client()
    bucket = storage_robot.bucket(gcs_bucket_name)
    blob = bucket.blob(gcs_blob_name)
    blob.upload_from_filename(local_file_name)


def gcs_to_local_file(gcs_bucket_name, gcs_blob_name, local_file_name=None):
    """
    This function downloads a file from Google Cloud Storage and saves the
    result to a local file. The function returns the name of the saved file.
    """
    if local_file_name is None:
        ext = pathlib.Path(gcs_blob_name).suffix
        with tempfile.NamedTemporaryFile(delete=False, suffix=ext) as local_file:
            local_file_name = local_file.name

    print(f'Saving from GCS file gs://{gcs_bucket_name}/{gcs_blob_name} '
          f'to local file {local_file_name}...')

    storage_robot = storage.Client()
    bucket = storage_robot.bucket(gcs_bucket_name)
    blob = bucket.blob(gcs_blob_name)
    blob.download_to_filename(local_file_name)

    return local_file_name


def local_file_to_gcs(local_file_name, gcs_bucket_name, gcs_blob_name, content_type=None):
    """
    This function uploads a file from the local machine to Google Cloud Storage.
    """
    print(f'Saving to GCS file gs://{gcs_bucket_name}/{gcs_blob_name} '
          f'from local file {local_file_name}...')

    storage_robot = storage.Client()
    bucket = storage_robot.bucket(gcs_bucket_name)
    blob = bucket.blob(gcs_blob_name)
    blob.upload_from_filename(local_file_name, content_type=content_type)


def gcs_to_db(gcs_bucket_name, gcs_blob_name, db_conn, table_name, column_names=None):
    """
    This function downloads a file from Google Cloud Storage, reads the file
    contents, and write the contents to a database.
    """
    # 1. Download file from GCS
    local_file_name = gcs_to_local_file(gcs_bucket_name, gcs_blob_name)

    # 2. Read data from downloaded file
    print(f'Reading data from file {local_file_name}...')
    df = pd.read_csv(local_file_name, names=column_names)

    # 3. Write data into database/data warehouse
    print(f'Writing data to table {table_name}...')
    df.to_sql(table_name, db_conn, index=False, if_exists='replace')


def geopandas_to_gbq(geodataframe, dataset_name, table_name, replace_table=True):
    """
    This function loads a GeoPandas GeoDataFrame into a BigQuery table. The
    geometry field on the data frame will be configured correctly within BQ.

    Note that there is a function called to_gbq that exists on Pandas already.
    But that function won't create geography fields in the appropriate places.
    Instead it will upload geographic data as a string.
    """
    import warnings; warnings.filterwarnings('ignore', message='.*initial implementation of Parquet.*')

    geog_field_name = geodataframe._geometry_column_name
    print(f'Loading data into `{dataset_name}.{table_name}` with geography field `{geog_field_name}`...')
    job_config = bigquery.LoadJobConfig(
        schema=[
            bigquery.SchemaField(geog_field_name, bigquery.enums.SqlTypeNames.GEOGRAPHY)
        ],
        write_disposition="WRITE_TRUNCATE" if replace_table else "WRITE_APPEND",
    )
    client = bigquery.Client()
    job = client.load_table_from_dataframe(
        geodataframe.to_crs(4326), f'{dataset_name}.{table_name}', job_config=job_config
    )
    return job.result()


def run_transform_gbq(dataset_name, table_name, sql_root):
    """
    This function will look for a file named 'sql/{dataset_name}/{table_name}.sql'
    next to the file specified by rel_to, and then create a table in the dataset
    with the specified name.
    """
    query_path = sql_root / dataset_name / f'{table_name}.sql'

    client = bigquery.Client()
    with open(query_path) as query_file:
        query = query_file.read()

    print(f'Creating or replacing table `{dataset_name}.{table_name}`...')
    query_job = client.query(f'CREATE OR REPLACE TABLE `{dataset_name}.{table_name}` AS ({query})')
    return query_job.result()
