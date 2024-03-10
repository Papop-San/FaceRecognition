import cv2
import face_recognition
import pickle
import os
# Import Firebase
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import storage

cred = credentials.Certificate("faceattenreal-time-firebase-adminsdk-vdkyg-eaaec9b1c6.json")
firebase_admin.initialize_app(cred,{
    'databaseURL':"https://faceattenreal-time-default-rtdb.firebaseio.com/",
    'storageBucket': "faceattenreal-time.appspot.com"
})

# Mange Path of file Image
folder_path = 'Image/Image_process'
mode_path_list = os.listdir(folder_path)
img_list = []
student_ids = []

# Loop Image File  For get Id only
for path in mode_path_list:
    img_list.append(cv2.imread(os.path.join(folder_path, path)))
    
    filename_without_extension = os.path.splitext(path)[0]
    numeric_part = filename_without_extension.split('_')[0]
    student_ids.append(numeric_part)

    file_name = os.path.join(folder_path, path)
    bucket = storage.bucket()
    blob = bucket.blob(file_name)
    blob.upload_from_filename(file_name)

print(len(student_ids))

def find_encoding(images_list):
    encode_list = []
    for img in images_list:
        # Convert image to RGB format (face_recognition requires RGB images)
        rgb_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        # Detect faces in the image
        face_locations = face_recognition.face_locations(rgb_img)
        if len(face_locations) == 0:
            print("No face found in the image.")
            continue
        
        # Extract face encodings
        encode = face_recognition.face_encodings(rgb_img, face_locations)[0]
        encode_list.append(encode)
    
    return encode_list

print("Encoding Started....")
encode_list_known = find_encoding(img_list)
encode_list_known_with_ids = [encode_list_known, student_ids]
print(encode_list_known)
print("Encoding Complete")

file = open('EncodeFile.p', 'wb')
pickle.dump(encode_list_known_with_ids, file)
file.close()
print('File Save')
