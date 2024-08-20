import face_recognition
import cv2
import os
import pickle

print(f'Face_Recognition_version: {face_recognition.__version__}')
print(f'OpenCV_version          : {cv2.__version__}')

Encodings = [] # array of encoding
Names = [] # same dimension array of encoding

# expect that traning data be NAMED for face to be found in image ex:"Donald Trump.jpg"
trainingPath = '/home/bubba/Downloads/Python_stuff/FaceRecognizer/demoImages/known'
testingPath = '/home/bubba/Downloads/Python_stuff/FaceRecognizer/demoImages/unknown'


# Restore from pickle 
with open('Train.pkl', 'rb') as theFile:
    Names = pickle.load(theFile)
    Encodings = pickle.load(theFile)

if len(Names) < 1 :
    print("No Training Data was loaded!, run trainSave first")
    exit


print(f'Evaluating images from \"{testingPath}\" ')

font = cv2.FONT_HERSHEY_SIMPLEX

# recursively walk thru every file in TEST folder
for root, dirs, files in os.walk(testingPath):
#    print(files)
    for filename in files:
        fullpath = os.path.join(root, filename)
        testImage = face_recognition.load_image_file(fullpath)
        print(f'Locate faces in \"{filename}\" ...')
        facePositions = face_recognition.face_locations(testImage)
        numFaces = len(facePositions)
        print(f'Recognizing {numFaces} face(s)...')
        foundEncodings = face_recognition.face_encodings(testImage, facePositions)

        # convert to BGR format openCV understands
        testbgrimage = cv2.cvtColor(testImage, cv2.COLOR_RGB2BGR)

        # clever double variable loop with 'zip'
        for (top, left, bottom, right), face_encoding in zip(facePositions, foundEncodings):
            #default to unknown
            name = 'Unknown Person'
            matches = face_recognition.compare_faces(Encodings, face_encoding)
            if True in matches:
                # over-ride default name with recognized name
                first_match_index = matches.index(True)
                name = Names[first_match_index]

                cv2.rectangle(testbgrimage, (left, top), (right, bottom), (0,0,255), 2)
                cv2.putText(testbgrimage, name, (left, top-6), font, 0.5, (0, 255, 255), 1)

        cv2.imshow('myWindow', testbgrimage)
        cv2.moveWindow('myWindow', 0,0)

        if cv2.waitKey(0) == ord('q'):
            cv2.destroyAllWindows()
            quit()
        else :
            cv2.destroyAllWindows()

