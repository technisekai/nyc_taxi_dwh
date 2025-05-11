from airflow import DAG
from airflow.operators.python_operator import PythonOperator, ShortCircuitOperator, BranchPythonOperator
from airflow.operators.dummy_operator import DummyOperator
from airflow.models import Variable
from airflow.providers.docker.operators.docker import DockerOperator
from docker.types import Mount 
from datetime import datetime

# DAG Configuration
default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "email_on_failure": False,
    "email_on_retry": False
}

with DAG(
    "nyc_taxi_silver",
    default_args=default_args,
    description="",
    schedule_interval=None,
    start_date=datetime(2025, 4, 4),
    catchup=False,
) as dag:
    start = DummyOperator(task_id="start", dag=dag)

    end = DummyOperator(task_id="end", dag=dag)

    silver_stage = DockerOperator(
        task_id='fact_and_dim',
        image='dbt:custom',
        api_version='auto',
        auto_remove=True,
        command='run --project-dir /project/nyc_taxi_silver',
        docker_url='tcp://docker-proxy:2375',
        network_mode='test-networks',
        mounts= [
            Mount(
                source='/Users/aaaa/Learns/nyc_taxi_dwh/dags/nyc_taxi_silver/',
                target='/project/nyc_taxi_silver',
                type='bind'
            )
        ]
    )

    start >> silver_stage >> end