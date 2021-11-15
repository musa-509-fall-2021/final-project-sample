from pipeline_tools import run_transform_gbq

def main(**kwargs):
    run_transform_gbq('staging', 'dated_safegraph_patterns', __file__)
    run_transform_gbq('staging', 'place_visit_counts', __file__)
    run_transform_gbq('staging', 'place_geographies', __file__)
    run_transform_gbq('final', 'corridors', __file__)

if __name__ == '__main__':
    main()
