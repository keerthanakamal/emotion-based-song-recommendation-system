import os
import requests
import base64
import time
from dotenv import load_dotenv

class SpotifyAuth:
    """Handle authentication with Spotify API"""
    
    def __init__(self):
        # Load environment variables
        load_dotenv()
        self.client_id = os.environ.get('SPOTIFY_CLIENT_ID')
        self.client_secret = os.environ.get('SPOTIFY_CLIENT_SECRET')
        self.token = None
        self.token_expiry = 0
    
    def get_token(self):
        """Get a valid access token for Spotify API"""
        # Check if we already have a valid token
        if self.token and time.time() < self.token_expiry:
            return self.token
        
        # If not, request a new token
        auth_string = f"{self.client_id}:{self.client_secret}"
        auth_bytes = auth_string.encode('utf-8')
        auth_base64 = base64.b64encode(auth_bytes).decode('utf-8')
        
        url = "https://accounts.spotify.com/api/token"
        headers = {
            "Authorization": f"Basic {auth_base64}",
            "Content-Type": "application/x-www-form-urlencoded"
        }
        data = {"grant_type": "client_credentials"}
        
        try:
            response = requests.post(url, headers=headers, data=data)
            response.raise_for_status()
            
            json_result = response.json()
            self.token = json_result["access_token"]
            # Set token expiry (subtract 60 seconds to be safe)
            self.token_expiry = time.time() + json_result["expires_in"] - 60
            return self.token
        except requests.exceptions.RequestException as e:
            print(f"Authentication error: {e}")
            return None
