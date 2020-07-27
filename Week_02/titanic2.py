# Import our libraries
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt

# Import sklearn libraries
from sklearn.model_selection import train_test_split, GridSearchCV, StratifiedKFold, cross_val_score
from sklearn.model_selection import cross_validate
from sklearn.metrics import accuracy_score, precision_score, recall_score, roc_curve, precision_recall_curve, auc, make_scorer, confusion_matrix, f1_score, fbeta_score

# Import the Naive Bayes, logistic regression, Bagging, RandomForest, AdaBoost, GradientBoost, Decision Trees and SVM Classifier

from sklearn.naive_bayes import MultinomialNB
from sklearn.ensemble import BaggingClassifier, RandomForestClassifier, AdaBoostClassifier, GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn import svm
from xgboost import XGBClassifier

import seaborn as sns
#from matplotlib import style
#plt.style.use('bmh')
#plt.style.use('ggplot')
#plt.style.use('seaborn-notebook')


from matplotlib.ticker import StrMethodFormatter

from sklearn.preprocessing import StandardScaler, MinMaxScaler, LabelBinarizer
import re

train_df = pd.read_csv("train.csv")
test_df = pd.read_csv("test.csv")

data = [train_df, test_df]

for dataset in data:
    mean = train_df["Age"].mean()
    std = test_df["Age"].std()
    is_null = dataset["Age"].isnull().sum()
    # compute random numbers between the mean, std and is_null
    rand_age = np.random.randint(mean - std, mean + std, size = is_null)
    # fill NaN values in Age column with random values generated
    age_slice = dataset["Age"].copy()
    age_slice[np.isnan(age_slice)] = rand_age
    dataset["Age"] = age_slice
    dataset["Age"] = train_df["Age"].astype(int)

embarked_mode = train_df['Embarked'].mode()
data = [train_df, test_df]
for dataset in data:
    dataset['Embarked'] = dataset['Embarked'].fillna(embarked_mode)

#SibSp + Parch = TravelledAlone
data = [train_df, test_df]
for dataset in data:
    dataset['relatives'] = dataset['SibSp'] + dataset['Parch']
    dataset.loc[dataset['relatives'] > 0, 'travelled_alone'] = 'No'
    dataset.loc[dataset['relatives'] == 0, 'travelled_alone'] = 'Yes'

# Drop 'PassengerId' from the train set, because it does not contribute to a persons survival probability.
train_df = train_df.drop(['PassengerId'], axis=1)

#Transform the Cabin category into the Deck number
deck = {"A": "A", "B": "B", "C": "C", "D": "D", "E": "E", "F": "F", "G": "G", "U": "U"}
data = [train_df, test_df]

for dataset in data:
    dataset['Cabin'] = dataset['Cabin'].fillna("U0")
    dataset['Deck'] = dataset['Cabin'].map(lambda x: re.compile("([a-zA-Z]+)").search(x).group())
    dataset['Deck'] = dataset['Deck'].map(deck)
    dataset['Deck'] = dataset['Deck'].fillna("U")
    #dataset['Deck'] = dataset['Deck'].astype(int)

# we can now drop the cabin feature
train_df = train_df.drop(['Cabin'], axis=1)
test_df = test_df.drop(['Cabin'], axis=1)


data = [train_df, test_df]


#Age fill NA with random numbers calculated by the STD of the mean.
for dataset in data:
    mean = train_df["Age"].mean()
    std = test_df["Age"].std()
    is_null = dataset["Age"].isnull().sum()
    # compute random numbers between the mean, std and is_null
    rand_age = np.random.randint(mean - std, mean + std, size = is_null)
    # fill NaN values in Age column with random values generated
    age_slice = dataset["Age"].copy()
    age_slice[np.isnan(age_slice)] = rand_age
    dataset["Age"] = age_slice
    dataset["Age"] = train_df["Age"].astype(int)


#Fill Embark column with mode (S). (Better to fill proportional wise between the three locations?)
common_value = train_df['Embarked'].mode().to_string(index=False).strip()

data = [train_df, test_df]

for dataset in data:
    dataset['Embarked'] = dataset['Embarked'].fillna(common_value)

#Fill NA in Fare with zeros and convert Fare from Float to Int. (Better to fill with mean or Mode?)
data = [train_df, test_df]

for dataset in data:
    dataset['Fare'] = dataset['Fare'].fillna(0)
    dataset['Fare'] = dataset['Fare'].astype(int)


#Name: Extract titles from name and build a new feature from that (Maybe leave it out and only fillNA?)

train_titles = train_df.Name.str.extract(' ([A-Za-z]+)\.', expand=False)

data = [train_df, test_df]
titles = {"Mr": 1, "Miss": 2, "Mrs": 3, "Master": 4, "Rare": 5}

for dataset in data:
    # extract titles
    dataset['Title'] = dataset.Name.str.extract(' ([A-Za-z]+)\.', expand=False)
    # replace titles with a more common title or as Rare
    dataset['Title'] = dataset['Title'].replace(['Lady', 'Countess','Capt', 'Col','Don', 'Dr',\
                                            'Major', 'Rev', 'Sir', 'Jonkheer', 'Dona'], 'Rare')
    dataset['Title'] = dataset['Title'].replace('Mlle', 'Miss')
    dataset['Title'] = dataset['Title'].replace('Ms', 'Miss')
    dataset['Title'] = dataset['Title'].replace('Mme', 'Mrs')
    # convert titles into numbers
    #dataset['Title'] = dataset['Title'].map(titles)
    # filling NaN with 0, to get safe
    dataset['Title'] = dataset['Title'].fillna("NA")
train_df = train_df.drop(['Name'], axis=1)
test_df = test_df.drop(['Name'], axis=1)

#Convert Sex into numbers (Maybe leave it categorical?)
genders = {"male": 0, "female": 1}
#data = [train_df, test_df]

for dataset in data:
    dataset['Sex'] = dataset['Sex'].map(genders)

#Drop Ticket Column
train_df = train_df.drop(['Ticket'], axis=1)
test_df = test_df.drop(['Ticket'], axis=1)

#Convert Embark to numbers (Maybe leave it categorical?)
ports = {"S": 0, "C": 1, "Q": 2}
#data = [train_df, test_df]

for dataset in data:
    dataset['Embarked'] = dataset['Embarked'].map(ports)

#Age multiplied by Class
data = [train_df, test_df]
for dataset in data:
    dataset['Age_Class']= dataset['Age']* dataset['Pclass']

#Fare per person
for dataset in data:
    dataset['Fare_Per_Person'] = dataset['Fare']/(dataset['relatives']+1)
    dataset['Fare_Per_Person'] = dataset['Fare_Per_Person'].astype(int)

#Binning the Age in different groups. (Better do it with qcut or KBinsDiscretizer?)
data = [train_df, test_df]
for dataset in data:
    dataset['Age'] = dataset['Age'].astype(int)
    dataset.loc[dataset['Age'] <= 11, 'Age'] = 0
    dataset.loc[(dataset['Age'] > 11) & (dataset['Age'] <= 18), 'Age'] = 1
    dataset.loc[(dataset['Age'] > 18) & (dataset['Age'] <= 22), 'Age'] = 2
    dataset.loc[(dataset['Age'] > 22) & (dataset['Age'] <= 27), 'Age'] = 3
    dataset.loc[(dataset['Age'] > 27) & (dataset['Age'] <= 33), 'Age'] = 4
    dataset.loc[(dataset['Age'] > 33) & (dataset['Age'] <= 40), 'Age'] = 5
    dataset.loc[(dataset['Age'] > 40) & (dataset['Age'] <= 66), 'Age'] = 6
    dataset.loc[dataset['Age'] > 66, 'Age'] = 7

    dataset['Age'] = dataset['Age'].astype(str)
    dataset.loc[dataset['Age'] == '0', 'Age'] = "Children"
    dataset.loc[dataset['Age'] == '1', 'Age'] = "Teens"
    dataset.loc[dataset['Age'] == '2', 'Age'] = "Youngsters"
    dataset.loc[dataset['Age'] == '3', 'Age'] = "Young Adults"
    dataset.loc[dataset['Age'] == '4', 'Age'] = "Adults"
    dataset.loc[dataset['Age'] == '5', 'Age'] = "Middle Age"
    dataset.loc[dataset['Age'] == '6', 'Age'] = "Senior"
    dataset.loc[dataset['Age'] == '7', 'Age'] = "Retired"

# let's see how it's distributed
# print(train_df['Age'].value_counts())

#Add Fare Bins
data = [train_df, test_df]

for dataset in data:
    dataset.loc[dataset['Fare'] <= 7.91, 'Fare'] = 0
    dataset.loc[(dataset['Fare'] > 7.91) & (dataset['Fare'] <= 14.454), 'Fare'] = 1
    dataset.loc[(dataset['Fare'] > 14.454) & (dataset['Fare'] <= 31), 'Fare'] = 2
    dataset.loc[(dataset['Fare'] > 31) & (dataset['Fare'] <= 99), 'Fare'] = 3
    dataset.loc[(dataset['Fare'] > 99) & (dataset['Fare'] <= 250), 'Fare'] = 4
    dataset.loc[dataset['Fare'] > 250, 'Fare'] = 5
    dataset['Fare'] = dataset['Fare'].astype(int)

    dataset['Fare'] = dataset['Fare'].astype(str)
    dataset.loc[dataset['Fare'] == '0', 'Fare'] = "Extremely Low"
    dataset.loc[dataset['Fare'] == '1', 'Fare'] = "Very Low"
    dataset.loc[dataset['Fare'] == '2', 'Fare'] = "Low"
    dataset.loc[dataset['Fare'] == '3', 'Fare'] = "High"
    dataset.loc[dataset['Fare'] == '4', 'Fare'] = "Very High"
    dataset.loc[dataset['Fare'] == '5', 'Fare'] = "Extremely High"


#Converting class into Strings
data = [train_df, test_df]

for dataset in data:
    dataset['Pclass'] = dataset['Pclass'].astype(str)
    dataset.loc[ dataset['Pclass'] == '1', 'Pclass'] = "Class1"
    dataset.loc[ dataset['Pclass'] == '2', 'Pclass'] = "Class2"
    dataset.loc[ dataset['Pclass'] == '3', 'Pclass'] = "Class3"

# let's see how it's distributed
# print(train_df['Age'].value_counts())
#
# print(train_df.info())

# Capture all the numerical features so that we can scale them later
#data = [train_df, test_df]
train_numerical_features = list(train_df.select_dtypes(include=['int64', 'float64', 'int32']).columns)

#Take out y
del train_numerical_features[0]

# Feature scaling - Standard scaler
ss_scaler = StandardScaler()
train_df_ss = pd.DataFrame(data = train_df)
train_df_ss[train_numerical_features] = ss_scaler.fit_transform(train_df_ss[train_numerical_features])

#Same For Testset
test_numerical_features = list(test_df.select_dtypes(include=['int64', 'float64', 'int32']).columns)

del test_numerical_features[0]

# Feature scaling - Standard scaler
test_ss_scaler = StandardScaler()
test_df_ss = pd.DataFrame(data = test_df)
test_df_ss[test_numerical_features] = test_ss_scaler.fit_transform(test_df_ss[test_numerical_features])

# One-Hot encoding / Dummy variables
encode_col_list = list(train_df.select_dtypes(include=['object']).columns)

for i in encode_col_list:
    train_df_ss = pd.concat([train_df_ss,pd.get_dummies(train_df_ss[i], prefix=i)],axis=1)
    train_df_ss.drop(i, axis = 1, inplace=True)

# One-Hot encoding / Dummy variables
test_encode_col_list = list(test_df.select_dtypes(include=['object']).columns)

for i in test_encode_col_list:
    test_df_ss = pd.concat([test_df_ss,pd.get_dummies(test_df_ss[i], prefix=i)],axis=1)
    test_df_ss.drop(i, axis = 1, inplace=True)

#ML Modelling
X_train = train_df_ss.drop("Survived", axis=1)
Y_train = train_df_ss["Survived"]
X_test  = test_df_ss.drop("PassengerId", axis=1).copy()


###Logistic Regression
# Instantiate our model
logreg = LogisticRegression()

# Fit our model to the training data
logreg.fit(X_train, Y_train)

# Predict on the test data
logreg_predictions = logreg.predict(X_test)

logreg_data = pd.read_csv('test.csv')
logreg_data.insert((logreg_data.shape[1]),'Survived',logreg_predictions)

#logreg_data.to_csv('LogisticRegression_SS_OH_FE2.csv')

###Adaptive Boosting
# Instantiate our model
adaboost = AdaBoostClassifier()

# Fit our model to the training data
adaboost.fit(X_train, Y_train)

# Predict on the test data
adaboost_predictions = adaboost.predict(X_test)

adaboost_data = pd.read_csv('test.csv')
adaboost_data.insert((adaboost_data.shape[1]),'Survived',adaboost_predictions)

#adaboost_data.to_csv('AdaptiveBoosting_SS_OH_FE.csv')

###Bagging Classifier
# Instantiate our model
bag = BaggingClassifier()

# Fit our model to the training data
bag.fit(X_train, Y_train)

# Predict on the test data
bag_predictions = bag.predict(X_test)

bag_data = pd.read_csv('test.csv')
bag_data.insert((bag_data.shape[1]),'Survived',bag_predictions)

#bag_data.to_csv('Bagging.csv')



#rf_data.to_csv('RandomForest_SS_OH.csv')


###Decision Trees
# Instantiate our model
dt = DecisionTreeClassifier()
dt.fit(X_train, Y_train)

dt_predictions = dt.predict(X_test)

dt_data = pd.read_csv('test.csv')
dt_data.insert((dt_data.shape[1]),'Survived',dt_predictions)

#dt_data.to_csv('DecisionTrees.csv')


###Gradient Boost
# Instantiate our model
gb = GradientBoostingClassifier()
gb.fit(X_train, Y_train)

gb_predictions = gb.predict(X_test)

gb_data = pd.read_csv('test.csv')
gb_data.insert((gb_data.shape[1]),'Survived',gb_predictions)

#gb_data.to_csv('GradientBoost_SS_OH_FE.csv')


###XGBoost
# Instantiate our model
xg = XGBClassifier(learning_rate=0.02, n_estimators=750,
                   max_depth= 3, min_child_weight= 1,
                   colsample_bytree= 0.6, gamma= 0.0,
                   reg_alpha= 0.001, subsample= 0.8
                  )
xg.fit(X_train, Y_train)

xg_predictions = xg.predict(X_test)

xg_data = pd.read_csv('test.csv')
xg_data.insert((xg_data.shape[1]),'Survived',xg_predictions)

#xg_data.to_csv('XGBoost_SS_OH_FE_GSCV.csv')









###Imports
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import GridSearchCV

###Random Forest Classifier

random_forest = RandomForestClassifier(random_state=0)


###GridSearchCV


params = { "n_estimators": [10,25,50,75,100,125,150,175,200],
           "min_samples_split" : range(2,15),
           "criterion" : ["gini", "entropy"]
           }

gsearch = GridSearchCV(estimator=random_forest,
                       param_grid=params,
                       cv=3,
                       verbose=1,
                       n_jobs=-1
                       )

gsearch.fit(X_train, Y_train)

print("\nScore: " + str(round(gsearch.score(X_train, Y_train),4)))

print("\nBest Parameters: "+ str(gsearch.best_params_))