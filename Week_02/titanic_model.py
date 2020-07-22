from sklearn.ensemble import RandomForestClassifier
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer

df = pd.read_csv("train.csv")
test = pd.read_csv("test.csv")

cat_cols = ["Sex", "Ticket", "Cabin", "Embarked"]
num_cols = ["PassengerId", "Pclass", "Age", "SibSp", "Parch", "Fare"]

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

preds = my_pipeline.predict(test)

print("Score: ", my_pipeline.score(X_valid, y_valid))

# Save test predictions to file
output = pd.DataFrame({'PassengerId': test.PassengerId,
                       'Survived': preds})

output.to_csv('submission.csv', index=False)