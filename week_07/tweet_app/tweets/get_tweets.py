import keys as config
from tweepy import OAuthHandler, Stream
from tweepy.streaming import StreamListener
import json
import logging
#from sqlalchemy import create_engine
import pymongo

#db = create_engine('postgres://postgres:1234@postgresdb:5432/postgres', echo=True)
client = pymongo.MongoClient("mongodb://mongodb:27017/")
db = client.robin
#sql = "create table if not exists tweets(userid varchar(50), tweet text);"

#db.execute(sql)

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
    auth = OAuthHandler(config.CONSUMER_API_KEY, config.CONSUMER_API_SECRET)
    auth.set_access_token(config.ACCESS_TOKEN, config.ACCESS_TOKEN_SECRET)

    return auth

class TwitterListener(StreamListener):

    def on_data(self, data):

        """Whatever we put in this method defines what is done with
        every single tweet as it is intercepted in real-time"""
        count = 200
        t = json.loads(data) #t is just a regular python dictionary.

        text = t['text']
        if 'extended_tweet' in t:
            text =  t['extended_tweet']['full_text']
        if 'retweeted_status' in t:
            r = t['retweeted_status']
            if 'extended_tweet' in r:
                text =  r['extended_tweet']['full_text']

        tweet = {
        'text': text,
        'username': t['user']['screen_name'],
        'followers_count': t['user']['followers_count']
        }

        logging.critical(f'\n\n\nTWEET INCOMING: {tweet["username"]} : {tweet["text"]}\n\n\n')

        #userid = '\'' + tweet['username'].replace('\'','').replace('\"','') + '\''
        #user_tweet = '\'' + tweet["text"].replace('\'','').replace('\"','') + '\''
        userid = tweet['username']
        text = tweet["text"]

        count += 1
        tweepy_tweet = {"user":userid,"tweet_text": text, "count":count}

        db.tweets.insert_one(tweepy_tweet)
        #sql = f"insert into tweets values({userid}, {user_tweet})"
        #db.execute(sql)


    def on_error(self, status):

        if status == 420:
            print(status)
            return False

if __name__ == '__main__':

    auth = authenticate()
    listener = TwitterListener()
    stream = Stream(auth, listener)
    stream.filter(track=['berlin'], languages=['en'])
