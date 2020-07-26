#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.dummy import DummyClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split


# In[8]:


df = pd.read_csv('train.csv', index_col=0)
df.head()


# In[9]:


# Split X and Y

y = df['Survived']
X = df.drop(columns=['Survived'])


# In[10]:


# define the model

m = DummyClassifier(strategy='most_frequent')
m.fit(X, y)
ypred = m.predict(X)


# In[11]:



ypred


# In[ ]:




