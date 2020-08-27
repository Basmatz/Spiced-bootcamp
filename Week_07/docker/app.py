import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd
import time
from datetime import datetime
from sqlalchemy import create_engine

##### Spotify API auth

cid = "76e34e7d6b9449899623db078669c2be"
secret = "f79c6f2fdc5545cb90d377f2498498e8"

client_credentials_manager = SpotifyClientCredentials(client_id=cid, client_secret=secret)
sp = spotipy.Spotify(client_credentials_manager = client_credentials_manager)


##### Setting up database connection

conns = 'postgresql://postgres:11223344@database-1.c10qo0hdky8j.eu-central-1.rds.amazonaws.com:5432/test'

db = create_engine(conns, encoding='latin1', echo=False)

##### variables set up

track_id = []
artist_name = []
track_name = []
release_date = []
popularity = []

new_albums = pd.DataFrame()

##### Get existing Album IDs


query = "SELECT album_id FROM test_albums;"

existing_ids = pd.read_sql(query, db)
existing_ids


###### Get new Albums and append in dataframe if not in database yet


for i in range(0,51,50):
    response = sp.new_releases(country="DE",limit=50, offset=i)
    #print(response)
    albums = response['albums']
    for u, item in enumerate(albums['items']):
        if item["id"] not in existing_ids.values:
            new_albums = new_albums.append({'album_id': item["id"],
                                'artist_name': item["artists"][0]["name"],
                                'album_name': item["name"],
                                'release_date': datetime.strptime((item["release_date"]),"%Y-%m-%d"),
                                'total_tracks': item["total_tracks"],
                                'release_date_precision': item["release_date_precision"],
                                'survey_date': datetime(*time.localtime(time.time())[0:3])
                                },
                                ignore_index=True)


##### Append new albums to databse
new_albums.to_sql("test_albums", db, if_exists='append')


#%%
##### Get the tracks from each album

query = "SELECT album_id, album_name, release_date, release_date_precision, survey_date, total_tracks FROM test_albums;"

album_ids = pd.read_sql(query, db)
album_ids["album_id"]


#%%


query = "SELECT track_id FROM test_songs;"

existing_song_ids = pd.read_sql(query, db)
existing_song_ids



#%%
song_ids = pd.DataFrame()

for id in album_ids["album_id"].values:
    response = sp.album_tracks(id, limit=50)
    tracks = response['items']
    for track in tracks:
        song_ids = song_ids.append({'track_id': track["id"]}, ignore_index=True)



#%%
song_ids

#%%

new_songs = pd.DataFrame()

for id in song_ids.values:
    track = sp.track(id[0])
    if track["id"] not in existing_song_ids.values:
        new_songs = new_songs.append({'track_id': track["id"],
                            'new_entry': True,
                            'artist_name': track["album"]["artists"][0]["name"],
                            'album_name': track["album"]["name"],
                            'track_name': track["name"],
                            'release_date': datetime.strptime((track["album"]["release_date"]),"%Y-%m-%d"),
                            'release_date_precision': track["album"]["release_date_precision"],
                            'total_tracks': track["album"]["total_tracks"],
                            'survey_date': datetime(*time.localtime(time.time())[0:3]),
                            'explicit': track["explicit"],
                            'duration_ms': track["duration_ms"],
                            'track_number': track["track_number"],
                            'popularity': track["popularity"],
                            'disc_number': track["disc_number"]
                            },
                            ignore_index=True)
    else:
        new_songs = new_songs.append({'track_id': track["id"],
                            'new_entry': False,
                            'artist_name': track["album"]["artists"][0]["name"],
                            'album_name': track["album"]["name"],
                            'track_name': track["name"],
                            'release_date': datetime.strptime((track["album"]["release_date"]),"%Y-%m-%d"),
                            'release_date_precision': track["album"]["release_date_precision"],
                            'total_tracks': track["album"]["total_tracks"],
                            'survey_date': datetime(*time.localtime(time.time())[0:3]),
                            'explicit': track["explicit"],
                            'duration_ms': track["duration_ms"],
                            'track_number': track["track_number"],
                            'popularity': track["popularity"],
                            'disc_number': track["disc_number"]
                            },
                            ignore_index=True)


#%%
new_songs.to_sql("test_songs", db, if_exists='append')

#%%