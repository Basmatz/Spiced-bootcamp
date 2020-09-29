#!/usr/bin/env python
# coding: utf-8

# In[149]:


# linear algebra
import numpy as np 

# data processing
import pandas as pd 

# data visualization
import seaborn as sns
get_ipython().run_line_magic('matplotlib', 'inline')
from matplotlib import pyplot as plt
from matplotlib import style

# Algorithms
from sklearn import linear_model
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import Perceptron
from sklearn.linear_model import SGDClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC, LinearSVC
from sklearn.naive_bayes import GaussianNB


# In[3]:


df = pd.read_csv('accepted_2007_to_2018Q4.csv')


# In[150]:


df


# In[77]:


df.info()


# In[78]:


df.describe()


# In[151]:


df.columns.values


# In[152]:


# Variable exploration. Difficult to identify each variable out of the 155 and to understand the titles.
# I assume that at the moment of loan acceptance the payment history of the client was flawless and there was no default records
# I want to explore default rate for new customers I am going to ignore the variables related to delinquencies with current customers
df_pred = df[['loan_amnt', 'term', 'int_rate', 'installment', 'grade', 'sub_grade', 'emp_title', 'emp_length', 'purpose', 'title', 'dti', 'home_ownership', 'annual_inc', 'open_acc', 'revol_bal', 'revol_util', 'total_acc','loan_status',]].copy()


# In[153]:


# Initial variables chosen to build the model are 17, including categorical and numerical 
df_pred


# In[154]:


df_pred.drop(['Total amount funded in policy code 1: 1465324575', 'Total amount funded in policy code 2: 521953170'])


# In[73]:


# Lets clean the chosen variables and explore if there is missing data and imputation is needed


# In[155]:


df_pred['dti'].sort_values(ascending=False)


# ### Feature engineering

# ### 1- Imputation

# In[156]:


# Before imputation
df_pred.isna().sum()


# In[157]:


# After imputation
df_pred.isna().sum()


# In[158]:


df['dti'].dtypes


# In[159]:


del df_pred['title']


# In[160]:


# Nice table with information about the total number of missing values for variable and its impact on the total amount
# Missing values are not significant, with a maximum number on 'employment title' and 'employment lenght'
# The rest of the variables with missing values are insignificant, nevertheless I am proceeding with the imputation to have a more neat dataset
total = df_pred.isnull().sum().sort_values(ascending=False)
percent_1 = df_pred.isnull().sum()/df_pred.isnull().count()*100
percent_2 = (round(percent_1, 1)).sort_values(ascending=False)
missing_data = pd.concat([total, percent_2], axis=1, keys=['Total', '%'])
missing_data


# In[161]:


# Inputation on string/object variables
df_pred['emp_title'].fillna('MISSING', inplace=True)


# In[162]:


df_pred['emp_length'].fillna('MISSING', inplace=True)


# In[163]:


df_pred['loan_status'].fillna('MISSING', inplace=True)


# In[164]:


df_pred['loan_status'].fillna('MISSING', inplace=True)


# In[165]:


df_pred['term'].fillna('MISSING', inplace=True)


# In[166]:


df_pred['purpose'].fillna('MISSING', inplace=True)


# In[167]:


df_pred['grade'].fillna('MISSING', inplace=True)


# In[168]:


df_pred['sub_grade'].fillna('MISSING', inplace=True)


# In[169]:


df_pred['home_ownership'].fillna('MISSING', inplace=True)


# In[170]:


df_emp = df['emp_length'].value_counts()


# In[171]:


# Imputation of integer variables with the median as replacement value
df_pred['loan_amnt'].median()


# In[172]:


df_pred['revol_util'].fillna(50.3, inplace=True)


# In[173]:


df_pred['dti'].fillna(17.84, inplace=True)


# In[174]:


df_pred['open_acc'].fillna(11, inplace=True)


# In[175]:


df_pred['total_acc'].fillna(22, inplace=True)


# In[176]:


df_pred['annual_inc'].fillna(65000, inplace=True)


# In[177]:


df_pred['int_rate'].fillna(12.62, inplace=True)


# In[178]:


df_pred['installment'].fillna(377.99, inplace=True)


# In[179]:


df_pred['revol_bal'].fillna(11324, inplace=True)


# In[180]:


df_pred['loan_amnt'].fillna(12900, inplace=True)


# In[181]:


df_pred


# In[182]:


df_pred1 = df_pred


# ### Encoding

# ### Homeownership

# In[183]:


encode_home = pd.get_dummies(df_pred1['home_ownership'])


# In[184]:


df_pred1 = pd.concat([df_pred1, encode_home], axis=1)


# In[185]:


df_pred1


# ### Encoding Loan status into binaries

# In[186]:


df_pred1['loan_status'].value_counts()


# In[187]:


encode_status = pd.get_dummies(df_pred1['loan_status'])


# In[188]:


encode_status


# In[189]:


# Creating a columns whith the successful loans being already paid off
encode_status['Fully_Paid_new'] = encode_status['Fully Paid'] + encode_status['Does not meet the credit policy. Status:Fully Paid']


# In[190]:


# Creating column with what I consider a decent default estimation
encode_status['Chargeoff_defaults_delays'] = encode_status['Charged Off'] + encode_status['Default'] + encode_status['Late (31-120 days)'] + encode_status['Does not meet the credit policy. Status:Charged Off'] + encode_status['In Grace Period'] + encode_status['MISSING'] 


# In[191]:


# Dropping all columns with defaults and delays
encode_status.drop(['Charged Off', 'Default', 'Late (31-120 days)', 'Does not meet the credit policy. Status:Charged Off', 'In Grace Period'], axis=1, inplace=True)


# In[192]:


encode_status


# In[193]:


# Drop columns with the information about loans still active. I include here the delinquencies between up to 30 days so we dont consider these ones as defaults
encode_status.drop(['Current', 'Late (16-30 days)'], axis=1, inplace=True)


# In[194]:


encode_status.drop(['MISSING'], axis=1, inplace=True)


# In[195]:


# Dropping columns with the information about loans alreday paid as we have created a combined column with the information
encode_status.drop(['Fully Paid', 'Does not meet the credit policy. Status:Fully Paid'], axis=1, inplace=True)


# In[196]:


# New encoded column with fully paid loans and loans defaulted, charged off and delayed more than 30 days
# With this binary 
encode_status


# In[197]:


df_pred1 = pd.concat([df_pred1, encode_status], axis=1)


# In[198]:


# Setting 'loan_status' as index so we can better drop the rows with observations as loan that we are not going to use
# current loans and delayed loan below 30 days
df_pred1.set_index('loan_status', inplace=True)


# In[199]:


df_pred1


# In[200]:


# we drop the data from the dataset
df_pred1.drop(['Current' , 'Late (16-30 days)'], inplace=True)


# In[201]:


df_pred1.reset_index('loan_status', inplace=True)


# In[202]:


df_pred1


# In[204]:


df_pred1.columns.value_counts


# In[205]:


df_pred_1 = df_pred1


# ### Dropping 14 variables. Model will be trained initially with only 3.

# In[206]:


# I create a new dataset with only the columns that are going to be needed for training the model
df_pred_1.drop(['loan_status', 'loan_amnt', 'term', 'int_rate', 'installment', 'grade', 'sub_grade', 'emp_title', 'purpose', 'dti', 'open_acc', 'revol_bal', 'revol_util', 'total_acc'], axis=1, inplace=True)


# In[207]:


df_pred_1


# ### Continuing the hot encoding of 'Homeownership'

# In[208]:


# We combine the data not defined as 'own' or 'mortgage' as rent. So we assume that the client has no property.
df_pred_1['Rent'] = df_pred_1['RENT'] + df_pred_1['ANY'] + df_pred_1['OTHER'] + df_pred_1['MISSING'] + df_pred_1['NONE']


# In[209]:


df_pred_1['Mortgage'] = df_pred_1['MORTGAGE']


# In[210]:


df_pred_1['Own'] = df_pred_1['OWN']


# In[211]:


df_pred_1.drop(['RENT', 'ANY', 'OTHER', 'MISSING', 'NONE', 'MORTGAGE', 'OWN'], axis=1, inplace=True)


# In[212]:


df_pred_1


# In[213]:


df_pred_1.drop(['Chargeoff_defaults_delays'], axis=1, inplace=True)


# In[216]:


# I set the column of 'Loan_status'
df_pred_1 = df_pred_1.rename(columns={'Fully_Paid_new': 'Loan_status'})


# In[217]:


df_pred_1


# In[218]:


df_pred_1.drop(['home_ownership'], axis=1, inplace=True)


# In[219]:


df_pred_1


# ### Binning the variable 'annual income'

# In[220]:


df_pred_1['annual_inc'].describe()


# In[221]:


Incomes_binned = pd.qcut(df_pred_1['annual_inc'], q=4)


# In[222]:


Incomes_binned.value_counts()


# In[223]:


df_pred_1['Incomes_binned'] = pd.qcut(df_pred_1['annual_inc'], q=4, labels=[1, 2, 3, 4])


# In[224]:


df_pred_1


# In[225]:


# Dropping the variable 'annual_inc'
df_pred_1.drop(['annual_inc'], axis=1, inplace=True)


# ### Binning the variable 'emp_lenght'

# In[226]:


df_pred_1['work_year'] = df_pred_1['emp_length']


# In[227]:


df_pred_1['work_year'].replace(to_replace=['10+ years'],
           value= [0], 
           inplace=True)


# In[228]:


df_pred_1['work_year'] = df_pred_1['work_year'].str.slice(0, -5, 1) 


# In[229]:


df_pred_1


# In[230]:


df_pred_1['work_year'].fillna(0, inplace=True)


# In[231]:


df_pred_1['work_year'].replace(to_replace=[0],
           value= ['10'], 
           inplace=True)


# In[232]:


df_pred_1


# In[233]:


df_pred_1['work_year'].replace(to_replace=['MI'],
           value= [0], 
           inplace=True)


# In[234]:


df_pred_1['work_year'].replace(to_replace=['< 1'],
           value= ['0.5'], 
           inplace=True)


# In[235]:


df_pred_1


# In[236]:


df_pred_1.drop(['emp_length'], axis=1, inplace=True)


# In[238]:


df_pred_1['work_year'].value_counts()


# In[239]:


df_pred_1['work_year'] = pd.to_numeric(df_pred_1['work_year'])


# In[240]:


df_pred_1['work_year'] = df_pred_1['work_year'].astype(int)


# In[241]:


Workyears_binned = pd.qcut(df_pred_1['work_year'], q=3)


# In[242]:


Workyears_binned.value_counts()


# In[243]:


df_pred_1['Workyears_binned'] = pd.qcut(df_pred_1['work_year'], q=3, labels=[1, 2, 3])


# In[244]:


df_pred_1.drop(['work_year'], axis=1, inplace=True)


# In[245]:


df_pred_1


# ### Training first model with Logistic Regression

# In[246]:


from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.metrics import precision_score
from sklearn.metrics import recall_score


# In[247]:


X = df_pred_1[['Rent', 'Mortgage', 'Own', 'Incomes_binned', 'Workyears_binned']]


# In[250]:


y = df_pred_1['Loan_status']


# In[251]:


X_test, X_train, y_test, y_train = train_test_split(X, y)


# In[252]:


m_logistic = LogisticRegression(random_state=10)


# In[253]:


m_logistic.fit(X_train, y_train)


# In[254]:


ypred_logistic = m_logistic.predict(X_train) # accuracy score
accuracy_logistic = accuracy_score(y_train, ypred_logistic)
accuracy_logistic


# In[255]:


m_logistic.score(X_train, y_train)


# In[256]:


precision_logistic = precision_score(y_train, ypred_logistic)
precision_logistic # precision score


# In[257]:


recall_score(y_train, ypred_logistic) # recall score


# ### Model with variable employment length 1 hot encoding

# In[221]:


df_emp = df


# In[222]:


df_emp['emp_title'].fillna('MISSING', inplace=True)


# In[225]:


encode_emp_lenght = pd.get_dummies(df_emp['emp_length'])


# In[226]:


encode_emp_lenght


# In[444]:


df_pred2 = pd.concat([df_plotting, encode_emp_lenght], axis=1)


# In[448]:


df_pred2['Rent'] = df_pred['RENT'] + df_pred['ANY'] + df_pred['OTHER'] + df_pred['MISSING'] + df_pred['NONE']


# In[449]:


df_pred2['Mortgage'] = df_pred['MORTGAGE']


# In[450]:


df_pred2['Own'] = df_pred['OWN']


# In[453]:


df_pred2['Incomes_binned'] = df_pred1['Incomes_binned']


# In[455]:


df_pred2.drop(['emp_length', 'home_ownership', 'annual_inc'], axis=1, inplace=True)


# In[456]:


df_pred2


# In[459]:


X = df_pred2[['Rent', 'Mortgage', 'Own', 'Incomes_binned', '1 year', '10+ years', '2 years', '3 years', '4 years', '5 years', '6 years', '7 years', '8 years', '9 years', '< 1 year', 'MISSING']]


# In[460]:


y = df_pred1['Loan_status']


# In[461]:


X_test, X_train, y_test, y_train = train_test_split(X, y)


# In[497]:


X


# In[462]:


m_logistic = LogisticRegression(random_state=10)


# In[463]:


m_logistic.fit(X_train, y_train)


# In[464]:


ypred_logistic = m_logistic.predict(X_train) # accuracy score
accuracy_logistic = accuracy_score(y_train, ypred_logistic)
accuracy_logistic


# ### Decision trees

# In[258]:


from sklearn.tree import DecisionTreeClassifier, plot_tree
from sklearn.model_selection import train_test_split


# In[259]:


X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.5, random_state=42)


# In[260]:


X_train


# In[262]:


y = df_pred_1['Loan_status']


# In[263]:


m = DecisionTreeClassifier(max_depth=2)  


# In[264]:


m.fit(X_train, y_train)


# In[265]:


ypred = m.predict(X_train) # accuracy score


# In[266]:


accuracy_decisiontree = accuracy_score(y_train, ypred)


# In[267]:


accuracy_decisiontree


# ### Random forest

# In[268]:


from sklearn.ensemble import RandomForestClassifier


# In[ ]:


m = RandomForestClassifier(n_estimators=10, max_depth=2, random_state=42)


# In[ ]:


m.fit(X_train, y_train)


# In[ ]:


m.score(X_train, y_train)

