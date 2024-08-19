import face_recognition
import cv2
import os


print('Train a whole folder...')
print(f'Face_Recognition_version: {face_recognition.__version__}')
print(f'OpenCV_version          : {cv2.__version__}')

Encodings = [] # array of encoding
Names = [] # same dimension array of encoding

# /home/bubba/Downloads/Python_stuff/FaceRecognizer/demoImages/known
# /home/bubba/Downloads/Python_stuff/FaceRecognizer/demoImages/unknown

image_dir = '/home/bubba/Downloads/Python_stuff/FaceRecognizer/demoImages/known'

# recursively walk thru every file in ... getting array of files
for root, dirs, files in os.walk(image_dir):
#    print(files)
    for filename in files:
        fullpath = os.path.join(root, filename)
#        print(fullpath)
        name = os.path.splitext(filename)[0]  # remove extension leaving just 'person name'
        print(name)
        person = face_recognition.load_image_file(fullpath)
        encoding = face_recognition.face_encodings(person)[0] # take first person if more than one
        # save off pair of data with name
        Encodings.append(encoding)
        Names.append(name)

