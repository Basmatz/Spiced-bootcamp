DROP TABLE IF EXISTS movies;
DROP TABLE IF EXISTS ratings;
DROP TABLE IF EXISTS tags;
DROP TABLE IF EXISTS links;



CREATE TABLE movies (
    movie_id INTEGER NOT NULL,
    title VARCHAR(300) NOT NULL,
    genres VARCHAR(200)

);

\COPY movies FROM 'C:\Users\Kriszta\Desktop\GitHub-Spiced\logistic-lemongrass-student-code\week_10\movies\ml-latest-small_movies.csv' DELIMITER ',' CSV HEADER;


CREATE TABLE ratings (
    user_id SMALLINT NOT NULL,
    movie_id INTEGER NOT NULL,
    rating REAL,
    timestamp INTEGER
);

\COPY ratings FROM 'C:\Users\Kriszta\Desktop\GitHub-Spiced\logistic-lemongrass-student-code\week_10\movies\ml-latest-small_ratings.csv' DELIMITER ',' CSV HEADER;

CREATE TABLE tags (
    user_id SMALLINT NOT NULL,
    movie_id INTEGER NOT NULL,
    tag VARCHAR(200),
    timestamp INTEGER
);

\COPY tags FROM 'C:\Users\Kriszta\Desktop\GitHub-Spiced\logistic-lemongrass-student-code\week_10\movies\ml-latest-small_tags.csv' DELIMITER ',' CSV HEADER;


CREATE TABLE links (
    movie_id INTEGER NOT NULL,
    imdb_id  INTEGER,
    tmdb_id  REAL
);

\COPY links FROM 'C:\Users\Kriszta\Desktop\GitHub-Spiced\logistic-lemongrass-student-code\week_10\movies\ml-latest-small_links.csv' DELIMITER ',' CSV HEADER;
