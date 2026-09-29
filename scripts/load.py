from sqlalchemy import text

def truncate_dw(engine):
    query = """
    TRUNCATE TABLE
        dw.fact_order_items,
        dw.dim_order,
        dw.dim_product
    RESTART IDENTITY CASCADE;
    """

    with engine.begin() as connection:
        connection.execute(text(query))

    print("DW tables truncated.")

def load_dim_product(schema, table_name, engine):
    query = f"""INSERT INTO {schema}.{table_name} (
                product_id, 
                product_name, 
                aisle_id, 
                aisle, 
                department_id, 
                department)
                SELECT
                    product_id,
                    product_name,
                    aisle_id,
                    aisle,
                    department_id,
                    department
                FROM staging.products;"""
    with engine.begin() as connection:
        connection.execute(text(query))
    print('Dimensional product table loaded successfully.')

def load_dim_order(schema, table_name, engine):
    query = f"""INSERT INTO {schema}.{table_name} (
                order_id, 
                user_id, 
                order_number, 
                order_dow, 
                order_hour_of_day, 
                days_since_prior_order)
                SELECT
                    order_id,
                    user_id,
                    order_number,
                    order_dow,
                    order_hour_of_day,
                    days_since_prior_order
                FROM staging.orders;"""
    with engine.begin() as connection:
        connection.execute(text(query))
    print('Dimensional order table loaded successfully.')

def load_fact_order_items(schema, table_name, engine):
    query = f"""INSERT INTO {schema}.{table_name} (
                order_key, 
                product_key, 
                add_to_cart_order, 
                reordered)
                SELECT
                    o.order_key,
                    p.product_key,
                    op.add_to_cart_order,
                    op.reordered
                FROM staging.order_products op
                INNER JOIN dw.dim_product p
                    ON op.product_id = p.product_id
                INNER JOIN dw.dim_order o
                    ON op.order_id = o.order_id;"""
    with engine.begin() as connection:
        connection.execute(text(query))
    print('Fact table loaded successfully.')

def add_fk_constraints(schema, table_name, key, engine):
    query = f"""ALTER TABLE {schema}.fact_order_items
                ADD CONSTRAINT fk__{table_name}
                FOREIGN KEY ({key})
                REFERENCES {schema}.{table_name}({key})
                NOT VALID;"""

    with engine.begin() as connection:
        connection.execute(text(query))
    print(f"Foreign key constraint added to {schema}.fact_order_items referencing {schema}.{table_name}({key}).")

def validate_fk_constraints(schema, table_name, key, engine):
    query = f"""ALTER TABLE {schema}.fact_order_items
                VALIDATE CONSTRAINT fk__{table_name};"""

    with engine.begin() as connection:
        connection.execute(text(query))
    print(f"Foreign key constraint validated for {schema}.fact_order_items referencing {schema}.{table_name}({key}).")

def create_index_dim_tables(schema, table_name, id_column, engine):
    query = f"""CREATE UNIQUE INDEX IF NOT EXISTS 
                idx_dim_{table_name}_{id_column}
                ON {schema}.{table_name} ({id_column});"""
    analyze_query = f"""
        ANALYZE {schema}.{table_name};
    """
    with engine.begin() as connection:
        connection.execute(text(query))
        connection.execute(text(analyze_query))