#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
import pandas as pd
import seaborn as sns
from sklearn.dummy import DummyClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.metrics import recall_score
from sklearn.metrics import precision_score
from sklearn.metrics import f1_score
from sklearn.metrics import plot_confusion_matrix
from sklearn.model_selection import cross_val_score
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import MinMaxScaler


# Project Titanic: Classification

# In[2]:


df = pd.read_csv('train.csv', index_col=0)
df.head()


# Train-test-split

# In[3]:


# Select X and y
X = df.drop(columns = ['Survived'])
y = df['Survived']


# Split the dataframe into training and testing data

X_train, X_test, y_train, y_test = train_test_split(X, y) 

# Syntax: train_test_split(X <-- df, y <--series)


# Baseline Model

# In[4]:


dummy_cols = ['Pclass', 'Age']

X_dummy_train = X_train[dummy_cols]
X_dummy_test = X_test[dummy_cols]


# In[5]:


baseline = DummyClassifier(strategy='most_frequent')
baseline.fit(X_dummy_train, y_train)
ypred_baseline = baseline.predict(X_dummy_train)


# In[6]:


baseline.score(X_dummy_train, y_train)
# Training data accuracy:


# Explore data/ Feature Engineering

# In[7]:


# Treat X_train as main df

X_train.isna().sum()


# In[8]:


sns.heatmap(X_train.isna())


# Fix missing values on dataset
# 
# Missing Age values

# In[9]:


# Exploring age avgs by sub-categories:

round(X_train['Age'].mean(), 2), X_train['Age'].median()


# In[10]:


X_train[X_train["Pclass"]==1]["Age"].mean()


# In[11]:


X_train[X_train["Pclass"]==2]["Age"].mean()


# In[12]:


X_train[X_train["Pclass"]==3]["Age"].mean()


# In[13]:


X_train[X_train["Sex"]=='male']["Age"].mean()


# In[14]:


X_train[X_train["Sex"]=='female']["Age"].mean()


# In[15]:


# imputation

X_train.groupby('Pclass').transform('mean')['Age']


# In[16]:


X_train['Age'].fillna(X_train.groupby('Pclass').transform('mean')['Age'], inplace=True)


# In[17]:


X_train.isna().sum()

# Nan Age values imputed:


# Missing Embarked Values

# In[18]:


sns.catplot(x = 'Embarked', kind = 'count', data = X_train)


# In[19]:


X_train['Embarked'] = X_train['Embarked'].fillna('S')
X_train.isna().sum()

# Nan Embarked values imputed:


# Missing Cabin values

# In[20]:


X_train['Cabin'].unique()


# In[21]:


X_train['Cabin'] = X_train['Cabin'].fillna('missing')


# In[22]:


X_train['Cabin'] = X_train['Cabin'].str[0]


# In[23]:


X_train['Cabin'].unique()


# In[24]:


X_train['Cabin'].value_counts()


# In[25]:


X_train.isna().sum()

# Nan Cabin values imputed:


# Normalizing Fare

# In[26]:


X_train['Fare'].min(), X_train['Fare'].max()


# In[27]:


scaler = MinMaxScaler()
scaler.fit(X_train[['Fare']])

X_train['Fare'] = scaler.transform(X_train[['Fare']])


# In[28]:


X_train['Fare'].min(), X_train['Fare'].max()


# Dropping non desired Columns

# In[29]:


X_train = X_train.drop(['Name', 'Ticket'], axis = 1)
X_train.head()


# Sex, and other string categories into binary

# In[30]:


X_train = pd.get_dummies(X_train, drop_first = True)
X_train.head()


# Train Model
# 
# Build a dummy classifier

# In[31]:


# strategy='most_frequent' creates a model that always predicts the majority class
m_dummy = DummyClassifier(strategy='most_frequent', random_state=10)


# In[32]:


m_dummy.fit(X_train, y_train)


# Build a Logistic Regression model

# In[33]:


# Create a model
m = LogisticRegression()


# In[34]:


# Train a model
m.fit(X_train, y_train)


# In[35]:


# create predicted values
ypred = m.predict(X_train)


# In[36]:


accuracy_score(ypred, y_train)
# Accuracy on adjusted model


# Performance evaluations and Cross-Validation score

# Creating Matrix

# In[37]:


plot_confusion_matrix(m, X_train, y_train)


# In[38]:


print('Accuracy: ' + str(m.score(X_train, y_train))), 
print('Precision: ' + str(precision_score(y_train, ypred))),
print('Recall: ' + str(recall_score(y_train, ypred))),
print('F1 score: ' + str(recall_score(y_train, ypred)))


# Cross-Validation

# In[39]:


accuracy = cross_val_score(m, X_train, ypred, cv=5, scoring='accuracy')
print("Cross-validation scores: ", accuracy)


# In[ ]:


Random Forest classification model


# In[40]:


RandomF = RandomForestClassifier(n_estimators = 100, max_depth = 3)
RandomF.fit(X_train, y_train)


# In[41]:


ypred_RandomF = RandomF.predict(X_train)


# In[42]:


print('Accuracy: ' + str(RandomF.score(X_train, y_train))), 
print('Precision: ' + str(precision_score(y_train, ypred_RandomF))),
print('Recall: ' + str(recall_score(y_train, ypred_RandomF))),
print('F1 score: ' + str(recall_score(y_train, ypred_RandomF)))


# In[44]:


accuracy = cross_val_score(m, X_train, ypred_RandomF, cv=5, scoring='accuracy')
print("Cross-validation scores: ", accuracy)

