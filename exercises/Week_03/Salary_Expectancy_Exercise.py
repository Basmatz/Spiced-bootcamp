#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

# Sets the figure size to (12,6)
plt.rcParams['figure.figsize'] = (12,6)


# # Setup
# Let's consider the easy case where we only have one input variable.
# 
# y = annual sallary in USD
# x = years of work_experience
# 
# With the assumed relationship
# 
# $$
# annual\_salary = \hat{b} + \hat{w_1} * years\_of\_work\_experience
# $$
# We do not know the true relationship!

# # 1) Applications of Linear Regression¶
# $$
# \hat{y} = \hat{b} + \hat{w}*x
# $$

# # 1.1) Prediction
# If a person has 10 years of work experience, what will its annualy salary be?
# 
# Main focus is on $\hat{y}$

# # 1.2) Estimation
# What is the effect of an additional year of work experience on the annual salary?
# 
# Main focus is on $\hat{\beta}$

# # 2) Assumptions of Linear Regression

# # A1) The relationship between X and y is linear
# The relationship between the dependent variable, y, and the input feature, x, is of the form
# $$
# y = w_0 + w_1 * x + \epsilon
# $$$$
# annual\_sallary = w_0 * 1 + w_1 * years\_of\_work\_experience + \epsilon
# $$
# or can be linearized. We will talk about how to linearize a relationship in the afternoon.

# # A2) The sample is a random sample
# A sample is part (or an extraction) of the population.
# 
# If this assumption does not hold the information gained is not representative for the whole population and the model fails to generalize.

# # A3) There is variation in the X variables¶
# The X variable(s) take(s) on different values. Otherwise no information can be gained by looking at X.

# # If we are only interested in prediction, these 3 assumptions are sufficient for generalizability!¶

# # If we are interested in estimation we should worry about further assumptions.

# # A4) Zero-conditional-mean assumption 
# The mean of the error term $\epsilon$ conditional on X is 0.
# 
# $$
# E(\epsilon|X) = 0
# $$
# There is no relationship between X and the error term $\epsilon$. This is a sophisticated way of saying that we did not fail to include an additional input feature that is correlated with our current input features and explains y.

# # Unbiasedness
# Under the assumptions A1 - A4 the linear regression estimator is unbiased.
# Unbiasedness refers to the coefficients. It means that the expected value of the coefficient estimats equals its true value:
# 
# $E(\hat{w}|X)=w$

# # Create some data for our model

# # Assume true relationship
# The true relationship between y and input features is
# 
# $$
# annual\_salary = w_0 + w_1 * years\_of\_work\_experience + w_2 * years\_of\_formal\_education + \epsilon
# $$

# In[10]:


# Choose a sample size
sample_size = 2000


# In[21]:


np.random.randint (0, 2, size=5)


# In[13]:


# Create an array of years_of_formal_education ratings
max_years_of_formal_education = 25
min_years_of_formal_education = 9
factor = 10
years_of_formal_education = np.random.randint(min_years_of_formal_education*factor, max_years_of_formal_education*factor, size=sample_size)/factor


# In[22]:


# Create an array of years of work_experience
max_years_of_work_experience = 50
min_years_of_work_experience = 0
years_of_work_experience = np.random.randint(min_years_of_work_experience*factor,
                                            max_years_of_work_experience*factor, size=sample_size)/factor \
                            - years_of_formal_education/5


# In[23]:


# Let's calculate the annual salary

# Define the true weights

# b: The baseline salary for a person with 0 years of formal education and 0 years of work experience
b = 20_000

# w_1: The increase in annual salary resulting from a 1 year increase in of work experience
w_1 = 1_000

# w_2: The increase in annual salary resulting from a 1 year increase in formal education
w_2 = 1_000


# create a random error (as array)
error = np.random.normal(size=sample_size) * 5_000

# calculate our annual salary according to the true relationship
annual_salary = b + w_1 * years_of_work_experience +                  w_2 * years_of_formal_education + error


# In[24]:


df = pd.DataFrame({
    'salary': annual_salary,
    'work_experience': years_of_work_experience,
    'education': years_of_formal_education
    })
df.head()


# In[25]:


# Plot the relationships
sns.pairplot(df)


# In[26]:


# Plot the relationship between work_experience and salary
sns.regplot(x='work_experience', y='salary', data=df)


# # Let's fit a model¶
# Option 1 - sklearn

# In[27]:


y = df['salary']
X = df[['work_experience']]


# In[28]:


# import the model
from sklearn.linear_model import LinearRegression


# In[29]:


# Instantiate the model
m = LinearRegression()


# In[30]:


# fit the model only on work experience
m.fit(X, y)


# In[31]:


# Make predictions and save them into the DataFrame
df['predictions'] = m.predict(df[['work_experience']])


# In[32]:


# Plot the real values and the predictions
sns.scatterplot(x='work_experience', y='salary', data=df)
sns.lineplot(x='work_experience', y='predictions', data=df, color='r')


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




