import pandas as pd
import numpy as np
from sqlalchemy import create_engine
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib
import sys

### Import data from Postgres Server

db = create_engine("postgresql://postgres:postgres@localhost:5433/markov")

mo = pd.read_sql("monday", db)
tu = pd.read_sql("tuesday", db)
we = pd.read_sql("wednesday", db)
th = pd.read_sql("thursday", db)
fr = pd.read_sql("friday", db)

total = pd.concat([mo, tu, we, th ,fr])

### Transform Data

desired_width = 300

pd.set_option('display.width', desired_width)
pd.set_option('display.max_columns',20)

def transitions(df_temp):
    df_temp["timestamp"] = pd.to_datetime(df_temp["timestamp"])
    df_temp.set_index(df_temp["timestamp"], inplace=True)
    df_temp.drop("timestamp",axis=1, inplace=True)
    df_temp = df_temp.groupby('customer_no').resample('T').ffill()
    df_temp = df_temp.reset_index('timestamp').set_index('timestamp')
    df_temp['before'] = df_temp['location'].shift(1)
    df_temp.loc[df_temp['before'] == 'checkout',"before"] = "entrance"
    df_temp.fillna('entrance', inplace=True)
    return df_temp

df = transitions(total)

print(df)
pd.read