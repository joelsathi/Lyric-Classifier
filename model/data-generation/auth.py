
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import lyricsgenius
from spotipy.oauth2 import SpotifyClientCredentials

import os
from dotenv import load_dotenv

load_dotenv()

def authenticate_spotify():
    # Spotify API credentials
    SPOTIPY_CLIENT_ID = os.getenv('SPOTIFY_CLIENT_ID')
    SPOTIPY_CLIENT_SECRET = os.getenv('SPOTIFY_CLIENT_SECRET')

    client_credentials_manager = SpotifyClientCredentials(client_id=SPOTIPY_CLIENT_ID, client_secret=SPOTIPY_CLIENT_SECRET)
    # Initialize the Spotify API client
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager, requests_timeout=40) #spotify object to access API

    return sp

def authenticate_genius():
    # Create a Genius API client
    GENIUS_CLIENT_ACCESS_TOKEN = os.getenv('GENIUS_ACCESS_TOKEN')
    genius = lyricsgenius.Genius(GENIUS_CLIENT_ACCESS_TOKEN, timeout=40)

    return genius