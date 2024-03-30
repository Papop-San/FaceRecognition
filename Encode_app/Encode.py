import cv2
import face_recognition
import pickle
import os
# Import Firebase
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import storage

# Initialize Firebase
cred = credentials.Certificate("./Encode_app/faceattenreal-time-firebase-adminsdk-vdkyg-eaaec9b1c6.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': "https://faceattenreal-time-default-rtdb.firebaseio.com/",
    'storageBucket': "faceattenreal-time.appspot.com"
})

# Manage Path of file Image
folder_path = 'Encode_app/Image/Image_process'
mode_path_list = os.listdir(folder_path)
img_list = []
student_ids = []

# Loop through Image Files to get ID only
for path in mode_path_list:
    full_path = os.path.join(folder_path, path)
    img = cv2.imread(full_path)
    if img is None:
        print(f"Warning: Unable to load image at {full_path}")
        continue

    img_list.append(img)

    filename_without_extension = os.path.splitext(path)[0]
    numeric_part = filename_without_extension.split('_')[0]
    student_ids.append(numeric_part)

    # Upload images to Firebase Storage
    bucket = storage.bucket()
    blob = bucket.blob(full_path)
    blob.upload_from_filename(full_path)

print(f"Total student IDs found: {len(student_ids)}")

def find_encoding(images_list):
    encode_list = []
    for img in images_list:
        # Convert image to RGB format (face_recognition requires RGB images)
        try:
            rgb_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        except cv2.error as e:
            print(f"Error converting image to RGB: {e}")
            continue

        # Detect faces in the image
        face_locations = face_recognition.face_locations(rgb_img)
        if not face_locations:
            print("Warning: No faces found in the image.")
            continue

        # Extract face encodings
        encode = face_recognition.face_encodings(rgb_img, face_locations)[0]
        encode_list.append(encode)

    return encode_list

print("Encoding Started....")
encode_list_known = find_encoding(img_list)
encode_list_known_with_ids = [encode_list_known, student_ids]
print("Encoding Complete")

# Save encoding data
with open('EncodeFile.p', 'wb') as file:
    pickle.dump(encode_list_known_with_ids, file)
print('File Saved')
