CREATE TABLE sales_history (
    order_id SERIAL PRIMARY KEY,
    product VARCHAR(255) NOT NULL,
    quantity INT NOT NULL,
    total DECIMAL(10, 2) NOT NULL,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
