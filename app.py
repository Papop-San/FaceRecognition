import cv2 
import os
import pickle
import face_recognition
import numpy as np
import cvzone
import firebase_admin 
from firebase_admin import db
from firebase_admin import storage




cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)

# Setting Background Image
background_path = './Resource/background.png'
if os.path.exists(background_path):
    imgBackground = cv2.imread(background_path)
else:
    print("Background image not found.")
    exit()

# Importing the mode images into a list
floderModePath = './Resource/Modes'
modePathList  = os.listdir(floderModePath)
imgModeList = []

for path in modePathList:
    imgModeList.append(cv2.imread(os.path.join(floderModePath, path)))




#Load encoding File 
print("Load Encoding File")

#Importing File 
file = open("EncodeFile.p",'rb')
encodeListKnowWithIds = pickle.load(file)
file.close()
encodeListKnow,studentIds = encodeListKnowWithIds
print(studentIds)
print("Load Encoding File Finish....")

modeType =0
counter = 0

while True:
    success, img = cap.read()

    imgS = cv2.resize(img,(0,0),None,0.25,0.25)
    imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

    FaceCurFrame = face_recognition.face_locations(imgS)
    encodeCurFrame = face_recognition.face_encodings(imgS,FaceCurFrame)


    if not success:
        print("Failed to capture frame.")
        break

    # Overlay webcam feed onto the background image
    imgBackground[162:162+480 ,55:55+640] = img
    imgBackground[44:44 + 633 , 808:808 + 414]= imgModeList[3]

    
    for encodeFace , faceLoc in zip(encodeCurFrame ,FaceCurFrame):
            matches = face_recognition.compare_faces(encodeListKnow,encodeFace)
            faceDis = face_recognition.face_distance(encodeListKnow,encodeFace)
            
            # print('Matches',matches)
            # print("FaceDis",faceDis)



            matcheIndex = np.argmin(faceDis)
            print("Match Index" , matcheIndex)

            if matches[matcheIndex]:
                # print('Know Face Detected ' )
                print(studentIds[matcheIndex])
                y1 ,x2 ,y2 ,x1 = faceLoc
                y1 ,x2 ,y2 ,x1 = y1*4 , x2*4 , y2*4 , x1*4      
                bbox = 55 +x1 , 162 +y1 , x2-x1 , y2-y1
                imgBackground = cvzone.cornerRect(imgBackground ,bbox ,rt=0)
                id = studentIds[matcheIndex]
                if counter == 0: 
                     counter = 1 
                     modeType = 1 
            else:
                print("Unknow Face")
            


    # Display the composite image
    cv2.imshow("Face Attendance", imgBackground)

    # Break the loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
