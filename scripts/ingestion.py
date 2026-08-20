import pandas as pd
from pathlib import Path

def ingest_data_to_postgres(file_path, table_name, schema_name, engine):
    df = pd.read_csv(file_path, nrows=1000)

    df_empty = df.head(0)

    print(f"Ingesting data from {file_path} to {table_name}.")

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
                next(f)  # Skip the header row
                cur.copy_expert(f"COPY {schema_name}.{table_name} FROM STDIN WITH CSV", f)

        raw_conn.commit()
        print(f"Data ingestion to {table_name} completed successfully.")

    except Exception as e:
        raw_conn.rollback()
        print(f"Error occurred while ingesting data to {table_name}: {e}")

    finally:
        raw_conn.close()

if __name__ == "__main__":
    from connection import create_db_engine

    engine = create_db_engine()

    folder_path = Path('data/raw')

    for file in folder_path.iterdir():
        if file.is_file() and file.suffix == '.csv':
            ingest_data_to_postgres(file, 
                                    file.stem, 
                                    'raw',
                                    engine)