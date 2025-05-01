# Use the official Apache Airflow image as the base
FROM ghcr.io/dbt-labs/dbt-core:1.9.2

# Upgrade pip and install Python dependencies
COPY requirements.txt /requirements.txt

COPY nyc_taxi /projects/nyc_taxi

COPY nyc_taxi/profiles.yml /root/.dbt/profiles.yml

RUN pip install -r /requirements.txt