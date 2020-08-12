### this will find me the weather stations I'm interested in: in the ARCTIC

import pandas as pd
import re
import os

### read in data.
all_stations = pd.read_csv('ECA_all_stations.txt', sep = ',', skiprows = 17)

all_stations.columns=all_stations.columns.map(str.strip)

# convert to decimal latitude and longitude
places = ['LAT', 'LON']

def make_lat_lon_cols(dimension):
    place_cols = all_stations[f'{dimension}'].str.split(':', 2, expand = True)
    place_cols.columns = [f'{dimension}_h', f'{dimension}_m', f'{dimension}_s']
    place_cols_num = place_cols.apply(pd.to_numeric)
    return place_cols_num

# Decimal Degrees = degrees + (minutes/60) + (seconds/3600)
def convert_lat_lon(LatLon):
    dd_lat = LatLon[0] + (LatLon[1]/60) + (LatLon[2]/3600)
    dd_lon = LatLon[3] + (LatLon[4]/60) + (LatLon[5]/3600)
    return dd_lat, dd_lon

LatLon = pd.DataFrame([])

for place in places:
    new = make_lat_lon_cols(place)
    LatLon = pd.concat([LatLon, new], axis = 1)

LatLon

LatLonConverted = []

for row in LatLon.iterrows():
    print(row)

LatLonConverted

for row in LatLon:
    print(row)
    # converted = convert_lat_lon(line)
    # LatLonConverted.append(converted)

# turn lat and lon variables into numbers instead of strings
# this is a hacky way to get at anything above 66° N (I don't know how to deal with lat/lon data yet)

all_stations = all_stations.replace(to_replace =':\d\d$', value = '', regex = True)
all_stations = all_stations.replace(to_replace ='\+', value = '', regex = True)
all_stations = all_stations.replace(to_replace =':', value = '.', regex = True)
all_stations.LAT = pd.to_numeric(all_stations.LAT)
all_stations.LON = pd.to_numeric(all_stations.LON
all_stations.HGHT = pd.to_numeric(all_stations.HGHT)


all_stations.head(10)
all_stations.info()


# find all of the stations north of the Arctic Circle
# the arctic circle is at approx. 66°
# so filter out those stations whose lat is above 66°

arctic = all_stations[all_stations.LAT >= 66]

arctic.columns

arctic.STANAME = arctic['STANAME'].str.strip()

arctic.STAID = pd.to_numeric(arctic.STAID)
arctic.HGHT = pd.to_numeric(arctic.HGHT)

# Create a dictionary linking STAID with all other data

arctic = arctic.set_index('STAID')

arctic

# don't need this dict after all
# station_dict = arctic.T.to_dict('list')
#
# station_dict

station_id = list(arctic.index)

# station_id

#### Concatenate data from Arctic stations only to create data set

arctic_data = pd.DataFrame([])

files = [f for f in os.listdir('all_weather_data/') if not f.startswith('.') and f.startswith('TG_STAID')]

# def get_station_info(dict):

all_weather = []
all_stations = []

for f in files[1:15]:
    staid = re.findall("TG_STAID(\d+).txt", f)[0]
    staid = pd.to_numeric(staid)
    print(staid)
    if staid in station_id:
        weather = pd.read_csv('all_weather_data/'+f, sep = ',', skiprows = 20)
        all_weather.append(weather)
        station_info = pd.DataFrame([arctic.loc[staid]] * len(weather))
        all_stations.append(station_info)

pd_weather = pd.concat(all_weather)
pd_stations = pd.concat(all_stations)

pd_weather.shape, pd_stations.shape

pd_weather.head()
pd_stations.head()

all_data =

# all_data = pd.merge(pd_stations, pd_weather)




#
