from gzip import GzipFile
from zipfile import ZipFile
import pandas as pd
from pandas_gbq.gbq import TableCreationError
import re


def main(**kwargs):
    loaded_file_ids = set()
    zipfile_path = '/home/mjumbewu/Code/musa/musa-509/data/SafeGraph Data Purchase Nov-02-2021.zip'
    load_patterns_file(zipfile_path, loaded_file_ids)


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
