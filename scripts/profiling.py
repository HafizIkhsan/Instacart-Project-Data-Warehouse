from connection import conn
import pandas as pd

tables = [
    "aisles",
    "departments",
    "order_products__prior",
    "order_products__train",
    "orders",
    "products"
]

def get_column_names(schema, table):
    query = f"""SELECT column_name
                FROM information_schema.columns
                WHERE table_schema = '{schema}'
                AND table_name = '{table}';"""
    df = pd.read_sql(query, conn)
    return df['column_name'].tolist()

def check_row_counts(table):
    for table in tables:
        query = f"SELECT COUNT(*) AS row_count FROM raw.{table};"
        df = pd.read_sql(query, conn)
        print(f"Table: {table}, Rows: {df['row_count'].iloc[0]}")

def check_null(schema, table):
    column_names = get_column_names(schema, table)
    for column in column_names:
        query = f"""SELECT 
                    COUNT (*) AS total_rows,
                    COUNT (*) FILTER (WHERE {column} IS NULL) AS {column}_null 
                    FROM {schema}.{table};"""
        df = pd.read_sql(query, conn)
        print(f"Table:{table}, Column: {column}, Total Rows: {df['total_rows'].iloc[0]}, Null Count: {df[f'{column}_null'].iloc[0]}")
    
def check_duplicates(schema, table):
    column_names = get_column_names(schema, table)
    for column in column_names:
        query = f"""SELECT 
                    COUNT (*) AS total_rows,
                    COUNT (DISTINCT {column}) AS distinct_count,
                    COUNT (*) - COUNT (DISTINCT {column}) AS duplicate_count
                    FROM {schema}.{table};"""
        df = pd.read_sql(query, conn)
        print(f"Table:{table}, Column: {column}, Total Rows: {df['total_rows'].iloc[0]}, Distinct Count: {df['distinct_count'].iloc[0]}, Duplicate Count: {df['duplicate_count'].iloc[0]}")

def check_relationship(schema, table1, table2, column1, column2):
    query = f"""SELECT 
                COUNT(*) AS total_rows,
                COUNT(*) FILTER (WHERE {table1}.{column1} IS NOT NULL AND {table2}.{column2} IS NOT NULL) AS matching_rows,
                COUNT(*) FILTER (WHERE {table1}.{column1} IS NOT NULL AND {table2}.{column2} IS NULL) AS missing_in_{table2},
                COUNT(*) FILTER (WHERE {table1}.{column1} IS NULL AND {table2}.{column2} IS NOT NULL) AS missing_in_{table1}
                FROM {schema}.{table1}
                FULL OUTER JOIN {schema}.{table2}
                ON {table1}.{column1} = {table2}.{column2};"""
    df = pd.read_sql(query, conn)
    print(f"Relationship between {table1}.{column1} and {table2}.{column2}: Total Rows: {df['total_rows'].iloc[0]}, Matching Rows: {df['matching_rows'].iloc[0]}, Missing in {table2}: {df[f'missing_in_{table2}'].iloc[0]}, Missing in {table1}: {df[f'missing_in_{table1}'].iloc[0]}")

def check_prior_train(schema, table1, table2):
    column_names1 = get_column_names(schema, table1)
    column_names2 = get_column_names(schema, table2)
    query = f"""SELECT 'prior' AS source,
                COUNT(*) AS total_rows
                FROM {schema}.{table1}
                UNION ALL
                SELECT 'train' AS source,
                COUNT(*) AS total_rows
                FROM {schema}.{table2};"""
    df = pd.read_sql(query, conn)
    for index, row in df.iterrows():
        print(f"Source: {row['source']}, Total Rows: {row['total_rows']}, Column Names: {column_names1 if row['source'] == 'prior' else column_names2}")  

if __name__ == "__main__":
    check_row_counts('raw')
    for table in tables:
        check_null('raw', table)
        check_duplicates('raw', table)
    check_relationship('raw', 'orders', 'order_products__prior', 'order_id', 'order_id')
    check_relationship('raw', 'orders', 'order_products__train', 'order_id', 'order_id')
    check_relationship('raw', 'products', 'order_products__prior', 'product_id', 'product_id')
    check_relationship('raw', 'products', 'order_products__train', 'product_id', 'product_id')
    check_prior_train('raw', 'order_products__prior', 'order_products__train')
    
