import os
import cv2
import numpy as np
import face_recognition
from deepface import DeepFace
from fer import FER
import mediapipe as mp

# Réduction des logs inutiles
os.environ["OPENCV_LOG_LEVEL"] = "SILENT"
os.environ["DEEPFACE_DETECTOR_BACKEND"] = "opencv"
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"

emotion_detector = FER(mtcnn=True)
pose_module = mp.solutions.pose
pose_estimator = pose_module.Pose()
FOCAL_LENGTH = 615
FACE_WIDTH_CM = 14.0

def estimate_distance(width_px):
    return round((FACE_WIDTH_CM * FOCAL_LENGTH) / width_px, 2) if width_px else None

def detect_posture(img):
    try:
        results = pose_estimator.process(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
        if results.pose_landmarks:
            return "Debout"
        return "Inconnu"
    except Exception as e:
        print("[MediaPipe Posture Error]", e)
        return "Erreur"

def detect_emotion(img):
    try:
        result = emotion_detector.detect_emotions(img)
        if result and "emotions" in result[0]:
            emotions = result[0]["emotions"]
            return max(emotions, key=emotions.get)
        return "Inconnu"
    except Exception as e:
        print("[FER Emotion Error]", e)
        return "Erreur"

def detect_dominant_color(image: np.ndarray) -> str:
    h, w, _ = image.shape
    y1, y2 = int(h * 0.5), int(h * 0.8)
    x1, x2 = int(w * 0.35), int(w * 0.65)
    cropped = image[y1:y2, x1:x2]
    avg_color = cropped.mean(axis=0).mean(axis=0)
    b, g, r = avg_color

    if r > 200 and g > 200 and b > 200:
        return "blanc"
    elif r < 50 and g < 50 and b < 50:
        return "noir"
    elif r > g and r > b:
        return "rouge"
    elif g > r and g > b:
        return "vert"
    elif b > r and b > g:
        return "bleu"
    else:
        return "gris ou autre"

def detecter_style(image: np.ndarray):
    h, w, _ = image.shape
    y1, y2 = int(h * 0.4), int(h * 0.8)
    x1, x2 = int(w * 0.35), int(w * 0.65)
    vetement_crop = image[y1:y2, x1:x2]

    avg_color = cv2.mean(vetement_crop)[:3]
    gray = cv2.cvtColor(vetement_crop, cv2.COLOR_BGR2GRAY)
    stddev = np.std(gray)

    motif = "motif" if stddev > 25 else "uni"
    style = "élégant" if avg_color[2] > 150 and motif == "uni" else "traditionnel" if avg_color[0] > 150 and motif == "motif" else "sportif"

    return {
        "couleur": detect_dominant_color(image),
        "motif": motif,
        "style": style,
        "texture": "faible" if stddev < 25 else "forte"
    }

def analyse_visage(image_bytes: bytes) -> dict:
    np_arr = np.frombuffer(image_bytes, np.uint8)
    frame = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

    small = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
    rgb_small = cv2.cvtColor(small, cv2.COLOR_BGR2RGB)
    face_locations = face_recognition.face_locations(rgb_small)
    visage_detecte = bool(face_locations)

    genre = "Inconnu"
    age = 0
    emotion = "Non détectée"

    if visage_detecte:
        try:
            deep_result = DeepFace.analyze(frame, actions=["age", "gender"], enforce_detection=True, detector_backend="opencv")
            data = deep_result[0] if isinstance(deep_result, list) else deep_result
            genre = "Homme" if data.get("dominant_gender") == "Man" else "Femme"
            age = int(data.get("age", 0))
        except Exception as e:
            print("[DeepFace Error]", e)

        emotion = detect_emotion(frame)

    posture = detect_posture(frame)
    distance = estimate_distance(frame.shape[1] // 2)
    style_info = detecter_style(frame)

    return {
        "visage_detecte": visage_detecte,
        "genre": genre,
        "âge_estimé": age,
        "émotion": emotion,
        "posture": posture,
        "distance_cm": distance,
        "style_vestimentaire": style_info
    }
