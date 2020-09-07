DROP TABLE IF EXISTS categories;
CREATE TABLE categories (
  categoryID SERIAL PRIMARY KEY,
  categoryName VARCHAR(100) NOT NULL,
  description VARCHAR(80),
  picture VARCHAR(300)
);
\copy categories  FROM 'C:/Users/oztur/OneDrive/MASAST~1/esra/github/LOGIST~1/week06/NORTHW~1/data/categories.csv' DELIMITER ',' CSV HEADER;

DROP TABLE IF EXISTS customers;
CREATE TABLE customers (
  customerID SERIAL PRIMARY KEY,
  companyName VARCHAR(100) NOT NULL,
  contactName varchar(100),
  contactTitle VARCHAR(30),
  address VARCHAR(150),
  city VARCHAR(80),
  region VARCHAR(80),
  postalCode VARCHAR(10),
  country VARCHAR(100),
  phone VARCHAR(15),
  fax VARCHAR(15)
);
\copy customers  FROM 'C:/Users/oztur/OneDrive/MASAST~1/esra/github/LOGIST~1/week06/NORTHW~1/data/customers.csv' DELIMITER ',' CSV HEADER;

DROP TABLE IF EXISTS employee_territories ;
CREATE TABLE employee_territories (
employeeID SERIAL PRIMARY KEY,
territoryID varchar(12)
);

\copy employee_territories  FROM 'C:/Users/oztur/OneDrive/MASAST~1/esra/github/LOGIST~1/week06/NORTHW~1/data/employee_territories.csv' DELIMITER ',' CSV HEADER;


DROP TABLE IF EXISTS employees;
CREATE TABLE employees (
employeeID SERIAL PRIMARY KEY,
lastName VARCHAR(80),
firstName VARCHAR(80),
title VARCHAR(80),
titleOfCourtesy,
birthDate,hireDate,
address VARCHAR(150),
city VARCHAR(80),
region VARCHAR(80),
postalCode VARCHAR(10),
country VARCHAR(80),
homePhone  VARCHAR(15),
extension VARCHAR(5),
photo VARCHAR(150),
notes VARCHAR(15),
reportsTo VARCHAR(15),
photoPath VARCHAR(15)
);
\copy employees  FROM 'C:/Users/oztur/OneDrive/MASAST~1/esra/github/LOGIST~1/week06/NORTHW~1/data/employees.csv' DELIMITER ',' CSV HEADER;

DROP TABLE IF EXISTS order_details;
CREATE TABLE order_details (
orderID INTEGER(5) PRIMARY KEY,
productID INTEGER(2),
unitPrice NUMERIC(5,2),
quantity INTEGER(3),
discount NUMERIC(5,2)
);
\copy order_details  FROM 'C:/Users/oztur/OneDrive/MASAST~1/esra/github/LOGIST~1/week06/NORTHW~1/data/order_details.csv' DELIMITER ',' CSV HEADER;

DROP TABLE IF EXISTS orders;
CREATE TABLE orders (
orderID,
customerID,
employeeID,
orderDate,
requiredDate,
shippedDate,
shipVia,
freight,
shipName,
shipAddress,
shipCity,
shipRegion,
shipPostalCode,
shipCountry
);
\copy orders  FROM 'C:/Users/oztur/OneDrive/MASAST~1/esra/github/LOGIST~1/week06/NORTHW~1/data/orders.csv' DELIMITER ',' CSV HEADER;


DROP TABLE IF EXISTS products;
CREATE TABLE products (
productID,
productName,
supplierID,
categoryID,
quantityPerUnit,
unitPrice,
unitsInStock,
unitsOnOrder,
reorderLevel,
discontinued
);
\copy products  FROM 'C:/Users/oztur/OneDrive/MASAST~1/esra/github/LOGIST~1/week06/NORTHW~1/data/products.csv' DELIMITER ',' CSV HEADER;


DROP TABLE IF EXISTS regions;
CREATE TABLE regions (
regionID,
regionDescription
);
\copy regions  FROM 'C:/Users/oztur/OneDrive/MASAST~1/esra/github/LOGIST~1/week06/NORTHW~1/data/regions.csv' DELIMITER ',' CSV HEADER;


DROP TABLE IF EXISTS shippers;
CREATE TABLE shippers (
shipperID SERIAL PRIMARY KEY,
companyName VARCHAR(100) NOT NULL,
phone VARCHAR(15)
);
\copy shippers  FROM 'C:/Users/oztur/OneDrive/MASAST~1/esra/github/LOGIST~1/week06/NORTHW~1/data/shippers.csv' DELIMITER ',' CSV HEADER;


DROP TABLE IF EXISTS suppliers;
CREATE TABLE suppliers (
supplierID,
companyName VARCHAR(100) NOT NULL,
contactName,
contactTitle,
address,
city,
region,
postalCode INTEGER (5),
country,
phone VARCHAR(15),
fax VARCHAR(15),
homePage
);
\copy suppliers FROM 'C:/Users/oztur/OneDrive/MASAST~1/esra/github/LOGIST~1/week06/NORTHW~1/data/suppliers.csv' DELIMITER ',' CSV HEADER;

DROP TABLE IF EXISTS territories;
CREATE TABLE territories (
territoryID,
territoryDescription,
regionID);
\copy territories FROM 'C:/Users/oztur/OneDrive/MASAST~1/esra/github/LOGIST~1/week06/NORTHW~1/data/territories.csv' DELIMITER ',' CSV HEADER;


