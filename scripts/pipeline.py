import ingestion
import transform
import load

from connection import create_db_engine
from pathlib import Path

def main():
    print("Starting the ETL pipeline...")

    engine = create_db_engine()

    # Ingestion Step
    print("Starting data ingestion...")
    folder_path = Path('data/raw')

    for file in folder_path.iterdir():
        if file.is_file() and file.suffix == '.csv':
            ingestion.ingest_data_to_postgres(file, file.stem, 'raw', engine)

    print("Data ingestion completed successfully.")

    # Transformation Step
    print("Starting data transformation...")

    transform.create_schema("staging", engine)
    transform.create_table_products("staging", "products", engine)
    transform.create_table_orders("staging", "orders", engine)
    transform.create_table_order_products("staging", "order_products", engine)

    print("Transformation process completed successfully.")

    # Loading Step
    print("Starting data loading...")

    load.truncate_dw(engine)
    load.load_dim_product("dw", "dim_product", engine)
    load.load_dim_order("dw", "dim_order", engine)
    load.load_fact_order_items("dw", "fact_order_items", engine)

    print("Data loading completed successfully.")


if __name__ == "__main__":
    main()

    

