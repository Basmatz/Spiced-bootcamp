
--Get the names and the quantities in stock for each product.
SELECT "productName", "unitsInStock" FROM products;



--Get a list of current products (Product ID and name).
SELECT "productID", "productName" FROM products;



--Get a list of the most and least expensive products (name and unit price).
SELECT concat(FirstSet."productName", SecondSet."productName"), FirstSet."unitPrice" as maxprice, SecondSet."unitPrice" as minprice

FROM (
        SELECT "productName", "unitPrice"
        FROM products
        WHERE "unitPrice" = (SELECT MAX("unitPrice") FROM products)
    ) as FirstSet

FULL OUTER JOIN (
        SELECT "productName", "unitPrice"
        FROM products
        WHERE "unitPrice" = (SELECT MIN("unitPrice") FROM products)
    ) as SecondSet
ON FirstSet."productName" = SecondSet."productName";




--Get products that cost less than $20.
SELECT "productName", "unitPrice" FROM products
WHERE "unitPrice" < 20;




--Get products that cost between $15 and $25.
SELECT "productName", "unitPrice" FROM products
WHERE "unitPrice" <= 25 AND "unitPrice" >= 15;



--Get products above average price.
SELECT "productName", "unitPrice" as above_AVG_price FROM products
WHERE "unitPrice" > (SELECT AVG("unitPrice") FROM products);


--Find the ten most expensive products.
SELECT "productName", "unitPrice" FROM products
ORDER BY "unitPrice" DESC
LIMIT 10;


--Get a list of discontinued products (Product ID and name).
SELECT "productID", "productName" FROM products
WHERE discontinued = 1;


--Count current and discontinued products.
SELECT count(FirstSet."productName") AS Continued, count(SecondSet."productName") AS Discontinued

FROM (
        SELECT "productName"
        FROM products
        WHERE discontinued = 0
    ) as FirstSet

FULL OUTER JOIN (
        SELECT "productName"
        FROM products
        WHERE discontinued = 1
    ) as SecondSet
ON FirstSet."productName" = SecondSet."productName";



--Find products with less units in stock than the quantity on order.
SELECT "productName", "unitsInStock", "unitsOnOrder"
FROM products
WHERE "unitsOnOrder" > "unitsInStock";



--Find the customer who had the highest order amount
SELECT "customerID", "count"
FROM (
         SELECT "customerID", COUNT("orderID")
         FROM orders
         GROUP BY "customerID"
     ) as subquery
ORDER BY "count" DESC
LIMIT 1;



--Get orders for a given employee and the according customer
SELECT "orderID", "employeeID", "customerID"
FROM orders
WHERE "employeeID" = 1;



--Find the hiring age of each employee
SELECT "employeeID", ("hireDate" - "birthDate") as hireage  FROM employees;



--Create views and/or named queries for some of these queries
