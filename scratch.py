import cv2

print(cv2.__version__)

dispW=640
dispH=360
flip=0
key = 0
# horrible string ... one long gstreamer launch
camSet0='nvarguscamerasrc sensor-id=0 !  video/x-raw(memory:NVMM), width=1920, height=1080, format=NV12, framerate=30/1 ! nvvidconv flip-method=' + str(flip)+' ! video/x-raw, width='+str(dispW)+', height='+str(dispH)+', format=BGRx ! videoconvert ! video/x-raw, format=BGR ! appsink'
camSet1='nvarguscamerasrc sensor-id=1 !  video/x-raw(memory:NVMM), width=1920, height=1080, format=NV12, framerate=30/1 ! nvvidconv flip-method=' + str(flip)+' ! video/x-raw, width='+str(dispW)+', height='+str(dispH)+', format=BGRx ! videoconvert ! video/x-raw, format=BGR ! appsink'

# create camera object
# cam0 = cv2.VideoCapture(camSet0)
cam1 = cv2.VideoCapture(camSet1)

# USB webcam
# webcam = cv2.VideoCapture(2)

while True:
#    ret, frame  = cam0.read()
#    cv2.imshow('Cam0', frame)

    ret, frame2 = cam1.read()
    cv2.imshow('Cam1', frame2)
    
    if cv2.waitKey(1) == ord('q'):
        break

# clean up
# cam0.release()
cam1.release()
cv2.destroyAllWindows()

