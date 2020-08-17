

### Import

import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from pylab import rcParams
from statsmodels.tsa.seasonal import seasonal_decompose

#Set Plot Size
rcParams['figure.figsize'] = 16,9


### Read Data

df = pd.read_csv("TG_STAID002759.txt")



### Rename Colummns

df.columns = ["Souid", "Date", "TG", "Q_TG"]



### Convert to datetime

df["Date"] = pd.to_datetime(df["Date"], format='%Y%m%d')

df.set_index("Date", inplace=True)

df["year"] = df.index.year
df["month"] = df.index.month
df["day"] = df.index.day


### Handle Outliers

df.loc['1945-04-25':'1945-11-05', 'TG'] = (df['1946-04-25':'1946-11-05']["TG"].values
                                           + df['1944-04-25':'1944-11-05']["TG"].values) / 2
df["Q_TG"].loc[df['Q_TG'] == 9] = 1


### Transform to Kelvin

df["TG"] /= 10
#df["TG"] +=  273.15


### Train Test Split

y_train = df[:'2019'].copy()
y_test = df['2020'].copy()


### Detrend time series Data

y_train["difference"] = y_train["TG"].diff().fillna(0.0)
y_train["difference"]



### De-seasonalize the series by subtracting daily means

y_train["daily_means"] = y_train.groupby("day")["difference"].transform("mean")
y_train["daily_means"]


## Baseline model

y0_train = y_train.iloc[0]['TG']

y_train.loc[0,'month_means'] = y0_train

y_train['Prediction'] = np.cumsum(y_train['month_means'])