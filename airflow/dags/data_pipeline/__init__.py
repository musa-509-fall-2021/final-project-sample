from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.dummy import DummyOperator
from datetime import datetime
from pathlib import Path
from pipeline_tools import run_transform_gbq

from . import extract_business_licenses
from . import extract_commercial_corridors
from . import extract_permits
from . import extract_planning_districts
from . import extract_properties
from . import extract_rcos
from . import load_business_licenses
from . import load_commercial_corridors
from . import load_permits
from . import load_planning_district_display_info
from . import load_planning_districts
from . import load_properties
from . import load_rcos
from . import load_safegraph_patterns

with DAG(dag_id='data_pipeline',
         schedule_interval='@monthly',
         start_date=datetime(2021, 10, 22),
         catchup=False) as dag:

    # EXTRACT TASKS ~~~~~

    extract_business_licenses_task = PythonOperator(
        task_id='extract_business_licenses',
        python_callable=extract_business_licenses.main,
    )
    extract_commercial_corridors_task = PythonOperator(
        task_id='extract_commercial_corridors',
        python_callable=extract_commercial_corridors.main,
    )
    extract_permits_task = PythonOperator(
        task_id='extract_permits',
        python_callable=extract_permits.main,
    )
    extract_planning_districts_task = PythonOperator(
        task_id='extract_planning_districts',
        python_callable=extract_planning_districts.main,
    )
    extract_properties_task = PythonOperator(
        task_id='extract_properties',
        python_callable=extract_properties.main,
    )
    extract_rcos_task = PythonOperator(
        task_id='extract_rcos',
        python_callable=extract_rcos.main,
    )

    # LOAD TASKS ~~~~~

    load_business_licenses_task = PythonOperator(
        task_id='load_business_licenses',
        python_callable=load_business_licenses.main,
    )
    load_commercial_corridors_task = PythonOperator(
        task_id='load_commercial_corridors',
        python_callable=load_commercial_corridors.main,
    )
    load_permits_task = PythonOperator(
        task_id='load_permits',
        python_callable=load_permits.main,
    )
    load_planning_district_display_info_task = PythonOperator(
        task_id='load_planning_district_display_info',
        python_callable=load_planning_district_display_info.main,
    )
    load_planning_districts_task = PythonOperator(
        task_id='load_planning_districts',
        python_callable=load_planning_districts.main,
    )
    load_properties_task = PythonOperator(
        task_id='load_properties',
        python_callable=load_properties.main,
    )
    load_rcos_task = PythonOperator(
        task_id='load_rcos',
        python_callable=load_rcos.main,
    )
    load_safegraph_patterns_task = PythonOperator(
        task_id='load_safegraph_patterns',
        python_callable=load_safegraph_patterns.main,
    )

    # TRANSFORM TASKS ~~~~~

    sql_dir = Path(__file__).parent / 'sql'

    transform_staging_building_base_task = PythonOperator(
        task_id='transform_staging_building_base',
        python_callable=run_transform_gbq,
        op_args=['staging', 'building_base', sql_dir],
    )
    transform_staging_corridor_base_task = PythonOperator(
        task_id='transform_staging_corridor_base',
        python_callable=run_transform_gbq,
        op_args=['staging', 'corridor_base', sql_dir],
    )
    transform_staging_corridor_filenames_task = PythonOperator(
        task_id='transform_staging_corridor_filenames',
        python_callable=run_transform_gbq,
        op_args=['staging', 'corridor_filenames', sql_dir],
    )
    transform_staging_corridor_health_task = PythonOperator(
        task_id='transform_staging_corridor_health',
        python_callable=run_transform_gbq,
        op_args=['staging', 'corridor_health', sql_dir],
    )
    transform_staging_corridor_planning_districts_task = PythonOperator(
        task_id='transform_staging_corridor_planning_districts',
        python_callable=run_transform_gbq,
        op_args=['staging', 'corridor_planning_districts', sql_dir],
    )
    transform_staging_corridor_visit_counts_task = PythonOperator(
        task_id='transform_staging_corridor_visit_counts',
        python_callable=run_transform_gbq,
        op_args=['staging', 'corridor_visit_counts', sql_dir],
    )
    transform_staging_corridor_visitor_home_cbgs_task = PythonOperator(
        task_id='transform_staging_corridor_visitor_home_cbgs',
        python_callable=run_transform_gbq,
        op_args=['staging', 'corridor_visitor_home_cbgs', sql_dir],
    )
    transform_staging_dated_safegraph_patterns_task = PythonOperator(
        task_id='transform_staging_dated_safegraph_patterns',
        python_callable=run_transform_gbq,
        op_args=['staging', 'dated_safegraph_patterns', sql_dir],
    )
    transform_staging_home_cbgs_task = PythonOperator(
        task_id='transform_staging_home_cbgs',
        python_callable=run_transform_gbq,
        op_args=['staging', 'home_cbgs', sql_dir],
    )
    transform_staging_place_geographies_task = PythonOperator(
        task_id='transform_staging_place_geographies',
        python_callable=run_transform_gbq,
        op_args=['staging', 'place_geographies', sql_dir],
    )
    transform_staging_place_visit_counts_task = PythonOperator(
        task_id='transform_staging_place_visit_counts',
        python_callable=run_transform_gbq,
        op_args=['staging', 'place_visit_counts', sql_dir],
    )
    transform_staging_place_visitor_home_cbgs_task = PythonOperator(
        task_id='transform_staging_place_visitor_home_cbgs',
        python_callable=run_transform_gbq,
        op_args=['staging', 'place_visitor_home_cbgs', sql_dir],
    )
    transform_final_corridors_task = PythonOperator(
        task_id='transform_final_corridors',
        python_callable=run_transform_gbq,
        op_args=['final', 'corridors', sql_dir],
    )
    transform_final_corridors_overview_task = PythonOperator(
        task_id='transform_final_corridors_overview',
        python_callable=run_transform_gbq,
        op_args=['final', 'corridors_overview', sql_dir],
    )
    transform_final_corridor_details_task = PythonOperator(
        task_id='transform_final_corridor_details',
        python_callable=run_transform_gbq,
        op_args=['final', 'corridor_details', sql_dir],
    )

    # DEPENDENCIES ~~~~~

    extract_business_licenses_task >> load_business_licenses_task
    extract_commercial_corridors_task >> load_commercial_corridors_task
    extract_permits_task >> load_permits_task
    extract_planning_districts_task >> load_planning_districts_task
    extract_properties_task >> load_properties_task
    extract_rcos_task >> load_rcos_task

    load_tasks = DummyOperator(task_id='wait_for_loads')
    load_tasks << [
        load_business_licenses_task,
        load_commercial_corridors_task,
        load_permits_task,
        load_planning_district_display_info_task,
        load_planning_districts_task,
        load_properties_task,
        load_rcos_task,
        load_safegraph_patterns_task,
    ]

    transform_staging_building_base_task << load_tasks
    transform_staging_corridor_base_task << load_tasks
    transform_staging_corridor_filenames_task << load_tasks
    transform_staging_corridor_health_task << load_tasks
    transform_staging_corridor_planning_districts_task << load_tasks
    transform_staging_corridor_visit_counts_task << load_tasks
    transform_staging_corridor_visitor_home_cbgs_task << load_tasks
    transform_staging_dated_safegraph_patterns_task << load_tasks
    transform_staging_home_cbgs_task << load_tasks
    transform_staging_place_geographies_task << load_tasks
    transform_staging_place_visit_counts_task << load_tasks
    transform_staging_place_visitor_home_cbgs_task << load_tasks

    transform_staging_corridor_base_task >> [
        transform_staging_building_base_task,
        transform_staging_corridor_visitor_home_cbgs_task,
    ]

    transform_staging_dated_safegraph_patterns_task >> [
        transform_staging_place_visit_counts_task,
        transform_staging_place_visitor_home_cbgs_task,
    ]

    transform_staging_place_geographies_task >> [
        transform_staging_corridor_visitor_home_cbgs_task,
    ]

    transform_staging_place_visitor_home_cbgs_task >> [
        transform_staging_corridor_visitor_home_cbgs_task,
        transform_staging_home_cbgs_task,
    ]

    transform_staging_tasks = DummyOperator(task_id='wait_for_staging_transforms')
    transform_staging_tasks << [
        transform_staging_building_base_task,
        transform_staging_corridor_base_task,
        transform_staging_corridor_filenames_task,
        transform_staging_corridor_health_task,
        transform_staging_corridor_planning_districts_task,
        transform_staging_corridor_visit_counts_task,
        transform_staging_corridor_visitor_home_cbgs_task,
        transform_staging_dated_safegraph_patterns_task,
        transform_staging_home_cbgs_task,
        transform_staging_place_geographies_task,
        transform_staging_place_visit_counts_task,
        transform_staging_place_visitor_home_cbgs_task,
    ]

    transform_final_corridors_task << transform_staging_tasks
    transform_final_corridors_overview_task << transform_staging_tasks
    transform_final_corridor_details_task << transform_staging_tasks
