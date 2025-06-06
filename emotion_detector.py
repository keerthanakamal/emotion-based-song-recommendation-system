from transformers import pipeline

class EmotionDetector:
    def __init__(self):
        # Load emotion classification model
        self.classifier = pipeline("text-classification", 
                                  "j-hartmann/emotion-english-distilroberta-base",
                                  top_k=None)
        
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
        

'''Emotion Detector Code Explanation
This code implements a text-based emotion detection system using a pre-trained machine learning model. Here's how it works:

Class Structure
The EmotionDetector class provides a simple interface for detecting emotions in text.

Initialization
def __init__(self):
    # Load emotion classification model
    self.classifier = pipeline("text-classification", 
                              "j-hartmann/emotion-english-distilroberta-base",
                              top_k=None)
    
    # Define our target emotions
    self.target_emotions = ["sadness", "anger", "fear", "joy", "neutral"]

Uses Hugging Face's transformers library to load a pre-trained emotion classification model
The model used is j-hartmann/emotion-english-distilroberta-base, which is trained to detect emotions in text
top_k=None means it returns probabilities for all emotion classes
Defines the target emotions the system can identify
Emotion Detection

def detect_emotion(self, text):
    """Detect emotion from text input"""
    results = self.classifier(text)
    emotions = {item["label"]: item["score"] for item in results[0]}
    
    # Find the emotion with highest confidence
    dominant_emotion = max(emotions.items(), key=lambda x: x[1])

    Takes text as input and passes it to the classifier
Converts the model's output to a dictionary mapping emotion labels to confidence scores
Identifies the emotion with the highest confidence score
Emotion Mapping
The method maps the model's technical output to more user-friendly emotion terms:

"sadness" → "sad"
"anger" → "angry"
"fear" → "fearful"
"joy" → "happy"
Other emotions → "neutral"
The final result is a single string representing the detected emotion.

    '''

