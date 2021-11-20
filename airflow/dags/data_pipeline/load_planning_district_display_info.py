"""
Loads a manual CSV file that contains corresponding names for planning districts
as well as display information like the order that districts should be listed,
and maybe colors they should have on maps, for consistency.

Because this file is so small, and is so specific to the display of the reports,
it makes sense to store it in this repository (as opposed to the SafeGraph data,
which is similarly static, but is large and not project specific).
"""

from pipeline_tools import gcs_to_local_file, geopandas_to_gbq
import pandas as pd
from pathlib import Path

def main():
    local_path = Path(__file__).parent / 'static_data' / 'planning_district_display_info.csv'

    print(f'Loading file {local_path} into a DataFrame...')
    df = pd.read_csv(local_path)

    dataset_name = 'staging'
    table_name = 'planning_district_display_info'

    print(f'Writing the file to bigquery as {dataset_name}.{table_name}...')
    df.to_gbq(f'{dataset_name}.{table_name}', if_exists='replace')

    print('Done.')

if __name__ == '__main__':
    main()
