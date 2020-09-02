import slack
#import pyjokes
import logging
import time
from sqlalchemy import create_engine
import pandas as pd

oauth_token = "xoxb-1227345553298-1330257325860-jGwb5bwonFww8KDhhSV8l1oT"

db_pg = create_engine("postgres://postgres:1234@postgresdb:5432/postgres", echo=False)

#query = "SELECT * FROM tweets2 order by followers desc limit 1"
query = "select * from tweets3 order by created_at desc limit 1;"


while True:
    df = pd.read_sql(query, db_pg)
    #result = db_pg.execute(query)

    client = slack.WebClient(token=oauth_token)

    logging.critical('---Tweeted into slack channel---')
    logging.critical(df)
    #
    logging.critical(f"This tweet by {df.user_name[0]} was just posted at {df.created_at[0]}: {df.text[0]}")

    #response = client.chat_postMessage(channel='#random', text=f"This tweet by {df.user_name[0]} was just posted at {df.created_at[0]}: {df.text[0]}")
    time.sleep(10)


'''
while True:
    client = slack.WebClient(token=oauth_token)
    joke = pyjokes.get_joke()
    logging.critical('---Tweeted into slack channel---')
    #response = client.chat_postMessage(channel='#random', text=f"Here is a Python joke (R): {joke}")
    time.sleep(10)


logging.critical('---sending python joke to Slack channel')
'''
