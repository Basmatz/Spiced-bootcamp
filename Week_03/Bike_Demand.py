import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import OneHotEncoder
from sklearn.model_selection import train_test_split
import time

pd.set_option('display.width', 300)
pd.set_option('display.max_columns',20)

train = pd.read_csv("train.csv")
test = pd.read_csv("test.csv")


X = train.drop(["count","casual","registered"], axis=1)
y = train["count"]

#Transform date column to datetime format
train["datetime"] = pd.to_datetime(train["datetime"])

#Create column for weekend
train.loc[(train["datetime"].apply(lambda x: x.weekday() > 4)), "weekend"] = 1
train.loc[(train["datetime"].apply(lambda x: x.weekday() <= 4)), "weekend"] = 0

cats = [#"datetime",
        "season",
        "holiday",
        "workingday",
        "weather",
        "temp",
        "atemp",
        "humidity",
        "windspeed",
        "weekend"
        ]

train["hour"] = train["datetime"].dt.hour
train["day"] = train["datetime"].dt.day
train["month"] = train["datetime"].dt.month
train["year"] = train["datetime"].dt.year
train["yday"] = train["datetime"].dt.dayofyear


df = train["count"].loc[
            (train["holiday"] == 0)
        ].mean()


df = train.loc[
    (train["holiday"] == 1)
    & (train["year"] == 2012)
                    ]

counti = train["count"].loc[
    (train["holiday"] == 1)
    & (train["year"] == 2011)
                    ].mean()

print(counti)

#fig, axs = plt.subplots()
fig = sns.regplot(x="hour",y="count",data=df)
fig.set(ylim=(-20,900),xlim=(-5,30))

df = train.loc[
            (train["holiday"] == 0)
            & (train["year"] == 2012)
            & (train["yday"].isin(range(194,201)))
        ]

counti = train["count"].loc[
            (train["holiday"] == 0)
            & (train["year"] == 2011)
            & (train["yday"].isin(range(194,201)))
        ].mean()

print(counti)

fig2 = sns.regplot(x="hour",y="count",data=df)
fig2.set(ylim=(-20,900),xlim=(-5,30))

sns.pairplot(df[["hour","count",
        "temp",
        "atemp",
        "humidity",
        #"windspeed",
        "holiday"
        ]], palette="husl", kind="reg")

plt.show()




































# X_train, X_test, y_train, y_test = train_test_split(X[cats], y, train_size=0.8, test_size=0.2, random_state=0)
#
# m = LinearRegression()
#
# m.fit(X_train,y_train)
#
# print(m.score(X_train,y_train))