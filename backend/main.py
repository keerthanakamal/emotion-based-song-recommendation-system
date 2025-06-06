from recommender import MoodIntensifyingRecommender
import os
from dotenv import load_dotenv

def main():
    # Make sure environment variables are loaded
    load_dotenv()
    
    # Path to local model
    model_path = os.path.join(os.path.dirname(__file__), "models", "emotion_model")
    
    # Create recommender with local model path
    recommender = MoodIntensifyingRecommender(model_path)
    
    print("===== Mood-Intensifying Music Recommender =====")
    print("This system will recommend songs that match and intensify your current mood.")
    
    while True:
        print("\nEnter some text describing how you feel (or 'exit' to quit):")
        user_input = input("> ")
        
        if user_input.lower() == 'exit':
            break
        
        print("\nAnalyzing your mood and finding matching songs...")
        
        recommendations = recommender.recommend_for_text(
            user_input, 
            num_songs=5
        )
        
        print("\nBased on your mood, here are songs that might intensify what you're feeling:")
        for i, (title, artist) in enumerate(recommendations, 1):
            print(f"{i}. '{title}' by {artist}")

if __name__ == "__main__":
    main()