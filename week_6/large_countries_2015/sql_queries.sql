-- Create Table
CREATE TABLE countries (
    country VARCHAR(100),
    population REAL,
    fertility REAL,
    continent VARCHAR(25)
);


-- Fill the table

\COPY countries FROM 'C:\Users\Kriszta\Desktop\GitHub-Spiced\logistic-lemongrass-encounter-notes\week_06\large_countries_2015.csv' DELIMITER ',' CSV HEADER;

-- can alter your TABLE

ALTER TABLE countries
ALTER COLUMN population TYPE INTEGER;

-- SELECT
-- Select all values
SELECT * FROM countries


-- Select only the columns country and population

SELECT country, population FROM countries;

-- Select the distinct continents - will give back the unique values

SELECT DISTINCT continent
FROM countries;

-- what if I was only interested in Asian countries, but I wanted to have all information on that

SELECT *
FROM countries
WHERE continent = 'Asia';


-- Select only the columns country and population and order by population size

SELECT country, population
FROM countries
ORDER BY population DESC;

-- if whant to have only Asian countries

SELECT country, population
FROM countries
WHERE continent= ' Asia'
ORDER BY population;

--  Select all countries with more than 200,000,000 inhabitants


-- Select the three countries with the highest fertility rate

SELECT countries, fertility
FROM countries
ORDER BY fertility DESC
LIMIT 3;


-- Select all countries which start with "I"

SELECT country
FROM countries
WHERE country like 'I%' ;


-- Select all countries which start with "I" and have more than 200,000,000 inhabitants

SELECT country
FROM countries
WHERE country like 'I%' AND population > 200000000;

-- Show the average population by continent

SELECT continent, AVG(population)
FROM countries
GROUP BY continent;

-- Show the average population by continent if it exceeds 300,000,000
-- applying a condition on a group by table, you have to use HAVING

SELECT continent, AVG(population)
FROM countries
GROUP BY continent
HAVING AVG(population) > 300000000;


-- can use subqueries

SELECT *
FROM (SELECT continent, AVG(population) as average_population
      FROM countries
      GROUP BY continent) AS subquery
WHERE average_population > 300000000;

-- other way to do a subquery

WITH subquery AS (
      SELECT continent, AVG(population) as average_population
      FROM countries
      GROUP BY continent)
SELECT *
FROM subquery
WHERE average_population > 300000000;


-- Update South America and North America to The Americas

-- CASE besically is a if statment in SQL
-- only see the new column when run this query

SELECT country,
       CASE
          WHEN continent = 'North America' THEN 'The Americas'
          WHEN continent = 'South America' THEN 'The Americas'
          ELSE continent
       END as updated_continent
FROM countries;

-- we want to make this change permanent
UPDATE TABLE countries
SET continent = CASE
                   WHEN continent = 'North America' THEN 'The Americas'
                   WHEN continent = 'South America' THEN 'The Americas'
                   ELSE continent
              END;


SELECT *
FROM countries;

-- Add a new column

ALTER TABLE countries
ADD COLUMN new_column INTEGER DEFAULT 1;

SELECT *
FROM countries;

-- Delete rows from a table

DELETE FROM countries
WHERE continent IS NULL;

-- where continent = 'Asia' - can any condition

-- Delete all entries from a table

TRUNCATE TABLE countries;

SELECT *
FROM countries;

-- now it is emply, just have the columns name

-- Delete whole database table

DROP TABLE countries;

-- Delete whole database

DROP DATABASE countries;
