### ARIMA model for Arctic weather stations on Spitsbergen/Svalbard



# imports
import pandas as pd
import seaborn as sns
import os
import matplotlib.pyplot as plt
import numpy as np
from datetime import date, timedelta
from statsmodels.graphics.tsaplots import plot_acf
from statsmodels.api import OLS, add_constant
from statsmodels.tsa.arima_model import ARIMA

# get data

all_stations = pd.read_csv('all_stations_latlon_converted.csv')


def find_stations(lat_min, lat_max, lon_min, lon_max):
    '''
    Returns weather information for all stations within a certain min/max range for latitude and longitude.
    Takes integers.
    Based on csv with all stations' latitude and longitude converted into decimal.
    '''
    stations = all_stations[all_stations['LAT_dec'] > lat_min]
    stations = stations[stations['LAT_dec'] < lat_max]
    stations = stations[stations['LON_dec'] > lon_min]
    stations = stations[stations['LON_dec'] < lon_max]
    return stations[['STAID', 'STANAME']]


# Svalbard archipelago is between 74°-81° N, 10°-35°E

all_svalbard_stations = find_stations(74, 81, 10, 35)

len(all_svalbard_stations)

svalbard_staids = list(all_svalbard_stations['STAID'])
svalbard_names = list(all_svalbard_stations['STANAME'].str.strip())

# convert staids to strings:
def station_id_to_char(id):
    '''
    Converts int station IDs into 6 digit string, with remainder filled with 0
    '''
    len_zeros = 6 - len(str(id))
    id_char = (str(0) * len_zeros) + str(id)
    return id_char

svalbard_staid_chars = []
for id in svalbard_staids:
    station_id_char = station_id_to_char(id)
    svalbard_staid_chars.append(station_id_char)

svalbard_dict = dict(zip(svalbard_staid_chars, svalbard_names))

files = [f for f in os.listdir('all_weather_data/') if not f.startswith('.') and f.startswith('TG_STAID')]

def get_data(staid, filename):
    '''
    Get data for a specific weather station ID and filename
    '''
    data = pd.read_csv('all_weather_data/' + filename, sep = ',', skiprows = 20)
    return data

svalbard = []
missing_data_staid = []

for staid in svalbard_staid_chars:
    filename = 'TG_STAID' + str(staid) + '.txt'
    print(filename)
    if filename in files:
        print(f'found filename {filename}')
        dat = get_data(staid, filename)
        dat['STANAME'] = svalbard_dict[staid]
        svalbard.append(dat)
    else:
        print(f'no data available for station {staid}')
        missing_data_staid.append(staid)


# take the stations we have no temp data for out of the list of stations
missing_data_staname = [svalbard_dict[x] for x in missing_data_staid]

svalbard_names_stripped = [x for x in svalbard_names if x not in missing_data_staname]

svalbard = pd.concat(svalbard)
# svalbard = svalbard.reset_index()

svalbard.columns = svalbard.columns.map(str.strip)

# svalbard.columns

svalbard['DATE'] = pd.to_datetime(svalbard['DATE'], format = '%Y%m%d')
svalbard['YEAR'] = pd.to_datetime(svalbard['DATE']).dt.year
svalbard['MONTH'] = pd.to_datetime(svalbard['DATE']).dt.month
svalbard['WEEK'] = pd.to_datetime(svalbard['DATE']).dt.week
svalbard['DAY'] = pd.to_datetime(svalbard['DATE']).dt.day
svalbard['YEAR_WEEK'] = svalbard['YEAR'].astype(str) + ' ' + svalbard['WEEK'].astype(str)
svalbard['YEAR_MONTH'] = svalbard['YEAR'].astype(str) + ' ' + svalbard['MONTH'].astype(str)

# find missing values everywhere
missing = svalbard.groupby(['STANAME'])['Q_TG'].value_counts()
missing

# plot missing values -- I want to see a) when each weather station is active, b) whether they are all missing data on the same days or if there is hope of using group averages from that day

def plot_q_tg(station):
    '''
    Plot missing values in separate plot for each station
    '''
    sns.lineplot(x = 'DATE', y = 'Q_TG', data = svalbard.loc[svalbard['STANAME'] == station])
    plt.xlim(svalbard['DATE'].min(), svalbard['DATE'].max())
    plt.title(str(station))
    plt.show()
    plt.close()

for station in svalbard_names_stripped:
    plot_q_tg(station)


### DATA DECISION:
# If data is actually missing, delete this line -- since the model will be able to fall back on other nearby weather stations
# If data is unreliable, replace with the average of the entire group... leave this for later.

svalbard = svalbard[svalbard.Q_TG != 9]

# check again:
# for station in svalbard_names:
#     plot_q_tg(station)

# for each year check balance of no. lines contributed by each station... leave this for later too


###### TEST-TRAIN SPLIT.
###### since we are getting into averaging, etc. territory...

y_train = svalbard[svalbard['DATE'] <= pd.to_datetime('1999-12-31')]
y_test = svalbard[svalbard['DATE'] > pd.to_datetime('1999-12-31')]

# average by week and month for each weather station; transform by mean.

y_train['weekly_mean'] = y_train.groupby(['YEAR_WEEK', 'STAID'])['TG'].transform('mean')
y_train['monthly_mean'] = y_train.groupby(['YEAR_MONTH', 'STAID'])['TG'].transform('mean')

# Check for trends, seasons etc. -- do I need to de-trend etc. before building a model?
print(plot_acf(y_train['weekly_mean'], lags=100))

# looks like there is a slight trend -- check seasonality
print(plot_acf(y_train['monthly_mean'], lags=100))


# looks like there is v little seasonality (maybe not surprising? it is always cold on Svalbard...)
# but it can't hurt to both de-season and de-trend the data.

# some plotting of the temps

plt.figure(figsize = (20,8))
sns.lineplot(x = 'DATE', y = 'weekly_mean', data = y_train, hue = 'STANAME', alpha = .3)



# DE-TREND AND DE-SEASON DATA.
# there is a strong seasonal effect, as we see in the plot above
# we saw from the autocorrelation plot that there is also a trends

# first, determine whether the trend is linear or quadratic

# add timestep: it needs to align by datetime, rather than by the index.

# len(y_train)
min_date = y_train['DATE'].min()
max_date = y_train['DATE'].max()

def get_timestep(date):
    timestep = date - min_date # timestep is a Timedelta object
    return timestep.days

# make linear timestep
y_train['TIMESTEP'] = y_train['DATE'].apply(get_timestep)

# plot just to check.
plt.plot(y_train['DATE'], y_train['TIMESTEP'])

# make quadratic TIMESTEP
y_train['TIMESTEP_sq'] = y_train['TIMESTEP']**2
plt.plot(y_train['DATE'], y_train['TIMESTEP_sq'])


# check if linear or quadratic timestep works better.
X = add_constant(y_train['TIMESTEP'])

X_sq = add_constant(y_train[['TIMESTEP', 'TIMESTEP_sq']])

# y_train.columns

m = OLS(y_train['monthly_mean'], X)
results = m.fit()
results.summary()


m_sq = OLS(y_train['monthly_mean'], X_sq)
results_sq = m_sq.fit()
results_sq.summary()

# conclusion: need to use quadratic timestep

## now actually de-trend & de-season
list_of_weather_data = list(y_train.groupby(['STAID']))

for i, station in list_of_weather_data:
    station['weekly_pct_change'] = station['weekly_mean'].pct_change()

dataframes = [station for i, station in list_of_weather_data]

y_train2 = pd.concat(dataframes)


# quick plots

y_train2['weekly_pct_change'].plot()


#### train ARIMA model
y_train2.columns

m_ar = ARIMA(list(y_train2['weekly_mean']), (1, 2, 2)) # (ar, d, ma) <- Order of the ARIMA model
m_ar.initialize()
results = m_ar.fit()
results.summary()















#
