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

SELECT pr.product_name, o.quantity, pr.unitis_in_stock
FROM order_details AS o
JOIN products AS pr
ON o.product_id = pr.product_id
WHERE pr.unitis_in_stock < o.quantity;

-- Find the customer who had the highest order amount
WITH subquery AS(
SELECT *, CASE WHEN discount = 0 THEN (unit_price*quantity)
               ELSE (unit_price*quantity*discount) END AS price
FROM order_details
ORDER BY price DESC)

SELECT o.order_id, o.customer_id, o.ship_name, sq.price
FROM orders AS o
JOIN subquery AS sq
ON sq.order_id = o.order_id
LIMIT 1;

-- Get orders for a given employee and the according customer

WITH t1 AS ( WITH subquery AS (
                               SELECT *, CASE WHEN discount = 0 THEN (unit_price*quantity)
                               ELSE (unit_price*quantity*discount) END AS price
                               FROM order_details
                               ORDER BY price DESC)

             SELECT o.order_id, o.customer_id, o.ship_name, sq.price, o.employee_id
             FROM orders AS o
             JOIN subquery AS sq
             ON sq.order_id = o.order_id
             LIMIT 1 )

SELECT o.customer_id,o.ship_name, o.order_id, o.employee_id
FROM orders AS o
JOIN t1
ON t1.employee_id = o.employee_id
WHERE t1.customer_id= o.customer_id;

-- Find the hiring age of each employee

WITH t1 AS ( SELECT DATE_PART('year', hire_date) AS hire_year,
			DATE_PART('year', birt_date) AS birth_year,
			employee_id
FROM employees)

SELECT e.last_name, e.first_name , (hire_year - birth_year) AS hiring_age
FROM employees AS e
JOIN t1
ON t1.employee_id = e.employee_id;

-- Create views and/or named queries for some of these queries

CREATE VIEW best_customer_view AS
WITH subquery AS(
SELECT *, CASE WHEN discount = 0 THEN (unit_price*quantity)
               ELSE (unit_price*quantity*discount) END AS price
FROM order_details
ORDER BY price DESC)

SELECT o.order_id, o.customer_id, o.ship_name, sq.price
FROM orders AS o
JOIN subquery AS sq
ON sq.order_id = o.order_id;

CREATE VIEW products_not_enough_in_stock AS
SELECT pr.product_name, o.quantity, pr.unitis_in_stock
FROM order_details AS o
JOIN products AS pr
ON o.product_id = pr.product_id
WHERE pr.unitis_in_stock < o.quantity;
