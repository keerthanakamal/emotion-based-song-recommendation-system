import os
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from dotenv import load_dotenv

class SpotifyClient:
    def __init__(self):
        load_dotenv()
        
        # Set up authentication
        client_id = os.getenv("SPOTIFY_CLIENT_ID")
        client_secret = os.getenv("SPOTIFY_CLIENT_SECRET")
        
        client_credentials_manager = SpotifyClientCredentials(
            client_id=client_id, client_secret=client_secret
        )
        self.sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
    
    def search_tracks_by_features(self, seed_genres=None, seed_tracks=None, 
                                 limit=10, **audio_features):
        """
        Search for tracks with specific audio features
        """
        if seed_genres is None:
            seed_genres = []
        if seed_tracks is None:
            seed_tracks = []
            
        # Get recommendations based on seeds and audio features
        results = self.sp.recommendations(
            seed_genres=seed_genres,
            seed_tracks=seed_tracks,
            limit=limit,
            **audio_features
        )
        
        return results['tracks']
    
    def get_track_features(self, track_id):
        """Get audio features for a specific track"""
        return self.sp.audio_features(track_id)[0]
    


    '''
Spotify Client Code Explanation
This code implements a client for interacting with the Spotify API using the spotipy library. It provides a clean interface for searching tracks and retrieving audio features.

Class Structure
The SpotifyClient class encapsulates the functionality for interacting with Spotify's API.

Initialization
def __init__(self):
    load_dotenv()
    
    # Set up authentication
    client_id = os.getenv("SPOTIFY_CLIENT_ID")
    client_secret = os.getenv("SPOTIFY_CLIENT_SECRET")
    
    client_credentials_manager = SpotifyClientCredentials(
        client_id=client_id, client_secret=client_secret
    )
    self.sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

Uses load_dotenv() to load environment variables from a .env file
Retrieves Spotify API credentials from environment variables
Sets up authentication using the Client Credentials flow
Creates a Spotipy client instance for making API calls
def search_tracks_by_features(self, seed_genres=None, seed_tracks=None, 
                             limit=10, **audio_features):
    """
    Search for tracks with specific audio features
    """
    if seed_genres is None:
        seed_genres = []
    if seed_tracks is None:
        seed_tracks = []
        
    # Get recommendations based on seeds and audio features
    results = self.sp.recommendations(
        seed_genres=seed_genres,
        seed_tracks=seed_tracks,
        limit=limit,
        **audio_features
    )
    
    return results['tracks']
    
    Takes seed genres, seed tracks, and audio features as parameters
Uses Spotify's recommendation engine to find matching tracks
The **audio_features parameter allows passing various audio characteristics (like tempo, energy, danceability)
Returns a list of track objects that match the criteria
Audio Feature Retrieval
def get_track_features(self, track_id):
    """Get audio features for a specific track"""
    return self.sp.audio_features(track_id)[0]

    Takes a track ID as input
Retrieves the audio features for that specific track
Returns a dictionary of audio features (such as tempo, key, energy, etc.)
This client provides a simplified interface to Spotify's API for finding music based on specific characteristics and analyzing audio features of tracks.

    '''