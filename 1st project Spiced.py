#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

get_ipython().run_line_magic('matplotlib', 'inline')


# In[357]:


df = pd.read_csv('gapminder_total_fertility.csv')


# In[342]:


df


# In[358]:


df = df.rename(columns={'Total fertility rate': 'Country'}) # replacement of wrong column name


# In[364]:


df


# In[363]:


df.set_index('Country', inplace=True) # setting the index as Country


# In[365]:


df


# In[270]:


df.shape # 260 countries for 216 years, we can clean the data to get a Data frame with countries with observations


# In[271]:


df = df.dropna() # All rows with non data are removed from the Dataframe for a better visualization


# In[349]:


df


# In[275]:


df.shape # 61 countries are removed from the Data frame


# In[276]:


df.head(5) # first 5 countries showing data for the first 9 years and last 10 years


# In[277]:


df.tail(10) # last 10 countries of the dataset


# In[333]:


df.describe() #we take a summory of the statistical info. of the general data frame. Fertility world rate dropped more than half in the last 200 years


# In[315]:


df['2015'].mean() # fertility mean for the 260 countries in the year 2015


# In[316]:


df['2015'].std()


# In[280]:


df[['2014','2015']].mean() # fertility mean for 2014 and 2015


# In[313]:


df[['2010','2012','2013','2014','2015']].mean() # fertility mean for the the year range from 2010 to 2015, dropping trend


# In[309]:


df.loc['Germany'].max()


# In[310]:


df.loc['Germany'].min() # fertility rate dropped more than half in Germany, now below replacement population


# In[311]:


df.loc['Spain'].max()


# In[312]:


df.loc['Spain'].min() # same as Germany


# In[282]:


df['2015'].max() # maximum fertility rate in 2015


# In[283]:


df[df['2015']==7.51] # Niger is identified as the country with the biggest fertility rate in 2015


# In[284]:


df['2015'].min() # minimum fertility rate in 2015


# In[285]:


df[df['2015']==1.13] # Macao is identified as the country with the lowest fertility rate in 2015


# In[286]:


df[df['2015']>5] # Countries with higher level of fertility rates a placed in the African continent with very low GDP´s and no industrialised economies


# In[287]:


df[df['2015']<1.5] # Countries with low fertility rates (below population replacement) are located in western countries with high GDPs and industrialised economies, with exceptions such as Lebanon and Thailand 


# In[326]:


df.assign(max_value=df.values.max(1)) #adding new column with maximum and minimum fertility rate for each country


# In[294]:


df.assign(min_value=df.values.min(1))


# In[324]:


df['max_value'] = df.max(axis=1)
print(df) # adding a new column with maximum values for each country


# In[323]:


df['min_value'] = df.min(axis=1)
print(df) # adding a new column with minimum values for each country


# In[321]:


df.loc['Germany']


# In[318]:


df.sort_values(by=['2015']) # countries fertility ordered from minimum to maximum


# In[319]:


df.sort_values(by='2015', ascending=False) # countries fertility ordered from maximum to minimum


# In[290]:


df.sort_values(by=['2015', '2014'])


# In[291]:


df.sort_values(by=['2015','2014'], ascending=False)


# In[292]:


df.plot.scatter('2014','2015') # fertility trend for the last 2 years of the sample


# In[306]:


df.plot.hist('Germany')


# In[ ]:




