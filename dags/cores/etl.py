import polars as pl

def clickhouse_exec(conn, query: str):
    conn.command(query)

def clickhouse_create_table(conn, destination_table_name: str, schema: dict):
    for x in schema.keys():
        pl_datatype = str(schema[x]).lower()

        if pl_datatype in ('object', 'string'):
            schema[x] = 'Nullable(varchar)'
        elif 'datetime' in pl_datatype:
            schema[x] = 'Nullable(datetime)'
        elif pl_datatype == 'int64':
            schema[x] = 'Nullable(Int64)'
        elif pl_datatype == 'float64':
            schema[x] = 'Nullable(Float64)'
        elif pl_datatype == 'int32':
            schema[x] = 'Nullable(Int32)'
        else:
            pass
    clickhouse_schema = ", ".join(f"{key} {value}" for key, value in schema.items())
    query = f"create table if not exists {destination_table_name} ({clickhouse_schema}, created_at DateTime DEFAULT now()) engine = MergeTree order by created_at"
    print(query)
    clickhouse_exec(conn, query)

# ETL
def clickhouse_batch_load(conn, destination_table_name: str, df, chunksize=500):
    columns = list(df.collect_schema().names())
    rows =  df.collect().height
    print("INF batch load: ", end="")
    for idx in range(0, rows, chunksize):
        tmp_df = df.slice(idx, idx+chunksize).collect()
        tmp_df = tmp_df.to_pandas()
        conn.insert(
            destination_table_name, 
            tmp_df.to_numpy(), 
            column_names=columns
        )
        print(f"{idx}", end=" ")
    print("\nINF done")