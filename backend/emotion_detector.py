from transformers import pipeline
import os

class EmotionDetector:
    def __init__(self, model_path=None):
        # Check if local model exists, otherwise use the online version
        if model_path and os.path.exists(model_path):
            print(f"Loading emotion model from local path: {model_path}")
            # Load emotion classification model from local path
            self.classifier = pipeline("text-classification", 
                                    model_path,
                                    top_k=None)
        else:
            print("Downloading emotion model (first run only)...")
            # Load emotion classification model from Hugging Face
            model_id = "j-hartmann/emotion-english-distilroberta-base"
            self.classifier = pipeline("text-classification", 
                                    model_id,
                                    top_k=None)
            # Optional: save the model locally after download
            if not model_path:
                model_path = "models/emotion_model"
            self.classifier.save_pretrained(model_path)
            print(f"Model saved to {model_path}")
        
        # Define our target emotions
        self.target_emotions = ["sadness", "anger", "fear", "joy", "neutral"]
    
    def detect_emotion(self, text):
        """Detect emotion from text input"""
        results = self.classifier(text)
        emotions = {item["label"]: item["score"] for item in results[0]}
        
        # Find the emotion with highest confidence
        dominant_emotion = max(emotions.items(), key=lambda x: x[1])
        
        # Map to simplified emotion categories
        if dominant_emotion[0] == "sadness":
            return "sad"
        elif dominant_emotion[0] == "anger":
            return "angry"
        elif dominant_emotion[0] == "fear":
            return "fearful"
        elif dominant_emotion[0] == "joy":
            return "happy"
        else:
            return "neutral"