import cv2
import face_recognition
import random
import math
import time
from datetime import datetime
from deepface import DeepFace
from fer import FER
import mediapipe as mp
from threading import Thread

# Initialisation des détecteurs
emotion_detector = FER(mtcnn=True)
mp_pose = mp.solutions.pose
pose_estimator = mp_pose.Pose()
mp_drawing = mp.solutions.drawing_utils

# Suivi des visiteurs
visitor_tracking = {}
latest_visitors_data = []

# Calibration distance
FOCAL_LENGTH = 615
FACE_WIDTH_CM = 14.0

def estimate_distance(face_width_px):
    if face_width_px == 0:
        return None
    return round((FACE_WIDTH_CM * FOCAL_LENGTH) / face_width_px, 2)

def update_visitor_timing(visitor_id):
    now = time.time()
    if visitor_id not in visitor_tracking:
        visitor_tracking[visitor_id] = {
            "first_seen": now,
            "last_seen": now,
            "last_attention_time": now,
            "total_attention_time": 0.0,
            "total_inattention_time": 0.0
        }
    else:
        last_seen = visitor_tracking[visitor_id]["last_seen"]
        delta = now - last_seen
        if delta > 3:
            visitor_tracking[visitor_id]["total_inattention_time"] += delta
            visitor_tracking[visitor_id]["last_attention_time"] = now
        else:
            visitor_tracking[visitor_id]["total_attention_time"] += delta
        visitor_tracking[visitor_id]["last_seen"] = now

def get_visitor_times(visitor_id):
    data = visitor_tracking.get(visitor_id, {})
    return (
        round(data.get("total_attention_time", 0), 2),
        round(data.get("total_inattention_time", 0), 2)
    )

def simuler_profil_via_deepface(face_img, id_visiteur=None):
    try:
        face_rgb = cv2.cvtColor(face_img, cv2.COLOR_BGR2RGB)
        analysis = DeepFace.analyze(
            face_rgb,
            actions=["gender", "age"],
            enforce_detection=True,
            detector_backend="mtcnn"
        )
        data = analysis[0] if isinstance(analysis, list) else analysis
        genre = "Homme" if data["dominant_gender"] == "Man" else "Femme"
        age = int(data["age"])
        return genre, age
    except Exception as e:
        print("[ERREUR DeepFace]", e)
        return random.choice(["Homme", "Femme"]), random.randint(18, 60)

def detect_emotion(face_img):
    try:
        result = emotion_detector.detect_emotions(face_img)
        if result and "emotions" in result[0]:
            emotions = result[0]["emotions"]
            return max(emotions, key=emotions.get)
        return "Inconnu"
    except Exception as e:
        print("[ERREUR FER]", e)
        return "Erreur"

def calculate_angle(a, b, c):
    ba = [a.x - b.x, a.y - b.y]
    bc = [c.x - b.x, c.y - b.y]
    dot_product = ba[0] * bc[0] + ba[1] * bc[1]
    mag_ba = math.hypot(*ba)
    mag_bc = math.hypot(*bc)
    if mag_ba * mag_bc == 0:
        return 0
    angle = math.acos(dot_product / (mag_ba * mag_bc))
    return math.degrees(angle)

def detect_posture(frame):
    try:
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = pose_estimator.process(frame_rgb)
        if results.pose_landmarks:
            landmarks = results.pose_landmarks.landmark
            hip = landmarks[mp_pose.PoseLandmark.LEFT_HIP.value]
            knee = landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value]
            ankle = landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value]
            angle = calculate_angle(hip, knee, ankle)
            if angle > 160:
                posture = "Debout"
            elif 70 < angle < 120:
                posture = "Assis"
            else:
                posture = "Autre posture"
            return posture, results.pose_landmarks
        return "Posture non détectée", None
    except Exception as e:
        print("[ERREUR MediaPipe]", e)
        return "Erreur", None

def detect_visitors_loop():
    global latest_visitors_data
    video_capture = cv2.VideoCapture(0)

    if not video_capture.isOpened():
        print("[ERREUR] Impossible d’ouvrir la caméra.")
        return

    id_count = 1
    print("[INFO] Analyse live active...")

    while True:
        ret, frame = video_capture.read()
        if not ret:
            continue

        visiteurs = []
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
        rgb_small_frame = small_frame[:, :, ::-1]
        face_locations = face_recognition.face_locations(rgb_small_frame)

        for (top, right, bottom, left) in face_locations:
            top *= 4
            right *= 4
            bottom *= 4
            left *= 4

            h, w, _ = frame.shape
            pad = 40
            top = max(0, top - pad)
            right = min(w, right + pad)
            bottom = min(h, bottom + pad)
            left = max(0, left - pad)

            face_img = frame[top:bottom, left:right]
            face_width = right - left

            update_visitor_timing(id_count)
            genre, age = simuler_profil_via_deepface(face_img, id_visiteur=id_count)
            emotion = detect_emotion(face_img)
            posture, _ = detect_posture(frame)
            distance = estimate_distance(face_width)
            attention_time, inattention_time = get_visitor_times(id_count)

            visiteurs.append({
                "id": id_count,
                "genre": genre,
                "âge_estimé": age,
                "émotion": emotion,
                "posture": posture,
                "distance_cm": distance,
                "temps_attention": attention_time,
                "temps_inattention": inattention_time
            })

        latest_visitors_data = visiteurs

def get_live_visitors():
    return {
        "status": "en direct",
        "timestamp": datetime.now().isoformat(),
        "visitors": latest_visitors_data
    }

# Démarrage de l'analyse live en arrière-plan
Thread(target=detect_visitors_loop, daemon=True).start()