'''
1. Extract data from mongodb
    - connect to the db
     - query the data

2. Transform data
- Sentiment analysis
- possibly we can transform datatypes

3. Load data into postgres
    - connect to postgres
    - insert into postgres

'''
import time
import logging


from pymongo import MongoClient
from sqlalchemy import create_engine

### create connection to mongodb

client = MongoClient(host='mongodb', port=27017)
# the port is the one in the yml file for the container
# host is the name of the container

db_mo = client.twitter
tweets = db_mo.tweets

### create connection to postgres:
# hostname : name of the other container!
db_pg = create_engine('postgres://postgres:1234@postgresdb:5432/postgres', echo=True)
#                   DB type    user     psw  host       port dbname

create_table = """
                CREATE TABLE IF NOT EXISTS tweets (
                user_name TEXT,
                text TEXT,
                sentiment NUMERIC
                );
                """
db_pg.execute(create_table)

def extract_tweets():
    """Extracts tweets from mongodb"""
    # Pull the tweets using .find
    extracted_tweets = list(tweets.find())

    return extracted_tweets


def transform_tweets(extracted_tweets):
    '''Transforms the data'''
    transformed_tweets = []
    for tweet in extracted_tweets:
        sentiment = 1 # Later on we will calculate the Sentiment
        tweet['sentiment'] = sentiment
        transformed_tweets.append(tweet)
    return transformed_tweets


def load(transformed_tweets):
    ''''Loads transformed data into postgres'''
    for tweet in transformed_tweets:

        insert_query = "INSERT INTO tweets VALUES (%s, %s, %s)"
        db_pg.execute(insert_query, (tweet['user_name'], tweet['text'], tweet['sentiment']))
        logging.critical('---- INSERTING TWEET INTO POSTGRES')
        logging.critical(tweet)

while True:
    extracted_tweets = extract_tweets()
    transformed_tweets = transform_tweets(extracted_tweets)
    load(transformed_tweets)
    time.sleep(10)

"""Richt now ETL extracts the whole mongodb db and appends it to  tje tweets
table in postgres. This wil llead to duplicates. We may want to only query the
 newest twqeets from mongo (or load all of the data and replace everything in postgres)
- The first option is better - this is called an incremental Load.
 - There are situations where you prefer the latter, eg. if historical data can change
 How can we do that?
  - can filter the data by a condition .find({condition})
  - can extract timestamp in the tweets
  - for the tweets extracted already, mark them as extracted
  (mongodb  command .update() or .updateMany() and query filtered by the unextracted)

 """
