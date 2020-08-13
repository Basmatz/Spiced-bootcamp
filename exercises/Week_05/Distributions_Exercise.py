#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
from PIL import Image # Python image library


# In[2]:


#binary numbers
#  0 : 0000 0000
#  2 : 0000 0010
# 15 : 0000 1111
# 16 : 0001 0000
#255 : 1111 1111


# In[3]:


np.random.randint(0, 9, size=(10,3)).T


# In[7]:


from matplotlib import pyplot as plt

get_ipython().run_line_magic('matplotlib', 'inline')


# # Uniform Distribution

# In[8]:


plt.hist(b.flatten(), bins=20)


# In[5]:


# create a 400 x 150 array with random values 0..255
b =  np.random.randint(0, 255, size=(400, 150), dtype=np.uint8)
Image.fromarray(b.T).resize((800, 300))


# In[10]:


a = np.zeros((400, 150), dtype=np.uint8)  # unsigned integer numbers with 8 binary digitis (bits)

xcoord = np.random.randint(0, 399, size=(300))
ycoord = np.random.randint(0, 149, size=(300))

a[xcoord, ycoord] = np.random.randint(0, 255, size=(300))  # random brightness

Image.fromarray(a.T).resize((800, 300))


# In[11]:


xcoord[:10], ycoord[:10]


# In[12]:


a[:10, :10]


# In[13]:


c = np.random.random(size=(10000))
plt.hist(c, bins=20)


# In[14]:


c[:10]


# # Normal or Gaussian Distribution

# In[15]:


d = np.random.normal(loc=128.0, scale=30.0, size=(100000))
p = plt.hist(d, bins=50)


# In[16]:


min(d), max(d)


# In[17]:


d = np.random.normal(loc=128.0, scale=30.0, size=(400, 150))
d = d.round().astype(np.uint8)
Image.fromarray(d.T).resize((800, 300))


# In[18]:


a = np.zeros((400, 150), dtype=np.uint8)  # unsigned integer numbers with 8 binary digitis (bits)

xcoord = np.random.normal(loc=200.0, scale=30.0, size=(300))
xcoord = xcoord.round().astype(np.uint16)

ycoord = np.random.normal(loc=75.0, scale=10.0, size=(300))
ycoord = ycoord.round().astype(np.uint16)

a[xcoord, ycoord] = np.random.randint(0, 255, size=(300))  # random brightness

Image.fromarray(a.T).resize((800, 300))


# # Triangular Distribution

# In[19]:


t = np.random.triangular(2, 7, 12, size=(100000)).round()
plt.hist(t, bins=11)


# In[20]:


r = np.random.randint(0,6, size=(100000, 20))
print(r.shape)

r = r.sum(axis=1)
print(r.shape)

p = plt.hist(r, bins=20)


# # Central Limit Theorem (Zentraler Grenzwertsatz)¶
# If you add up many distributions you end up with a normal distribution
# 
# THIS WORKS EVEN WITH THE DISTRIBUTIONS NOT BEING EQUAL

# # Binomial
# Coin Tosses

# In[22]:


# toss a coin 10 times and get heads 3 times?


# In[23]:


coins = np.random.binomial(n=20, p=0.8, size=(100000))
# for high n --> similar to normal
# with p != 0.5 --> skewed


# In[24]:


import pandas as pd

pd.Series(coins).value_counts().sort_index().plot.bar()


# # Poisson Distribution
# "In dancing schools, a single falls in love every 11 minutes"
# 
# rare event
# we know the average frequency and not much else
# we assume that the events are independent of each other

# In[25]:


singles_per_minute = 1/11.0
singles_per_hour = 60/11.0
print(singles_per_hour)

p = np.random.poisson(lam=singles_per_hour, size=(100000))


# In[26]:


r = plt.hist(p, bins=18)


# # Example with climate data¶
# number of days above 35 degrees in Berlin

# In[ ]:




