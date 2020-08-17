
# SET SPOTIPY_CLIENT_ID = 76e34e7d6b9449899623db078669c2be
# SET SPOTIPY_CLIENT_SECRET= f79c6f2fdc5545cb90d377f2498498e8

#util.prompt_for_user_token(username,scope,client_id='76e34e7d6b9449899623db078669c2be',client_secret='f79c6f2fdc5545cb90d377f2498498e8',redirect_uri='http://localhost/')

# # shows artist info for a URN or URL
#
# import spotipy
# from spotipy.oauth2 import SpotifyOAuth
#
# sp = spotipy.Spotify(auth_manager=SpotifyOAuth())
#
# response = sp.new_releases()
#
# while response:
#     albums = response['albums']
#     for i, item in enumerate(albums['items']):
#         print(albums['offset'] + i, item['name'])
#
#     if albums['next']:
#         response = sp.next(albums)
#     else:
#         response = None


import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
cid = "76e34e7d6b9449899623db078669c2be"
secret = "f79c6f2fdc5545cb90d377f2498498e8"
client_credentials_manager = SpotifyClientCredentials(client_id=cid, client_secret=secret)
sp = spotipy.Spotify(client_credentials_manager = client_credentials_manager)

artist_name = []
track_name = []
popularity = []
track_id = []

for i in range(0,10000,50):
    #track_results = sp.new_releases(country="DE", limit=50, offset=i)
    track_results = sp.search(q='classic', type='track', limit=50,offset=i)

    for i, t in enumerate(track_results['tracks']['items']):
        artist_name.append(t['artists'][0]['name'])
        track_name.append(t['name'])
        track_id.append(t['id'])
        popularity.append(t['popularity'])
        print("Artist: " + t['artists'][0]['name'])
        print("Track Name: " + t['name'])
        print("Popularity: " + str(t['popularity']))


print(sp.artist_top_tracks("spotify:artist:3jOstUTkEu2JkjvRdBA5Gu"))

shows artist info for a URN or URL
response = sp.new_releases(country="DE",limit=50, offset=0)
print(response)


for i in range(0,10000,50):
    response = sp.new_releases(country="DE",limit=50, offset=i)
    print(response)
    albums = response['albums']
    for u, item in enumerate(albums['items']):
        print(albums['offset'] + u, item['name'])

if albums['next']:
    response = sp.next(albums)
else:
    response = None