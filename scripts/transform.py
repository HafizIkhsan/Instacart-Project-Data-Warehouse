from sqlalchemy import text

def create_schema(name,engine):
    query = f"CREATE SCHEMA IF NOT EXISTS {name};"
    with engine.begin() as connection:
        connection.execute(text(query))

def create_table_products(schema, table_name, engine):
    query = f"""DROP TABLE IF EXISTS {schema}.{table_name};
                CREATE TABLE {schema}.{table_name} AS 
                SELECT
                    p.product_id,
                    p.product_name,
                    p.aisle_id,
                    a.aisle,
                    p.department_id,
                    d.department
                FROM raw.products p
                LEFT JOIN raw.aisles a
                    ON p.aisle_id = a.aisle_id
                LEFT JOIN raw.departments d
                    ON p.department_id = d.department_id;"""
    with engine.begin() as connection:
        connection.execute(text(query))

def create_table_orders(schema, table_name, engine):
    query = f"""DROP TABLE IF EXISTS {schema}.{table_name};
                CREATE TABLE {schema}.{table_name} AS 
                SELECT
                    o.order_id,
                    o.user_id,
                    o.order_number,
                    o.order_dow,
                    o.order_hour_of_day,
                    o.days_since_prior_order
                FROM raw.orders o;"""
    with engine.begin() as connection:
        connection.execute(text(query))

def create_table_order_products(schema, table_name, engine):
    query = f"""DROP TABLE IF EXISTS {schema}.{table_name};
                CREATE TABLE {schema}.{table_name} AS 
                SELECT
                    op.order_id,
                    op.product_id,
                    op.add_to_cart_order,
                    op.reordered
                FROM raw.order_products__prior op
                UNION ALL
                SELECT
                    op.order_id,
                    op.product_id,
                    op.add_to_cart_order,
                    op.reordered
                FROM raw.order_products__train op;"""
    with engine.begin() as connection:
        connection.execute(text(query))

if __name__ == "__main__":
    from connection import create_db_engine

    engine = create_db_engine()

    create_schema("staging", engine)
    create_table_products("staging", "products", engine)
    create_table_orders("staging", "orders", engine)
    create_table_order_products("staging", "order_products", engine)
    print("Transformation process completed successfully.")