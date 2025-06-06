import React, { useState } from "react";
import './App.css';

// Mood images (Unsplash or similar, replace with your own if needed)
const moodImages = {
  sad: "https://images.unsplash.com/photo-1464983953574-0892a716854b?auto=format&fit=crop&w=400&q=80",
  happy: "https://images.unsplash.com/photo-1506744038136-46273834b3fb?auto=format&fit=crop&w=400&q=80",
  angry: "https://images.unsplash.com/photo-1519125323398-675f0ddb6308?auto=format&fit=crop&w=400&q=80",
  fearful: "https://images.unsplash.com/photo-1465101046530-73398c7f28ca?auto=format&fit=crop&w=400&q=80",
  neutral: "https://images.unsplash.com/photo-1465101178521-c1a9136a3b99?auto=format&fit=crop&w=400&q=80",
  music: "https://images.unsplash.com/photo-1511671782779-c97d3d27a1d4?auto=format&fit=crop&w=400&q=80"
};

function App() {
  // State for user input, clustering, loading, result, and error
  const [userText, setUserText] = useState("");
  const [useClustering, setUseClustering] = useState(true);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);

  // Handle form submit
  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    setResult(null);

    try {
      const response = await fetch("/recommend", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          user_text: userText,
          use_clustering: useClustering,
        }),
      });
      if (!response.ok) throw new Error("API error");
      const data = await response.json();
      setResult(data);
    } catch (err) {
      setError("Failed to get recommendations. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  const emotionColors = {
    sad: "#3498db",
    happy: "#f1c40f",
    angry: "#e74c3c",
    fearful: "#9b59b6",
    neutral: "#7f8c8d",
  };

  return (
    <div style={{
      maxWidth: 600,
      margin: "40px auto",
      padding: 24,
      background: "#fff",
      borderRadius: 16,
      boxShadow: "0 4px 32px #e0e0e0"
    }}>
      {/* Music-themed header image */}
      <img
        src={moodImages.music}
        alt="Music"
        style={{
          width: 80,
          height: 80,
          objectFit: "cover",
          borderRadius: "50%",
          display: "block",
          margin: "0 auto 16px",
          boxShadow: "0 2px 8px #ddd"
        }}
      />
      <h1 style={{ color: "#1DB954", textAlign: "center", marginBottom: 8 }}>
        Mood-Based Music Recommender
      </h1>
      <p style={{ textAlign: "center", color: "#444", marginBottom: 24 }}>
        Enter how you’re feeling and get song recommendations to intensify your mood!
      </p>
      <form onSubmit={handleSubmit} style={{ marginTop: 8 }}>
        <textarea
          rows={4}
          style={{
            width: "100%",
            fontSize: 16,
            padding: 12,
            borderRadius: 8,
            border: "1px solid #ddd",
            marginBottom: 12,
            resize: "vertical"
          }}
          placeholder="Describe your current mood..."
          value={userText}
          onChange={(e) => setUserText(e.target.value)}
          required
        />
        <div style={{ margin: "12px 0" }}>
          <label style={{ fontSize: 15 }}>
            <input
              type="checkbox"
              checked={useClustering}
              onChange={(e) => setUseClustering(e.target.checked)}
              style={{ marginRight: 8 }}
            />
            Use advanced clustering for better matches
          </label>
        </div>
        <button
          type="submit"
          style={{
            background: "#1DB954",
            color: "#fff",
            border: "none",
            padding: "12px 28px",
            fontSize: 17,
            borderRadius: 6,
            cursor: "pointer",
            fontWeight: "bold",
            boxShadow: "0 2px 8px #d4f5df"
          }}
          disabled={loading}
        >
          Get Recommendations
        </button>
      </form>

      {/* Loading State */}
      {loading && (
        <div style={{ margin: "32px 0", textAlign: "center" }}>
          <div className="spinner" style={{
            margin: "0 auto 12px",
            border: "4px solid #eee",
            borderTop: "4px solid #1DB954",
            borderRadius: "50%",
            width: 36,
            height: 36,
            animation: "spin 1s linear infinite"
          }} />
          <div style={{ color: "#888" }}>Analyzing your mood and finding matching songs...</div>
        </div>
      )}

      {/* Error State */}
      {error && (
        <div style={{ color: "#e74c3c", margin: "24px 0", textAlign: "center" }}>{error}</div>
      )}

      {/* Results */}
      {result && (
        <div style={{
          marginTop: 32,
          background: "#fafbfc",
          borderRadius: 12,
          padding: 20,
          boxShadow: "0 2px 12px #f0f0f0"
        }}>
          {/* Mood image */}
          <img
            src={moodImages[result.emotion] || moodImages.neutral}
            alt={result.emotion}
            style={{
              width: 70,
              height: 70,
              objectFit: "cover",
              borderRadius: "50%",
              display: "block",
              margin: "0 auto 12px",
              border: `3px solid ${emotionColors[result.emotion] || "#ccc"}`
            }}
          />
          <div
            style={{
              fontWeight: "bold",
              fontSize: 22,
              marginBottom: 18,
              color: emotionColors[result.emotion] || "#222",
              textAlign: "center",
              letterSpacing: 1
            }}
          >
            Detected Mood: {result.emotion.charAt(0).toUpperCase() + result.emotion.slice(1)}
          </div>
          {/* Show message if no recommendations */}
          {result.recommendations.length === 0 ? (
            <div style={{ color: "#e74c3c", textAlign: "center", fontWeight: "bold" }}>
              {result.message || "No recommendations found for your mood."}
            </div>
          ) : (
            <div>
              {result.recommendations.map((song, idx) => (
                <div
                  key={idx}
                  style={{
                    background: "#fff",
                    borderRadius: 10,
                    boxShadow: "0 2px 8px #e8e8e8",
                    padding: 18,
                    marginBottom: 14,
                    display: "flex",
                    alignItems: "center",
                    gap: 16
                  }}
                >
                  {/* Music note icon */}
                  <span style={{
                    fontSize: 26,
                    color: "#1DB954",
                    marginRight: 8
                  }}>🎵</span>
                  <div>
                    <span style={{ fontWeight: "bold", fontSize: 17 }}>
                      {idx + 1}. {song.title}
                    </span>
                    <br />
                    <span style={{ color: "#555", fontSize: 15 }}>{song.artist}</span>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      )}

      {/* Spinner animation keyframes */}
      <style>
        {`
          @keyframes spin {
            0% { transform: rotate(0deg);}
            100% { transform: rotate(360deg);}
          }
        `}
      </style>
    </div>
  );
}

export default App;
