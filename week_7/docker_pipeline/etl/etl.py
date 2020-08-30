'''
1. Extract data from MongoDB
- Connect to the database
- Query the data

2. Transform the data
- Sentiment Analysis (will see this in the afternoon)
- Possibly we could transform datatypes

3. Load it into Postgres
- Connect to postgres
- Insert Into postgres
'''

import time
import logging

from pymongo import MongoClient
from sqlalchemy import create_engine
import psycopg2
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

# Connect to MongoDB (1. database)
client = MongoClient(host='mongodb', port=27017)
db_mongo = client.twitter
tweets = db_mongo.tweets

# Connect to Postgres (2. datavase)

db_pg = create_engine('postgres://postgres:1234@postgresdb:5432/postgres', echo=True)
#                   DB type    user     psw  host       port dbname

#create table in the 2. database

create_table = """
                CREATE TABLE IF NOT EXISTS tweets (
                user_name TEXT,
                text TEXT,
                sentiment NUMERIC
                );
               """

db_pg.execute(create_table)
 # sentiment analyser

analyzer = SentimentIntensityAnalyzer()

def extract():
    '''Extracts tweets from the MongoDB database'''

    extracted_tweets = list(tweets.find({'extracted': 'no'}))

    db_mongo.tweets.update_many({'extracted': 'no'}, {'$set':{'extracted': 'yes'}})

    return extracted_tweets

def sentiment_analyzer(tweet):
    sentiment= analyzer.polarity_scores(tweet)
    return sentiment['compound']  # compound is the weighted normalized result of each 3 values (negative,neutral,positive )

def transform(extracted_tweets):
    '''Transforms the data'''
    transformed_tweets = []
    for tweet in extracted_tweets:
        sentiment = sentiment_analyzer(tweet['text'])
        tweet['sentiment'] = sentiment
        transformed_tweets.append(tweet)

    return transformed_tweets

def load(transformed_tweets):
    '''Load transformed data into the postgres database'''
    for tweet in transformed_tweets:
        insert_query = "INSERT INTO tweets VALUES (%s, %s, %s)"
        db_pg.execute(insert_query, (tweet['user_name'], tweet['text'], tweet['sentiment']))
        logging.critical('---Inserted a new tweet into postgres---')
        logging.critical(tweet)


while True:
    extracted_tweets = extract()
    transformed_tweets = transform(extracted_tweets)
    load(transformed_tweets)
    time.sleep(10)
