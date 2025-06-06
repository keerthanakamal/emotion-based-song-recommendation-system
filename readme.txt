# Emotion Based Song Recommendation System

A system that recommends songs based on the emotional content of input text. The system detects emotions in text and matches them with appropriate music using Spotify's recommendation API.

## Setup Instructions

### Step 1: Install required packages

```
pip install python-dotenv spotipy scikit-learn transformers pandas numpy
```

Or install from requirements file:

```
pip install -r requirements.txt
```

### Step 2: Project Structure

```
emotion-based-song-recommendation-system/
├── .env                  # Spotify API credentials
├── emotion_detector.py   # Emotion detection logic
├── spotify_client.py     # Spotify API wrapper
├── mood_mapper.py        # Maps emotions to audio features
├── recommender.py        # Recommendation engine
└── main.py               # Entry point
```

### Step 3: Set up Spotify API

1. Create an account at [Spotify Developer Dashboard](https://developer.spotify.com/dashboard/)
2. Create a new app and note down Client ID and Client Secret
3. Add http://localhost:8888/callback to Redirect URIs
4. Create a `.env` file at the root of your project with:
   ```
   SPOTIFY_CLIENT_ID=your_client_id_here
   SPOTIFY_CLIENT_SECRET=your_client_secret_here
   ```

### Step 4: Run the Application

```
python main.py
```

## How It Works

1. The system prompts you for text describing your emotional state
2. An AI model analyzes the text to detect the primary emotion
3. The emotion is mapped to audio features (tempo, energy, valence, etc.)
4. These features are sent to Spotify's API to find matching songs
5. Songs that match and potentially intensify the detected emotion are displayed

## Advanced Features

- Handles API errors gracefully
- Validates genre seeds against Spotify's available genres

## Troubleshooting

If you encounter issues with Spotify API:
- Verify your Client ID and Secret are correct in the .env file
- Ensure you have an active internet connection
- Check that your Spotify Developer app is properly configured