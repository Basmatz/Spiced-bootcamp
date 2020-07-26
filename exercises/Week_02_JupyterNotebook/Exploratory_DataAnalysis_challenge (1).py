#!/usr/bin/env python
# coding: utf-8

# Step 1
# 
# Read the file train.csv and print rows

# In[1]:


import pandas as pd


# In[2]:


df= pd.read_csv ('train.csv', index_col=0)
df.head()


# Step 2
# 
# Calculate the number of survivivor and non survivors passegers and display as a bar plot.
# 
# 
# 

# In[4]:


df.groupby(['Survived']).count()


# In[5]:


import numpy as np
import matplotlib.pyplot as plt


# In[6]:


df[['Embarked', 'Survived']].groupby(['Survived']).count()


# In[7]:


df[['Embarked', 'Survived']].groupby(['Survived']).count().plot.bar()


# Step 3
# 
# Calculate the proportion of surviving 1st class passengers considering the total number of the 1st class.

# In[8]:


df2 = df[df['Pclass'] == 1]


# In[9]:


totalfc = df2['Embarked'].count()
totalfc


# In[10]:


#Survivors in the 1st class

df3 = df2[df2['Survived'] == 1]
df3.head()


# In[11]:


survfc = df3['Embarked'].count()
survfc


# In[12]:


survfc/totalfc


# Step 4
# 
# Create a bar plot with separate bars for male/female passengers by class

# In[13]:



df[['Embarked', 'Sex', 'Pclass']].groupby(['Sex', 'Pclass']).count().plot.bar()


# Step 5 
# 
# Create a Histogram with the age and compare Survivors/ Non-Survivors.

# In[17]:


df['Age'].plot.hist()


# In[18]:


df1 = df[df['Survived'] == 1]
df0 = df[df['Survived'] == 0]


# In[19]:


df1['Age'].plot.hist()


# In[20]:


df0['Age'].plot.hist()


# In[21]:


ax1=df[df["Survived"]==0]["Age"].hist(alpha=0.5)
ax2=df[df["Survived"]==1]["Age"].hist(alpha=0.5)
plt.legend([ax1, ax2], labels=["Did not survive", "Survived"])


# In[ ]:


Step 6 
Calculate average age for survived and drowned passengers in separate.


# In[23]:


#Survivors
df1['Age'].mean()


# In[24]:


#drowned
df0['Age'].mean()


# Step 7 
# 
# Replace age values missing for the mean age.
# 
# 

# In[25]:



mean_age = df['Age'].mean()
mean_age


# In[26]:


df_c = df['Age'].fillna(mean_age)
df_c


# Step 8
# Create a table considering the number of survivors and non-survivors for each class

# In[27]:


df[['Embarked', 'Sex', 'Pclass', 'Survived']].groupby(['Pclass', 'Sex', 'Survived']).count()


# In[28]:


# All survivors
df4 = df1[['Sex', 'Pclass', 'Survived']]

df4.groupby(['Sex', 'Pclass']).count().plot.bar()

