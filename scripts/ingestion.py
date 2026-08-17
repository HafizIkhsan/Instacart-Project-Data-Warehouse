import pandas as pd
from pathlib import Path

def ingest_data_to_postgres(file_path, table_name, schema_name, engine):
    df = pd.read_csv(file_path)

    print(f"Ingesting data from {file_path} to {table_name} with {len(df)} records.")

    df.to_sql(
        table_name,
        engine,
        schema=schema_name,
        if_exists='replace',
        index=False,
        chunksize=50000,
        method='multi'
    )

    print(f"Data ingestion to {table_name} completed successfully.")

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