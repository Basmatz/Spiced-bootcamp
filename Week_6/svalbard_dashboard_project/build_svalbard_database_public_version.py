### script to build svalbard DATABASE

# if running on EC2 machine

# sudo yum groupinstall ‘Development Tools’
# sudo yum install python-devel
#
# sudo yum pandas
# print('installed pandas')
#
# sudo yum tqdm
# print("installed tqdm")
#
# sudo yum sqlalchemy
# print("installed sqlalchemy")
#
# sudo yum psycopg2
# print("installed psycopg2")
#
# sudo yum os
# print("installed os")

# imports
import pandas as pd
import sqlalchemy
from sqlalchemy import create_engine
import psycopg2
import os
from tqdm import tqdm


# connect to DATABASE

# conn = f'postgres://{logisticlemongrass.c1ipxvq2s9x8.eu-central-1.rds.amazonaws.com}{lara}'

HOST = ''# ENTER CONNECTION LINK HERE
PORT = '5432'
USER = 'postgres'
PASSWORD = '' # ENTER PASSWORD
DATABASE = 'lara'

conn = f'postgres://{USER}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}'

# create tables
create_tables_query = '''
DROP TABLE IF EXISTS svalbard_stations;
DROP TABLE IF EXISTS svalbard_temperature;
DROP TABLE IF EXISTS svalbard_precipitation;

CREATE TABLE svalbard_temperature (
index SERIAL PRIMARY KEY,
staid SMALLINT,
souid SMALLINT,
date DATE,
tg SMALLINT,
q_tg SMALLINT,
year SMALLINT,
month SMALLINT,
week SMALLINT,
year_month VARCHAR(20)
);

CREATE TABLE svalbard_precipitation (
index SERIAL PRIMARY KEY,
staid SMALLINT,
souid SMALLINT,
date DATE,
rr SMALLINT,
q_rr SMALLINT,
year SMALLINT,
month SMALLINT,
week SMALLINT,
year_month VARCHAR(20)
);
'''


# read in and process files

def clean_data(file, directory):
    '''
    processes data to clean it up & assign correct data types before sending to database
    file: name of file to be read in (csv format)
    directory: string, either /svalbard_RR or /svalbard_TG
    '''
    data = pd.read_csv(directory + file)
    data['DATE'] = pd.to_datetime(data['DATE'])
    data.columns = data.columns.map(str.lower)
    return data

# first, add weather stations data
svalbard_stations = pd.read_csv('/Users/laraehrenhofer/Documents/Coding_Projects/git_repos/logistic-lemongrass-student-code/Week_6/svalbard_dashboard_project/arctic_stations.csv')

svalbard_stations = svalbard_stations.drop(['LAT', 'LON'], axis = 1)
svalbard_stations.columns = svalbard_stations.columns.map(str.strip)
svalbard_stations.columns = svalbard_stations.columns.map(str.lower)


drop_all = '''
DROP TABLE IF EXISTS svalbard_stations;
DROP TABLE IF EXISTS svalbard_temperature;
DROP TABLE IF EXISTS svalbard_precipitation;
'''

# engine.execute(drop_all)

# then need to create an initial table for both temp and precip

files_RR = [f for f in os.listdir('svalbard_RR/') if not f.startswith('.')]
first_precip = clean_data(files_RR[0], 'svalbard_RR/')

files_TG = [f for f in os.listdir('svalbard_TG/') if not f.startswith('.')]
first_temp = pd.read_csv('svalbard_TG/' + files_TG[0])
first_temp = clean_data(files_TG[0], 'svalbard_TG/')


##########################

if __name__ == '__main__':

    engine = create_engine(conn, encoding = 'latin1', echo= False)
    print('created engine')

    # wipe database clean

    # engine.execute(drop_all)
    # print('dropped previous tables')

    # engine.execute(create_tables_query)
    # print('created new tables')

    svalbard_stations.to_sql('svalbard_stations', engine, method = 'multi')
    print('created new table with svalbard weather station info')

    first_precip.to_sql('svalbard_precipitation', engine, if_exists = 'append', method = 'multi')
    print('added first precip file')
    for precip in tqdm(files_RR[1:]):
        data = clean_data(precip, 'svalbard_RR/')
        # data = data.head(2)
        data.to_sql('svalbard_precipitation', engine, if_exists = 'append', method = 'multi')
        print(f'added file {precip} to precipitation table in database')
    print(f'done with precipitation files \n \n')

    print('launching temperature files')
    first_temp.to_sql('svalbard_temperature', engine, if_exists = 'append', method = 'multi')
    print('added first temp file')
    for temp in tqdm(files_TG[1:]):
        data = clean_data(temp, 'svalbard_TG/')
        # data = data.head(2)
        data.to_sql('svalbard_temperature', engine, if_exists = 'append', method = 'multi')
        print(f'added file {temp} to precipitation table in database')








#
