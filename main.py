import spotipy
from spotipy.oauth2 import SpotifyOAuth
import random

from config import SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET

# Set your credentials here
SPOTIPY_REDIRECT_URI = "http://localhost:8080"  # or any other valid URI

# Authenticate with Spotify
sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        client_id=SPOTIPY_CLIENT_ID,
        client_secret=SPOTIPY_CLIENT_SECRET,
        redirect_uri=SPOTIPY_REDIRECT_URI,
        scope=["user-library-read", "playlist-read-private"],  # scopes required
    )
)

# Load already-selected songs from the file into a set
file_name = "selected_songs.txt"
try:
    with open(file_name, "r") as file:
        already_selected = {line.strip() for line in file}
except FileNotFoundError:
    already_selected = set()

# Get a list of the user's playlists
playlists = sp.current_user_playlists()["items"]

# Randomly select a playlist
selected_playlist = random.choice(playlists)
playlist_id = selected_playlist["id"]

print(f"Randomly selected playlist: {selected_playlist['name']}")

# Fetch the tracks from the selected playlist
tracks = sp.playlist_items(playlist_id)["items"]

if not tracks:  # If the playlist has no tracks
    print("The selected playlist is empty!")
else:
    # Select a new song that hasn't been selected before
    while True:
        selected_track = random.choice(tracks)
        track_name = selected_track["track"]["name"]
        track_artist = selected_track["track"]["artists"][0]["name"]
        song_key = f"{track_name} by {track_artist}"

        if song_key not in already_selected:
            break

    print(f"Randomly selected track: {song_key}")

    # Add the new song to the file and the set
    with open(file_name, "a") as file:
        file.write(song_key + "\n")
    already_selected.add(song_key)
