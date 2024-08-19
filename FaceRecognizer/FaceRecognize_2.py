import face_recognition
import cv2

print('Training...')
print(f'Face_Recognition_version: {face_recognition.__version__}')
print(f'OpenCV_version          : {cv2.__version__}')


# T R A I N I N G
# ======================
# to learn a face:
#   load a face, then encode it -- thats basis of training

donFace = face_recognition.load_image_file('/home/bubba/Downloads/Python_stuff/FaceRecognizer/demoImages/known/Donald Trump.jpg')
# returns series of arrays... 
donEncoded = face_recognition.face_encodings(donFace)[0]

nancyFace = face_recognition.load_image_file('/home/bubba/Downloads/Python_stuff/FaceRecognizer/demoImages/known/Nancy Pelosi.jpg')
# returns series of arrays... 
nancyEncoded = face_recognition.face_encodings(nancyFace)[0]

# need array of NAMES (meta data) to track encodings and names by position
Encodings = [donEncoded, nancyEncoded]
Names     = ['Donald Trump', 'Nancy Pelosi']



# T E S T I N G
# ======================
# now load test image to compare with known face
font = cv2.FONT_HERSHEY_SIMPLEX
testImage = face_recognition.load_image_file('/home/bubba/Downloads/Python_stuff/FaceRecognizer/demoImages/unknown/u3.jpg')

facePositions = face_recognition.face_locations(testImage)

allEncodings = face_recognition.face_encodings(testImage, facePositions)

# convert to format the openCV deals with BGR
testbgrimage = cv2.cvtColor(testImage, cv2.COLOR_RGB2BGR)

for (top, left, bottom, right) in face_locations:
    cv2.rectangle(rgbimage, (col1, row1), (col2, row2), (0,0,255), 2)

cv2.imshow('myWindow', rgbimage)

if cv2.waitKey(0) == ord('q'):
    cv2.destroyAllWindows()


