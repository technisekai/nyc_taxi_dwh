
  
    
    
    
        
         


        insert into `stg-silver`.`fact_trip__dbt_backup`
        ("taxi_id", "vendor_id", "payment_id", "pickup_time", "dropoff_time", "trip_distance", "tolls_amount", "passenger_count", "tip_amount", "total_amount", "mta_tax", "extra")

with src_yellow as (
	select distinct
		1001 as taxi_id,
		y.VendorID,
		y.payment_type,
		y.tpep_pickup_datetime,
		y.tpep_dropoff_datetime,
		y.trip_distance,
		y.tolls_amount,
		y.passenger_count,
		y.tip_amount,
		y.total_amount,
		y.mta_tax
	from `stg-bronze`.yellow y 
),
src_green as (
	select distinct
		1002 as taxi_id,
		g.VendorID,
		g.payment_type,
		g.lpep_pickup_datetime,
		g.lpep_dropoff_datetime,
		g.trip_distance,
		g.tolls_amount,
		g.passenger_count,
		g.tip_amount,
		g.total_amount,
		g.mta_tax,
		g.extra
	from `stg-bronze`.green g 
),
trf as (
	select distinct
		y.taxi_id,
		cast(y.VendorID as Int64) as vendor_id,
		cast(y.payment_type as Int64) as payment_id,
		cast(y.tpep_pickup_datetime as datetime) as pickup_time,
		cast(y.tpep_dropoff_datetime as datetime) as dropoff_time,
		y.trip_distance,
		y.tolls_amount,
		y.passenger_count,
		y.tip_amount,
		y.total_amount,
		y.mta_tax,
		null as extra
	from src_yellow y 
	union all
	select distinct
		g.taxi_id,
		cast(g.VendorID as Int64) as vendor_id,
		cast(g.payment_type as Int64) as payment_id,
		cast(g.lpep_pickup_datetime as datetime) as pickup_time,
		cast(g.lpep_dropoff_datetime as datetime) as dropoff_time,
		g.trip_distance,
		g.tolls_amount,
		g.passenger_count,
		g.tip_amount,
		g.total_amount,
		g.mta_tax,
		g.extra
	from src_green g 
)
select * from trf
  