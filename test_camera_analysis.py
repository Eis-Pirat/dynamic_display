import os
os.environ["OPENCV_LOG_LEVEL"] = "SILENT"
os.environ["DEEPFACE_DETECTOR_BACKEND"] = "opencv"
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"

import cv2
import face_recognition
from deepface import DeepFace
from fer import FER
import mediapipe as mp
import random
import math
import time
import json

# Initialisation
emotion_detector = FER(mtcnn=True)
pose_estimator = mp.solutions.pose.Pose()
FOCAL_LENGTH = 615
FACE_WIDTH_CM = 14.0

def estimate_distance(face_width_px):
    if face_width_px == 0:
        return None
    return round((FACE_WIDTH_CM * FOCAL_LENGTH) / face_width_px, 2)

def simuler_profil_via_deepface(face_img):
    try:
        face_rgb = cv2.cvtColor(face_img, cv2.COLOR_BGR2RGB)
        result = DeepFace.analyze(face_rgb, actions=["gender", "age"], detector_backend="opencv", enforce_detection=True)
        data = result[0] if isinstance(result, list) else result
        genre = "Homme" if data["dominant_gender"] == "Man" else "Femme"
        return genre, int(data["age"])
    except Exception:
        return random.choice(["Homme", "Femme"]), random.randint(18, 60)

def detect_emotion(face_img):
    try:
        emotions = emotion_detector.detect_emotions(face_img)
        if emotions and "emotions" in emotions[0]:
            return max(emotions[0]["emotions"], key=emotions[0]["emotions"].get)
        return "Inconnu"
    except:
        return "Erreur"

def detect_posture(frame):
    try:
        results = pose_estimator.process(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        if results.pose_landmarks:
            lmk = results.pose_landmarks.landmark
            hip = lmk[mp.solutions.pose.PoseLandmark.LEFT_HIP.value]
            knee = lmk[mp.solutions.pose.PoseLandmark.LEFT_KNEE.value]
            ankle = lmk[mp.solutions.pose.PoseLandmark.LEFT_ANKLE.value]
            angle = calculate_angle(hip, knee, ankle)
            if angle > 160: return "Debout"
            elif 70 < angle < 120: return "Assis"
            else: return "Autre posture"
        return "Non détectée"
    except:
        return "Erreur"

def calculate_angle(a, b, c):
    ba = [a.x - b.x, a.y - b.y]
    bc = [c.x - b.x, c.y - b.y]
    dot = ba[0]*bc[0] + ba[1]*bc[1]
    mag_ba = math.hypot(*ba)
    mag_bc = math.hypot(*bc)
    return math.degrees(math.acos(dot / (mag_ba * mag_bc))) if mag_ba * mag_bc != 0 else 0

# Capture vidéo
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
if not cap.isOpened():
    print("[❌] Erreur : Caméra inaccessible")
    exit()

print("[✅] Caméra ouverte. Analyse en cours...")

while True:
    ret, frame = cap.read()
    if not ret:
        continue

    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
    rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)
    faces = face_recognition.face_locations(rgb_small_frame)

    if faces:
        top, right, bottom, left = [coord * 4 for coord in faces[0]]
        h, w, _ = frame.shape
        pad = 40
        top, right, bottom, left = max(0, top-pad), min(w, right+pad), min(h, bottom+pad), max(0, left-pad)
        face_img = frame[top:bottom, left:right]
        face_width = right - left

        genre, age = simuler_profil_via_deepface(face_img)
        emotion = detect_emotion(face_img)
        posture = detect_posture(frame)
        distance = estimate_distance(face_width)

        result = {
            "genre": genre,
            "âge_estimé": age,
            "émotion": emotion,
            "posture": posture,
            "distance_cm": distance
        }
        print(json.dumps(result, indent=2, ensure_ascii=False))
        time.sleep(2)

    cv2.imshow("Appuyez sur Q pour quitter", frame)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
