import clickhouse_connect

def clickhouse_conn(creds: dict):
    conn = clickhouse_connect.get_client(
        host=creds["host"], 
        username=creds["user"], 
        password=creds["pass"], 
        port=creds["port"],
        database=creds["database"]
    )
    return conn

def connect(db_type: str, creds: dict):
    if db_type == 'clickhouse':
        return clickhouse_conn(creds=creds)