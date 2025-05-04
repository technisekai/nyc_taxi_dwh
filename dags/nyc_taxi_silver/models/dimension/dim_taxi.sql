{{ config(materialized='table') }}

with src_dim_taxi as (

    select 
        1001 as taxi_id
        'taxi_yellow' as taxi_name
        current_timestamp as _created_at
    union all
    select 
        1002 as taxi_id
        'taxi_green' as taxi_name
        current_timestamp as _created_at

)

select *
from src_dim_taxi