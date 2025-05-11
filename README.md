# NYC Taxi Data Warehouse

## Goals
- Create scalable data pipelines to serve data from sources to data warehouse
- Implement medallion architecture in data warehouse
- Implement data quality to make sure accuracy, completeness, consistency, timeliness, uniqueness, validity, integrity, consistency across time

## Future works
- Define variables for images name, networks name so easy to call in dags or docker-compose or docker build
- Automatically create database if doesnt exists [bronze, silver]
- Handle if bronze schemas change automatically
- Pipeline handle duplicate data (skip if exists) and incremental in silver stage
- DBT declare credentials as jinja not hardcoded
- Indexing and partioning
- Implements soda for checking data quality
- Create dashboard to show insight

## How to run
1. run `bash init-tools.sh`
2. run this following sql to create databases using tools like dbeaver, etc
    ```
    create database `prod-bronze`;
    create database `prod-silver`;
    ```
3. access airflow (https://localhost:8080) then setting airflow variables

    ```
    conn_dwh_secret: {
        "host": "dwh-db-clickhouse",
        "port": 8123,
        "user": "admin",
        "pass": "admin123",
        "database": "default"
    }

    nyc_bronze_config: {
        "env": "prod",
        "taxi_type": ["green", "yellow"],
        "dates": ["2024-01"]
    }
    ```
    _note: you can change dates in nyc_bronze_config to download or load taxi trip data in dates defined_
4. then access airflow (https://localhost:8080) and execute silver, bronze pipelines

## Descriptions
The New York City Taxi and Limousine Commission (TLC), created in 1971, is the agency responsible for licensing and regulating New York City's Medallion (Yellow) taxi cabs, for-hire vehicles (community-based liveries, black cars and luxury limousines), commuter vans, and paratransit vehicles. This data has great rows and attributes so suitable to use for learning how to serve data end-to-end from sources into insight!

## Theory
- Data Warehouse

    Designed to enable and support business intelligence (BI) activities to perform queries and analysis and often contain large amounts of historical data from multiple sources.

- Medallion Architecture
    - Bronze

        land all the data from external source systems. The table structures in this layer correspond to the source system table structures "as-is," along with any additional metadata columns that capture the load date/time, process ID, etc.
    - Silver

        The data from the Bronze layer is matched, merged, conformed and cleansed ("just-enough") so that the Silver layer can provide an "Enterprise view" of all its key business entities, concepts and transactions.
    - Gold

        organized in consumption-ready "project-specific" databases. The Gold layer is for reporting and uses more de-normalized and read-optimized data models with fewer joins.

- Data Orchestration

    method or a tool that manages data-related activities. The tasks include gathering data,
    performing quality checks, moving data across systems, automating workflows, and more.

- Data Quality

    measures how well a dataset meets criteria for accuracy, completeness, validity, consistency, uniqueness, timeliness and fitness for purpose, and it is critical to all data governance initiatives within an organization.

## Tools
- Python
- Airflow
- Soda
- DBT

## Schemas (for Silver Stage)
[View Database Diagram on dbdiagram.io](https://dbdiagram.io/e/67e7ab284f7afba184a5bedd/6820c30b5b2fc4582f19f7af)