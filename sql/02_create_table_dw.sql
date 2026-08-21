CREATE TABLE IF NOT EXISTS dw.orders (
    order_key BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    order_id INTEGER NOT NULL, 
    user_id INTEGER, 
    order_number INTEGER, 
    order_dow INTEGER, 
    order_hour_of_day INTEGER, 
    days_since_prior_order NUMERIC
);

CREATE TABLE IF NOT EXISTS dw.products (
    product_key BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    product_id INTEGER NOT NULL, 
    product_name TEXT, 
    aisle_id INTEGER, 
    aisle TEXT, 
    department_id INTEGER, 
    department TEXT
)

CREATE TABLE IF NOT EXISTS dw.order_items (
    order_item_key BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    order_key BIGINT NOT NULL, 
    product_key BIGINT NOT NULL, 
    add_to_cart_order INTEGER, 
    reordered INTEGER,

    CONSTRAINT fk_fact_order
        FOREIGN KEY (order_key)
        REFERENCES dw.orders (order_key),
    
    CONSTRAINT fk_fact_product
        FOREIGN KEY (product_key)
        REFERENCES dw.products (product_key)
)