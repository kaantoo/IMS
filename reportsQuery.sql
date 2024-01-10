CREATE TABLE reports (
    report_id SERIAL PRIMARY KEY,
    report_type VARCHAR(50) NOT NULL,
    description TEXT,
    generated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
ALTER TABLE reports
ADD COLUMN sales_amount DECIMAL(10, 2),
ADD COLUMN sales_date DATE;
