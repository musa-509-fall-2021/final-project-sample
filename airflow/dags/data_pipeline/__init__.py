from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
from pipeline_tools import run_transform_gbq

from . import extract_business_licenses
from . import extract_commercial_corridors
from . import extract_permits
from . import extract_rcos
from . import load_business_licenses
from . import load_commercial_corridors
from . import load_permits
from . import load_planning_districts
from . import load_rcos
from . import load_safegraph_patterns

with DAG(dag_id='addresses_pipeline',
         schedule_interval='@daily',
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
    load_planning_districts_task = PythonOperator(
        task_id='load_planning_districts',
        python_callable=load_planning_districts.main,
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

    # DEPENDENCIES ~~~~~

    extract_business_licenses_task >> load_business_licenses_task
    extract_commercial_corridors_task >> load_commercial_corridors_task
    extract_permits_task >> load_permits_task
    extract_rcos_task >> load_rcos_task
