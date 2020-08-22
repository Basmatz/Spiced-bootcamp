CREATE TABLE shippers (
  shipper_id SERIAL PRIMARY KEY,
  company_name VARCHAR(100) NOT NULL,
  phone VARCHAR(15)
);

COPY shippers FROM '...' DELIMITER ',' CSV HEADER;
