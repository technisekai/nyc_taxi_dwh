import pandas as pd

def clickhouse_exec(conn, query: str):
    conn.command(query)

def clickhouse_create_table(conn, destination_table_name: str, schema: dict):
    for x in schema.keys():
        if schema[x] == 'object':
            schema[x] = 'Nullable(varchar)'
        elif 'datetime' in schema[x]:
            schema[x] = 'Nullable(datetime)'
        elif schema[x] == 'int64':
            schema[x] = 'Nullable(Int64)'
        elif schema[x] == 'float64':
            schema[x] = 'Nullable(Float64)'
        else:
            pass
    clickhouse_schema = ", ".join(f"{key} {value}" for key, value in schema.items())
    query = f"create table if not exists {destination_table_name} ({clickhouse_schema}, created_at DateTime DEFAULT now()) engine = MergeTree order by created_at"
    print(query)
    clickhouse_exec(conn, query)

# ETL
def clickhouse_batch_load(conn, destination_table_name: str, df: pd.DataFrame, chunksize=500):
    columns = list(df.columns)
    print("INF batch load: ", end="")
    for idx in range(0, df.shape[0], chunksize):
        conn.insert(
            destination_table_name, 
            df.iloc[idx:idx+chunksize].to_numpy(), 
            column_names=columns
        )
        print(f"{idx}", end=" ")
    print("\nINF done")