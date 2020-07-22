from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.ensemble import RandomForestClassifier
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from xgboost import XGBRegressor
from xgboost import XGBClassifier
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from matplotlib import pyplot as plt
from sklearn.metrics import mean_absolute_error
import seaborn as sns
import category_encoders as ce
from sklearn.dummy import DummyClassifier
from sklearn.metrics import plot_confusion_matrix

df = pd.read_csv("train.csv")

cat_cols = ["Sex", "Ticket", "Cabin", "Embarked"]
num_cols = ["PassengerId", "Pclass", "Age", "SibSp", "Parch", "Fare"]

m_dummy = DummyClassifier()


#X = df[data_cols].join(encoded)
y = df.Survived
X = df.drop(["Survived"], axis=1)


X_train, X_valid, y_train, y_valid = train_test_split(X, y,
                                                      train_size=0.8,
                                                      test_size=0.2,
                                                      random_state=0
                                                      )


# Preprocessing for numerical data
numerical_transformer = SimpleImputer(strategy='constant')

# Preprocessing for categorical data
categorical_transformer = Pipeline(steps=[
    ('imputer', SimpleImputer(strategy='most_frequent')),
    ('OneHot', OneHotEncoder(handle_unknown="ignore"))
])



# # Create the encoder
# count_enc = ce.CountEncoder()
#
# # Transform the features, rename the columns with the _count suffix, and join to dataframe
# count_encoded = count_enc.fit_transform(ks[cat_features])
# data = data.join(count_encoded.add_suffix("_count"))
#
# # Train a model
# train, valid, test = get_data_splits(data)
# train_model(train, valid)

# Bundle preprocessing for numerical and categorical data
preprocessor = ColumnTransformer(
    transformers=[
        ('num', numerical_transformer, num_cols),
        ('cat', categorical_transformer, cat_cols)
    ])

#Random Forest model
model = RandomForestClassifier(n_estimators=1000, random_state=0)


# Bundle preprocessing and modeling code in a pipeline
my_pipeline = Pipeline(steps=[('preprocessor', preprocessor),
                              ('model', model)
                             ])

my_pipeline.fit(X_train, y_train)

preds = my_pipeline.predict(X_valid)

print("Score: ", my_pipeline.score(X_valid, y_valid))

# Evaluate the model
score = mean_absolute_error(y_valid, preds)
print('MAE:', score)

# plot_confusion_matrix(my_pipeline, X_train, y_train)
# plt.show()

# # Preprocessing for numerical data
# numerical_transformer = SimpleImputer(strategy='mean')
#
# # Imputation
# imputed_X_train_num = pd.DataFrame(numerical_transformer.fit_transform(X_train[num_cols]))
# imputed_X_valid_num = pd.DataFrame(numerical_transformer.transform(X_valid[num_cols]))
#
# # Imputation removed column names; put them back
# imputed_X_train_num.columns = X_train[num_cols].columns
# imputed_X_valid_num.columns = X_valid[num_cols].columns
#
# # Preprocessing for categorical data
# categorical_transformer = SimpleImputer(strategy='most_frequent')
#
# # Imputation
# imputed_X_train_cat = pd.DataFrame(categorical_transformer.fit_transform(X_train[cat_cols]))
# imputed_X_valid_cat = pd.DataFrame(categorical_transformer.transform(X_valid[cat_cols]))
#
# # Imputation removed column names; put them back
# imputed_X_train_cat.columns = X_train[cat_cols].columns
# imputed_X_valid_cat.columns = X_valid[cat_cols].columns
#
# # Apply one-hot encoder to each column with categorical data
# OH_encoder = OneHotEncoder(handle_unknown='ignore', sparse=False)
# imputed_X_train_cat = pd.DataFrame(OH_encoder.fit_transform(imputed_X_train_cat))
# imputed_X_valid_cat = pd.DataFrame(OH_encoder.transform(imputed_X_valid_cat))
#
#
# X_train_final = imputed_X_train_cat.join(imputed_X_train_num)
# X_valid_final = imputed_X_valid_cat.join(imputed_X_valid_num)


# #Logistic Regression model
# model = LogisticRegression(random_state=0,
#                            max_iter=10000
#                            )
#
# model.fit(X_train_final, y_train)
#
# ypred_test = model.predict(X_valid_final)
#
# print(model.score(X_valid_final, y_valid))
#
# #Random Forest model
# model = RandomForestRegressor(n_estimators=100, random_state=0)
#
# model.fit(X_train_final, y_train)
#
# ypred_test = model.predict(X_valid_final)
#
# print(model.score(X_valid_final, y_valid))
#
#
#
# #XGBoost
# model = XGBClassifier(n_estimators=1000, learning_rate=0.05, n_jobs=4)
# model.fit(X_train_final, y_train,
#              early_stopping_rounds=50,
#              eval_set=[(X_valid_final, y_valid)],
#              verbose=False)
#
# ypred_test = model.predict(X_valid_final)
#
# print(model.score(X_valid_final, y_valid))
#
# from sklearn.model_selection import cross_val_score
#
# # Multiply by -1 since sklearn calculates *negative* MAE
# scores = -1 * cross_val_score(model, X_valid_final, y_valid,
#                               cv=5,
#                               scoring='neg_mean_absolute_error')
#
# print("MAE scores:\n", scores)
# print("Average MAE score (across experiments):")
# print(scores.mean())

# # Preprocessing for categorical data
# categorical_transformer = Pipeline(steps=[
#     ('imputer', SimpleImputer(strategy='most_frequent')),
#     ('label', LabelEncoder())
# ])
#
# # Bundle preprocessing for numerical and categorical data
# preprocessor = ColumnTransformer(
#     transformers=[
#         ('num', numerical_transformer, num_cols),
#         ('cat', categorical_transformer, cat_cols)
#     ])



# # Bundle preprocessing and modeling code in a pipeline
# my_pipeline = Pipeline(steps=[('preprocessor', preprocessor),
#                               ('model', model)
#                              ])
#
# # Preprocessing of training data, fit model
# my_pipeline.fit(X_train, y_train)
#
# # Preprocessing of validation data, get predictions
# preds = my_pipeline.predict(X_valid)


# encoder = LabelEncoder()
# encoded = df[cat_features].apply(encoder.fit_transform)



desired_width = 300

pd.set_option('display.width', desired_width)
pd.set_option('display.max_columns',20)


#number of surviving/non-surviving passengers
survived = df[df["Survived"]==1].Survived.value_counts()
died = df[df["Survived"]==0].Survived.value_counts()


#seaborn plot
plt.figure(figsize=(10,6))
# plt.title("Number of surviving/non-surviving passengers")
# barplot = sns.barplot(x=df["Survived"].unique(), y=df["Survived"].value_counts())
# barplot.set_xticklabels(["Died", "Survived"])
# plt.ylabel("Number of passengers")
# plt.show()

#proportion of surviving 1st class passengers with regards to the total number of 1st class passengers.

# print((df.loc[(df["Survived"]==1) & (df["Pclass"]==1)].Survived.count()) / (df[df["Pclass"]==1].Pclass.count()))


#bar plot with separate bars for male/female passengers and 1st/2nd/3rd class passengers.

# sns.countplot(x=df.Pclass, hue=df.Sex)
# plt.ylabel("Number of passengers")
# plt.xlabel("Class")
# plt.show()


#a histogram showing the age distribution of passengers. Compare surviving/non-surviving passengers.

# survivedage = df["Age"].loc[df["Survived"] == 1].dropna()
# diedage = df["Age"].loc[df["Survived"] == 0].dropna()
#
# fig, ax=plt.subplots(2)
# sns.distplot(df.Age.dropna(), bins=30, kde=False, ax=ax[0], label="Age", color="blue")
#

# sns.distplot(survivedage, bins=30, kde=False, ax=ax[1], label="Survived", color="green")
# sns.distplot(diedage, bins=30, kde=False, ax=ax[1], color="red")
# plt.legend(labels=['Age', 'Survived', 'Died'])
# plt.show()


# #Calculate the average age for survived and drowned passengers separately.
#
# print("Average age for survived: ", df["Age"].loc[df["Survived"] == 1].mean())
# print("Average age for died: ", df["Age"].loc[df["Survived"] == 0].mean())
#
# #Replace missing age values by the mean age.

#print(df["Age"].fillna(value=df["Age"].mean()))

tdf = df.groupby(["Pclass", "Sex",]).transform("mean")["Age"]
print(tdf)

#Create a table counting the number of surviving/dead passengers separately for 1st/2nd/3rd class and male/female.

tdf = df.groupby(["Pclass", "Sex",])["Survived"].count()
#.apply(print)#