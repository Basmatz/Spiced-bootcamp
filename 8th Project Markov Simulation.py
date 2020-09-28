#!/usr/bin/env python
# coding: utf-8

# In[2]:


import pandas as pd
import numpy as np
from itertools import product
import matplotlib.pyplot as plt
import seaborn as sns
get_ipython().run_line_magic('matplotlib', 'inline')


# In[3]:


df = pd.read_csv('monday.csv')


# In[4]:


df # reading the first dataframe with the information


# In[5]:


# separating the strings wihtout the semicolon 
df["timestamp;customer_no;location"] = df["timestamp;customer_no;location"].str.replace(";"," ") 


# In[6]:


df


# In[7]:


df.rename({'timestamp;customer_no;location': 'column'}, axis=1, inplace=True) # simplifying column´s name


# In[8]:


df


# In[9]:


df.column.str.split().tolist() # splitting the string into a list


# In[10]:


# creating a data frame with columns named after the different elements in the supermarket
df = pd.DataFrame(df.column.str.split().tolist(), columns="Date Time Customer_no Location".split())


# In[11]:


df


# In[12]:


# converting dates and time into a datetime timestamp
df['Datetime'] = pd.to_datetime(df['Date'] + ' ' + df['Time'])


# In[13]:


df


# In[14]:


df['hour'] = df['Datetime'].dt.hour 


# In[15]:


df['minute'] = df['Datetime'].dt.minute


# In[16]:


df


# ### Calculate the total number of customers in each section

# In[17]:


df['Location'].value_counts() # using value_counts function to get the total number of customer in each section


# ### Calculate the total number of customers in each section over time

# In[18]:


# getting the number of customer in each section over time by grouping by with time, location and customers
a = df.groupby(['Time', 'Location', 'Customer_no']).sum()


# In[19]:


a.head(20)


# ### Display the number of customers at checkout over time

# In[20]:


df_checkout = df.loc[df['Location'] == 'checkout'] # filtering by checkout to get the customers at checkout over time


# In[21]:


df_checkout


# In[22]:


# grouping time and customers by checkout to get the information at checkout over time
df_checkout.groupby(['Time', 'Customer_no']).sum() 


# ### Calculate the time each customer spent in the market

# In[23]:


# grouping by customer, time and location to get general info about customer and time spent in the market
df.groupby(['Customer_no', 'Time', 'Location']).sum() 


# In[24]:


df_6['Minute per Location'] = df_6['minute'].diff() # calculating with diff. method the amount of minutes per location


# In[25]:


df_6


# In[26]:


df_6['Minute per Location'].sum() # getting the total amount of minutes of customer number 6 with the sum() method 


# ### Calculate the total number of customers present in the supermarket over time.

# In[27]:


df_custcount = df.groupby(["Time"]).count().rename(columns={"Customer_no" : "Sum of customers"}).reset_index()


# In[28]:


# groupying by time and customers to get info. customers in the supermarket at a given time during the day
df.groupby(["Time"])["Customer_no"].count().reset_index()


# In[29]:


df_custcount


# In[30]:


del df_custcount['Location']


# In[31]:


df_custcount.loc[(df_custcount['Time'] == '07:04:00')]


# In[37]:


df["counter"] = df.groupby(["Customer_no", "Time"], as_index = False)['Location'].transform("count")


# In[38]:


df


# In[39]:


z = df.groupby(["Customer_no", "Time"]).size().to_frame('count')


# In[41]:


z


# ### Plot the distribution of customers of their first visited section versus following sections

# In[42]:


df['Customer_no'] = df['Customer_no'].astype(int)


# In[43]:


df_7 = df.loc[((df['hour'] == 7) & (df['Customer_no'] == 7))]


# In[44]:


# I try to plot the different stages of the customer number 7 in the supermarket
sns.scatterplot(data = df_7, x = 'minute', y = 'Location')


# In[48]:


df_6 = df.loc[((df['hour'] == 7) & (df['Customer_no'] == 6))]


# In[49]:


# plotting the behavior of customer 6 during his stay in the market
sns.scatterplot(data = df_6, x = 'minute', y = 'Location')


# In[50]:


df_z = df.loc[((df['hour'] == 7) & (df['Customer_no'] < 20))]


# In[51]:


df_z


# In[52]:


# i try to get a distribution of 20 customers in a plot to check their first visit section. Not very useful.
sns.scatterplot(data = df_z, x = 'minute', y = 'Location', hue = 'Customer_no')


# In[53]:


df_visit = df.groupby(["Customer_no", 'Time', 'Location']).count().reset_index()


# In[54]:


df_visit['Customer_no'] = df_visit['Customer_no'].astype(int)


# In[55]:


df_visit


# ### Calculate transition probabilites

# In[70]:


df_6 = df.loc[(df['Customer_no'] == 6)] # i try to calculate to transition probability for customer 6


# In[71]:


df_6


# In[57]:


df_6.drop(['Date', 'Time', 'Datetime', 'hour', 'counter'], axis=1, inplace=True)


# In[192]:


df_6


# In[58]:


df_6['Minute per Location'] = df_6['minute'].diff() # i get the amount of minutes spent in each section of the market


# In[59]:


df_6['Location before'] = df_6['Location'].shift(1) # I get the last section visited


# In[60]:


df_6.fillna('entrance', inplace=True)


# In[61]:


df_6 # new dataframe with 'minute per location' and 'location before' new columns


# In[62]:


df_6['Minute per Location'] = df_6['minute'].diff()


# In[63]:


df_6.fillna(0, inplace=True) # fill the first section as entrance


# In[64]:


df_6


# In[65]:


df_6['Minute per Location'].sum()


# In[66]:


# i get the transition probability matrix for customer 6
df_6.groupby(['Location', 'Location before']).count()['Customer_no'].unstack 


# In[67]:


pd.crosstab(df_6['Location'], df_6['Location before'], normalize=0)


# ### Calculate transition probabilites for 2 customers

# In[68]:


df_2 = df.loc[(df['Customer_no'] == 7) & (df['Customer_no'] == 8)]


# In[69]:


df_2


# ### implement a Markov Chain-based simulator

# In[204]:


(df_6['Location before'] + '->' + df['Location']).value_counts() # getting the transition counts


# In[205]:


df_6['dummy'] = 1


# In[206]:


ct = df_6.groupby(['Location before', 'Location'])['dummy'].count().unstack()


# In[207]:


ct.fillna(0, inplace=True)


# In[209]:


ct 


# In[212]:


# i get the transition probability matrix for customer 6
P = (ct.T / ct.sum(axis=1)).T
P


# In[215]:


# i get the probabilities for the next move
initial_state = np.array([0.0, 0.0, 0.0, 1.0])     
section_plus_one = np.dot(initial_state, P) 
section_plus_one


# In[219]:


# i get the probability for the next move and so on
section_plus_two = section_plus_one.dot(P)
section_plus_two 


# In[217]:


section_plus_one.dot(P).dot(P)


# In[218]:


section_plus_one.dot(P).dot(P).dot(P)


# ### Visualization of customer 6

# In[2]:


import numpy as np
import cv2
import random

TILE_SIZE = 32
OFS = 50

MARKET = """
##################
##..............##
##..##..##..##..##
##..##..##..##..##
##..##..##..##..##
##..##..##..##..##
##..##..##..##..##
##...............#
##..##..##..##...#
##..##..##..##...#
##...............#
##################
""".strip()


class TiledMap:

    def __init__(self, layout, tiles):
        self.tiles = tiles
        self.contents = [list(row) for row in layout.split('\n')]
        self.xsize =  len(self.contents[0])
        self.ysize = len(self.contents)
        self.image = np.zeros((self.ysize * TILE_SIZE, self.xsize * TILE_SIZE, 3), dtype=np.uint8)
        self.prepare_map()

    def get_tile_bitmap(self, char):
        if char == '#':
            return self.tiles[0:32, 0:32, :]
        else:
            return self.tiles[32:64, 64:96, :]

    def prepare_map(self):
        for y, row in enumerate(self.contents):
            for x, tile in enumerate(row):
                bm = self.get_tile_bitmap(tile)
                self.image[y * TILE_SIZE:(y+1)*TILE_SIZE,
                      x * TILE_SIZE:(x+1)*TILE_SIZE] = bm

    def draw(self, frame):
        frame[OFS:OFS+self.image.shape[0], OFS:OFS+self.image.shape[1]] = self.image


background = np.zeros((700, 1000, 3), np.uint8)
tiles = cv2.imread('tiles.png')

tmap = TiledMap(MARKET, tiles)

while True:
    frame = background.copy()
    tmap.draw(frame)

    cv2.imshow('frame', frame)

    key = chr(cv2.waitKey(1) & 0xFF)
    if key == 'q':
        break

cv2.destroyAllWindows()

