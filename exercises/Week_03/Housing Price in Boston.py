#!/usr/bin/env python
# coding: utf-8

# Exploring Boston Housing dataset.
# 
# Dataset: https://scikit-learn.org/stable/modules/generated/sklearn.datasets.load_boston.html
# 
# 
# 
# 
# 
# 

# In[51]:


# Importing needed modules
import numpy as np
import pandas as pd
import scipy.stats as stats
import matplotlib.pyplot as plt
import sklearn
import seaborn as sns
get_ipython().run_line_magic('matplotlib', 'inline')


# In[2]:


# The dataset Boston is already available on scikit-learn, I just loaded it.
from sklearn.datasets import load_boston
boston = load_boston()


# In[3]:


# Verifying the variable type
type(boston)


# In[4]:


# Visualizing the shape of the dataset.
boston.data.shape


# In[5]:


# Dataset description
print (boston.DESCR)


# In[6]:


print(boston.feature_names)


# In[7]:


# Converting the dataset em pandas 
df = pd.DataFrame(boston.data)
df.head()


# In[8]:


# Converting the columns title
df.columns = boston.feature_names
df.head()


# In[9]:


# boston.target is an array with the price of the houses
boston.target


# In[10]:


# Adding the price to the DataFrame
df['PRICE'] = boston.target
df.head()


# Predicting the Prices:
# 
# Y- Dependent variable (Price of the houses).
# X- Independent variable (All other houses characteristics).
# 
# 
# 

# In[11]:


# Importing the Linear Regression module.
from sklearn.linear_model import LinearRegression


# In[28]:


# Dropping the price as a dependent variable. Cutting the target column
X = df.drop('PRICE', axis = 1)


# In[29]:


# Defining Y
Y = df.PRICE


# In[30]:



plt.scatter(df.RM, Y)
plt.xlabel("Average Rooms by House")
plt.ylabel("House Price")
plt.title("Relation Rooms and Price")
plt.show()


# In[33]:


# Creating the object 
regr = LinearRegression()


# In[34]:


# Defining the type
type(regr)


# In[35]:


# Training the model
regr.fit(X, Y)


# In[36]:


# Coeficient with 13 variables, Multiple LinearRegression model.
print("Coeficient: ", regr.intercept_)
print("Number of Coeficients: ", len(regr.coef_))


# In[37]:


# Predicting considering X, not ideal because is the same value...
regr.predict(X)


# In[50]:


# Comparing original price vs Predict prices

plt.scatter(df.PRICE, regr.predict(X))
plt.xlabel("Original Price")
plt.ylabel("Predict Price")
plt.title("Original price x Predict price")
plt.show()


# In[39]:


# Calculating the MSE (Mean Squared Error) from the original price x the predict price, using 13 variables.
msel = np.mean((df.PRICE - regr.predict(X))**2)
print(msel)


# In[40]:


# Using only 1 pred. variable the MSE goes up..
regr = LinearRegression()
regr.fit(X[['PTRATIO']], df.PRICE)
mse2 = np.mean((df.PRICE - regr.predict(X[['PTRATIO']])) **2)
print(mse2)


# In[ ]:


#MSE using a variable is not an option.




# In[41]:


from sklearn.model_selection import train_test_split


# In[42]:


#Dividing X and y using random.
X_train, X_test, Y_train, Y_test = train_test_split(X, df.PRICE, test_size = 0.30, random_state =5)


# In[43]:


print(X_train.shape, X_test.shape, Y_train.shape, Y_test.shape )


# In[44]:


# Constructing the model
regr = LinearRegression()


# In[45]:


#Training the module.
regr.fit(X_train, Y_train)


# In[47]:


#Defining pred in training and test
pred_train = regr.predict(X_train)
pred_test = regr.predict(X_test)


# In[49]:


# Checking the differnce between train x test pred to see if the module suffers overfitting or underfitting.
plt.scatter(regr.predict(X_train), regr.predict(X_train) - Y_train, c = 'b',s = 40, alpha = 0.5) 
plt.scatter(regr.predict(X_test), regr.predict(X_test) - Y_test, c = 'g', s = 40, alpha = 0.5)
plt.hlines(y = 0, xmin = 0, xmax = 50)
plt.ylabel("Residual")
plt.title("Residual Plot - Train (Blue), Test (Green)")
plt.show()



# # Cross Validation Steps

# In[ ]:




