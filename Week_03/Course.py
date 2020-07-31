import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
import seaborn as sns
import matplotlib.pyplot as plt
# Show PolynomialFeatures
from sklearn.preprocessing import PolynomialFeatures
from sklearn.model_selection import cross_val_score
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

plt.figure(figsize=(14, 5))

np.random.seed(42)
x = np.linspace(0, 20, 15)
y = 5 * x + np.random.normal(0.0, 20.0, 15)
X = x.reshape(15, 1)

#sns.regplot(x=X, y=y)
#plt.show()

# Create a polynomial feature transformer
polynomial_transformer = PolynomialFeatures(degree=3, include_bias=False)

poly = polynomial_transformer.fit_transform(X)

poly = pd.DataFrame(poly)

print(poly[[0,1]])
#
# sns.regplot(x=X, y=poly[x0^3])
# #plt.show()
#
linear_regressor = LinearRegression()

linear_regressor.fit(poly,y)

pred = linear_regressor.predict(poly)


print(X)
print(pred)

sns.pointplot(x=x, y=pred, markers="", color="r")
sns.pointplot(x=x, y=y, markers="o", linestyles="")
plt.show()


scaler = StandardScaler()

scaled = scaler.fit_transform(poly)

scaled2 = pd.DataFrame(scaled, columns=scaler.get_feature_names())
print(scaled2)












<

degrees = [2,5,9]

def true_fun(X):
    return np.cos(1.5 * np.pi * X)

for i in degrees:
    ax = plt.subplot(1, len(degrees), i + 1)
    plt.setp(ax, xticks=(), yticks=())

    # Make a pipeline
    polynomial_features = PolynomialFeatures(degree=degrees[i],
                                             include_bias=True)
    linear_regression = LinearRegression()
    pipeline = Pipeline([("polynomial_features", polynomial_features),
                         ("linear_regression", linear_regression)])
    pipeline.fit(x[:, np.newaxis], y)

    # Evaluate the models using crossvalidation
    scores = cross_val_score(pipeline, x[:, np.newaxis], y,
                             scoring="neg_mean_squared_error", cv=10)

    # Actually plot the function
    X_test = np.linspace(0, 1, 100)
    plt.plot(X_test, pipeline.predict(X_test[:, np.newaxis]), label="Model")
    plt.plot(X_test, true_fun(X_test), label="True function")
    plt.scatter(X, y, edgecolor='b', s=20, label="Samples")
    plt.xlabel("x")
    plt.ylabel("y")
    plt.xlim((0, 1))
    plt.ylim((-2, 2))
    plt.legend(loc="best")
    plt.title("Degree {}\nMSE = {:.2e}(+/- {:.2e})".format(
        degrees[i], -scores.mean(), scores.std()))

plt.show()>