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

if __name__ == "__main__":
    from connection import create_db_engine

    engine = create_db_engine()

    truncate_dw(engine)
    load_dim_product("dw", "dim_product", engine)
    create_index_dim_tables("dw", "dim_product", "product_id", engine)
    load_dim_order("dw", "dim_order", engine)
    create_index_dim_tables("dw", "dim_order", "order_id", engine)
    load_fact_order_items("dw", "fact_order_items", engine)