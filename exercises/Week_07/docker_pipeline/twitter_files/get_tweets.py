import credentials
from tweepy import OAuthHandler, Stream
from tweepy.streaming import StreamListener
import json
import logging
from pymongo import MongoClient

### Create connection to mongodb
# We want to talk to the database inside the mongodb container
# host is the name of the container
# port is the port inside the container
client = MongoClient(host='mongodb', port=27017)
# we want to connect to the twitter database
db_mongo = client.twitter
# connect to the tweets collection
tweets = db_mongo.tweets

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
    auth = OAuthHandler(credentials.CONSUMER_API_KEY, credentials.CONSUMER_API_SECRET)
    auth.set_access_token(credentials.ACCESS_TOKEN, credentials.ACCESS_TOKEN_SECRET)

    return auth

class TwitterListener(StreamListener):

    def on_data(self, data):

        """Whatever we put in this method defines what is done with
        every single tweet as it is intercepted in real-time"""

        t = json.loads(data) #t is just a regular python dictionary.

        tweet = {
        'text': t['text'],
        'username': t['user']['screen_name'],
        'followers_count': t['user']['followers_count']
        }

        logging.critical(f'\n\n\nTWEET INCOMING: {tweet["text"]}\n\n\n')


    def on_error(self, status):

        if status == 420:
            print(status)
            return False

if __name__ == '__main__':

    auth = authenticate()
    listener = TwitterListener()
    stream = Stream(auth, listener)
    stream.filter(track=['Denny'], languages=['en'])
