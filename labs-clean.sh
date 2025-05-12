# labs-clean.sh - destroy tools for running project nyc taxi data warehouse
# Author: Technisekai
# Usage: bash labs-clean.sh

#!/bin/bash

# Clean containers
docker-compose down

# Unset variables env
echo "INF Unset staging environtment"
unset $(grep -v '^#' env-stag.env | grep -v '^$' | cut -d= -f1)