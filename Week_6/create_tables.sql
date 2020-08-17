DROP SCHEMA public CASCADE;
CREATE SCHEMA public;

CREATE TABLE shippers (
  shipper_ID SERIAL PRIMARY KEY,
  company_name VARCHAR(100) NOT NULL,
  phone VARCHAR(20)
);

CREATE TABLE customers (
  customer_ID VARCHAR(15) PRIMARY KEY,
  company_name VARCHAR(100) NOT NULL,
  contact_name VARCHAR(100) NOT NULL,
  contact_title VARCHAR(100) NOT NULL,
  address VARCHAR(100) NOT NULL,
  city VARCHAR(100) NOT NULL,
  region VARCHAR(100),
  postal_code VARCHAR(20) NOT NULL,
  country VARCHAR(50) NOT NULL,
  phone VARCHAR(20),
  fax VARCHAR(20)
);

CREATE TABLE employee_territories (
  employee_ID  SMALLINT,
  territory_ID BIGINT NOT NULL
);

CREATE TABLE order_details (
  order_ID SMALLINT,
  product_ID SMALLINT NOT NULL,
  unit_price REAL NOT NULL,
  quantity SMALLINT NOT NULL,
  discount REAL NOT NULL
);

CREATE TABLE orders (
  order_ID SERIAL PRIMARY KEY,
  customer_ID VARCHAR(15) NOT NULL,
  employee_ID SMALLINT NOT NULL,
  order_date TIMESTAMP NULL,
  required_date TIMESTAMP NULL,
  shipped_date TIMESTAMP NULL,
  ship_via VARCHAR(5) NOT NULL,
  freight REAL NOT NULL,
  ship_name VARCHAR(100) NOT NULL,
  ship_address VARCHAR(100) NOT NULL,
  ship_city VARCHAR(100) NOT NULL,
  ship_region VARCHAR(100),
  ship_postcode VARCHAR(100) NOT NULL,
  ship_country VARCHAR(100) NOT NULL
);

CREATE TABLE products (
  product_ID SMALLINT PRIMARY KEY,
  product_name VARCHAR(50) NOT NULL,
  supplier_ID SMALLINT NOT NULL,
  category_ID SMALLINT NOT NULL,
  quantity_per_unit VARCHAR(100),
  unit_price REAL NOT NULL,
  units_in_stock SMALLINT NOT NULL,
  units_on_order SMALLINT NOT NULL,
  reoder_level SMALLINT NOT NULL,
  discontinued VARCHAR(1)
);

CREATE TABLE regions (
  region_ID INTEGER CHECK (region_ID<=5),
  region_description VARCHAR(20) NOT NULL
);

CREATE TABLE suppliers (
  supplier_ID SERIAL PRIMARY KEY,
  company_name VARCHAR(100) NOT NULL,
  contact_name VARCHAR(100) NOT NULL,
  contact_title VARCHAR(100) NOT NULL,
  address VARCHAR(100) NOT NULL,
  city VARCHAR(100) NOT NULL,
  region VARCHAR(100),
  postal_code VARCHAR(20) NOT NULL,
  country VARCHAR(50) NOT NULL,
  phone VARCHAR(20),
  fax VARCHAR(20),
  homepage VARCHAR(100)
);

CREATE TABLE territories (
  territory_ID BIGINT PRIMARY KEY,
  territory_description VARCHAR(100),
  region_ID SMALLINT CHECK (region_ID<=5)
);

CREATE TABLE categories (
  category_ID SMALLINT PRIMARY KEY,
  category_name VARCHAR(100),
  description VARCHAR(100)
);

CREATE TABLE employees (
  employee_ID SMALLINT PRIMARY KEY,
  last_name VARCHAR(50) NOT NULL,
  title VARCHAR(50),
  title_of_courtesy VARCHAR(5),
  birth_date TIMESTAMP NULL,
  hire_date TIMESTAMP NULL,
  address VARCHAR(50) NOT NULL,
  city VARCHAR(50) NOT NULL,
  region VARCHAR(5),
  postal_code VARCHAR(20) NOT NULL,
  country VARCHAR(50),
  phone VARCHAR(20),
  extension VARCHAR(15),
  notes TEXT,
  reports_to SMALLINT,
  photo_path VARCHAR(100)
);


COPY shippers FROM '/Users/laraehrenhofer/Documents/Coding_Projects/git_repos/logistic-lemongrass-student-code/Week_6/northwind_data_clean-master/data/shippers.csv' DELIMITER ',' CSV HEADER;
COPY customers FROM '/Users/laraehrenhofer/Documents/Coding_Projects/git_repos/logistic-lemongrass-student-code/Week_6/northwind_data_clean-master/data/customers.csv' DELIMITER ',' CSV HEADER;
COPY categories FROM '/Users/laraehrenhofer/Documents/Coding_Projects/git_repos/logistic-lemongrass-student-code/Week_6/northwind_data_clean-master/data/categories.csv' DELIMITER ',' CSV HEADER;
COPY employee_territories FROM '/Users/laraehrenhofer/Documents/Coding_Projects/git_repos/logistic-lemongrass-student-code/Week_6/northwind_data_clean-master/data/employee_territories.csv' DELIMITER ',' CSV HEADER;
COPY order_details FROM '/Users/laraehrenhofer/Documents/Coding_Projects/git_repos/logistic-lemongrass-student-code/Week_6/northwind_data_clean-master/data/order_details.csv' DELIMITER ',' CSV HEADER;
COPY orders FROM '/Users/laraehrenhofer/Documents/Coding_Projects/git_repos/logistic-lemongrass-student-code/Week_6/northwind_data_clean-master/data/orders.csv' DELIMITER ',' CSV HEADER;
COPY products FROM '/Users/laraehrenhofer/Documents/Coding_Projects/git_repos/logistic-lemongrass-student-code/Week_6/northwind_data_clean-master/data/products.csv' DELIMITER ',' CSV HEADER;
COPY regions FROM '/Users/laraehrenhofer/Documents/Coding_Projects/git_repos/logistic-lemongrass-student-code/Week_6/northwind_data_clean-master/data/regions.csv' DELIMITER ',' CSV HEADER;
COPY suppliers FROM '/Users/laraehrenhofer/Documents/Coding_Projects/git_repos/logistic-lemongrass-student-code/Week_6/northwind_data_clean-master/data/suppliers.csv' DELIMITER ',' CSV HEADER;
COPY territories FROM '/Users/laraehrenhofer/Documents/Coding_Projects/git_repos/logistic-lemongrass-student-code/Week_6/northwind_data_clean-master/data/territories.csv' DELIMITER ',' CSV HEADER;
