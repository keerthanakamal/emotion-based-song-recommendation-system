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
        self._available_genres = None
    
    def get_available_genres(self):
        """Get a list of available genre seeds from Spotify"""
        if self._available_genres is None:
            try:
                result = self.sp.recommendation_genre_seeds()
                self._available_genres = result.get('genres', [])
            except Exception as e:
                print(f"Error fetching genre seeds: {str(e)}")
                self._available_genres = []
        return self._available_genres
    
    def search_tracks_by_features(self, seed_genres=None, seed_tracks=None, 
                                 limit=10, **audio_features):
        """
        Search for tracks with specific audio features
        """
        if seed_genres is None:
            seed_genres = []
        if seed_tracks is None:
            seed_tracks = []
        
        # Validate genres against available Spotify genres
        available_genres = self.get_available_genres()
        valid_seed_genres = [genre for genre in seed_genres if genre in available_genres]
        
        # If no valid genres after filtering, use default popular genres
        if not valid_seed_genres and not seed_tracks:
            valid_seed_genres = ['pop', 'rock', 'electronic'][:5]
            print(f"Warning: No valid genre seeds provided. Using default genres: {valid_seed_genres}")
        elif valid_seed_genres != seed_genres:
            print(f"Warning: Some genres were invalid. Using: {valid_seed_genres}")
            print(f"Available genres include: {', '.join(available_genres[:10])}...")
        
        try:
            # Get recommendations based on seeds and audio features
            results = self.sp.recommendations(
                seed_genres=valid_seed_genres[:5],  # Spotify allows max 5 seed genres
                seed_tracks=seed_tracks,
                limit=limit,
                **audio_features
            )
            
            return results['tracks']
        except spotipy.exceptions.SpotifyException as e:
            print(f"Spotify API error: {str(e)}")
            return []
        except Exception as e:
            print(f"Error getting recommendations: {str(e)}")
            return []
    
    def get_track_features(self, track_id):
        """Get audio features for a specific track"""
        try:
            return self.sp.audio_features(track_id)[0]
        except Exception as e:
            print(f"Error fetching track features: {str(e)}")
            return None