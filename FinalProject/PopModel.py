# SET SPOTIPY_CLIENT_ID = 76e34e7d6b9449899623db078669c2be
# SET SPOTIPY_CLIENT_SECRET= f79c6f2fdc5545cb90d377f2498498e8
#
# SET SPOTIPY_CLIENT_ID = 76e34e7d6b9449899623db078669c2be
# SET SPOTIPY_CLIENT_SECRET= f79c6f2fdc5545cb90d377f2498498e8

# shows artist info for a URN or URL

import spotipy
from spotipy.oauth2 import SpotifyOAuth

sp = spotipy.Spotify(auth_manager=SpotifyOAuth())

response = sp.new_releases()

while response:
    albums = response['albums']
    for i, item in enumerate(albums['items']):
        print(albums['offset'] + i, item['name'])

    if albums['next']:
        response = sp.next(albums)
    else:
        response = None
