import joblib
import numpy as np
import os

# === Load model and encoders ===
model = joblib.load("app/models/ad_recommender.pkl")
le_genre = joblib.load("app/models/le_genre.pkl")
le_emotion = joblib.load("app/models/le_emotion.pkl")
le_label = joblib.load("app/models/le_label.pkl")

def recommend_ad(genre: str, age: int, emotion: str) -> str:
    try:
        genre_encoded = le_genre.transform([genre])[0]
        emotion_encoded = le_emotion.transform([emotion])[0]
        input_data = np.array([[genre_encoded, age, emotion_encoded]])
        prediction = model.predict(input_data)[0]
        return le_label.inverse_transform([prediction])[0]
    except Exception as e:
        return f"Erreur dans la prédiction : {e}"
