'''
1. Extract data from MongoDB
- Connect to mongodb

2. Transform the data
- sentiment analysis

3. Load into PostgresDB
- Connect to postgresdb

'''

import time
import logging

from pymongo import MongoClient
from sqlalchemy import create_engine
from GerVADER.vaderSentimentGER import SentimentIntensityAnalyzer
import psycopg2


# connect to mongodb database
client = MongoClient(host = 'navalny_mongo', port = 27017)
db = client.twitter_navalny
tweets = db.tweets_navalny

## connect to postgres database
db_pg = create_engine('postgres://postgres:1234@navalny_postgres:5432/postgres', echo = True)

## create table in postgres
create_table = '''CREATE TABLE IF NOT EXISTS tweets_navalny_pg (
user_name VARCHAR(50),
tweet_text TEXT,
sentiment REAL
);
'''

db_pg.execute(create_table)

# initialise sentiment analyser
GERanalyzer = SentimentIntensityAnalyzer()

def extract():
    '''Extract tweets from MongoDB database'''
    # pull previously un-extracted tweets out of mongodb database
    extracted_tweets = list(tweets.find({'extracted': false}))

    # mark these tweets as extracted: add a new field "extracted" with value true to the existing tweets
    db.tweets_navalny.update({}, {$set: {'extracted': true}}, false, true)
    return extracted_tweets

def analyse_sentiment(tweet):
    sentiment = GERanalyzer.polarity_scores(tweet)
    return sentiment['compound']

def transform(extracted_tweets):
    '''Transform data and return sentiment analysis'''
    transformed_tweets = []
    for tweet in extracted_tweets:
        sentiment = analyse_sentiment(tweet)
        # datatype of the tweet: dictionary; add sentiment to dictionary
        tweet['sentiment'] = sentiment
        transformed_tweets.append
    return transformed_tweets

def load(transformed_tweets):
    '''Load transformed data into postgres database'''
    for tweet in transformed_tweets:
        insert_query = "INSERT INTO tweets_navalny_pg VALUES (%s, %s, %s, %s, %s, %s);" # %s notation is placeholder, which we'll pass in below; more robust for handling quotation marks in tweet texts
        db_pg.execute(insert_query, (tweet['user_name'], tweet['tweet_text'], tweet['sentiment'], tweet['timestamp'], tweet['was_retweeted'], tweet['place']))
        logging.critical('---Inserting new tweet into postgres---')
        logging.critical(tweet)

while True:
    extracted_tweets = extract()
    transformed_tweets = transform(extracted_tweets)
    load(transformed_tweets)
    time.sleep(10) # wait time in case the rate of tweeting is slow and there are no tweets to process by the time the current run is done


'''
Currently the ETL job extracts the entire mongodb database in each run and appends the tweets to the table in postgres.
This will lead to a lot of duplicates!

So we want to either query only recent tweets (more efficient/elegant; 'incremental loading'), or replace all of the data each time.

If you're considering cases where the historical data changes, you might want to consider the full load.
- filter data in query: .find({condition})
- findOne()
- find the last 100.
- find tweets from the last 5 mins (timestamp in data)
- for tweets that have been extracted already, mark as extracted .update() or updateMany(), then query only the ones that have been extracted yet
'''
