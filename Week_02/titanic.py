from sklearn.linear_model import LogisticRegression
import pandas as pd
from sklearn.model_selection import train_test_split

from sklearn.preprocessing import LabelEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer

desired_width = 300

pd.set_option('display.width', desired_width)
pd.set_option('display.max_columns',20)

df = pd.read_csv("train.csv")

cat_cols = ["Sex", "Ticket", "Cabin", "Embarked"]
num_cols = ["PassengerId", "Pclass", "Age", "SibSp", "Parch", "Fare"]
#df.dropna(#subset=data_cols, inplace=True)


#X = df[data_cols].join(encoded)
y = df.Survived
X = df.drop(["Survived", "Name"], axis=1)


X_train, X_valid, y_train, y_valid = train_test_split(X, y,
                                                      train_size=0.8,
                                                      test_size=0.2,
                                                      random_state=0
                                                      )

# Preprocessing for numerical data
numerical_transformer = SimpleImputer(strategy='mean')

# Imputation
imputed_X_train_num = pd.DataFrame(numerical_transformer.fit_transform(X_train[num_cols]))
imputed_X_valid_num = pd.DataFrame(numerical_transformer.transform(X_valid[num_cols]))

# Imputation removed column names; put them back
imputed_X_train_num.columns = X_train[num_cols].columns
imputed_X_valid_num.columns = X_valid[num_cols].columns

# Preprocessing for categorical data
categorical_transformer = SimpleImputer(strategy='most_frequent')

# Imputation
imputed_X_train_cat = pd.DataFrame(categorical_transformer.fit_transform(X_train[cat_cols]))
imputed_X_valid_cat = pd.DataFrame(categorical_transformer.transform(X_valid[cat_cols]))

# Imputation removed column names; put them back
imputed_X_train_cat.columns = X_train[cat_cols].columns
imputed_X_valid_cat.columns = X_valid[cat_cols].columns

# Label Encoding
cat_encoder = LabelEncoder()

for col in cat_cols:
    imputed_X_train_cat[col] = cat_encoder.fit_transform(imputed_X_train_cat[col])
    imputed_X_valid_cat[col] = cat_encoder.transform(imputed_X_valid_cat[col])


X_train_final = imputed_X_train_cat.join(imputed_X_train_num)
X_valid_final = imputed_X_valid_cat.join(imputed_X_valid_num)


#Define Logistic Regression model
model = LogisticRegression(random_state=0,
                           max_iter=1000
                           )


model.fit(X_train_final, y_train)

ypred_test = model.predict(X_valid_final)

print(model.score(X_valid_final, ypred_test))

print(ypred_test)


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



