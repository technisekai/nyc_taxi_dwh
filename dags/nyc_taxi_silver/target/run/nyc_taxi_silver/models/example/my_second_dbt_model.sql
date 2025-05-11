

  create or replace view `stg-silver`.`my_second_dbt_model` 
  
    
  
  
    
    
  as (
    -- Use the `ref` function to select from other models

select *
from `stg-silver`.`my_first_dbt_model`
where id = 1
    
  )
      
      
                    -- end_of_sql
                    
                    