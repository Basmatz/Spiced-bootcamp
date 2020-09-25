DROP TABLE IF EXISTS movies;
DROP TABLE IF EXISTS ratings;

CREATE TABLE movies (
  movieId INTEGER,
  title TEXT,
  genres TEXT

);

CREATE TABLE ratings (
  userId INTEGER,
  movieId INTEGER,
  rating TEXT,
  ts VARCHAR(20)

);


--COPY order_details (orderID, productID, unitPrice, quantity, discount) FROM '/Users/rjt.weber/Documents/Work/SPICED/repo/logistic-lemongrass-student-code/week_06/data/order_details.csv' DELIMITER ',' CSV HEADER NULL 'NULL';
COPY movies FROM '/Users/rjt.weber/Documents/Work/SPICED/repo/logistic-lemongrass-student-code/week_10/data_100k/movies.csv' DELIMITER ',' CSV HEADER;
COPY ratings (userId, movieId, rating, ts) FROM '/Users/rjt.weber/Documents/Work/SPICED/repo/logistic-lemongrass-student-code/week_10/data_100k/ratings.csv' DELIMITER ',' CSV HEADER;
