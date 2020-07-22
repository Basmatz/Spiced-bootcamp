import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split


desired_width = 300

pd.set_option('display.width', desired_width)
pd.set_option('display.max_columns',20)

df = pd.read_csv("all_penguins_clean.csv")

df.dropna(inplace=True)

X = df[["Culmen Depth (mm)", "Culmen Length (mm)"]]
y = df["Species"]

print(X)

sns.scatterplot(x=X.iloc[:,0], y=X.iloc[:,1], hue=y)
plt.show()

predictions = []

for i, row in X.iterrows():
    if row["Culmen Length (mm)"] < 43:
        if row["Culmen Depth (mm)"] > 15:
            predictions.append("Adelie")
        else:
            predictions.append(("Gentoo"))
    else:
        if row["Culmen Depth (mm)"] > 17:
            predictions.append("Chinstrap")
        else:
            predictions.append("Gentoo")



from sklearn.metrics import accuracy_score

print(round(accuracy_score(predictions, y), 2))


X_train, X_test, y_train, y_test = train_test_split(X,y,train_size=0.8, test_size=0.2, random_state=0)

#Random Forest model
model = RandomForestClassifier(n_estimators=1000, random_state=0)

model.fit(X_train, y_train)

ypred = model.predict(X_test)

print(model.score(X_test,y_test))