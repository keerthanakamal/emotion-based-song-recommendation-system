from transformers import AutoTokenizer, TFAutoModelForSequenceClassification
import os

# Define the model name
model_name = "j-hartmann/emotion-english-distilroberta-base"

# Create a directory to store it
save_path = "models/emotion_model"
os.makedirs(save_path, exist_ok=True)

# Download the model and tokenizer
print(f"Downloading model from {model_name}...")
tokenizer = AutoTokenizer.from_pretrained(model_name)
# Use TF version instead of PyTorch
model = TFAutoModelForSequenceClassification.from_pretrained(model_name)

# Save locally
print("Saving model locally...")
tokenizer.save_pretrained(save_path)
model.save_pretrained(save_path)

print(f"Model downloaded and saved successfully to {save_path}!")