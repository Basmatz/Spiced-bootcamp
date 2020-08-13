### ARIMA model for 6 Arctic weather stations on Spitsbergen/Svalbard



# imports
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
from datetime import date, timedelta
from statsmodels.graphics.tsaplots import plot_acf

# get data

svalbard_stations = ['000186', '002755', '018777', '019036', '018099', '019003', '018145', '018181', '002756']
svalbard_names = ['Svalbard Airport', 'Isford Radio', 'Barentsburg', 'Green Harbour', 'Pyramiden', 'Longyearbyen', 'Adventdalen', 'Sveagruva', 'Sveagruva II']

# took out: 'Janssonhaugen Vest','Reindalspasset',

svalbard_dict = dict(zip(svalbard_stations, svalbard_names))

type(svalbard_stations[0])


def get_data(staid):
    filename = 'all_weather_data/TG_STAID' + str(staid) + '.txt'
    data = pd.read_csv(filename, sep = ',', skiprows = 20)
    return data

svalbard = []

for staid in svalbard_stations:
    data = get_data(staid)
    data['STANAME'] = svalbard_dict[staid]
    svalbard.append(data)

svalbard = pd.concat(svalbard)

svalbard.columns = svalbard.columns.map(str.strip)
# svalbard.columns

svalbard['DATE'] = pd.to_datetime(svalbard['DATE'], format = '%Y%m%d')
svalbard['YEAR'] = pd.to_datetime(svalbard['DATE']).dt.year
svalbard['MONTH'] = pd.to_datetime(svalbard['DATE']).dt.month
svalbard['WEEK'] = pd.to_datetime(svalbard['DATE']).dt.week
svalbard['DAY'] = pd.to_datetime(svalbard['DATE']).dt.day
svalbard['YEAR_WEEK'] = svalbard['YEAR'].astype(str) + ' ' + svalbard['WEEK'].astype(str)
svalbard['YEAR_MONTH'] = svalbard['YEAR'].astype(str) + ' ' + svalbard['MONTH'].astype(str)

len(svalbard)

# find missing values everywhere
missing = svalbard.groupby(['STANAME'])['Q_TG'].value_counts()

missing

# plot missing values -- I want to see a) when each weather station is active, b) whether they are all missing data on the same days or if there is hope of using group averages from that day

def plot_q_tg(station):
    sns.lineplot(x = 'DATE', y = 'Q_TG', data = svalbard.loc[svalbard['STANAME'] == station])
    plt.xlim(svalbard['DATE'].min(), svalbard['DATE'].max())
    plt.title(str(station))
    plt.show()
    plt.close()

for station in svalbard_names:
    plot_q_tg(station)


### DATA DECISION:
# If data is actually missing, delete this line -- since the model will be able to fall back on other nearby weather stations
# If data is unreliable, replace with the average of the entire group... leave this for later.

svalbard = svalbard[svalbard.Q_TG != 9]

# check again:
for station in svalbard_names:
    plot_q_tg(station)

# for each year check balance of no. lines contributed by each station... leave this for later too

# average by week and month for each weather station
svalbard.columns

svalbard['weekly_mean'] = svalbard.groupby('YEAR_WEEK')['TG'].transform('mean')
svalbard['monthly_mean'] = svalbard.groupby('YEAR_MONTH')['TG'].transform('mean')

# Check for trends, seasons etc. -- do I need to de-trend etc. before building a model?
print(plot_acf(svalbard['weekly_mean'], lags=100))

# looks like there is a slight trend -- check seasonality
print(plot_acf(svalbard['monthly_mean'], lags=100))


# looks like there is v little seasonality (maybe not surprising? it is always cold on Svalbard...)
# but it can't hurt to both de-season and de-trend the data.

# first do a train-test split: training = first 20 days of each month, test = rest
# y_train = svalbard[svalbard.DAY < 20]
# y_test = svalbard[svalbard.DAY < 20]

y_train = svalbard[svalbard['DATE'] < pd.to_datetime('2020-05-31')]
y_test = svalbard[svalbard['DATE'] > pd.to_datetime('2020-05-31')]

# Need to re-do the average temps to avoid test-train contamination.

y_train['weekly_mean'] = y_train.groupby(['YEAR_WEEK', 'STANAME'])['TG'].transform('mean')
y_train['monthly_mean'] = y_train.groupby(['YEAR_MONTH', 'STANAME'])['TG'].transform('mean')

y_test['weekly_mean'] = y_test.groupby(['YEAR_WEEK', 'STANAME'])['TG'].transform('mean')
y_test['monthly_mean'] = y_test.groupby(['YEAR_MONTH', 'STANAME'])['TG'].transform('mean')

y_train.STANAME.value_counts()

# some plotting of the temps

plt.figure(figsize = (20,8))
sns.lineplot(x = 'DATE', y = 'weekly_mean', data = y_train, hue = 'STANAME', alpha = .3)

# find the gaps in different stations' dataset

longyearbyen = svalbard[svalbard['STANAME'] == 'Longyearbyen']

longyearbyen.iloc[3000]

longyearbyen.iloc[3012]

longyearbyen.iloc[3013]




deltas = longyearbyen['DATE'].diff()

deltas.to_csv('deltas.csv')


longyearbyen[1910:1925]



# Filter diffs (here days > 1, but could be seconds, hours, etc)
gaps = deltas[deltas > timedelta(days=1)]

gaps


for i, g in gaps.iteritems():
    print(i)
    print(g)
    # gap_start = longyearbyen['DATE'][i - 1]
    # print(f'Start: {datetime.strftime(gap_start, "%Y-%m-%d")} | '
    #       f'Duration: {str(g.to_pytimedelta())}')

len(gaps)

gaps

gaps2 = gaps.reset_index()
gaps2.columns = ['index','gap size']

index = 1919

longyearbyen.iloc[index]

longyearbyen.iloc[index+1]

longyearbyen.iloc[index+2]

longyearbyen.iloc[index-1]

gap_info = []
for index in gaps2['index']:
    # gap_info.append(svalbard.loc[row])

gaps2

gaps
















#
