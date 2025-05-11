# Use the official Apache Airflow image as the base
FROM ghcr.io/dbt-labs/dbt-core:1.9.2

# Upgrade pip and install Python dependencies
COPY requirements.txt /requirements.txt

RUN pip install --no-cache-dir  -r /requirements.txt