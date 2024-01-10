CREATE TABLE inventory_history (
    id SERIAL PRIMARY KEY,
    product_id INT REFERENCES products(product_id),
    timestamp TIMESTAMP NOT NULL,
    new_quantity INT NOT NULL
);
