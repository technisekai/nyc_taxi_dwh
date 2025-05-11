# init-tools.sh - prepare tools for running project nyc taxi data warehouse
# Author: Technisekai
# Usage: ./init-tools.sh

#!/bin/bash

root_directory="$PWD"

# Create custom images airflow
cd "$root_directory/airflow-image/"
echo "INF create airflow custom image"
docker build -t airflow-mod:v1.0.0 .

# Create custom images dbt
cd "$root_directory/dbt-image/"
echo "INF create dbt custom image"
docker build -t dbt-mod:v1.0.0 .

# Create docker network
docker network create dwh-network

# Running container
docker-compose up