import pandas as pd
import numpy as np
import sqlalchemy
from sqlalchemy import create_engine
import psycopg2


# import data

HOST = ''# ENTER CONNECTION LINK HERE
PORT = '5432'
USER = 'postgres'
PASSWORD = '1234' # ENTER PASSWORD
DATABASE = 'movieratings'

conn = f'postgres://{USER}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}'

create_tables_query = '''
DROP TABLE IF EXISTS movies;
DROP TABLE IF EXISTS ratings;
DROP TABLE IF EXISTS links;

CREATE TABLE movies (
movieid SERIAL PRIMARY KEY,
title VARCHAR(250),
genres VARCHAR(150)
);

CREATE TABLE links (
movieid SERIAL PRIMARY KEY,
imdbid VARCHAR(10),
tmdbid BIGINT
);

'''

# CREATE TABLE ratings (
# userid SMALLINT PRIMARY KEY,
# movieid BIGINT,
# rating REAL
# );

ratings = pd.read_csv('/Users/laraehrenhofer/Documents/Spiced_Academy/Course_Notes/Week_10/ml-latest-small/ratings.csv')

ratings = ratings.drop('timestamp', axis = 1)

create_movies = '''COPY movies FROM '/Users/laraehrenhofer/Documents/Spiced_Academy/Course_Notes/Week_10/ml-latest-small/movies.csv' DELIMITER ',' CSV HEADER;'''

create_links = '''COPY links FROM '/Users/laraehrenhofer/Documents/Spiced_Academy/Course_Notes/Week_10/ml-latest-small/links.csv' DELIMITER ',' CSV HEADER;'''


if __name__ == '__main__':

    engine = create_engine(conn, encoding = 'latin1', echo= False)
    print('created engine')

    engine.execute(create_tables_query)
    print('created tables')

    engine.execute(create_movies)
    print('created movies table')

    ratings.to_sql('ratings', engine, if_exists='append')

    engine.execute(create_links)
    print('created links table')

















#
