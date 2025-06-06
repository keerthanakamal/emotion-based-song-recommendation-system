from emotion_detector import EmotionDetector
from spotify_client import SpotifyClient
from mood_mapper import MoodMapper
import pandas as pd
from sklearn.cluster import KMeans
import os
import json
import base64
import numpy as np
import requests
from typing import List, Tuple, Dict, Optional
from transformers import AutoTokenizer, TFAutoModelForSequenceClassification
import tensorflow as tf
from datetime import datetime, timedelta
import random

class MoodIntensifyingRecommender:
    """
    A recommendation system that suggests songs based on the emotional content of text.
    Uses a pre-trained emotion detection model and Spotify's API to find music that matches
    and potentially intensifies the detected emotion.
    """
    
    SPOTIFY_TOKEN_URL = "https://accounts.spotify.com/api/token"
    SPOTIFY_SEARCH_URL = "https://api.spotify.com/v1/search"
    
    # Emotion to music genre/mood mapping
    EMOTION_MAPPING = {
        "joy": ["happy", "upbeat", "energetic", "dance"],
        "sadness": ["sad", "melancholy", "somber", "emotional"],
        "anger": ["angry", "intense", "rage", "heavy metal"],
        "fear": ["dark", "tense", "suspense", "atmospheric"],
        "surprise": ["uplifting", "inspiring", "unexpected", "dramatic"],
        "neutral": ["chill", "relaxed", "ambient", "easy listening"]
    }
    
    def __init__(self, model_path: str):
        """
        Initialize the recommender with a local emotion detection model.
        
        Args:
            model_path: Path to the local emotion detection model directory
        """
        self.model_path = model_path
        self.load_model()
        self.spotify_token = None
        self.token_expiry = 0
        
        # Sample song database organized by emotion and language
        # In a real implementation, this would come from a database or API
        self.song_database = {
            "happy": {
                "hindi": [
                    ("Badtameez Dil", "Pritam, Benny Dayal"),
                    ("Balam Pichkari", "Vishal-Shekhar, Shalmali Kholgade"),
                    ("Desi Girl", "Shankar-Ehsaan-Loy, Vishal Dadlani"),
                    ("Kala Chashma", "Badshah, Neha Kakkar"),
                    ("Gallan Goodiyaan", "Shankar-Ehsaan-Loy, Yashita Sharma")
                ],
                "malayalam": [
                    ("Jimmiki Kammal", "Vidya Vox, Kutty"),
                    ("Entammede Jimikki Kammal", "Vineeth Sreenivasan"),
                    ("Manikya Malaraya Poovi", "Vineeth Sreenivasan"),
                    ("Appangal Embadum", "Vineeth Sreenivasan"),
                    ("Lailakame", "Vijay Yesudas")
                ]
            },
            "sad": {
                "hindi": [
                    ("Channa Mereya", "Arijit Singh"),
                    ("Judaai", "Arijit Singh"),
                    ("Tum Hi Ho", "Arijit Singh"),
                    ("Kabira", "Tochi Raina, Rekha Bhardwaj"),
                    ("Agar Tum Saath Ho", "Alka Yagnik, Arijit Singh")
                ],
                "malayalam": [
                    ("Akale", "Vineeth Sreenivasan"),
                    ("Pranayame", "Shreya Ghoshal"),
                    ("Mazha Padum", "K.J. Yesudas"),
                    ("Aaromale", "Benny Dayal"),
                    ("Karalil Tharum", "K.S. Chithra")
                ]
            },
            "angry": {
                "hindi": [
                    ("Chikni Chameli", "Shreya Ghoshal"),
                    ("Jumme Ki Raat", "Mika Singh"),
                    ("Dhoom Machale", "Sunidhi Chauhan"),
                    ("Desi Boyz", "Sonia Mangal"),
                    ("Zinda", "Siddharth Mahadevan")
                ],
                "malayalam": [
                    ("Kalippu", "Najim Arshad"),
                    ("Kadali Kanmani", "K J Yesudas"),
                    ("Minnaminni", "K J Yesudas"),
                    ("Ee Puzhayum", "K J Yesudas"),
                    ("Kaadum Thazharayum", "P. Jayachandran")
                ]
            },
            "fearful": {
                "hindi": [
                    ("Darr Ke Aage Jeet Hai", "Sukhwinder Singh"),
                    ("Main Rahoon Ya Na Rahoon", "Amaal Mallik, Armaan Malik"),
                    ("Sooraj Dooba Hain", "Amaal Mallik, Arijit Singh"),
                    ("Zehnaseeb", "Chinmayi, Shekhar Ravjiani"),
                    ("Hasi", "Ami Mishra")
                ],
                "malayalam": [
                    ("Ee Kalbitha", "K.S. Chithra"),
                    ("Onnam Ragam", "K.S. Chithra"),
                    ("Mizhiyoram", "K.S. Chithra"),
                    ("Aaromale", "Benny Dayal"),
                    ("Thamarapoovil", "K.S. Chithra, K.J. Yesudas")
                ]
            },
            "neutral": {
                "hindi": [
                    ("Kun Faya Kun", "A.R. Rahman, Javed Ali"),
                    ("Iktara", "Amit Trivedi, Kavita Seth"),
                    ("Phir Le Aya Dil", "Arijit Singh"),
                    ("Ilahi", "Arijit Singh"),
                    ("Tum Saath Ho", "Alka Yagnik, Arijit Singh")
                ],
                "malayalam": [
                    ("Malare", "Vijay Yesudas"),
                    ("Kannadi Koodum", "Najeem Arshad"),
                    ("Ethu Kari Raavilum", "Vijay Yesudas"),
                    ("Pranayame", "Shreya Ghoshal"),
                    ("Aaro Nenjil", "K.S. Chithra")
                ]
            }
        }
    
    def load_model(self):
        """Load the emotion detection model and tokenizer from the provided path."""
        try:
            self.tokenizer = AutoTokenizer.from_pretrained(self.model_path)
            self.model = TFAutoModelForSequenceClassification.from_pretrained(self.model_path)
            # Get emotion labels from model config
            self.emotion_labels = self.model.config.id2label if hasattr(self.model.config, 'id2label') else {
                0: "joy", 1: "sadness", 2: "anger", 3: "fear", 4: "surprise", 5: "neutral"
            }
            print(f"Emotion model loaded successfully with {len(self.emotion_labels)} emotions")
        except Exception as e:
            print(f"Error loading emotion model: {e}")
            raise
    
    def get_spotify_token(self) -> str:
        """
        Get a valid Spotify API token using client credentials flow.
        
        Returns:
            A valid Spotify access token
        """
        import time
        
        # Return existing token if it's still valid
        if self.spotify_token and time.time() < self.token_expiry:
            return self.spotify_token
        
        # Get credentials from environment variables
        client_id = os.getenv("SPOTIFY_CLIENT_ID")
        client_secret = os.getenv("SPOTIFY_CLIENT_SECRET")
        
        if not client_id or not client_secret:
            raise ValueError("Spotify API credentials not found in environment variables")
        
        # Encode client ID and secret as required by Spotify
        auth_header = base64.b64encode(f"{client_id}:{client_secret}".encode()).decode()
        
        # Request a new token
        headers = {"Authorization": f"Basic {auth_header}"}
        data = {"grant_type": "client_credentials"}
        
        response = requests.post(self.SPOTIFY_TOKEN_URL, headers=headers, data=data)
        
        if response.status_code != 200:
            raise Exception(f"Failed to get Spotify token: {response.json()}")
        
        token_data = response.json()
        self.spotify_token = token_data["access_token"]
        # Set token expiry time (subtract 60 seconds as a buffer)
        self.token_expiry = time.time() + token_data["expires_in"] - 60
        
        return self.spotify_token
    
    def detect_emotion(self, text: str) -> Tuple[str, Dict[str, float]]:
        """
        Detect the emotion in the provided text using the pre-trained model.
        
        Args:
            text: The text to analyze for emotional content
            
        Returns:
            A tuple containing (primary_emotion, emotion_scores_dict)
        """
        # Tokenize the input
        inputs = self.tokenizer(text, return_tensors="tf", padding=True, truncation=True, max_length=512)
        
        # Get prediction from model
        outputs = self.model(inputs)
        logits = outputs.logits.numpy()[0]
        
        # Convert logits to probabilities
        probabilities = np.exp(logits) / np.sum(np.exp(logits))
        
        # Create a dictionary of emotions and their scores
        emotion_scores = {self.emotion_labels[i]: float(prob) for i, prob in enumerate(probabilities)}
        
        # Find the dominant emotion
        primary_emotion = max(emotion_scores, key=emotion_scores.get)
        
        return primary_emotion, emotion_scores
    
    def search_spotify_for_songs(self, query: str, limit: int = 20) -> List[Dict]:
        """
        Search Spotify for songs based on the query.
        
        Args:
            query: The search query string
            limit: Maximum number of results to return
            
        Returns:
            A list of track objects from Spotify
        """
        token = self.get_spotify_token()
        
        headers = {"Authorization": f"Bearer {token}"}
        params = {
            "q": query,
            "type": "track",
            "limit": limit,
            "market": "US"  # Can be changed to match user's region
        }
        
        response = requests.get(self.SPOTIFY_SEARCH_URL, headers=headers, params=params)
        
        if response.status_code != 200:
            print(f"Error searching Spotify: {response.json()}")
            return []
        
        results = response.json()
        return results.get("tracks", {}).get("items", [])
    
    def get_song_features(self, track_ids: List[str]) -> List[Dict]:
        """
        Get audio features for multiple tracks from Spotify.
        
        Args:
            track_ids: List of Spotify track IDs
            
        Returns:
            A list of audio feature objects for each track
        """
        if not track_ids:
            return []
            
        token = self.get_spotify_token()
        url = "https://api.spotify.com/v1/audio-features"
        headers = {"Authorization": f"Bearer {token}"}
        
        # Split into chunks of 100 (Spotify's limit)
        feature_results = []
        for i in range(0, len(track_ids), 100):
            chunk = track_ids[i:i+100]
            params = {"ids": ",".join(chunk)}
            response = requests.get(url, headers=headers, params=params)
            
            if response.status_code == 200:
                feature_results.extend(response.json().get("audio_features", []))
        
        return [f for f in feature_results if f is not None]
    
    def cluster_songs(self, tracks: List[Dict], features: List[Dict], emotion: str, n_clusters: int = 3) -> List[Dict]:
        """
        Cluster songs by audio features and select the cluster that best matches the emotion.
        
        Args:
            tracks: List of track objects from Spotify
            features: List of audio features for each track
            emotion: The detected emotion
            n_clusters: Number of clusters to create
            
        Returns:
            A list of track objects from the best matching cluster
        """
        if not tracks or not features:
            return []
            
        # Create feature vectors for clustering
        feature_vectors = []
        for feature in features:
            # Select relevant features for clustering
            vector = [
                feature.get("energy", 0),
                feature.get("valence", 0),  # happiness/positivity
                feature.get("danceability", 0),
                feature.get("acousticness", 0),
                feature.get("instrumentalness", 0),
                feature.get("tempo", 0) / 200  # normalize tempo
            ]
            feature_vectors.append(vector)
        
        # Only cluster if we have enough songs
        if len(feature_vectors) < n_clusters:
            return tracks
            
        # Perform clustering
        kmeans = KMeans(n_clusters=n_clusters, random_state=42)
        clusters = kmeans.fit_predict(feature_vectors)
        
        # Determine which cluster best matches the emotion
        cluster_scores = self._score_clusters_for_emotion(features, clusters, n_clusters, emotion)
        best_cluster = max(cluster_scores, key=cluster_scores.get)
        
        # Return tracks from the best cluster
        clustered_tracks = [track for i, track in enumerate(tracks) if clusters[i] == best_cluster]
        
        return clustered_tracks if clustered_tracks else tracks
    
    def _score_clusters_for_emotion(self, features: List[Dict], clusters: List[int], n_clusters: int, emotion: str) -> Dict[int, float]:
        """
        Score each cluster based on how well it matches the target emotion.
        
        Args:
            features: List of audio features for each track
            clusters: Cluster assignment for each track
            n_clusters: Number of clusters
            emotion: Target emotion
            
        Returns:
            Dictionary mapping cluster IDs to their emotion matching scores
        """
        cluster_scores = {i: 0.0 for i in range(n_clusters)}
        
        for i in range(n_clusters):
            # Get features for this cluster
            cluster_features = [f for j, f in enumerate(features) if clusters[j] == i]
            
            if not cluster_features:
                continue
                
            # Calculate average features for the cluster
            avg_energy = np.mean([f.get("energy", 0) for f in cluster_features])
            avg_valence = np.mean([f.get("valence", 0) for f in cluster_features])
            avg_tempo = np.mean([f.get("tempo", 0) for f in cluster_features])
            avg_dance = np.mean([f.get("danceability", 0) for f in cluster_features])
            
            # Score based on emotion (customize these mappings based on music psychology)
            if emotion == "joy":
                score = (avg_valence * 0.5) + (avg_energy * 0.3) + (avg_dance * 0.2)
            elif emotion == "sadness":
                score = ((1-avg_valence) * 0.5) + ((1-avg_energy) * 0.3) + ((1-avg_tempo/200) * 0.2)
            elif emotion == "anger":
                score = (avg_energy * 0.6) + ((1-avg_valence) * 0.4)
            elif emotion == "fear":
                score = ((1-avg_valence) * 0.4) + (avg_energy * 0.3) + ((1-avg_dance) * 0.3)
            else:  # neutral or other
                score = 0.5  # No preference for neutral
                
            cluster_scores[i] = score
            
        return cluster_scores
    
    def recommend_for_text(self, text: str, num_songs: int = 5, languages: Optional[List[str]] = None) -> List[Tuple[str, str]]:
        """
        Generate song recommendations based on the emotional content of text.
        
        Args:
            text: Text describing the user's mood or emotional state
            num_songs: Number of songs to recommend
            languages: List of languages to include (e.g., ["hindi", "malayalam"])
            
        Returns:
            A list of tuples containing (song_title, artist_name)
        """
        # Detect emotion in the text
        emotion, emotion_scores = self.detect_emotion(text)
        print(f"Detected emotion: {emotion}")
        
        # Get search terms for this emotion
        search_terms = self.EMOTION_MAPPING.get(emotion, ["music"])
        
        # Collect songs from multiple searches
        all_tracks = []
        for term in search_terms:
            query = f"{term} music"
            tracks = self.search_spotify_for_songs(query, limit=10)
            all_tracks.extend(tracks)
        
        # If no songs found, try a more generic search
        if not all_tracks:
            all_tracks = self.search_spotify_for_songs(f"{emotion} mood", limit=20)
        
        # Still no results? Use a default query
        if not all_tracks:
            all_tracks = self.search_spotify_for_songs("popular music", limit=num_songs)
        
        # Use basic sorting - this could be improved with additional logic
        selected_tracks = all_tracks[:num_songs]
        
        # Format results
        recommendations = []
        for track in selected_tracks:
            title = track.get("name", "Unknown Title")
            artist = track.get("artists", [{}])[0].get("name", "Unknown Artist") if track.get("artists") else "Unknown Artist"
            recommendations.append((title, artist))
        
        # Filter recommendations by language if specified
        if languages:
            filtered_recommendations = []
            for lang in languages:
                # Get songs for this language
                lang_songs = self.song_database.get(emotion, {}).get(lang, [])
                
                # Add random songs from this language
                if lang_songs:
                    selected_songs = random.sample(lang_songs, min(len(lang_songs), num_songs))
                    filtered_recommendations.extend(selected_songs)
            
            # If we couldn't find enough songs in the preferred languages, fall back to any available
            if len(filtered_recommendations) < num_songs:
                additional_needed = num_songs - len(filtered_recommendations)
                for lang in languages:
                    if additional_needed <= 0:
                        break
                    
                    # Get additional songs from this language
                    lang_songs = self.song_database.get(emotion, {}).get(lang, [])
                    for song in lang_songs:
                        if song not in filtered_recommendations:
                            filtered_recommendations.append(song)
                            additional_needed -= 1
                            if additional_needed <= 0:
                                break
            
            recommendations = filtered_recommendations
        
        return recommendations[:num_songs]