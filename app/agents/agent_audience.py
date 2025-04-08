import cv2
import face_recognition
import random
from datetime import datetime
from deepface import DeepFace
from fer import FER
import mediapipe as mp

# Initialisation des détecteurs
emotion_detector = FER(mtcnn=True)
mp_pose = mp.solutions.pose
pose_estimator = mp_pose.Pose()
mp_drawing = mp.solutions.drawing_utils

def simuler_profil_via_deepface(face_img, id_visiteur=None):
    try:
        face_rgb = cv2.cvtColor(face_img, cv2.COLOR_BGR2RGB)
        if id_visiteur:
            cv2.imwrite(f"face_debug_{id_visiteur}.jpg", face_img)

        analysis = DeepFace.analyze(
            face_rgb,
            actions=["gender", "age"],
            enforce_detection=True,
            detector_backend="mtcnn"
        )

        print("[DEBUG DeepFace output]", analysis)
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
            dominant_emotion = max(emotions, key=emotions.get)
            return dominant_emotion
        return "Inconnu"
    except Exception as e:
        print("[ERREUR FER]", e)
        return "Erreur"

def detect_posture(frame):
    try:
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = pose_estimator.process(frame_rgb)
        if results.pose_landmarks:
            return "Debout", results.pose_landmarks
        return "Posture inconnue", None
    except Exception as e:
        print("[ERREUR MediaPipe]", e)
        return "Erreur", None

def detect_visitors(display: bool = True):
    video_capture = cv2.VideoCapture(0)
    visiteurs = []
    id_count = 1

    print("[INFO] Détection en cours... Appuie sur 'q' pour quitter.")

    while True:
        ret, frame = video_capture.read()
        if not ret:
            break

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

            genre, age = simuler_profil_via_deepface(face_img, id_visiteur=id_count)
            emotion = detect_emotion(face_img)
            posture, landmarks = detect_posture(frame)

            visiteurs.append({
                "id": id_count,
                "genre": genre,
                "âge_estimé": age,
                "émotion": emotion,
                "posture": posture
            })

            print(f"[INFO] Visiteur {id_count} : {genre}, {age} ans, émotion: {emotion}, posture: {posture}")
            id_count += 1

            if display:
                cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
                if landmarks:
                    mp_drawing.draw_landmarks(frame, landmarks, mp_pose.POSE_CONNECTIONS)

        if display:
            cv2.imshow("Analyse Visiteur (q pour quitter)", frame)
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break
        else:
            if id_count > 1:
                break

    video_capture.release()
    if display:
        cv2.destroyAllWindows()

    return {
        "status": "scan terminé",
        "timestamp": datetime.now().isoformat(),
        "visitors": visiteurs
    }
