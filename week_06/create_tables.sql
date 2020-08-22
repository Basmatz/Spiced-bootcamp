DROP TABLE IF EXISTS customers;
DROP TABLE IF EXISTS categories;
DROP TABLE IF EXISTS regions;
DROP TABLE IF EXISTS employee_territories;
DROP TABLE IF EXISTS employees;
DROP TABLE IF EXISTS order_details;
DROP TABLE IF EXISTS orders;
DROP TABLE IF EXISTS products;
DROP TABLE IF EXISTS shippers;
DROP TABLE IF EXISTS suppliers;
DROP TABLE IF EXISTS territories;



CREATE TABLE customers (
  customerID VARCHAR(50) Primary Key,
  companyName VARCHAR(50),
  contactName VARCHAR(50),
  contactTitle VARCHAR(50),
  address VARCHAR(50),
  city VARCHAR(50),
  region VARCHAR(50),
  postalCode VARCHAR(50),
  country VARCHAR(50),
  phone VARCHAR(50),
  tax VARCHAR(50)
);

CREATE TABLE categories (
  categoryID Integer Primary Key,
  categoryName VARCHAR(50),
  description VARCHAR(256),
  picture BYTEA
);

CREATE TABLE regions (
  regionID Integer Primary Key,
  regionDescription VARCHAR(50)
);

CREATE TABLE employee_territories (
  id Serial Primary Key,
  employeeID Integer,
  territoryID Integer
);

CREATE TABLE employees (
  employeeID Integer Primary Key,
  lastName VARCHAR(50),
  firstName VARCHAR(50),
  title VARCHAR(50),
  titleOfCourtesy VARCHAR(10),
  birthDate Date,
  hireDate Date,
  address VARCHAR(50),
  city VARCHAR(50),
  region VARCHAR(50),
  postalCode VARCHAR(50),
  country VARCHAR(50),
  homePhone VARCHAR(50),
  extension Integer,
  photo BYTEA,
  notes VARCHAR(256),
  reportsTo Integer,
  photoPath VARCHAR(256)

);


CREATE TABLE order_details (
  id Serial Primary Key,
  orderID Integer,
  productID Integer,
  unitPrice Double Precision,
  quantity Integer,
  discount Double Precision

);

CREATE TABLE orders (
  orderID Integer Primary Key,
  customerID VARCHAR(50),
  employeeID Integer,
  orderDate Date,
  requiredDate Date,
  shippedDate Date,
  shipVia Integer,
  freight Double Precision,
  shipName VARCHAR(50),
  shipAddress VARCHAR(50),
  shipCity VARCHAR(50),
  shipRegion VARCHAR(50),
  shipPostalCode VARCHAR(50),
  shipCountry VARCHAR(50)
);

CREATE TABLE products (
  productID Integer Primary Key,
  productName VARCHAR(50),
  supplierID Integer,
  categoryID Integer,
  quantityPerUnit VARCHAR(50),
  unitPrice VARCHAR(50),
  unitsInStock Integer,
  unitsOnOrder Integer,
  reorderLevel Integer,
  discontinued Integer

);

CREATE TABLE shippers (
  shipperID Integer Primary Key,
  companyName VARCHAR(50),
  phone VARCHAR(50)
);

CREATE TABLE suppliers (
  supplierID Integer Primary Key,
  companyName VARCHAR(50),
  contactName VARCHAR(50),
  contactTitle VARCHAR(50),
  address VARCHAR(50),
  city VARCHAR(50),
  region VARCHAR(50),
  postalCode VARCHAR(50),
  country VARCHAR(50),
  phone VARCHAR(50),
  fax VARCHAR(50),
  homePage VARCHAR(256)
);

CREATE TABLE territories (
  territoryID Integer,
  territoryDescription VARCHAR(50),
  regionID Integer

);

COPY order_details (orderID, productID, unitPrice, quantity, discount) FROM '/Users/rjt.weber/Documents/Work/SPICED/repo/logistic-lemongrass-student-code/week_06/data/order_details.csv' DELIMITER ',' CSV HEADER NULL 'NULL';
COPY employees FROM '/Users/rjt.weber/Documents/Work/SPICED/repo/logistic-lemongrass-student-code/week_06//data/employees.csv' DELIMITER ',' CSV HEADER NULL 'NULL';
COPY customers FROM '/Users/rjt.weber/Documents/Work/SPICED/repo/logistic-lemongrass-student-code/week_06/data/customers.csv' DELIMITER ',' CSV HEADER NULL 'NULL';
COPY categories FROM '/Users/rjt.weber/Documents/Work/SPICED/repo/logistic-lemongrass-student-code/week_06/data/categories.csv' DELIMITER ',' CSV HEADER NULL 'NULL';
COPY regions FROM '/Users/rjt.weber/Documents/Work/SPICED/repo/logistic-lemongrass-student-code/week_06/data/regions.csv' DELIMITER ',' CSV HEADER NULL 'NULL';
COPY employee_territories (employeeID, territoryID) FROM '/Users/rjt.weber/Documents/Work/SPICED/repo/logistic-lemongrass-student-code/week_06/data/employee_territories.csv' DELIMITER ',' CSV HEADER NULL 'NULL';
COPY orders FROM '/Users/rjt.weber/Documents/Work/SPICED/repo/logistic-lemongrass-student-code/week_06/data/orders.csv' DELIMITER ',' CSV HEADER NULL 'NULL';
COPY products FROM '/Users/rjt.weber/Documents/Work/SPICED/repo/logistic-lemongrass-student-code/week_06/data/products.csv' DELIMITER ',' CSV HEADER NULL 'NULL';
COPY shippers FROM '/Users/rjt.weber/Documents/Work/SPICED/repo/logistic-lemongrass-student-code/week_06/data/shippers.csv' DELIMITER ',' CSV HEADER NULL 'NULL';
COPY suppliers FROM '/Users/rjt.weber/Documents/Work/SPICED/repo/logistic-lemongrass-student-code/week_06/data/suppliers.csv' DELIMITER ',' CSV HEADER NULL 'NULL';
COPY territories FROM '/Users/rjt.weber/Documents/Work/SPICED/repo/logistic-lemongrass-student-code/week_06/data/territories.csv' DELIMITER ',' CSV HEADER NULL 'NULL';
