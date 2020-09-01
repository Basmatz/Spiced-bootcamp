DROP TABLE IF EXISTS shippers;
DROP TABLE IF EXISTS regions;
DROP TABLE IF EXISTS categories;
DROP TABLE IF EXISTS customers;
DROP TABLE IF EXISTS employee_territories;
DROP TABLE IF EXISTS employees;
DROP TABLE IF EXISTS orders;
DROP TABLE IF EXISTS order_details;
DROP TABLE IF EXISTS suppliers;
DROP TABLE IF EXISTS territories;


CREATE TABLE shippers(
  shipper_id INT PRIMARY KEY,
  company_name VARCHAR(100) NOT NULL,
  phone VARCHAR(15)
);
COPY shippers FROM '/home/stazhe/Spiced/logistic-lemongrass-student-code/week_06/data/shippers.csv' DELIMITER ',' CSV HEADER;

CREATE TABLE regions(
  region_id INT PRIMARY KEY,
  region_description VARCHAR(100) NOT NULL
);
COPY regions FROM '/home/stazhe/Spiced/logistic-lemongrass-student-code/week_06/data/regions.csv' DELIMITER ',' CSV HEADER;

CREATE TABLE territories(
  territory_id INT PRIMARY KEY,
  territory_description VARCHAR(100) NOT NULL,
  region_id INT,
	FOREIGN KEY(region_id) REFERENCES regions(region_id)
);

COPY territories FROM '/home/stazhe/Spiced/logistic-lemongrass-student-code/week_06/data/territories.csv' DELIMITER ',' CSV HEADER;

CREATE TABLE categories(
  category_id INT PRIMARY KEY,
  category_name VARCHAR(100) NOT NULL,
  description TEXT,
  picture TEXT
);
COPY categories FROM '/home/stazhe/Spiced/logistic-lemongrass-student-code/week_06/data/categories.csv' DELIMITER ',' CSV HEADER;

CREATE TABLE customers(
  customer_id VARCHAR(5) PRIMARY KEY,
  customer_company_name VARCHAR(100) NOT NULL,
  customer_contact_name VARCHAR(50),
  customer_contact_title VARCHAR(30),
  customer_address VARCHAR(50),
  customer_city VARCHAR(50),
  customer_region VARCHAR(50),
  customer_postal_code VARCHAR(20),
  customer_country VARCHAR(20),
  customer_phone VARCHAR(20),
  customer_fax VARCHAR(20)
);
COPY customers FROM '/home/stazhe/Spiced/logistic-lemongrass-student-code/week_06/data/customers.csv' DELIMITER ',' CSV HEADER;


CREATE TABLE orders(
  order_id INT PRIMARY KEY,
  customer_id VARCHAR(5) NOT NULL,
  employee_id INT NOT NULL,
  order_date DATE,
  required_date DATE,
  shipped_date DATE,
  ship_via INT NOT NULL,
  freight REAL,
  ship_name VARCHAR(50),
  ship_address VARCHAR(100),
  ship_city VARCHAR(50),
  ship_region VARCHAR(50),
  ship_postal_code VARCHAR(20),
  ship_country VARCHAR(20),
	FOREIGN KEY(customer_id) REFERENCES customers(customer_id),
	FOREIGN KEY(employee_id) REFERENCES employees(employee_id),
	FOREIGN KEY(ship_via) REFERENCES shippers(shipper_id)
	
);

COPY orders FROM '/home/stazhe/Spiced/logistic-lemongrass-student-code/week_06/data/orders.csv' DELIMITER ',' CSV HEADER;

CREATE TABLE order_details(
  order_id INT NOT NULL,
  product_id INT NOT NULL,
  unit_price REAL NOT NULL,
  order_quantity INT,
  order_discount REAL,
  FOREIGN KEY(order_id) REFERENCES orders(order_id),
  FOREIGN KEY(product_id) REFERENCES products(product_id)
);

COPY orders_details FROM '/home/stazhe/Spiced/logistic-lemongrass-student-code/week_06/data/order_details.csv' DELIMITER ',' CSV HEADER;



CREATE TABLE suppliers(
  supplier_id INT PRIMARY KEY,
  supplier_company_name VARCHAR(100) NOT NULL,
  supplier_contact_name VARCHAR(50),
  supplier_contact_title VARCHAR(30),
  supplier_address VARCHAR(50),
  supplier_city VARCHAR(50),
  supplier_region VARCHAR(50),
  supplier_postal_code VARCHAR(20),
  supplier_country VARCHAR(20),
  supplier_phone VARCHAR(20),
  supplier_fax VARCHAR(20),
  supplier_homepage TEXT

);

COPY suppliers FROM '/home/stazhe/Spiced/logistic-lemongrass-student-code/week_06/data/suppliers.csv' DELIMITER ',' CSV HEADER;


CREATE TABLE employees(
    employee_id INT PRIMARY KEY,
    employee_last_name VARCHAR(20),
    employee_first_name VARCHAR(20),
    employee_title VARCHAR(30),
    employee_courtesy_title VARCHAR(5),
    employee_birth_date DATE,
    employee_hire_date DATE,
    employee_address VARCHAR(100),
    employee_city VARCHAR(50),
    employee_region VARCHAR(50),
    employee_postal_code VARCHAR(20),
    employee_country VARCHAR(20),
    employee_phone VARCHAR(20),
    employee_ext VARCHAR(4),
    employee_photo TEXT,
    employee_notes TEXT,
    employee_reports_to INT,
    empolyee_photo_path TEXT,
    FOREIGN KEY(employee_reports_to) REFERENCES employees(employee_id)

);
COPY employees FROM '/home/stazhe/Spiced/logistic-lemongrass-student-code/week_06/data/employees.csv' DELIMITER ',' CSV HEADER;

CREATE TABLE products(
    product_id INT PRIMARY KEY,
    product_name VARCHAR(50),
    supplier_id INT,
    category_id INT,
    quantity_per_unit VARCHAR(50),
    unit_price REAL,
    units_in_stock INT,
    units_on_order INT,
    reorder_level INT,
    discontinued BOOLEAN,
    FOREIGN KEY(supplier_id) REFERENCES suppliers(supplier_id),
    FOREIGN KEY(category_id) REFERENCES categories(category_id)
);
COPY products FROM '/home/stazhe/Spiced/logistic-lemongrass-student-code/week_06/data/products.csv' DELIMITER ',' CSV HEADER;

--CREATE TABLE employee_territories(
--  employee_id INT,
--  territory_id INT,
--  FOREIGN KEY(employee_id) REFERENCES employees(employee_id),
--  FOREIGN KEY(territory_id) REFERENCES territories(territory_id),
	--PRIMARY KEY(employee_id, territory_id)

--);
--COPY categories FROM '/home/stazhe/Spiced/logistic-lemongrass-student-code/week_06/data/categories.csv' DELIMITER ',' CSV HEADER;
