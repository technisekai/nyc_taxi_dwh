# Use the official Apache Airflow image as the base
FROM apache/airflow:2.9.3-python3.11

# Set Airflow version
ARG AIRFLOW_VERSION=2.9.3

# Switch to root user for installing dependencies
USER root

# Install required system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    gcc \
    g++ \
    libpq-dev \
    python3-dev \
    git \
    && rm -rf /var/lib/apt/lists/*

# Switch back to airflow user (default in base image)
USER airflow

# Upgrade pip and install Python dependencies
COPY requirements.txt /requirements.txt

RUN pip install --upgrade pip && \
    pip install --no-cache-dir "apache-airflow[pandas,postgres,celery,redis]==${AIRFLOW_VERSION}" \
    -r /requirements.txt

# Switch back to airflow user (default in base image)
USER airflow
