from bs4 import BeautifulSoup
import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from api import *

# Get input of date and store it in variable
date = input("Enter date (YYYY-MM-DD): ")
url = "https://www.billboard.com/charts/hot-100/"+date+""
print(url)
response = requests.get(url)
soup = BeautifulSoup(response.text, "lxml")
# print(soup.prettify())

# Get the song title and artist
title = soup.find_all("h3", class_="c-title a-no-trucate a-font-primary-bold-s u-letter-spacing-0021 lrv-u-font-size-18@tablet lrv-u-font-size-16 u-line-height-125 u-line-height-normal@mobile-max a-truncate-ellipsis u-max-width-330 u-max-width-230@tablet-only")
artist = soup.find_all("span", class_="c-label a-no-trucate a-font-primary-s lrv-u-font-size-14@mobile-max u-line-height-normal@mobile-max u-letter-spacing-0021 lrv-u-display-block a-truncate-ellipsis-2line u-max-width-330 u-max-width-230@tablet-only")
title = [i.text.strip() for i in title]
artist = [i.text.strip() for i in artist]
print(title)
print(artist)
print(len(title))
print(len(artist))

song_list = dict(zip(title, artist))

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=spotify_client_id,
                                               client_secret=spotify_client_secret,
                                               scope="playlist-modify-private",
                                               redirect_uri="http://localhost:8888/callback",
                                               show_dialog=True,
                                               cache_path="token.txt"
                                               ))
user_id = sp.current_user()["id"]
# playlist_id = sp.user_playlist_create(user=user_id, name=date, public=False)["id"]
print(user_id)
# to search for a track in spotify
# with open('token.txt') as f:
#     token = f.read()
# sp = spotipy.Spotify(auth=token)
song_uris = []
for i in range(len(title)):
    result = sp.search(q=f'artist:{artist[i]} track:{title[i]}', type='track')
    # print(result)
    try:
        uri = result["tracks"]["items"][0]["uri"]
        song_uris.append(uri)
    except IndexError:
        print(f"{title[i]} doesn't exist in Spotify. Skipped.")

# print(song_uris)
# dict_song_uris = dict(zip(song_uris))
# print(dict_song_uris)
# Create a playlist in spotify and add the songs
playlist_id = sp.user_playlist_create(user=user_id, name=date, public=False)["id"]
print(playlist_id)
sp.user_playlist_add_tracks(user=user_id, playlist_id=playlist_id, tracks=song_uris)
print(f"{date} playlist created and songs added.")

