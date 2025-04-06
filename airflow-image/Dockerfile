# Use the official Apache Airflow image as the base
FROM apache/airflow:2.6.2-python3.11

# Set Airflow version
ARG AIRFLOW_VERSION=2.6.2

# Upgrade pip and install Python dependencies
COPY requirements.txt /requirements.txt

RUN pip install --upgrade pip && \
    pip install --no-cache-dir "apache-airflow[pandas,postgres,celery,redis]==${AIRFLOW_VERSION}" \
    -r /requirements.txt

# Switch back to airflow user (default in base image)
USER airflow

# Expose ports
EXPOSE 8080
EXPOSE 8793
EXPOSE 5555