from airflow import DAG
from airflow.operators.python_operator import PythonOperator, ShortCircuitOperator
from airflow.operators.dummy_operator import DummyOperator
from airflow.models import Variable
import requests
import wget
import pandas as pd
from datetime import datetime
from cores.connection import connect
from cores.etl import clickhouse_create_table, clickhouse_batch_load

def is_file_exists(url: str):
    # Check if file exists in url
    res = requests.head(
        url, 
        timeout=30
    )
    if res.status_code == 200:
        return True
    return False

def get_file(dir_path: str, url: str):
    filename = url.split('/')[-1]
    path = f"{dir_path}/"
    # Download file
    wget.download(url=url, out=path)

def load_data(path: str, database: str, creds: dict):
    # Read dataframe
    df = pd.read_parquet(path)
    table_name = f"`{database}`.`{path.split('/')[-1].split('_')[0]}`"
    conn = connect(db_type="clickhouse", creds=creds)
    # Check is destination table exists
    schema = df.dtypes.apply(lambda x: x.name).to_dict()
    clickhouse_create_table(conn, table_name, schema)
    # Inject data
    clickhouse_batch_load(conn, table_name, df)
    conn.close()


# DAG Configuration
default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "email_on_failure": False,
    "email_on_retry": False
}

with DAG(
    "nyc_taxi_bronze",
    default_args=default_args,
    description="",
    schedule_interval=None,
    start_date=datetime(2025, 4, 4),
    catchup=False,
) as dag:
    bronze_config = Variable.get("nyc_bronze_config", deserialize_json=True)
    dwh_creds = Variable.get("conn_dwh_secret", deserialize_json=True)

    start = DummyOperator(task_id="start", dag=dag)

    end = DummyOperator(task_id="end", dag=dag)

    for date in bronze_config["dates"]:
        for taxi in bronze_config["taxi_type"]:
            check_file = ShortCircuitOperator(
                task_id=f"check_{taxi}_{date}_file",
                python_callable=is_file_exists,
                op_kwargs={
                    "url": f"https://d37ci6vzurychx.cloudfront.net/trip-data/{taxi}_tripdata_{date}.parquet"
                }
            )

            download_file = PythonOperator(
                task_id=f"download_{taxi}_{date}_dataset",
                python_callable=get_file,
                op_kwargs={
                    "dir_path": "/opt/airflow/dags/data",
                    "url": f"https://d37ci6vzurychx.cloudfront.net/trip-data/{taxi}_tripdata_{date}.parquet"
                }
            )

            load_file_into_db = PythonOperator(
                task_id=f"load_{taxi}_{date}_into_bronze",
                python_callable=load_data,
                op_kwargs={
                    "path": f"/opt/airflow/dags/data/{taxi}_tripdata_{date}.parquet",
                    "database": f"{bronze_config['env']}-bronze",
                    "creds": dwh_creds
                }
            )

            start >> check_file >> download_file >> load_file_into_db >> end