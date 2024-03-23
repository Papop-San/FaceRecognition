from flask import Flask, jsonify
import cv2 
import pickle
import face_recognition
import numpy as np

app = Flask(__name__)

# Load encoding File
print("Load Encoding File")
file = open("EncodeFile.p", 'rb')
encodeListKnowWithIds = pickle.load(file)
file.close()
encodeListKnow, studentIds = encodeListKnowWithIds
print(studentIds)
print("Load Encoding File Finish....")

# Initialize the camera
cap = cv2.VideoCapture(0)
cap.set(3, 320)
cap.set(4, 240)

@app.route('/detect_faces', methods=['GET'])
def detect_faces():
    global cap, encodeListKnow, studentIds

    success, img = cap.read()

    imgS = cv2.resize(img, (0,0), None, 0.25, 0.25)
    imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

    face_locations = face_recognition.face_locations(imgS)
    encodeCurFrame = face_recognition.face_encodings(imgS, face_locations)

    if not success:
        return jsonify({"error": "Failed to capture frame"})

    response_data = {"detected_faces": []}

    for encodeFace, faceLoc in zip(encodeCurFrame, face_locations):
        matches = face_recognition.compare_faces(encodeListKnow, encodeFace)
        faceDis = face_recognition.face_distance(encodeListKnow, encodeFace)
        
        matchIndex = np.argmin(faceDis)

        if matches[matchIndex]:
            response_data["detected_faces"].append({"student_id": studentIds[matchIndex], "location": faceLoc})
    
    return jsonify(response_data)

if __name__ == '__main__':
    app.run(debug=True)
