from emotion_detector import EmotionDetector
from spotify_client import SpotifyClient
from mood_mapper import MoodMapper
import pandas as pd
from sklearn.cluster import KMeans

class MoodIntensifyingRecommender:
    def __init__(self):
        self.emotion_detector = EmotionDetector()
        self.spotify = SpotifyClient()
        self.mood_mapper = MoodMapper()
    
    def recommend_for_text(self, text, num_songs=5, use_clustering=False):
        """
        Main recommendation function - takes text input and returns song recommendations
        """
        # Detect emotion from text
        emotion = self.emotion_detector.detect_emotion(text)
        
        # Get audio features for the detected emotion
        emotion_features = self.mood_mapper.get_features_for_emotion(emotion)
        
        # Extract seed genres
        seed_genres = emotion_features.pop("seed_genres", [])[:5]  # Spotify allows max 5 seed genres
        
        # Format remaining features for the Spotify API
        api_features = {}
        for key, value in emotion_features.items():
            # Convert from target_X to target_X (Spotify API format)
            api_key = key.replace("target_", "target_")
            api_features[api_key] = value
        
        # Get initial recommendations
        tracks = self.spotify.search_tracks_by_features(
            seed_genres=seed_genres,
            limit=50 if use_clustering else num_songs,
            **api_features
        )
        
        if not use_clustering:
            return [(track['name'], track['artists'][0]['name']) for track in tracks[:num_songs]]
        else:
            return self._refined_recommendations_with_clustering(tracks, emotion_features, num_songs)
    
    def _refined_recommendations_with_clustering(self, tracks, target_features, num_songs):
        """Refine recommendations using clustering to find the most intense matches"""
        # Get audio features for all tracks
        track_ids = [track['id'] for track in tracks]
        features_list = []
        
        # Batch process to avoid API limits
        for i in range(0, len(track_ids), 50):
            batch = track_ids[i:i+50]
            features = self.spotify.sp.audio_features(batch)
            features_list.extend(features)
        
        # Create DataFrame with features
        df = pd.DataFrame(features_list)
        
        # Select relevant columns for clustering
        feature_cols = ['valence', 'energy', 'tempo', 'mode']
        df_features = df[feature_cols]
        
        # Perform k-means clustering
        kmeans = KMeans(n_clusters=min(5, len(df_features)), random_state=42)
        df['cluster'] = kmeans.fit_predict(df_features)
        
        # Find the cluster closest to our target features
        target_vector = [
            target_features.get('target_valence', 0.5),
            target_features.get('target_energy', 0.5),
            target_features.get('target_tempo', 120) / 200,  # normalize tempo
            target_features.get('target_mode', 0)
        ]
        
        # Calculate distance from each cluster center to target
        distances = []
        for i, center in enumerate(kmeans.cluster_centers_):
            dist = sum((center[j] - target_vector[j])**2 for j in range(len(center)))
            distances.append((i, dist))
        
        # Get the cluster with minimum distance
        best_cluster = min(distances, key=lambda x: x[1])[0]
        
        # Get tracks from the best cluster
        best_tracks = df[df['cluster'] == best_cluster].index.tolist()[:num_songs]
        
        # Return the track information
        result = []
        for idx in best_tracks:
            track = tracks[idx]
            result.append((track['name'], track['artists'][0]['name']))
        
        return result