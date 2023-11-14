import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pickle

# Set up Spotify API credentials
with open("data/secrets.dat","rb") as credentials:
    temp_cred=pickle.load(credentials)
    client_credentials_manager = SpotifyClientCredentials(client_id=temp_cred[0], client_secret=temp_cred[1])
    sp = spotipy.Spotify(client_credentials_manager = client_credentials_manager)

def get_spotify_playlist_tracks(playlist_link):

    # Extract playlist ID from the playlist link
    playlist_id = playlist_link.split("?si")[0].split('/')[-1]
    print(playlist_id)
    # Get the playlist tracks
    results = sp.playlist_tracks(playlist_id)

    # Extract song names and add them to a list
    song_names = [track['track']['name'] for track in results['items']]

    return song_names

