from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.sensors.external_task_sensor import ExternalTaskSensor
from datetime import datetime

from . import generate_report

with DAG(dag_id='report_generator',
         schedule_interval='@monthly',
         start_date=datetime(2021, 10, 22),
         catchup=False) as dag:

    # REPORT RENDERING TASKS ~~~~~

    generate_report_task = PythonOperator(
        task_id='generate_report',
        python_callable=generate_report.main,
    )
    wait_for_data_pipeline_task = ExternalTaskSensor(
        task_id="wait_for_data_pipeline",
        external_dag_id='data_pipeline',
        external_task_id='wait_for_final_transforms',
    )

    # DEPENENCIES ~~~~~

    wait_for_data_pipeline_task >> generate_report_task
