## EXPLORING ARCTIC DATA

## Data for Arctic research station Ostrov Ajon (island off the northern coast of Siberia)

## imports

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

from statsmodels.api import OLS, add_constant


# read in data from Svalbard Airport.

svalbard = pd.read_csv('Svalbard_Airport_Data/TG_STAID000186.txt', sep = ',', skiprows = 18)

svalbard.columns = svalbard.columns.map(str.strip)

svalbard.columns = ['source', 'date', 'temp', 'q_code']

svalbard['station'] = '186'

# add dates in datetime format
svalbard['month'] = pd.to_datetime(svalbard['date'], format = '%Y%m%d').dt.month
svalbard['year'] = pd.to_datetime(svalbard['date'], format = '%Y%m%d').dt.year
svalbard['date_month'] = pd.to_datetime(svalbard['year'].astype(str) + ' ' + svalbard['month'].astype(str))
svalbard.set_index('date_month', inplace = True)

# change cols to numeric
svalbard.q_code = pd.to_numeric(svalbard.q_code)
svalbard.temp = pd.to_numeric(svalbard.temp)



svalbard.head()

# Find out how many days have no recorded data/how much of a problem we have with missing or unreliable dataset

svalbard['q_code'].value_counts()


# plot if there are significant stretches of missing data

sns.lineplot(x = svalbard.index, y = 'q_code', data = svalbard)


# reliable data collection starts in late 1950s, find out when

testing = svalbard['1955':'1960']

testing2 = testing[testing.q_code < 9]

testing2

sns.lineplot(x = testing.index, y = 'q_code', data = testing)


## answer: reliable data collection started in 1957
# drop data points before
# also drop that one missing data point from 2020


svalbard = svalbard['1957':]

svalbard = svalbard[:-1]


## some plotting of average temps

# find  monthly averages

svalbard['monthly_mean'] = svalbard.groupby('date_month')['temp'].transform('mean')

# plot raw temp
sns.lineplot(x = svalbard.index, y = 'monthly_mean', data = svalbard)



# Questions to answer:
# 1. is the trend linear or quadratic?
# 2. then: de-seasonalise
# 3. de-trend
# 4. make predictions


### step 1: split into training and test data

y_train = svalbard[:'2019-06']

y_train.tail()

y_test = svalbard['2019-07':]

y_test.head()

# Aggregate by month

y_train = y_train.resample('M').mean()

y_train = y_train.drop(['source', 'date', 'monthly_mean'], axis = 1)

y_train.head()

y_train.rename(columns = {'temp' : 'monthly_mean_temp'}, inplace = True)

sns.lineplot(x = y_train.index, y = 'monthly_mean_temp', data = y_train)


## Identify whether trend is linear or quadratic

y_train['timestep'] = np.arange(1 , len(y_train)+1)

y_train['timestep_sq'] = y_train['timestep']**2

# fit OLS model, compare outcomes.

X = add_constant(y_train['timestep'])

X_sq = add_constant(y_train[['timestep', 'timestep_sq']])

m = OLS(y_train['monthly_mean_temp'], X)
results = m.fit()
results.summary()


m_sq = OLS(y_train['monthly_mean_temp'], X_sq)
results_sq = m_sq.fit()
results_sq.summary()

######  UPSHOT: for my Svalbard data, looks like a quadratic function explains the trend better.

### DE-TRENDING WITH SECOND ORDER DIFFERENCING

y_train['diff'] = y_train['monthly_mean_temp'].diff()
y_train['2diff'] = y_train['diff'].diff()

# plot:
sns.lineplot(x = y_train.index, y = '2diff', data = y_train)

### remove volatility (?)

y_train['pct_change'] = y_train['monthly_mean_temp'].pct_change()

sns.lineplot(x = y_train.index, y = 'pct_change', data = y_train)

## Remove seasonality:

# mean monthly pct change

y_train['mean_monthly_pct_change'] = y_train.groupby('month')['pct_change'].transform('mean')

y_train['deseasonalized'] = y_train['pct_change'] - y_train['mean_monthly_pct_change']

sns.lineplot(x = y_train.index, y = 'deseasonalized', data = y_train)

## Prediction: Seasonal means of de-trended time series

# first also resample y_test by month

y_test = y_test.resample('M').mean()

y_test.rename(columns = {'temp' : 'monthly_mean_temp'}, inplace = True)

# create precicted values
y_test['y_pred_mean_monthly_pct_change'] = y_train['mean_monthly_pct_change'][:12].values

y_test['y_pred_mean_monthly_pct_change'] += 1

# cumulative product

y_test['y_pred_cumprod'] = np.cumprod(y_test['y_pred_mean_monthly_pct_change'])

last_obs = y_test['monthly_mean'][-1]

y_test['y_pred_mean_monthly_pct_change'] *= last_obs

y_test.head()

# now plot prediction:

plt.figure(figsize=(25,4))
sns.lineplot(x = y_train.index, y = 'monthly_mean_temp', data = y_train, label = 'Actual Data to 2019')
sns.lineplot(x = y_test.index, y = 'monthly_mean_temp', data = y_test, label = 'Actual Data 2020')
sns.lineplot(x = y_test.index, y = 'y_pred_mean_monthly_pct_change', data = y_test, label = 'Predicted Data')









#
