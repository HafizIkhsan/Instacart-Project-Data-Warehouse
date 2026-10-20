import pandas as pd
from pathlib import Path
import logging

def load_raw_to_postgres(file_path, table_name, schema_name, engine):
    df = pd.read_csv(file_path, nrows=1000)

    df_empty = df.head(0)

    print(f"Loading data from {file_path} to {table_name}.")

    df_empty.to_sql(
        table_name,
        engine,
        schema=schema_name,
        if_exists='replace',
        index=False
    )

    raw_conn = engine.raw_connection()
    try:
        with raw_conn.cursor() as cur:
            with open(file_path, 'r') as f:
                next(f) 
                cur.copy_expert(f"COPY {schema_name}.{table_name} FROM STDIN WITH CSV", f)

        raw_conn.commit()
        logging.info(f"Data ingestion to {table_name} completed successfully.")

    except Exception as e:
        raw_conn.rollback()
        logging.error(f"Error occurred while ingesting data to {table_name}: {e}")

    finally:
        raw_conn.close()