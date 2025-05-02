from airflow import DAG
from airflow.operators.python_operator import PythonOperator, ShortCircuitOperator, BranchPythonOperator
from airflow.operators.dummy_operator import DummyOperator
from airflow.models import Variable
import requests
import wget
import polars as pl
import os
from datetime import datetime
from cores.connection import connect
from cores.etl import clickhouse_create_table, clickhouse_batch_load

def get_the_file(path_file: str, url: str):
    # Checking file is it exists in local
    is_file_exists = os.path.isfile(path_file)
    if not is_file_exists:
        # Checking url is it valid
        is_url_valid = requests.head(url, timeout=30).status_code
        if is_url_valid == 200:
            print(f"file not exists, download file from {url}")
            wget.download(url=url, out=path_file)
            return True
        else:
            print(f"file not exists, but {url} is broken")
            return False
    else:
        print(f"file in local, skipped")
        return True

def load_data(path: str, database: str, creds: dict):
    # Read dataframe
    df = pl.scan_parquet(path)
    table_name = f"`{database}`.`{path.split('/')[-1].split('_')[0]}`"
    conn = connect(db_type="clickhouse", creds=creds)
    # Check is destination table exists
    schema = dict(zip(df.columns, df.dtypes))
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
            get_file = ShortCircuitOperator(
                task_id=f"get_{taxi}_{date}_file",
                python_callable=get_the_file,
                op_kwargs={
                    "path_file": f"/opt/airflow/dags/data/{taxi}_tripdata_{date}.parquet",
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

            start >> get_file >> load_file_into_db >> end