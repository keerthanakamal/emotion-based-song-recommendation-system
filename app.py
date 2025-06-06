from flask import Flask, request, jsonify
from flask_cors import CORS
from emotion_detector import EmotionDetector
from recommender import MoodIntensifyingRecommender
import os
from dotenv import load_dotenv
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Path to local model
model_path = os.path.join(os.path.dirname(__file__), "models", "emotion_model")

# Initialize emotion detector and recommender
try:
    emotion_detector = EmotionDetector(model_path)
    recommender = MoodIntensifyingRecommender(model_path)
    logger.info("Emotion detector and recommender initialized successfully")
except Exception as e:
    logger.error(f"Error initializing components: {str(e)}")
    raise

@app.route('/health', methods=['GET'])
def health_check():
    """Endpoint to check if the API is running"""
    return jsonify({"status": "healthy", "message": "API is running"}), 200

@app.route('/recommend', methods=['POST'])
def recommend():
    """Main endpoint for song recommendations based on emotion"""
    try:
        # Get JSON data from request
        data = request.json
        
        if not data or 'user_text' not in data:
            return jsonify({"error": "Missing required field 'user_text'"}), 400
        
        user_text = data['user_text']
        languages = data.get('languages', ["hindi", "malayalam"])
        
        logger.info(f"Received recommendation request: {user_text[:50]}...")
        
        # Detect emotion from text
        emotion = emotion_detector.detect_emotion(user_text)
        logger.info(f"Detected emotion: {emotion}")
        
        # Get song recommendations
        raw_recommendations = recommender.recommend_for_text(
            user_text, 
            num_songs=5,
            languages=languages
        )
        
        # Format recommendations according to API specification
        formatted_recommendations = []
        for title, artist in raw_recommendations:
            # Determine language (this implementation depends on your recommender's capabilities)
            # For now, we'll alternate between Hindi and Malayalam as a placeholder
            language = languages[len(formatted_recommendations) % len(languages)]
            
            formatted_recommendations.append({
                "title": title,
                "artist": artist,
                "language": language
            })
        
        # Return response
        response = {
            "emotion": emotion,
            "recommendations": formatted_recommendations
        }
        
        return jsonify(response), 200
        
    except Exception as e:
        logger.error(f"Error processing recommendation request: {str(e)}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
