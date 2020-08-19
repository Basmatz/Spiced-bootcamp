DROP TABLE IF EXISTS categories;
DROP TABLE IF EXISTS customers;
DROP TABLE IF EXISTS employee_territories;
DROP TABLE IF EXISTS employees;
DROP TABLE IF EXISTS order_details;
DROP TABLE IF EXISTS orders;
DROP TABLE IF EXISTS products;
DROP TABLE IF EXISTS regions;
DROP TABLE IF EXISTS shippers;
DROP TABLE IF EXISTS suppliers;
DROP TABLE IF EXISTS territories;



CREATE TABLE categories (
    category_id SMALLINT NOT NULL,
    category_name VARCHAR(50) NOT NULL,
    description TEXT,
    picture BYTEA
);

\COPY categories FROM 'C:\Users\Kriszta\Desktop\GitHub-Spiced\logistic-lemongrass-student-code\week_6\northwind\categories.csv' DELIMITER ',' CSV HEADER;


CREATE TABLE customers (
    customer_id VARCHAR(15) NOT NULL,
    company_name VARCHAR(50),
    contact_name VARCHAR(40),
    contact_title VARCHAR(40),
    address VARCHAR(50),
    city VARCHAR(20),
    region VARCHAR(20),
    postal_code VARCHAR(15),
    country VARCHAR(20),
    phone VARCHAR(20),
    fax VARCHAR(20)
);

\COPY customers FROM 'C:\Users\Kriszta\Desktop\GitHub-Spiced\logistic-lemongrass-student-code\week_6\northwind\customers.csv' DELIMITER ',' CSV HEADER;

CREATE TABLE employee_territories (
    employee_id  SMALLINT NOT NULL,
    territory_id  VARCHAR(20) NOT NULL
);

\COPY employee_territories FROM 'C:\Users\Kriszta\Desktop\GitHub-Spiced\logistic-lemongrass-student-code\week_6\northwind\employee_territories.csv' DELIMITER ',' CSV HEADER;


CREATE TABLE employees (
    employee_id SMALLINT NOT NULL,
    last_name VARCHAR(20) NOT NULL,
    first_name VARCHAR(20) NOT NULL,
    title VARCHAR(30),
    title_of_courtesy VARCHAR(20),
    birt_date DATE,
    hire_date DATE,
    address VARCHAR(50),
    city VARCHAR(40),
    region VARCHAR(10),
    postal_code VARCHAR(15),
    country VARCHAR(20),
    home_phone VARCHAR(15),
    extenstion VARCHAR(6),
    photo BYTEA,
    notes TEXT,
    report_to VARCHAR(6),
    photo_path VARCHAR(50)
);

\COPY employees FROM 'C:\Users\Kriszta\Desktop\GitHub-Spiced\logistic-lemongrass-student-code\week_6\northwind\employees.csv' DELIMITER ',' CSV HEADER;

CREATE TABLE order_details (
    order_id SMALLINT NOT NULL,
    product_id SMALLINT NOT NULL,
    unit_price REAL NOT NULL,
    quantity SMALLINT NOT NULL,
    discount REAL NOT NULL
);

\COPY order_details FROM 'C:\Users\Kriszta\Desktop\GitHub-Spiced\logistic-lemongrass-student-code\week_6\northwind\order_details.csv' DELIMITER ',' CSV HEADER;

CREATE TABLE orders (
    order_id SMALLINT NOT NULL,
    customer_id TEXT,
    employee_id SMALLINT ,
    order_data DATE,
    required_date DATE,
    shipped_date VARCHAR(25),
    ship_via SMALLINT,
    freight REAL,
    ship_name VARCHAR(50),
    ship_address VARCHAR(60),
    ship_city VARCHAR(20),
    ship_region VARCHAR(15),
    ship_postal_code VARCHAR(15),
    ship_country TEXT
);

\COPY orders FROM 'C:\Users\Kriszta\Desktop\GitHub-Spiced\logistic-lemongrass-student-code\week_6\northwind\orders.csv' DELIMITER ',' CSV HEADER;

CREATE TABLE products (
    product_id SMALLINT NOT NULL,
    product_name VARCHAR(40),
    supplier_id SMALLINT,
    category_id SMALLINT,
    quantity_per_unit VARCHAR(30),
    unit_price REAL,
    unitis_in_stock SMALLINT,
    units_on_order SMALLINT,
    reorder_level SMALLINT,
    discontinued SMALLINT
);

\COPY products FROM 'C:\Users\Kriszta\Desktop\GitHub-Spiced\logistic-lemongrass-student-code\week_6\northwind\products.csv' DELIMITER ',' CSV HEADER;

CREATE TABLE regions (
    region_id SMALLINT NOT NULL,
    region_description TEXT
);

\COPY regions FROM 'C:\Users\Kriszta\Desktop\GitHub-Spiced\logistic-lemongrass-student-code\week_6\northwind\regions.csv' DELIMITER ',' CSV HEADER;

CREATE TABLE shippers (
  shipper_id SMALLINT NOT NULL,
  company_name VARCHAR(50) NOT NULL,
  phone VARCHAR(25)
);

\COPY shippers FROM 'C:\Users\Kriszta\Desktop\GitHub-Spiced\logistic-lemongrass-student-code\week_6\northwind\shippers.csv' DELIMITER ',' CSV HEADER;

CREATE TABLE suppliers (
    supplier_id SMALLINT NOT NULL,
    company_name VARCHAR(100) NOT NULL,
    contact_name VARCHAR(40),
    contact_title VARCHAR(40),
    address VARCHAR(50),
    city VARCHAR(20),
    region VARCHAR(10),
    postal_code VARCHAR(15),
    country VARCHAR(20),
    phone VARCHAR(15),
    fax VARCHAR(15),
    home_phone VARCHAR(120)
);

\COPY suppliers FROM 'C:\Users\Kriszta\Desktop\GitHub-Spiced\logistic-lemongrass-student-code\week_6\northwind\suppliers.csv' DELIMITER ',' CSV HEADER;

CREATE TABLE territories (
    territory_id VARCHAR(10) NOT NULL,
    territory_description VARCHAR(20),
    region_id SMALLINT NOT NULL
);

\COPY territories FROM 'C:\Users\Kriszta\Desktop\GitHub-Spiced\logistic-lemongrass-student-code\week_6\northwind\territories.csv' DELIMITER ',' CSV HEADER;
