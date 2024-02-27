import cv2
import face_recognition
import pickle
import os

#Mange Paht of file Image
floderpath = 'Image/Image_process'
modePathList = os.listdir(floderpath)
# print(modePathList)
imgList = []
studentIds =[]

#Loop Image File  For get Id only
for path in modePathList:
    imgList.append(cv2.imread(os.path.join(floderpath, path)))
    
    filename_without_extension = os.path.splitext(path)[0]
    numeric_part = filename_without_extension.split('_')[0]
    studentIds.append(numeric_part)

print(len(studentIds))


 
def findEncoding(imagesList):
    encodeList = []
    for img in imagesList:
        # Convert image to RGB format (face_recognition requires RGB images)
        rgb_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        # Detect faces in the image
        face_locations = face_recognition.face_locations(rgb_img)
        if len(face_locations) == 0:
            print("No face found in the image.")
            continue
        
        # Extract face encodings
        encode = face_recognition.face_encodings(rgb_img, face_locations)[0]
        encodeList.append(encode)
    
    return encodeList

print("Encoding Started....")
encodeListKnow = findEncoding(imgList)
encodeListKnowWithIds = [encodeListKnow,studentIds]
print(encodeListKnow)
print("Encoding Complete")

file = open('EncodeFile.p','wb')
pickle.dump(encodeListKnowWithIds,file)
file.close()
print('File Save')
