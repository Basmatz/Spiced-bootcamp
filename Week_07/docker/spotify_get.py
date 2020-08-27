import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd
import time
from datetime import datetime
from sqlalchemy import create_engine
import pymongo

##### Spotify API auth

cid = "76e34e7d6b9449899623db078669c2be"
secret = "f79c6f2fdc5545cb90d377f2498498e8"

client_credentials_manager = SpotifyClientCredentials(client_id=cid, client_secret=secret)
sp = spotipy.Spotify(client_credentials_manager = client_credentials_manager)


##### Setting up database connections
#### MongoDB
username = "bepeem"
password = "mongo11223344"
client = pymongo.MongoClient(f"mongodb+srv://{username}:{password}@cluster0.9vhde.mongodb.net/?retryWrites=true")
db_mongo = client.spotify
albums_db = db_mongo.albums
songs_info_db = db_mongo.songs_info
songs_features_db = db_mongo.songs_features
songs_analysis_db = db_mongo.songs_analysis

#####Postgtres
# conns = 'postgresql://postgres:11223344@database-1.c10qo0hdky8j.eu-central-1.rds.amazonaws.com:5432/test'
# db_pg2 = create_engine(conns, encoding='latin1', echo=False)

##### Get existing Album IDs
existing_albums = pd.DataFrame(albums_db.find())["id"].values

###### Get new Albums and append in database if not in existing yet

for i in range(0,51,50):
    response = sp.new_releases(country="DE",limit=50, offset=i)
    albums = response['albums']
    for item in albums['items']:
        if item["id"] not in existing_albums:
            item["survey_date"] = datetime(*time.localtime(time.time())[0:6])
            albums_db.insert_one(item)


##### Get updated list of existing Album IDs
existing_albums = pd.DataFrame(albums_db.find())["id"].values


for id in existing_albums:
    album_tracks = sp.album_tracks(id, limit=50)
    tracks = album_tracks['items']
    for track in tracks:
        track_info = sp.track(track["id"])
        track_info["survey_date"] = datetime(*time.localtime(time.time())[0:6])
        #track_features = sp.audio_features(track["id"])
        #track_analysis = sp.audio_analysis(track["id"])
        songs_info_db.insert_one(track_info)
        #songs_features_db.insert_one(track_features[0])
        # track_analysis["id"] = track["id"]
        # songs_analysis_db.insert_one(track_analysis)