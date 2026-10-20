from sqlalchemy import text
import logging

def create_schema(name,engine):
    query = f"CREATE SCHEMA IF NOT EXISTS {name};"
    with engine.begin() as connection:
        connection.execute(text(query))

    logging.info(f"Schema {name} created successfully.")

def create_table_products(schema, table_name, engine):
    query = f"""DROP TABLE IF EXISTS {schema}.{table_name};
                CREATE TABLE {schema}.{table_name} AS 
                SELECT
                    CAST(p.product_id AS INTEGER) AS product_id,
                    CAST(p.product_name AS VARCHAR(255)) AS product_name,
                    CAST(p.aisle_id AS INTEGER) AS aisle_id,
                    CAST(a.aisle AS VARCHAR(255)) AS aisle,
                    CAST(p.department_id AS INTEGER) AS department_id,
                    CAST(d.department AS VARCHAR(255)) AS department
                FROM raw.products p
                LEFT JOIN raw.aisles a
                    ON p.aisle_id = a.aisle_id
                LEFT JOIN raw.departments d
                    ON p.department_id = d.department_id;"""
    with engine.begin() as connection:
        connection.execute(text(query))

    logging.info(f"Table {schema}.{table_name} created successfully.")

def create_table_orders(schema, table_name, engine):
    query = f"""DROP TABLE IF EXISTS {schema}.{table_name};
                CREATE TABLE {schema}.{table_name} AS 
                SELECT
                    CAST(o.order_id AS INTEGER) AS order_id,
                    CAST(o.user_id AS INTEGER) AS user_id,
                    CAST(o.order_number AS INTEGER) AS order_number,
                    CAST(o.order_dow AS SMALLINT) AS order_dow,
                    CAST(o.order_hour_of_day AS SMALLINT) AS order_hour_of_day,
                    CAST(o.days_since_prior_order AS SMALLINT) AS days_since_prior_order
                FROM raw.orders o;"""
    with engine.begin() as connection:
        connection.execute(text(query))

    logging.info(f"Table {schema}.{table_name} created successfully.")

def create_table_order_products(schema, table_name, engine):
    query = f"""DROP TABLE IF EXISTS {schema}.{table_name};
                CREATE TABLE {schema}.{table_name} AS 
                SELECT
                    CAST(op.order_id AS INTEGER) AS order_id,
                    CAST(op.product_id AS INTEGER) AS product_id,
                    CAST(op.add_to_cart_order AS INTEGER) AS add_to_cart_order,
                    CAST(op.reordered AS SMALLINT) AS reordered
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

    logging.info(f"Table {schema}.{table_name} created successfully.")
