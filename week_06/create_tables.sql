CREATE TABLE shippers(
  shipper_id SERIAL PRIMARY KEY,
  company_name VARCHAR(100) NOT NULL,
  phone VARCHAR(15)

);

COPY shippers FROM '/home/stazhe/Spiced/logistic-lemongrass-student-code/week_06/data/shippers.csv' DELIMITER ',' CSV HEADER;

CREATE TABLE categories(
  category_id SERIAL PRIMARY KEY,
  category_name VARCHAR(100) NOT NULL,
  description TEXT,
  --picture

);

COPY categories FROM '/home/stazhe/Spiced/logistic-lemongrass-student-code/week_06/data/categories.csv' DELIMITER ',' CSV HEADER;

CREATE TABLE customers(
  customerID VARCHAR(5),
  customer_company_name VARCHAR(100) NOT NULL,
  customer_contact_name VARCHAR(50),

PRIMARY KEY (`id`)

  --picture

);

COPY categories FROM '/home/stazhe/Spiced/logistic-lemongrass-student-code/week_06/data/categories.csv' DELIMITER ',' CSV HEADER;
