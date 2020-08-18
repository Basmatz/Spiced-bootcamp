DROP TABLE IF EXISTS cities;
-- Drop table if it already exists

CREATE TABLE cities (
  id SERIAL PRIMARY KEY, -- name, datatype, constraints, PK = unique!
  name VARCHAR (50),
  population INTEGER,
  country VARCHAR(50)
);

INSERT INTO cities (name, population,  country)
VALUES ('Berlin', 38000000, 'Germany');
INSERT INTO cities (name, population,  country)
VALUES ('Paris', 80000000, 'France');
INSERT INTO cities (name, population,  country)
VALUES ('New York City', 1200000000, 'USA');
