# labs-init.sh - prepare tools for running project nyc taxi data warehouse
# Author: Technisekai
# Usage: bash labs-init.sh

#!/bin/bash

root_directory="$PWD"

# Set variables
echo "INF set environtment variables"
set -a
source .env
set +a

# Create custom images airflow
cd "$root_directory/airflow-image/"
echo "INF create airflow custom image"
docker build -t $AIRFLOW_IMAGE_NAME .

# Create custom images dbt
cd "$root_directory/dbt-image/"
echo "INF create dbt custom image"
docker build -t $DBT_IMAGE_NAME .

# Create docker network
docker network create $DWH_NETWORK_NAME

# Running container
docker-compose up