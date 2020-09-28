#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.metrics import precision_score
from sklearn.metrics import recall_score

get_ipython().run_line_magic('matplotlib', 'inline')


# In[288]:


df = pd.read_csv('train.csv')


# In[289]:


df.set_index('Name', inplace=True) # indexing by name


# In[156]:


df.shape


# In[259]:


df.head(3)


# In[260]:


df.shape


# ### Inputation

# In[191]:


df.isna().sum() # locating X variables with missing values


# In[261]:


df.isna().sum().loc[['Age', 'Cabin', 'Embarked']] # isolating and assessing variables with missing values


# In[263]:


df[['Cabin', 'Embarked']].fillna('MISSING', inplace=True) # replacing missing values of categorical variables


# In[264]:


df['Age'].mean() # identifying the median value for 'Age' 


# In[265]:


df['Age'].median() # identifying the median value for 'Age' 


# In[266]:


df['Age'].fillna(28, inplace=True) # replacing missing values of numerical variables for the median 


# ### Encoding

# In[267]:


new_Embarked = pd.get_dummies(df[['Embarked', 'Sex']]) # categorical variables to be encoded
new_Embarked # New columns with the 3 different locations where the different titanic passangers embarked and 2  different genders


# In[270]:


df_feature_engineered = pd.concat([df, new_Embarked], axis=1) # data frame renamed containing the changes as we add and modify columns
del df_feature_engineered['Sex']
del df_feature_engineered['Embarked']


# In[271]:


df_feature_engineered.head(10) # new data frame with new columns 


# ### Binning

# In[272]:


df['Age'].fillna(28, inplace=True) # imputation of missing values


# In[273]:


df['Age'].describe() 


# In[274]:


Age_binning = pd.qcut(df['Age'], q=3) # 3 age intervals with alike distribution
Age_binning.head(5)


# In[275]:


Age_binning.value_counts()


# In[276]:


df_feature_engineered['Age_by_labels'] = pd.qcut(df['Age'], q=3, labels=['kids/teens/early 20´s', 'mid 20´s/early 30´s', 'adults over 31'])

df_feature_engineered['Age_by_labels'].head(3) # labeling of 3 different bins to a better identification of the variables


# In[277]:


df_feature_engineered


# ### Scaling

# In[278]:


Age_range = df['Age'].max() - df['Age'].min() # calculation of age range identifying maximum and minimum values amont the passengers
Age_range


# In[279]:


df_feature_engineered['Age_scaled'] = ( df['Age'] - df['Age'].min() ) / Age_range
df_feature_engineered['Age_scaled'].head(3)


# In[280]:


df_feature_engineered


# In[281]:


X = df_feature_engineered[['Embarked_C', 'Embarked_Q', 'Embarked_S']] # model prediction for 'Embarked' variable after being featured engineered


# In[282]:


y = df_feature_engineered['Survived']


# In[283]:


X_test, X_train, y_test, y_train = train_test_split(X, y)


# In[284]:


X_test


# In[240]:


m_logistic = LogisticRegression(random_state=10)


# In[242]:


m_logistic.fit(X_train, y_train)


# In[244]:


ypred_logistic = m_logistic.predict(X_train) # accuracy score
accuracy_logistic = accuracy_score(y_train, ypred_logistic)
accuracy_logistic


# In[250]:


m_logistic.score(X_train, y_train)


# In[257]:


precision_logistic = precision_score(y_train, ypred_logistic)
precision_logistic # precision score


# In[258]:


recall_score(y_train, ypred_logistic) # recall score

