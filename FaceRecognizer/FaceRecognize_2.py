import face_recognition
import cv2

print('Training...')
print(f'Face_Recognition_version: {face_recognition.__version__}')
print(f'OpenCV_version          : {cv2.__version__}')


# T R A I N I N G
# ======================
# to learn a face:
#   load a face, then encode it -- thats basis of training

print('Loading Training image...')

print('Loading image...')
donFace = face_recognition.load_image_file('/home/bubba/Downloads/Python_stuff/FaceRecognizer/demoImages/known/Donald Trump.jpg')

# returns series of arrays... 
print('Encoding...')
donEncoded = face_recognition.face_encodings(donFace)[0]
print('Encoded...')

print('Loading image...')
nancyFace = face_recognition.load_image_file('/home/bubba/Downloads/Python_stuff/FaceRecognizer/demoImages/known/Nancy Pelosi.jpg')

# returns series of arrays... 
print('Encoding...')
nancyEncoded = face_recognition.face_encodings(nancyFace)[0]
print('Encoded...')

# need array of NAMES (meta data) to track encodings and names by position
Encodings = [donEncoded, nancyEncoded]
Names     = ['Donald Trump', 'Nancy Pelosi']


print('Evaluating images...')
# T E S T I N G
# ======================
# now load test image to compare with known face
font = cv2.FONT_HERSHEY_SIMPLEX
testImage = face_recognition.load_image_file('/home/bubba/Downloads/Python_stuff/FaceRecognizer/demoImages/unknown/u3.jpg')

print('Finding faces...')
facePositions = face_recognition.face_locations(testImage)

print('Recognizing faces...')
allEncodings = face_recognition.face_encodings(testImage, facePositions)


# convert to format the openCV deals with BGR
testbgrimage = cv2.cvtColor(testImage, cv2.COLOR_RGB2BGR)

# clever double variable loop with 'zip'
for (top, left, bottom, right), face_encoding in zip(facePositions, allEncodings):
    #default to unknown
    name = 'Unknown Person'
    matches = face_recognition.compare_faces(Encodings, face_encoding)
    if True in matches:
        # over-ride default name with recognized name
        first_match_index = matches.index(True)
        name = Names[first_match_index]

    cv2.rectangle(testbgrimage, (left, top), (right, bottom), (0,0,255), 2)
    cv2.putText(testbgrimage, name, (left, top-6), font, 0.5, (255,255,0), 1)

cv2.imshow('myWindow', testbgrimage)

if cv2.waitKey(0) == ord('q'):
    cv2.destroyAllWindows()


