### this will find me the weather stations I'm interested in: in the ARCTIC

import pandas as pd
import re
import os

### read in data.
all_stations = pd.read_csv('ECA_all_stations.txt', sep = ',', skiprows = 17)

all_stations.columns=all_stations.columns.map(str.strip)

# convert to decimal latitude and longitude

def make_lat_lon_cols(dimension):
    '''
    Split current degree:minute:second format of weather station location into separate columns.
    dimension = LAT or LON in original station data
    '''
    place_cols = all_stations[f'{dimension}'].str.split(':', 2, expand = True)
    place_cols.columns = [f'{dimension}_h', f'{dimension}_m', f'{dimension}_s']
    place_cols_num = place_cols.apply(pd.to_numeric)
    return place_cols_num

# Decimal Degrees = degrees + (minutes/60) + (seconds/3600)
def convert_lat_lon(LatLon):
    '''
    Converts lat/lon info from degrees, minutes, seconds to decimal
    LatLon has six cols in order degrees, min, sec for first lat, then lon
    Note: this function is set so indices will work inside the for loop below,
    which uses .iterrows(), where row[0] = the index
    '''
    dd_lat = LatLon[1] + (LatLon[2]/60) + (LatLon[3]/3600)
    dd_lon = LatLon[4] + (LatLon[5]/60) + (LatLon[6]/3600)
    return [dd_lat, dd_lon]

LatLon = pd.DataFrame([])

places = ['LAT', 'LON']

for place in places:
    new = make_lat_lon_cols(place)
    LatLon = pd.concat([LatLon, new], axis = 1)

# create separate list of lists with all of the converted lat/lon details in decimal format
LatLonConverted = []
for row in LatLon.itertuples():
    converted = convert_lat_lon(row)
    LatLonConverted.append(converted)

# turn into df for ease of merging.
LatLonConverted = pd.DataFrame(LatLonConverted)
LatLonConverted.columns = ['LAT_dec', 'LON_dec']

# add these back into stations data as new lat/lon coordinates
all_stations = all_stations.join(LatLonConverted)


# find all of the stations north of the Arctic Circle
# the arctic circle is at 66°33′48.2″ according to Wikipedia; convert to decimal
arctic_circle = 66 + 33/60 + 48.2/3600

arctic = all_stations[all_stations.LAT_dec >= arctic_circle]

# strip out whitespace in station names
arctic.STANAME = arctic['STANAME'].str.strip()

# this method/how-to may be useful for later...
# don't need this dict after all
# station_dict = arctic.T.to_dict('list')
# station_dict

# create list with arctic station ID numbers
station_id = list(arctic.STAID)

#### Get data from Arctic stations only to create final data set for project

arctic_data = pd.DataFrame([])

files = [f for f in os.listdir('all_weather_data/') if not f.startswith('.') and f.startswith('TG_STAID')]

# def get_station_info(dict):

all_arctic_weather = []
all_arctic_stations = []

for f in files:
    staid = re.findall("TG_STAID(\d+).txt", f)[0]
    staid = pd.to_numeric(staid)
    print(staid)
    if staid in station_id:
        weather = pd.read_csv('all_weather_data/'+f, sep = ',', skiprows = 20)
        all_arctic_weather.append(weather)
        # print(f'len of weather is ', len(weather))
        single_station_line = arctic.loc[arctic['STAID'] == staid]
        station_info = pd.concat([single_station_line] * len(weather), ignore_index = True)
        # print(f'len of station info is ', len(station_info))
        all_arctic_stations.append(station_info)

# wipe clean just in case
pd_weather = pd.DataFrame([])
pd_stations = pd.DataFrame([])

# all_arctic_weather, all_arctic_stations are both lists of lists -- turn them into data frames.
pd_weather = pd.concat(all_arctic_weather)
pd_stations = pd.concat(all_arctic_stations)

pd_weather.shape

# join things together, clean up
all_arctic = pd_weather.join(pd_stations, on = 'STAID', how='left', lsuffix='_left', rsuffix='_right')
all_arctic = all_arctic.drop(['STAID_right'], axis = 1)
all_arctic = all_arctic.rename({'STAID_left' : 'STAID'}, axis = 1)

# write out data as csv

all_arctic.to_csv('all_arctic.csv', index = False)

#
