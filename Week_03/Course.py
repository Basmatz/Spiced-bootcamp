import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split

df = sns.load_dataset("anscombe")

X = pd.DataFrame(df["x"])
y = pd.DataFrame(df["y"])

print(df.x.shape)
print(df.y.shape)

X_train, X_test, y_train, y_test = train_test_split(X, y, train_size=0.8, test_size=0.2, random_state=0)

# sns.lmplot(x="x", y="y",
#             hue="dataset",
#             col="dataset",
#             ci=None,
#             height=4,
#             data=df)

# grid = sns.FacetGrid(df, col="dataset")
# grid = grid.map(plt.scatter, "x", "y")
# grid = grid.map(sns.lmplot, x="x", y="y", data=df)
#sns.scatterplot(x=df.x, y=df.y, hue=df.dataset)

plt.show()

m = LinearRegression()

m.fit(X_train,y_train)

print(m.score(X_train,y_train))

pred = m.predict(X_test)

print(m.score(y_test, pred))
