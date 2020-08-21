# Script to get Svalbard temperature and precipitation files into the desired format.

# aims: add station id to each file, save as separate files

import pandas as pd
import os
import zipfile
import time
from tqdm import tqdm


# - find IDs and names of Svalbard weather stations
# - read in only those files; add a col for station id
# - save as CSV

arctic_stations = pd.read_csv('arctic_stations.csv')
arctic_stations = arctic_stations.drop(['LAT', 'LON'], axis=1)

# make file list
zip_TG = zipfile.ZipFile('ECA_blend_tg.zip').namelist()
zip_RR = zipfile.ZipFile('ECA_blend_rr.zip').namelist()
# need these separately for opening
zf_TG = zipfile.ZipFile('ECA_blend_tg.zip')
zf_RR = zipfile.ZipFile('ECA_blend_rr.zip')

files_TG = [f for f in zip_TG if not f.startswith('.') and f.startswith('TG_STAID')]
files_RR = [f for f in zip_RR if not f.startswith('.') and f.startswith('RR_STAID')]


def find_stations(lat_min, lat_max, lon_min, lon_max):
    '''
    Finds all weather stations within min and max lat and lon values
    '''
    stations = arctic_stations[arctic_stations['LAT_dec'] > lat_min]
    stations = stations[stations['LAT_dec'] < lat_max]
    stations = stations[stations['LON_dec'] > lon_min]
    stations = stations[stations['LON_dec'] < lon_max]
    return stations[['STAID', 'STANAME']]


def station_id_to_char(id):
    '''
    Turns numeric Station ID into character STAID
    '''
    len_zeros = 6 - len(str(id))
    id_char = (str(0) * len_zeros) + str(id)
    return id_char

def process_files(staid, type, zip_list, zip_folder):
    '''
    processes files according to staid (weather station id; numeric); data type (string; 'TG' = temperature data, 'RR' = precipitation data); zip_list (list of files in zip folder for each data type), zip_folder (zipfile opener)
    '''
    temporary_weather = []
    filename_txt = f'{str(type)}_STAID' + staid + '.txt'
    if filename_txt in zip_list:
        filename_csv = f'{type}_STAID' + staid + '.csv'
        weather = pd.read_csv(zip_folder.open(filename_txt), sep=',', skiprows=20)
        weather.columns = weather.columns.map(str.strip)
        # remove all rows that are missing data
        weather = weather[weather[f'Q_{type}'] != 9]
        weather['DATE'] = pd.to_datetime(weather['DATE'], format = '%Y%m%d')
        weather['YEAR'] = pd.to_datetime(weather['DATE']).dt.year
        weather['MONTH'] = pd.to_datetime(weather['DATE']).dt.month
        weather['WEEK'] = pd.to_datetime(weather['DATE']).dt.week
        weather['YEAR_MONTH'] = weather['YEAR'].astype(str) + ' ' + weather['MONTH'].astype(str)
        weather[str(type)] = weather[str(type)] / 10
        temporary_weather.append(weather)
        csv_weather = pd.concat(temporary_weather)
        csv_weather.to_csv(f'svalbard_{type}/' + filename_csv, index=False)


###############################

if __name__ == '__main__':

    station_id_chars = []
    station_id_final_tg = []
    station_id_final_rr = []

    # get Svalbard weather stations
    # SVALBARD COORDS: 74° - 81° N, 10° - 35° E
    svalbard_stations = find_stations(74, 81, 10, 35)
    station_id = list(svalbard_stations['STAID'])

    # get string versions of station IDs from Arctic weather station set
    for id in station_id:
        station_id_char = station_id_to_char(id)
        station_id_chars.append(station_id_char)

    # create list of the filenames that we actually have data for:
    for staid in station_id_chars:
        filename = 'TG_STAID' + staid + '.txt'
        if filename in files_TG:
            station_id_final_tg.append(staid)

    for staid in station_id_chars:
        filename = 'RR_STAID' + staid + '.txt'
        if filename in files_RR:
            station_id_final_rr.append(staid)

    # loop over files in each data folder
    for staid in tqdm(station_id_final_tg):
        process_files(staid, 'TG', zip_TG, zf_TG)

    for staid in tqdm(station_id_final_rr):
        process_files(staid, 'RR', zip_RR, zf_RR)


#
