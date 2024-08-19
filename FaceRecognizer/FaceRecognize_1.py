import face_recognition
import cv2

print(f'Face_Recognition_version: {face_recognition.__version__}')
print(f'OpenCV_version          : {cv2.__version__}')

image = face_recognition.load_image_file('/home/bubba/Downloads/Python_stuff/FaceRecognizer/demoImages/unknown/u3.jpg')

face_locations = face_recognition.face_locations(image)

# convert to format the openCV deals with BGR
bgrimage = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

for (row1, col1, row2, col2) in face_locations:
    cv2.rectangle(bgrimage, (col1, row1), (col2, row2), (0,0,255), 2)

cv2.imshow('myWindow', bgrimage)

if cv2.waitKey(0) == ord('q'):
    cv2.destroyAllWindows()


