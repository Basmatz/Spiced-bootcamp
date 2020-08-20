-- Get the names and the quantities in stock for each product.

SELECT product_name, quantity_per_unit, unitis_in_stock
FROM products
WHERE unitis_in_stock >0 ;

-- Get a list of current products (Product ID and name)

SELECT product_name, product_id
FROM products ;

--Get a list of the most and least expensive products (name and unit price).

-- the 10 most expensive products

SELECT product_name, unit_price
FROM products
ORDER BY unit_price DESC
LIMIT 10;

-- the 10 least expensive products

SELECT product_name, unit_price
FROM products
ORDER BY unit_price
LIMIT 10;

-- Get products that cost less than $20

SELECT product_name, unit_price
FROM products
WHERE unit_price < 20
GROUP BY product_name, unit_price
ORDER BY unit_price DESC;

-- Get products that cost between $15 and $25

SELECT product_name, unit_price
FROM products
WHERE unit_price BETWEEN 15 AND 20
GROUP BY product_name, unit_price
ORDER BY unit_price DESC;

-- Get products above average price.

SELECT product_name, unit_price
FROM products
WHERE unit_price > (SELECT AVG(unit_price) FROM products)
ORDER BY unit_price;

-- Find the ten most expensive products.

SELECT product_name, unit_price
FROM products
ORDER BY unit_price DESC
LIMIT 10;

-- Get a list of discontinued products (Product ID and name).

SELECT product_id, product_name
FROM products
WHERE discontinued > 0 ;

-- Count current and discontinued products.

SELECT SUM(case when discontinued = '0' then 1 else 0 end) as current_Count,
SUM(case when discontinued = '0' then 0 else 1 end) as disc_Count
FROM products;

-- Find products with less units in stock than the quantity on order.


-- Find the customer who had the highest order amount

-- Get orders for a given employee and the according customer

-- Find the hiring age of each employee

-- Create views and/or named queries for some of these queries
