import pandas as pd
from sqlalchemy import create_engine, text
import urllib
import time

server = "database-1.chek4ea2izsv.us-west-1.rds.amazonaws.com"
database = "BusinessAssessmentRDS"
username = "admin"
password = "RE60as87$&"

params = urllib.parse.quote_plus(
    f"DRIVER={{ODBC Driver 18 for SQL Server}};"
    f"SERVER={server};DATABASE={database};"
    f"UID={username};PWD={password};"
    f"Encrypt=yes;TrustServerCertificate=yes;"
)

files = {
    "date_dim": "/Users/raidriar/business_insight_assessment/source_data/date_dim.csv",
    "order_item_options": "/Users/raidriar/business_insight_assessment/source_data/order_item_options.csv",
    "order_items": "/Users/raidriar/business_insight_assessment/source_data/order_items.csv",
}

def make_engine():
    return create_engine(
        f"mssql+pyodbc:///?odbc_connect={params}",
        pool_pre_ping=True,
        pool_recycle=280,
    )

def load_with_retry(table_name, path, max_retries=5):
    df = pd.read_csv(path)
    engine = make_engine()
    with engine.begin() as conn:
        conn.execute(text(f"IF OBJECT_ID('dbo.{table_name}', 'U') IS NOT NULL DROP TABLE dbo.{table_name};"))

    chunk_size = 500
    total = len(df)
    start = 0
    while start < total:
        chunk = df.iloc[start:start+chunk_size]
        for attempt in range(max_retries):
            try:
                chunk.to_sql(table_name, engine, if_exists="append", index=False)
                break
            except Exception as e:
                wait = 2 ** attempt
                print(f"  chunk {start}-{start+chunk_size} attempt {attempt+1} failed: {e}. Retrying in {wait}s...")
                time.sleep(wait)
                engine.dispose()
                engine = make_engine()
        else:
            raise RuntimeError(f"Chunk {start}-{start+chunk_size} failed after {max_retries} retries")
        start += chunk_size
    engine.dispose()
    print(f"Loaded {total} rows into {table_name}")

for table_name, path in files.items():
    load_with_retry(table_name, path)
