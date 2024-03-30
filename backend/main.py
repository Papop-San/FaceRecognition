from flask import Flask, jsonify, request, render_template 
import cv2
import pickle
import face_recognition
import numpy as np
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from datetime import datetime, time
import pandas as pd

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
cap.set(3, 640)
cap.set(4, 480)

def adjust_time(current_time):
    if current_time >= time(13, 0) and current_time <= time(16, 0):
        return time(13, 0)
    else:
        return time(9, 0)

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
    any_recognized = False  # Flag to check if any face is recognized

    for encodeFace, faceLoc in zip(encodeCurFrame, face_locations):
        matches = face_recognition.compare_faces(encodeListKnow, encodeFace)
        faceDis = face_recognition.face_distance(encodeListKnow, encodeFace)
        
        matchIndex = np.argmin(faceDis)

        if matches[matchIndex]:
            any_recognized = True  # Set flag to True if face is recognized
            student_id = studentIds[matchIndex]
            student_data_ref = db.reference(f"Students/{student_id}")
            student_data = student_data_ref.get()

            # Retrieve department of the detected student
            department = student_data.get("depart", "Unknown")

            # Get today's date
            current_date = datetime.now().strftime("%d:%m:%Y")

            # Adjust the current time
            current_time = datetime.now().time()
            adjusted_time = adjust_time(current_time)

            # Search for the department, date, and time in the subjects
            subject_ref = db.reference(f"Subject/{department}/{current_date}/{adjusted_time}")
            subject_info = subject_ref.get()

            print("Department:", department)
            print("Date:", current_date)
            print("Time:", adjusted_time)
            print("Subject Info:", subject_info)

            response_data["detected_faces"].append({
                "student_id": student_id,
                "location": faceLoc,
                "department": department,
                "student_data": student_data,
                "subject_info": subject_info
            })
        else:
            # If the face is not matched, set student ID as "Unknown"
            response_data["detected_faces"].append({
                "student_id": "Unknown",
                "location": faceLoc,
                "department": "Unknown",
                "student_data": None,
                "subject_info": None
            })

    # Convert the detected faces data to a pandas DataFrame
    detected_faces_df = pd.DataFrame(response_data["detected_faces"])

    # Add a column for the time of saving
    detected_faces_df['Time for save'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Save the data to the Excel file
    try:
        existing_data = pd.read_excel('detected_faces.xlsx', engine='openpyxl')
        combined_data = pd.concat([existing_data, detected_faces_df], ignore_index=True)
        combined_data.to_excel('detected_faces.xlsx', index=False)
    except FileNotFoundError:
        # If the file doesn't exist, create a new one
        detected_faces_df.to_excel('detected_faces.xlsx', index=False)

    return jsonify(response_data)

if __name__ == '__main__':
    app.run(debug=True)
