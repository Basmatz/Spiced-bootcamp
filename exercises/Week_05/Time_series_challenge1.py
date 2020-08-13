#!/usr/bin/env python
# coding: utf-8

# In[1]:


import seaborn as sns
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Set figure size to (12, 6)
plt.rcParams['figure.figsize'] = (12,6)


# In[3]:


df = pd.read_csv('TG_STAID002759.txt', sep =',' , skiprows = 19)


# In[4]:


df.head()


# In[5]:


df.plot()


# In[ ]:




