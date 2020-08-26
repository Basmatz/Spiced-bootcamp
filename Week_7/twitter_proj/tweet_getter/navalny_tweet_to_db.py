import credentials
from tweepy import OAuthHandler, Stream
from tweepy.streaming import StreamListener
import json
import logging
import pymongo

client = pymongo.MongoClient("mongodb://navalny_db:27017/")
navalnytweet_db = client.navalny_db
tweets = navalnytweet_db.tweet

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

class TwitterListener(StreamListener):

    def on_data(self, data):

        """Whatever we put in this method defines what is done with
        every single tweet as it is intercepted in real-time"""

        t = json.loads(data) #t is just a regular python dictionary.

        text = t['text']
        if 'extended_tweet' in t:
            text =  t['extended_tweet']['full_text']
        if 'retweeted_status' in t:
            r = t['retweeted_status']
            if 'extended_tweet' in r:
                text =  r['extended_tweet']['full_text']

        if 'RT ' in text:
            was_retweeted = True
        else:
            was_retweeted = False

        tweet = {
        'text': text,
        'username': t['user']['screen_name'],
        'followers_count': t['user']['followers_count'],
        'was_retweeted' : was_retweeted,
        'place' : t['place'],
        'timestamp' : t['created_at']
        }

        # print(f'\n\n\nTWEET INCOMING: {tweet["text"]}}\n\n\n')
        logging.critical(f'\n\n\nTWEET INCOMING: {tweet["text"]}\n\n\n')
        tweets.insert_one(tweet)


    def on_error(self, status):

        if status == 420:
            print(status)
            return False

if __name__ == '__main__':

    auth = authenticate()
    listener = TwitterListener()
    stream = Stream(auth, listener)
    stream.filter(track=['navalny', 'nawalny'], languages=['de'])
