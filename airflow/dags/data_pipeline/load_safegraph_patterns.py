import json
import os
import re
from gzip import GzipFile
from zipfile import ZipFile

from google.cloud import storage
import pandas as pd
from pandas_gbq.gbq import TableCreationError
from pipeline_tools import gcs_to_local_file


def main():
    bucket_name = 'mjumbewu_cloudservices'
    blob_folder = f'safegraph_patterns/'

    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket_name)
    blobs = bucket.list_blobs(prefix=blob_folder)

    loaded_file_ids = set()

    for blob in blobs:
        blob_name = blob.name
        if not blob_name.endswith('.zip'):
            continue

        zipfile_path = gcs_to_local_file(
            gcs_bucket_name=bucket_name,
            gcs_blob_name=blob_name,
        )
        load_patterns_file(zipfile_path, loaded_file_ids)

        # Clean up; these files can be pretty large
        os.remove(zipfile_path)


def load_patterns_file(zipfile_path, loaded_file_ids):
    dataset_name = 'safegraph'
    file_id_pattern = re.compile(r'PA-CORE_POI-PATTERNS-(?P<file_id>\d{4}_\d{2}).*')

    with ZipFile(open(zipfile_path, mode='rb')) as safegraph_multi_zipfile:
        zipfiles = [n for n in safegraph_multi_zipfile.namelist() if n.endswith('.zip')]
        for zf in zipfiles:
            file_id_match = file_id_pattern.match(zf)
            assert file_id_match is not None, f'Could not find file id in {zf!r}'

            file_id = file_id_match['file_id']
            if file_id not in loaded_file_ids:
                loaded_file_ids.add(file_id)
            else:
                print(f'Skipping zipped file {zf} with id {file_id}')
                continue

            print(f'Opening zipped file {zf} with id {file_id}')
            with ZipFile(safegraph_multi_zipfile.open(zf)) as safegraph_zipfile:

                print(f'Opening gzipped file with name core_poi-patterns.csv.gz')
                with GzipFile(fileobj=safegraph_zipfile.open('core_poi-patterns.csv.gz')) as patterns_csv_file:

                    print('Reading the ungzipped csv file')
                    safegraph_patterns_df = pd.read_csv(patterns_csv_file)

                    # Transform the visitor_home_cbgs column so that it's easier
                    # to work with in SQL. Change it from:
                    #
                    # {
                    #   geoid1: count1,
                    #   geoid2: count2,
                    #   ...
                    # }
                    #
                    # To:
                    #
                    # [
                    #   {'geo_id': geoid1, 'count': count1},
                    #   {'geo_id': geoid2, 'count': count2},
                    #   ...
                    # ]
                    safegraph_patterns_df['visitor_home_cbgs'] = safegraph_patterns_df.visitor_home_cbgs.fillna('{}').apply(
                        lambda d: json.dumps([
                            {'geo_id': geo_id, 'count': count}
                            for geo_id, count in json.loads(d).items()
                        ])
                    )

                    print(f'Writing the file to bigquery as safegraph_patterns_{file_id}')
                    try:
                        # Since these tables are so large, and because past data
                        # shouldn't change, I'm going to not load data that's
                        # already present in the dataset. To re-trigger a load,
                        # I'll have to delete the existing table.
                        safegraph_patterns_df.to_gbq(f'{dataset_name}.safegraph_patterns_{file_id}', if_exists='fail')
                    except TableCreationError:
                        print('Table seems to already exist. Skipping.')
                        continue


if __name__ == '__main__':
    main()
