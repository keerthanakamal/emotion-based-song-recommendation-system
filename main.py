from recommender import MoodIntensifyingRecommender

def main():
    recommender = MoodIntensifyingRecommender()
    
    print("===== Mood-Intensifying Music Recommender =====")
    print("This system will recommend songs that match and intensify your current mood.")
    
    while True:
        print("\nEnter some text describing how you feel (or 'exit' to quit):")
        user_input = input("> ")
        
        if user_input.lower() == 'exit':
            break
        
        use_clustering = input("Use advanced clustering for better matches? (y/n): ").lower() == 'y'
        
        print("\nAnalyzing your mood and finding matching songs...")
        
        recommendations = recommender.recommend_for_text(
            user_input, 
            num_songs=5,
            use_clustering=use_clustering
        )
        
        print("\nBased on your mood, here are songs that might intensify what you're feeling:")
        for i, (title, artist) in enumerate(recommendations, 1):
            print(f"{i}. '{title}' by {artist}")

if __name__ == "__main__":
    main()