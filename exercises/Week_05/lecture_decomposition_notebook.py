#!/usr/bin/env python
# coding: utf-8

# # Project Temperature/Time Series
# 
# ## Time Series Data
# 
# "An obvious characteristic of time series data that distinguishes it from cross-sectional data is temporal ordering." - Introductory Econometrics, J. Wooldridge
# 
# Time Series data has (or can have) the following components:
# 1. Trend
# - Seasonality
# - Remainder:
#     - Randomness
#     - Time Dependence
# 
# ## Time Series Analysis
# 
# Time Series Analysis is a field of statistical Analysis that deals with modelling **time dependence**. The other properties of time series will have to be taken into account in order to model it, but the time dependence is what we try to understand in time series analysis. Thereby, we can extract meaningful information from the past.
# 
# Ask yourself the question:
# Is there meaningful information in the past observations of the time series that cannot be captured by any covarying variable?
# If the answer is **yes**, that is when time series analysis comes into play. This could be the case if we either can't model any other relationship or we cannot access the necessary data.
# 
# ## Topics we will cover this week
# 
# **Time Series:**
# 
# - Decompose time series data into its different components
# - Use a naive forecast as a baseline model
# - Learn how to use Autoregressive (AR) and Autoregressive-Integrated-Moving-Average (ARIMA) Models to predict the future.
# - Evaluate your forecasts
# 
# **Miscellaneous:**
# 
# - Distribution Functions
# - Python Namespaces
# - Useful Python Modules
# - Plotting on Maps
# 
# ## Main Project Goal
# 
# - Understand the purpose of and the idea behind time series analysis
# - Be able to make short term temperature forecasts
# 
# ## Possible project results at the end of the week
# 
# - Data Wrangling: Create a large dataset of climate data from individual files
# - Interactive Visualizations: geojson, geopandas, folium/ plotly library
# - Forecasting: Create a model that is able to make short term temperature forecasts (using statsmodels, sklearn, sktime or fbprophet) and evaluate their performance

# # Time Series Decomposition

# In[1]:



import seaborn as sns
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Set figure size to (12, 6)
plt.rcParams['figure.figsize'] = (12,6)


# ## Step 1 - Load the Data

# In[2]:


# Load the flights dataset from seaborn
df = sns.load_dataset('flights')
df.head()


# ## Step 2 - Plot the time series

# In[11]:



# Combine the month and year column and make a new column out of it
df['Date'] = pd.to_datetime(df['year'].astype(str) + ' ' + df['month'].astype(str))
df.head()



# In[12]:



# Set the new columns as the index
df.set_index('Date', inplace=True)


# In[5]:


df.head()


# In[6]:


# Plot the series
df['passengers'].plot()


# ## Step 3 - Remove the trend
# 
# - Differencing - if the trend is linear
# - Second order differencing - if the trend is quadratic
# 
# ### 3.1) Differencing

# In[13]:


df['passengers'].diff()


# In[14]:


# Create a column with the differences of passengers
df['difference'] = df['passengers'].diff()
df.head()


# In[15]:


# Plot the result
df['difference'].plot()


# In[16]:


# Look at the mean
df['difference'].mean()


# #1.2) Second order differencing
# Second order differencing is used if the time series has an quadratic trend rather than a linear trend.

# In[17]:


# Create a column with the differences of passengers
df['second_order_difference'] = df['difference'].diff()
df.head()


# In[18]:


# Plot the result
df['second_order_difference'].plot()


# How could we check for a trend and assess what kind of trend our data follows?

# In[19]:


df['passengers'].plot()


# This could be a linear trend or maybe a slightly exponential trend.
# 
# A way we can deal with that is to fit a linear regression on a timestamp (and/or a squared timestamp) to figure out whether there is evidence for a trend and which kind of trend might describe the trend best.
# 
# hint: this week we will generally use statsmodels rather than sklearn

# In[20]:



from statsmodels.api import OLS, add_constant


# In[21]:


# Create a timestep variable
df['timestep'] = np.arange(1, len(df)+1)

# Create a squared timestep variable as well
df['timestep^2'] = df['timestep']**2
df.head()


# In[22]:


# fit the model
X = add_constant(df['timestep'])
X_sq = add_constant(df[['timestep', 'timestep^2']])
X.head()


# In[23]:


y = df['passengers']


# In[24]:


# Create a model with the timestep only
m = OLS(y, X) # OLS stands for ordinary least squares and it is a method
# to solve a linear regression
results = m.fit()
results.summary()


# In[25]:


# Create a model with the squared timestep
m_sq = OLS(y, X_sq)
results_sq = m_sq.fit()
results_sq.summary()


# In[ ]:





# ## Step 4 - Remove trend and changes in volatility
# 
# **Only do this if the time series shows changes in volatility, this might not be the case in the project!!!**

# In[26]:


# Create a column with the percentage change of passenger numbers
df['percentage_change'] = df['passengers'].pct_change()
df.head()


# In[27]:


# Plot the result
df['percentage_change'].plot()


# ## Step 5 - Remove the seasonality
# 
# Demean each value by subtracting the monthly mean.

# In[28]:


# Calculate the monthly mean percentage change of passenger numbers
df.groupby('month')['percentage_change'].mean()


# In[29]:


# Create a new column
df['monthly_mean'] = df.groupby('month')['percentage_change'].transform('mean')
df.head()


# In[30]:


# Demean the percentage change
df['deseasonalized'] = df['percentage_change'] - df['monthly_mean']
df.head()


# In[31]:


# Plot the result
df['deseasonalized'].plot()


# ## This is the time series we will actually do our analysis on!
# 
# 1. We make predictions for the `df['deseasonalized']`
# - We add back on the monthly_mean
# - We take the first value and create whole log_series
# - We exponentiate the values to arrive back at the acutal values

# ## Step 6 - Run a time series model on the remainder

# In[ ]:





# ## Step 7 - Reconstruct actual values from predictions

# In[ ]:





# ## Hint - statsmodels

# In[ ]:


# Import seasonal_decompose from statsmodels


# In[32]:



from statsmodels.tsa.seasonal import seasonal_decompose


# In[33]:



# Additive decomposition
seasonal = seasonal_decompose(df['passengers'])


# In[34]:


seasonal.plot()
plt.show()


# In[36]:


# Multiplicative decomposition
seasonal_mult = seasonal_decompose(df['passengers'], model='multiplicative')


# In[37]:


seasonal_mult.plot()
plt.show()


# In[38]:


seasonal_mult.resid.plot()


# In[ ]:




