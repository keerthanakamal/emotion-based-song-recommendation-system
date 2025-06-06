class MoodMapper:
    def __init__(self):
        # Define the audio features to intensify each emotion
        self.emotion_features = {
            "sad": {
                "target_valence": 0.1,    # Very negative/sad music
                "target_energy": 0.3,     # Low energy
                "target_tempo": 70,       # Slow tempo
                "target_mode": 0,         # Minor key
                "seed_genres": ["sad", "acoustic", "piano", "indie"],
            },
            "angry": {
                "target_valence": 0.2,    # Negative valence
                "target_energy": 0.9,     # High energy
                "target_tempo": 150,      # Fast tempo
                "target_mode": 0,         # Minor key
                "seed_genres": ["metal", "hardcore", "heavy-metal", "punk"],
            },
            "fearful": {
                "target_valence": 0.15,   # Very negative valence
                "target_energy": 0.6,     # Medium energy
                "target_instrumentalness": 0.6,  # More instrumental
                "seed_genres": ["ambient", "soundtracks", "experimental"], 
            },
            "happy": {
                "target_valence": 0.9,    # Very positive valence
                "target_energy": 0.8,     # High energy
                "target_danceability": 0.8, # Very danceable
                "target_mode": 1,         # Major key
                "seed_genres": ["pop", "dance", "happy", "party"],
            },
            "neutral": {
                "target_valence": 0.5,    # Middle valence
                "target_energy": 0.5,     # Medium energy
                "seed_genres": ["indie", "folk", "alt-pop"],
            }
        }
    
    def get_features_for_emotion(self, emotion):
        """Return appropriate audio features for the given emotion"""
        if emotion in self.emotion_features:
            return self.emotion_features[emotion]
        else:
            # Default to neutral if emotion not found
            return self.emotion_features["neutral"]