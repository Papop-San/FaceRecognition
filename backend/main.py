from flask import Flask, jsonify, request,render_template 
import cv2
import pickle
import face_recognition
import numpy as np
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

app = Flask(__name__)

# Initialize Firebase app
cred = credentials.Certificate("./backend/faceattenreal-time-firebase-adminsdk-vdkyg-eaaec9b1c6.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://faceattenreal-time-default-rtdb.firebaseio.com/'
})

# Load encoding file
with open("./backend/EncodeFile.p", 'rb') as file:
    encodeListKnowWithIds = pickle.load(file)
encodeListKnow, studentIds = encodeListKnowWithIds

# Initialize the camera
cap = cv2.VideoCapture(0)
cap.set(3, 320)
cap.set(4, 240)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/detect_faces', methods=['POST'])
def detect_faces():
    success, img = cap.read()

    imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
    imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

    face_locations = face_recognition.face_locations(imgS)
    encodeCurFrame = face_recognition.face_encodings(imgS, face_locations)

    response_data = {"detected_faces": []}

    for encodeFace, faceLoc in zip(encodeCurFrame, face_locations):
        matches = face_recognition.compare_faces(encodeListKnow, encodeFace)
        faceDis = face_recognition.face_distance(encodeListKnow, encodeFace)
        
        matchIndex = np.argmin(faceDis)

        if matches[matchIndex]:
            student_id = studentIds[matchIndex]
            student_data_ref = db.reference(f"Students/{student_id}")
            student_data = student_data_ref.get()

            response_data["detected_faces"].append({
                "student_id": student_id,
                "location": faceLoc,
                "student_data": student_data
            })
    
    return jsonify(response_data)

if __name__ == '__main__':
    app.run(debug=True)