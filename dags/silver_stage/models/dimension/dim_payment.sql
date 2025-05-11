{{ config(materialized='table') }}

with src_dim_payment as (
    select 
        0 as payment_id,
        'Flex Fare trip' as payment_name,
        now() as _created_at
    union all
    select 
        1 as payment_id,
        'Credit card' as payment_name,
        now() as _created_at
    union all
    select 
        2 as payment_id,
        'Cash' as payment_name,
        now() as _created_at
    union all
    select 
        3 as payment_id,
        'No Charge' as payment_name,
        now() as _created_at
    union all
    select 
        4 as payment_id,
        'Dispute' as payment_name,
        now() as _created_at
    union all
    select 
        5 as payment_id,
        'Unknown' as payment_name,
        now() as _created_at
    union all
    select 
        6 as payment_id,
        'Voided trip' as payment_name,
        now() as _created_at
)
select *
from src_dim_payment