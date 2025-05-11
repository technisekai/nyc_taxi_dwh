
  
    
    
    
        
         


        insert into `stg-silver`.`dim_vendor__dbt_backup`
        ("vendor_id", "vendor_name", "_created_at")

with src_dim_vendor as (

    select 
        1 as vendor_id,
        'Creative Mobile Technologies, LLC' as vendor_name,
        now() as _created_at
    union all
    select 
        2 as vendor_id,
        'Curb Mobility, LLC' as vendor_name,
        now() as _created_at
    union all
    select 
        6 as vendor_id,
        'Myle Technologies Inc' as vendor_name,
        now() as _created_at
    union all
    select 
        7 as vendor_id,
        'Myle Technologies Inc' as vendor_name,
        now() as _created_at
)

select *
from src_dim_vendor
  