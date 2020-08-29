#!/usr/bin/env python3
"""
Created on Fri 28 Aug 2020


This script scrapes tweets on a specific keyword.
This version is in German and non-geo-specific.

"""


import credentials
import tweepy
from tweepy import OAuthHandler
import pandas as pd
from datetime import timedelta
import pymongo
from pymongo import MongoClient
import json
import logging
import time
from tqdm import tqdm
import cardinality

client = pymongo.MongoClient(host = 'navalny_mongo', port = 27017)
navalnytweet_db = client.navalny_db
mongo_tweets = navalnytweet_db.tweet


# set up authorisation keys: must retrieve from separate file or risk privacy breach
# in auth.k, oder of info: customer key, customer secret, access key, access secret
def authenticate():
    """Function for handling Twitter Authentication. Please note
       that this script assumes you have a file called config.py
       which stores the 4 required authentication tokens:

       1. CONSUMER_API_KEY
       2. CONSUMER_API_SECRET
       3. ACCESS_TOKEN
       4. ACCESS_TOKEN_SECRET

    See course material for instructions on getting your own Twitter credentials.
    """
    auth = OAuthHandler(credentials.consumer_key, credentials.consumer_secret)
    auth.set_access_token(credentials.access_token, credentials.access_token_secret)

    return auth

query = 'navalny OR nawalny' + '-filter:retweets'

tweets_processed_for_db = []

# start = pd.to_datetime("2020-08-22", format = '%Y-%m-%d')
end = pd.to_datetime("2020-08-27", format = '%Y-%m-%d')

def get_tweets(end):
    '''
    gets tweets with a specific time range (start - end); returns n number of tweets
    '''
    api = tweepy.API(auth)
    tweets = tweepy.Cursor(api.search, q=query, lang = 'de', until=str(end), wait_on_rate_limit=True, wait_on_rate_limit_notify = True, count = 50).items(50)
    logging.critical(f'logging type of tweets within get_tweets: {type(tweets)}')


    return tweets

#

def tweet_to_json(tweet):
    '''
    re-processes tweet into json format
    '''

    if 'extended_tweet' in tweet._json:
        text =  tweet._json['extended_tweet']['full_text']
    else:
        text = tweet._json['text']

    if 'retweeted_status' in tweet._json:
        r = tweet._json['retweeted_status']
        if 'extended_tweet' in r:
            text =  r['extended_tweet']['full_text']

    if 'RT ' in text:
        was_retweeted = True
    else:
        was_retweeted = False

    tweet_processed = {
        'text': text,
        'username': tweet._json['user']['screen_name'],
        'followers_count': tweet._json['user']['followers_count'],
        'was_retweeted' : was_retweeted,
        'extracted' : 'no',
        'timestamp' : tweet._json['created_at'],
        'tweet_ID' : tweet._json['id_str']
    }
    # logging.critical(f'printing tweet_processed: {tweet_processed}')
    return tweet_processed

def tweets_to_mongo(tweet):
    '''
    writes tweets to MongoDB
    '''
    docID = mongo_tweets.insert_one(tweet).inserted_id
    logging.critical(f'\n\n\nTWEET INCOMING write to navalny_db: {tweet["text"]}\n\n\n')
    logging.critical(f'{str(docID)}')


#####################################
if __name__ == '__main__':

    while True:
        auth = authenticate()
        tmp = get_tweets(end)
        for tweet in tqdm(tmp):
            # logging.critical(f'logging length of tweets within get_tweets: {cardinality.count(tmp)}')
            # logging.critical(f'inside for loop')
            # # start += timedelta(days = 1)
            # # end += timedelta(days = 1)
            # logging.critical(tweet.text)
            new = tweet_to_json(tweet)
            # logging.critical(f'working on tweet: {new["tweet_ID"]}')
            # # tweets_processed_for_db.append(new)
            # logging.critical(f'here is its username: {new["username"]}')
            # logging.critical(mongo_tweets.find({"tweet_ID" : str(new["tweet_ID"])}).count())
            if mongo_tweets.find({"tweet_ID" : str(new["tweet_ID"])}).count() == 0: # ensures that we do not insert duplicate tweets into MongoDB
                tweets_to_mongo(new)
            time.sleep(10)
