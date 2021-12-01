from pipeline_tools import run_transform_gbq
from pathlib import Path

sql_dir = Path(__file__).parent / 'sql'

def main():
    # run_transform_gbq('staging', 'dated_safegraph_patterns', sql_dir)
    # run_transform_gbq('staging', 'place_visit_counts', sql_dir)
    # run_transform_gbq('staging', 'place_visitor_home_cbgs', sql_dir)
    # run_transform_gbq('staging', 'home_cbgs', sql_dir)
    # run_transform_gbq('staging', 'place_geographies', sql_dir)
    # run_transform_gbq('staging', 'corridor_base', sql_dir)
    # run_transform_gbq('staging', 'corridor_filenames', sql_dir)
    # run_transform_gbq('staging', 'corridor_planning_districts', sql_dir)
    # run_transform_gbq('staging', 'corridor_visit_counts', sql_dir)
    # run_transform_gbq('staging', 'corridor_health', sql_dir)
    # run_transform_gbq('staging', 'corridor_visitor_home_cbgs', sql_dir)
    # run_transform_gbq('staging', 'building_base', sql_dir)
    # run_transform_gbq('final', 'corridors', sql_dir)
    # run_transform_gbq('final', 'corridors_overview', sql_dir)
    run_transform_gbq('final', 'corridor_details', sql_dir)

if __name__ == '__main__':
    main()
