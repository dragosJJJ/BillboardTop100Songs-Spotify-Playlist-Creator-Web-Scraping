from pprint import pprint

import requests, os, spotipy
from bs4 import BeautifulSoup
from spotipy.oauth2 import SpotifyClientCredentials, SpotifyOAuth

SPOTIFY_ID = os.environ["Spotify_ClientId"]
SPOTIFY_SECRET = os.environ["Spotify_ClientSecret"]
#same redirect URI as the one set in spotify settings
REDIRECT_URI = "http://example.com"
SCOPE = "playlist-modify-public"

date = input("Choose a particualr date for the top 100 songs. Type the date in this format YYYY-MM-DD: ")
URL = f"https://www.billboard.com/charts/hot-100/{date}"
SPOTIFY_URL = "https://api.spotify.com/v1/search"

response = requests.get(url=URL)

soup = BeautifulSoup(response.text, "html.parser")
songs = [song.find("h3").get_text(strip=True) for song in soup.find_all(class_="o-chart-results-list-row-container")]

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=SPOTIFY_ID, client_secret=SPOTIFY_SECRET, redirect_uri=REDIRECT_URI, scope=SCOPE))
user = sp.current_user()["id"]
playlist_params = {
    "user": user,
    "name": f"Top100Songs-{date}",
    "public": True,
    "description": "",
}
playlist_id = sp.user_playlist_create(** playlist_params)["id"]
tracks_URIs = []
for song in songs:
    results = sp.search(q=song, limit=1, type="track")
    if results["tracks"]["items"]:
        track_uri = results["tracks"]["items"][0]["uri"]
        tracks_URIs.append(track_uri)


sp.user_playlist_add_tracks(user,playlist_id,tracks_URIs)

print(songs)
