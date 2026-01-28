"""
SMART AI MIRROR 

This is a complete modular architecture for a Smart AI Mirror system.


FEATURES IMPLEMENTED / STRUCTURE PROVIDED:

1.  Webcam smart mirror interface (OpenCV)
2.  Custom mirror name + theme color
3.  GUI control panel (Tkinter)
4.  Voice assistant (Speech Recognition + Text-to-Speech)
5.  Rule-based AI + extendable NLP
6.  Face detection + recognition scaffold
7.  Pose tracking + posture feedback
8.  Gesture control (MediaPipe Hands)
9.  Emotion detection (placeholder – CNN ready)
10. Memory / user profile system
11. Health monitoring scaffold (heart rate, fatigue)
12. AR filters scaffold (glasses, makeup, hair)
13. Smart home / IoT command interface
14. Multilingual voice ready
15. REAL CNN EMOTION MODEL (OPTIONAL ADVANCED)
16. REAL FACE RECOGNITION (SECURITY + PERSONALIZATION)
17. CHATGPT AI (REAL CONVERSATION)
18. IOT / SMART HOME (MQTT)
19. BEHAVIOR ANALYSIS (DATA LOGGING)


-------------------------------------------------
INSTALL REQUIREMENTS:

pip install opencv-python mediapipe numpy speechrecognition pyttsx3 pyaudio tkinter face-recognition

-------------------------------------------------
RUN:

python smart_ai_mirror.py

ESC to exit
-------------------------------------------------
"""

# ======================= IMPORTS =======================
import cv2
import mediapipe as mp
import numpy as np
import threading
import time
import json
import speech_recognition as sr
import pyttsx3
import tkinter as tk
from tkinter import ttk

# ======================= GLOBAL SETTINGS =======================
MIRROR_NAME = "My Smart Mirror"
THEME_COLOR = (0, 255, 255)   # Cyan
LANGUAGE = "en"             # Future multilingual

# ======================= MEMORY / PROFILE SYSTEM =======================
# This can later be saved in a JSON file or database
user_profile = {
    "name": "User",
    "favorite_color": "Blue",
    "last_mood": "Happy",
    "last_login": time.ctime(),
    "daily_activity": []
}

# ======================= TEXT TO SPEECH ENGINE =======================
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)
engine.setProperty('rate', 170)


def speak(text):
    """Speak any text using TTS"""
    engine.say(text)
    engine.runAndWait()

# ======================= SPEECH RECOGNITION =======================
recognizer = sr.Recognizer()

# ======================= MEDIA PIPE MODELS =======================
mp_pose = mp.solutions.pose
mp_hands = mp.solutions.hands
mp_face = mp.solutions.face_detection

pose = mp_pose.Pose()
hands = mp_hands.Hands(max_num_hands=1)
face_detector = mp_face.FaceDetection(model_selection=0)

# ======================= AI RESPONSE ENGINE =======================

def ai_reply(text):
    """Rule-based + extendable AI brain"""
    text = text.lower()

    # Romantic / fun replies
    if "love you" in text:
        return "I love you too baby"

    # Greeting
    if "hello" in text or "hi" in text:
        return f"Hello! Welcome back, {user_profile['name']}"

    # Name query
    if "your name" in text:
        return f"My name is {MIRROR_NAME}"

    # Time query
    if "time" in text:
        return "Current time is " + time.ctime()

    # Mood based
    if "tired" in text:
        return "You should take some rest and drink water"

    # Smart home placeholder
    if "turn on" in text or "turn off" in text:
        smart_home_command(text)
        return "Smart home command executed"

    return "I am listening to you"

# ======================= VOICE ASSISTANT THREAD =======================

def listen_and_talk():
    """Continuously listen and reply using voice"""
    while True:
        try:
            with sr.Microphone() as source:
                recognizer.adjust_for_ambient_noise(source)
                audio = recognizer.listen(source)
                text = recognizer.recognize_google(audio)

                print("You said:", text)
                reply = ai_reply(text)

                speak(reply)

        except:
            pass

# Start voice assistant in background
threading.Thread(target=listen_and_talk, daemon=True).start()

# ======================= POSTURE MONITORING =======================

def check_posture(landmarks):
    """Basic posture analysis using shoulder and hip alignment"""
    try:
        shoulder = landmarks.landmark[mp_pose.PoseLandmark.LEFT_SHOULDER]
        hip = landmarks.landmark[mp_pose.PoseLandmark.LEFT_HIP]

        if abs(shoulder.y - hip.y) < 0.05:
            return "Good Posture"
        else:
            return "Straighten your back"
    except:
        return ""

# ======================= GESTURE CONTROL =======================

def detect_gesture(hand_landmarks):
    """Detect simple hand gestures"""
    fingers = hand_landmarks.landmark

    # Index finger up
    if fingers[8].y < fingers[6].y:
        return "Nice Move!"

    return ""

# ======================= FACE RECOGNITION (BASIC) =======================

def recognize_face(frame):
    """Detect face and greet user (placeholder for real recognition)"""
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = face_detector.process(rgb)

    if result.detections:
        return f"Welcome back, {user_profile['name']}"
    else:
        return "Unknown user detected"

# ======================= EMOTION RECOGNITION =======================

def detect_emotion(face_img):
    """Placeholder for CNN emotion detection"""
    # Later integrate FER2013 / deep CNN
    return "Happy"

# ======================= HEALTH MONITORING =======================

def estimate_heart_rate(face_img):
    """Placeholder for camera-based heart rate estimation"""
    return "72 BPM"

# ======================= AR FILTER SYSTEM =======================

def apply_ar_filter(frame):
    """Placeholder for AR effects (glasses, makeup, hair)"""
    return frame

# ======================= SMART HOME / IOT =======================

def smart_home_command(cmd):
    """Placeholder for MQTT / IoT control"""
    print("[SMART HOME] Command:", cmd)

# ======================= GUI CONTROL PANEL =======================

def gui_panel():
    global MIRROR_NAME, THEME_COLOR

    def update_name():
        global MIRROR_NAME
        MIRROR_NAME = name_entry.get()

    def set_blue():
        global THEME_COLOR
        THEME_COLOR = (255, 0, 0)

    def set_green():
        global THEME_COLOR
        THEME_COLOR = (0, 255, 0)

    def set_pink():
        global THEME_COLOR
        THEME_COLOR = (255, 105, 180)

    root = tk.Tk()
    root.title("Smart Mirror Control Panel")

    ttk.Label(root, text="Mirror Name").pack()
    name_entry = ttk.Entry(root)
    name_entry.pack()

    ttk.Button(root, text="Update Name", command=update_name).pack()

    ttk.Label(root, text="Theme Color").pack()
    ttk.Button(root, text="Blue", command=set_blue).pack()
    ttk.Button(root, text="Green", command=set_green).pack()
    ttk.Button(root, text="Pink", command=set_pink).pack()

    ttk.Button(root, text="Exit", command=root.destroy).pack()

    root.mainloop()

# Start GUI thread
threading.Thread(target=gui_panel, daemon=True).start()

# ======================= MAIN CAMERA LOOP =======================
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    h, w, _ = frame.shape

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # ---------------- POSE TRACKING ----------------
    pose_result = pose.process(rgb)

    if pose_result.pose_landmarks:
        mp.solutions.drawing_utils.draw_landmarks(
            frame, pose_result.pose_landmarks, mp_pose.POSE_CONNECTIONS
        )

        posture_msg = check_posture(pose_result.pose_landmarks)
        cv2.putText(frame, posture_msg, (30, 90),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)

    # ---------------- HAND GESTURES ----------------
    hand_result = hands.process(rgb)

    if hand_result.multi_hand_landmarks:
        for hand_landmarks in hand_result.multi_hand_landmarks:
            mp.solutions.drawing_utils.draw_landmarks(
                frame, hand_landmarks, mp_hands.HAND_CONNECTIONS
            )

            gesture_msg = detect_gesture(hand_landmarks)
            cv2.putText(frame, gesture_msg, (30, 130),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 0, 0), 2)

    # ---------------- FACE + EMOTION ----------------
    greeting = recognize_face(frame)
    emotion = detect_emotion(frame)

    cv2.putText(frame, greeting, (30, 170),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 0), 2)

    cv2.putText(frame, f"Mood: {emotion}", (30, 210),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

    # ---------------- HEALTH ----------------
    heart_rate = estimate_heart_rate(frame)

    cv2.putText(frame, f"Heart Rate: {heart_rate}", (30, 250),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)

    # ---------------- AR FILTER ----------------
    frame = apply_ar_filter(frame)

    # ---------------- UI OVERLAY ----------------
    cv2.rectangle(frame, (10, 10), (w - 10, h - 10), THEME_COLOR, 3)

    cv2.putText(frame, MIRROR_NAME, (30, 50),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

    # ---------------- SHOW WINDOW ----------------
    cv2.imshow("SMART AI MIRROR", frame)

    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()


# ======================= ADVANCED EMOTION CNN (ADD-ON) =======================
from fer import FER

emotion_detector = FER(mtcnn=True)

def advanced_detect_emotion(frame):
    """
    CNN-based real emotion detection (FER-2013)
    """
    try:
        emotions = emotion_detector.detect_emotions(frame)
        if emotions:
            emotion, score = max(
                emotions[0]["emotions"].items(),
                key=lambda x: x[1]
            )
            return emotion.capitalize()
        else:
            return "Neutral"
    except:
        return "Neutral"


# ======================= ADVANCED FACE RECOGNITION (ADD-ON) =======================
import face_recognition

known_image = face_recognition.load_image_file("user.jpg")
known_encoding = face_recognition.face_encodings(known_image)[0]

def advanced_recognize_face(frame):
    """
    Real face recognition using face encodings
    """
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    locations = face_recognition.face_locations(rgb)
    encodings = face_recognition.face_encodings(rgb, locations)

    for encoding in encodings:
        match = face_recognition.compare_faces([known_encoding], encoding)
        if match[0]:
            return "Authorized User Detected"
    return "Unknown User"



# ======================= CHATGPT AI ADD-ON =======================
import openai

openai.api_key = "YOUR_OPENAI_API_KEY"

def chatgpt_ai_reply(user_text):
    """
    Advanced conversational AI using ChatGPT
    """
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a caring smart mirror assistant."},
            {"role": "user", "content": user_text}
        ]
    )
    return response.choices[0].message["content"]




# ======================= SMART HOME IOT ADD-ON =======================
import paho.mqtt.client as mqtt

mqtt_client = mqtt.Client()
mqtt_client.connect("broker.hivemq.com", 1883, 60)

def iot_smart_home(cmd):
    """
    Control smart devices using MQTT
    """
    if "light" in cmd:
        mqtt_client.publish("smartmirror/light", "ON")
    elif "fan" in cmd:
        mqtt_client.publish("smartmirror/fan", "ON")



# ======================= USER BEHAVIOR ANALYSIS ADD-ON =======================
import csv

def log_user_activity(emotion, posture):
    """
    Save user behavior for analysis
    """
    with open("user_activity.csv", "a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([time.ctime(), emotion, posture])


