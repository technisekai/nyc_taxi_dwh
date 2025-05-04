{{ config(materialized='table') }}

with src_dim_vendor as (

    select 
        1 as vendor_id
        'Creative Mobile Technologies, LLC' as vendor_name
        current_timestamp as _created_at
    union all
    select 
        2 as vendor_id
        'Curb Mobility, LLC' as vendor_name
        current_timestamp as _created_at
    union all
    select 
        6 as vendor_id
        'Myle Technologies Inc' as vendor_name
        current_timestamp as _created_at
    union all
    select 
        7 as vendor_id
        'Myle Technologies Inc' as vendor_name
        current_timestamp as _created_at
)

select *
from src_dim_vendor