#!/usr/bin/env python
# coding: utf-8

# ####Naive Forecasts¶
# Why do we care about naive forecasts? They allow us to assess our model quality against a very simple baseline.

# In[1]:


import seaborn as sns
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Set figure size to (12, 6)
plt.rcParams['figure.figsize'] = (12,6)


# ## Step 1 - Load the Data

# In[2]:


# Load the  dataset 
df = sns.load_dataset('flights')
df.head()


# In[3]:


# Set the date as index
df['date'] = pd.to_datetime(df.year.astype(str) + "-" + df.month.astype(str))
df.set_index('date', inplace=True)
df.head()


# In[4]:


# Plot the data
df['passengers'].plot(title='Passenger Data')



# #Step 2 - Split the time series into training and test set¶

# In[5]:


df.tail()


# In[6]:


# If we have a DatetimeIndex as our DataFrame.index, we can use that
# To slice by dates


# In[8]:


y_train = df[:'1959'].copy()
y_test = df['1960'].copy()


# In[9]:


y_train.head()


# In[10]:


y_train['1949-01':'1949-03']


# In[11]:


# What happens if we have a column with name '1949'
# y_train['1949'] = 1


# In[14]:


y_train = df[:'1959'].copy()
y_test = df['1960'].copy()


# In[15]:


# Second thing I wanted to mention is that we split train and test by date


# In[17]:


#Step 3 - Detrend your time series data


# In[19]:


# Create the pct_change
y_train['pct_change'] = y_train['passengers'].pct_change()
y_train.head()


# In[20]:


# Plot the pct_change
y_train['pct_change'].plot()


# ## Step 4-De-seasonalize the series by subtracting monthly means
# 
# 

# In[21]:


# Create monthly means of the pct_change
y_train['monthly_means'] = y_train.groupby('month')['pct_change'].transform('mean')
y_train.head()


# In[22]:


# Subtract the monthly mean from the actual values
y_train['deseasonalized'] = y_train['pct_change'] - y_train['monthly_means']
y_train.head()


# In[23]:


# Plot the deseasonalized data
y_train['deseasonalized'].plot()


# #1) The mean of the time series
# 

# In[25]:


y_train['passengers'].mean()


# In[26]:


# Add the mean value of passengers as prediction for y_test
y_test['y_pred_mean'] = y_train['passengers'].mean()
y_test.head()



# In[27]:


# Define a function that plots the forecast for us
def plot_forecast(y_train, y_test, columns):
    '''
    Plots forecasts of passenger data
    
    Params:
    -------
    y_train: The training data
    y_test: The test data
    columns: Name of the prediction columns form a DataFrame
    
    '''
    # Plot the actual values
    y_train.passengers.plot(label='Training Data')
    y_test.passengers.plot(label=('Test Data'))
    
    # Plot each prediction
    for column in columns:
        y_test[column].plot(label=column)
    
    # General settings
    plt.title('Nr. of Passengers per Month over Time', fontsize=15)
    plt.ylabel('Nr. of Passengers', fontsize=12)
    plt.xlabel('Date', fontsize=12)
    plt.legend()
    # plt.savefig('mean_baseline.png')
    plt.show()



# In[28]:


# Plot the forecast
plot_forecast(y_train, y_test, ['y_pred_mean'])


# Predicting the mean does not make sense for a time series with trend. What if we instead use the mean pct_change?
# 
# 

# 2) The mean of the detrended time series

# In[30]:


# Take the mean percentage change
y_test['y_pred_mean_pct_change'] = y_train['pct_change'].mean()
y_test.head()


# Convert the prediction back to nr. of passengers

# In[31]:


# Add 1 to y_pred_mean_diff
y_test['y_pred_mean_pct_change'] += 1
y_test.head()


# In[32]:


# Take the cumulative product of the series
y_test['y_pred_mean_pct_change'] = np.cumprod(y_test['y_pred_mean_pct_change'])
y_test.head()


# In[33]:


x = 1.015544


# In[34]:


x**2


# In[35]:


x**3


# In[36]:


# Take the last actual observation as starting point
last_observation = y_train['passengers'][-1]


# In[37]:


# Take the last actual observation as starting point
last_observation = y_train['passengers'][-1]


# In[38]:


last_observation


# In[39]:


y_test['y_pred_mean_pct_change'] *= last_observation
y_test.head()


# In[40]:


# Plot the forecast
plot_forecast(y_train, y_test, ['y_pred_mean_pct_change'])


# 3) The seasonal means of the time series

# # Create a new column with the monthly mean passengers

# In[41]:


# Plot the forecast


# Again, taking the monthly mean does not make sense in case of a time series with trend. Let's try to use the monthly mean differences instead.

# 

# 4) The seasonal means of the detrended time series

# In[43]:


# Take the monthly means of the pct_change
y_train.groupby('month')['pct_change'].mean()


# In[44]:


y_train['monthly_means'][:12].values


# In[45]:


len(y_test)


# In[46]:


# Create a new column containing the monthly mean percentage changes
y_test['y_pred_monthly_mean_pct'] = y_train['monthly_means'][:12].values
y_test.head()


# In[47]:


# Add 1 to that value
y_test['y_pred_monthly_mean_pct'] += 1
y_test.head()


# In[48]:


# Take the cumulative product
y_test['y_pred_monthly_mean_pct'] = np.cumprod(y_test['y_pred_monthly_mean_pct'])
y_test.head()


# In[50]:


#Multiply the last observed passenger number
y_test['y_pred_monthly_mean_pct'] *= last_observation
y_test.head()


# In[51]:


# Plot the forecast
plot_forecast(y_train, y_test, ['y_pred_monthly_mean_pct'])


# 3) Persistence Forecast

# In[52]:


y_test['passengers'].shift()


# In[53]:


# Always predict the last observed value
y_test['y_pred_persistence'] = y_test['passengers'].shift()
y_test.head()


# In[54]:


y_test.loc['1960-01-01', 'y_pred_persistence'] = last_observation
y_test.head()


# In[55]:


# Plot the prediction
plot_forecast(y_train, y_test, ['y_pred_persistence'])


# 4) Plot all of them together

# In[56]:


predictions = y_test.columns[3:]


# In[57]:


plot_forecast(y_train, y_test, predictions)


# Compare their mean absolute errors
# 

# In[59]:


from sklearn.metrics import mean_absolute_error


# In[60]:


for prediction in predictions:
    print(f'The mean absolute error of {prediction} is')
    print(f'{mean_absolute_error(y_test["passengers"], y_test[prediction])}')
    print()

