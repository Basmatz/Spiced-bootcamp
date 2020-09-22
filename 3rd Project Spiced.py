#!/usr/bin/env python
# coding: utf-8

# In[2]:


import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import PolynomialFeatures


# In[3]:


df = pd.read_csv('train (2).csv')


# In[4]:


df.head(5)


# In[6]:


df['datetime'] = pd.to_datetime(df['datetime'])


# In[7]:


df['hour'] = df['datetime'].dt.hour 


# In[501]:


df['second'] = df['datetime'].dt.second


# In[502]:


df['minute'] = df['datetime'].dt.minute


# In[503]:


df['day'] = df['datetime'].dt.day


# In[504]:


df['month'] = df['datetime'].dt.month


# In[505]:


df['year'] = df['datetime'].dt.year


# In[506]:


df.head(5)


# In[9]:


df_hour = df.loc[df['hour'] == 14]


# In[10]:


df_hour.shape


# ### Linear regression-hour

# In[11]:


sns.heatmap(df_hour.corr())


# In[12]:


sns.pairplot(df_hour)


# In[13]:


sns.pairplot(df_hour.df['count'], df_hour)


# In[ ]:


y_hour = df_hour['count']


# In[ ]:


x_hour = df_hour['temp']


# In[ ]:


plt.scatter(x_hour, y_hour)


# In[527]:


sns.pairplot(df_hour, x_vars=["temp", "humidity", "weather", "season", "holiday", "workingday", "windspeed"], y_vars=["count"])


# In[17]:


df_hour.groupby(['season', 'weather', 'holiday', 'workingday']).mean()


# In[19]:


sns.pairplot(df_hour, x_vars=[:], y_vars=["count"])


# In[20]:


df_hour_clean = df_hour.loc[((df_hour['season'] < 5) & (df_hour['holiday'] == 0) & (df_hour['workingday'] == 0))]


# In[21]:


df_hour_clean[['temp','count']]


# In[22]:


sns.pairplot(df_hour_clean, x_vars=["temp", "humidity", "weather", "season", "holiday", "workingday", "windspeed"], y_vars=["count"])


# In[23]:


y_clean = df_hour_clean['count']


# In[24]:


x_clean = df_hour_clean['temp']


# In[38]:


df2 = df. loc[((df['a'] > 1) & (df['b'] > 0)) | ((df['a'] < 1) & (df['c'] == 100))] # example selection with conditions


# In[36]:


df3 = df_hour_clean.loc[((df_hour_clean['temp'] > 29) & (df_hour_clean['humidity']) & (df_hour_clean['windspeed']))]


# In[41]:


df3.head(5)


# In[53]:


df4 = df3.drop(['season', 'holiday', 'atemp', 'workingday', 'weather', 'casual', 'registered'], 1)


# In[54]:


df4


# In[ ]:


plt.scatter(x_clean, y_clean)


# In[474]:


df.shape


# In[475]:


df['count'].max() # maximum number of bikes rented


# In[476]:


df['datetime'].loc[df['count'].max()] # date for the max. number of bikes rented


# In[54]:


df['count'].min() # minimum number of bikes rented


# In[58]:


df['datetime'].loc[df['count'].min()] # date for the min. number of bikes rented


# In[11]:


sns.heatmap(df.isnull(),cbar=False) # no missing values in the data frame


# In[10]:


df.isna()


# ### First model with 1 variable

# ### Linear regression

# In[371]:


y = df['count'] # definition of y variable


# In[372]:


x = df[['temp']] # definition of x variable


# In[373]:


plt.scatter(x, y) # plot is with extremely dispersed observations, seems to follow a linear relation though


# In[374]:


X_test, X_train, y_test, y_train = train_test_split(x, y)


# In[375]:


X_train.shape, y_train.shape


# In[376]:


X_test.shape, y_test.shape


# In[377]:


m = LinearRegression()


# In[378]:


m.fit(X_train, y_train) 


# In[379]:


m.score(X_train, y_train) # poor model score 


# In[380]:


ypred = m.predict(X_train)


# In[382]:


plt.scatter(x, y)                 # regression line with a extremely poor probability of prediction
plt.plot(X_train, ypred, 'r')
plt.show


# ### Polinomial 

# In[383]:


polynomial_transformer = PolynomialFeatures(degree=2, include_bias=False)


# In[384]:


polynomial_features = polynomial_transformer.fit_transform(X_train)


# In[385]:


m.fit(polynomial_features, y_train)


# In[386]:


m.score(polynomial_features, y_train) # almost same poor result as linear


# In[387]:


ypred = m.predict(polynomial_features)


# In[389]:


plt.scatter(x, y)              # polinomial regression not givig reliability to the model
plt.plot(X_train, ypred, 'r')
plt.show


# ### Second model with 2 variables

# ### Linear regression

# In[399]:


x = df[['temp', 'weather']] # weather is added to the  temperature variable


# In[400]:


X_test, X_train, y_test, y_train = train_test_split(x, y)


# In[401]:


X_train.shape, y_train.shape


# In[402]:


m = LinearRegression()


# In[403]:


m.fit(X_train, y_train) 


# In[404]:


m.score(X_train, y_train) # worse result than the linear regression just with the "temperature" variable


# ### Polinomial

# In[405]:


polynomial_transformer = PolynomialFeatures(degree=2, include_bias=False)


# In[406]:


polynomial_features = polynomial_transformer.fit_transform(X_train)


# In[407]:


m.fit(polynomial_features, y_train)


# In[408]:


m.score(polynomial_features, y_train) # better than lineal but nothing significant, model is very poor


# ### Third model with 3 variables

# In[409]:


x = df[['temp', 'weather', 'holiday']]


# In[410]:


X_test, X_train, y_test, y_train = train_test_split(x, y)


# In[411]:


X_train.shape, y_train.shape


# In[412]:


m = LinearRegression()


# In[413]:


m.fit(X_train, y_train) 


# In[414]:


m.score(X_train, y_train) # worse result than with 2 variables


# ### Polinomial

# In[415]:


polynomial_transformer = PolynomialFeatures(degree=2, include_bias=False)


# In[416]:


polynomial_features = polynomial_transformer.fit_transform(X_train)


# In[417]:


m.fit(polynomial_features, y_train)


# In[418]:


m.score(polynomial_features, y_train) 


# ### Data frame with observations only for season 1

# In[330]:


df2 = df.loc[df['season'] == 1]


# In[331]:


df2.shape


# ### Linear regression

# In[332]:


x = df2[['temp']]


# In[333]:


y = df2['count']


# In[334]:


plt.scatter(x, y)


# In[419]:


X_test, X_train, y_test, y_train = train_test_split(x, y)


# In[420]:


X_train.shape, y_train.shape


# In[421]:


m = LinearRegression()


# In[422]:


m.fit(X_train, y_train) 


# In[423]:


m.score(X_train, y_train)


# ### Data frame with observations for temperatures between 10 and 25 degrees

# In[424]:


df3 = df.loc[((df['temp'] > 10) & (df['temp'] < 25))]


# In[425]:


x = df3[['temp']]


# In[426]:


y = df3['count']


# In[427]:


plt.scatter(x, y)


# ### Linear Regression

# In[428]:


X_test, X_train, y_test, y_train = train_test_split(x, y)


# In[429]:


X_train.shape, y_train.shape


# In[430]:


m = LinearRegression()


# In[431]:


m.fit(X_train, y_train) 


# In[432]:


m.score(X_train, y_train)


# ### Datetime columns

# In[484]:


df['hour'] = pd.to_datetime(df['datetime'], format='%H:%M:%S').dt.hour
                

