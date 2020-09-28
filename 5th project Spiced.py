#!/usr/bin/env python
# coding: utf-8

# In[202]:


import pandas as pd
import matplotlib.pyplot as plt
import re
import numpy as np

# Set figure size to (12, 6)
plt.rcParams['figure.figsize'] = (12,6)


# ### Quick way

# In[56]:


dfn = pd.read_csv('TG_STAID002759.txt', skiprows = 19)


# In[150]:


dfn


# In[60]:


dfn.columns=dfn.columns.map(str.strip)


# In[63]:


dfn


# In[62]:


dfn['Date_t'] = pd.to_datetime(dfn['DATE'])


# ### Exploratory way

# In[238]:


df_t = pd.read_csv('TG_STAID002759.txt', delimiter="\t") # getting started dowloading the text file into a pandas csv


# In[239]:


df_t


# In[240]:


df_t = pd.read_csv('TG_STAID002759.txt', delimiter="\t")


# In[241]:


df_t = df_t.drop(df_t.index[0:14]) # deleting first 13 rows containing not relevant info for our assessment


# In[242]:


df_t['column'] = df_t['EUROPEAN CLIMATE ASSESSMENT & DATASET (ECA&D), file created on 11-08-2020']  


# In[243]:


df_t # renaming the column by creating a new one and deleting the other one


# In[244]:


del df_t['EUROPEAN CLIMATE ASSESSMENT & DATASET (ECA&D), file created on 11-08-2020']


# In[245]:


# 1st step: the values are strings separated by commas, we must find a way to eliminate those commas
df_t["column"] = df_t["column"].str.replace(",","") # using the str.replace function to cancel the commas


# In[246]:


df_t['column']


# In[247]:


df_t


# In[248]:


# 2nd step: transforming the strings into a list. we get that by using the str.split.tolist function.
# we have the sting together with the date, i ll try to fix it in next steps
df_t.column.str.split().tolist()


# In[249]:


# 3rd step: splitting and naming the columns with the different variables
df_t = pd.DataFrame(df_t.column.str.split().tolist(), columns="Date Mean_Temp Code ".split())


# In[250]:


df_t 


# In[251]:


# 4rd step: recalculation of the temperature multiplying by 0.1
df_t['Mean_Temp'] 


# In[252]:


df_t['Mean_Temp'] = df_t['Mean_Temp'].astype(int)


# In[253]:


df_t['Mean_Temp'] = df_t['Mean_Temp'] * 0.1


# In[254]:


df_t['Mean_Temp'] 


# In[255]:


df_t.head(10) # dataframe with the temperature recalculated


# In[256]:


# 4th step: creating a new column by removing the information about the station and keeping the value refering to the dates
df_t['Date'] = df_t['Date'].str[6:]


# In[257]:


df_t['Date'] 


# In[258]:


df_t.set_index('Date', inplace=True) # continue setting the Date as index


# In[259]:


df_t['Mean_Temp'].plot() # we can already plot the temperature


# In[260]:


df_t


# In[261]:


df_t.reset_index(level=0, inplace=True)


# In[262]:


df_t


# In[263]:


# 5 step: Creating columns for years, months, and days
df_t['Year'] = df_t['Date'].str[0:4] # creating a new column for the year


# In[264]:


df_t['Month'] = df_t['Date'].str[4:6] # creating a new column for the month


# In[265]:


df_t['Day'] = df_t['Date'].str[6:8] # creating a new column for the day


# In[266]:


df_t


# In[267]:


# 6th step: creating a new column with the date set into a datetime
df_t['Date_new'] = pd.to_datetime(df_t.Year.astype(str) + "-" + df_t.Month.astype(str) + "-" + df_t.Day.astype(str))


# In[268]:


df_t


# In[269]:


df_t.set_index('Date_new', inplace=True) # setting the index with the datetime column "Date_new"


# In[270]:


df_t


# ### Getting some relevant information out of the dataframe

# In[271]:


df_t[df_t['Mean_Temp']==df_t['Mean_Temp'].max()] # maximum average temperature was reached in July 12th 2010 with 30.5 degrees


# In[272]:


df_t[df_t['Mean_Temp']==df_t['Mean_Temp'].min()] # minimum average temperature was reached in February 10th 1929 with -22.6 degrees


# In[273]:


df_t.groupby(['Year']).mean() # we group the mean by year so we can spot trends related with increasing or decreasing average temperatures


# In[274]:


df_gr = df_t.groupby(['Year']).mean() 


# In[275]:


df_gr[df_gr['Mean_Temp']==df_gr['Mean_Temp'].max()] # maximum average temperature was reached in 2019 with 11.82 degrees


# In[276]:


df_gr[df_gr['Mean_Temp']==df_gr['Mean_Temp'].min()] # minimum average temperature was reached in 1945 with 2.9 degrees


# In[277]:


df_grm = df_t.groupby(['Month']).mean() # we group the mean by months to spot the colder and hotter months of the year


# In[278]:


df_grm[df_grm['Mean_Temp']==df_grm['Mean_Temp'].max()] # hottest month is July with an average temperature of 18.88 degrees


# In[279]:


df_grm[df_grm['Mean_Temp']==df_grm['Mean_Temp'].min()] # coldest month is January with an average temperature of -0.015 degrees


# In[280]:


df_grd = df_t.groupby(['Day']).mean() # we group the mean by days


# In[281]:


df_grd[df_grd['Mean_Temp']==df_grd['Mean_Temp'].max()] # hottest day in average is the 30th with 10.1 degrees


# In[282]:


df_grd[df_grd['Mean_Temp']==df_grd['Mean_Temp'].min()] # coldest day in average is the 13th with 9.12 degrees


# In[283]:


df_t.groupby(['Month', 'Day']).mean() # we group the average temperature by month and day so we can make some predictions based on that mean


# In[284]:


df_t.groupby(['Month', 'Day'])['Mean_Temp'].mean()


# In[285]:


# I create a new column with the mean temperatures in order to better locate average temperature for a given day and month
df_t['New_Mean_Temp'] = df_t.groupby(['Month', 'Day'])['Mean_Temp'].transform('mean')


# In[286]:


df_t.loc['2019-08-15'] # according to the average calculated, the
# temperature to be expected tomorrow Saturday 15th August in Templehof Berlin is 18.22 degrees


# In[287]:


df_t['Mean_Temp'].plot()

