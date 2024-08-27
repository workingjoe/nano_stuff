import face_recognition
import cv2
import os
import pickle

print(f'OpenCV_version          : {cv2.__version__}')

Encodings = [] # array of encoding
Names = []     # same dimension array of encoding

# Restore from pickle 
with open('Train.pkl', 'rb') as theFile:
    Names = pickle.load(theFile)
    Encodings = pickle.load(theFile)

if len(Names) < 1 :
    print("No Training Data was loaded!, run trainSave first")
    exit

# create a gstreamer pipeline command for CSI cameras
def gstreamer_pipeline(
    sensor_id=0,
    capture_width=1920,
    capture_height=1080,
    display_width=1920,
    display_height=1080,
    framerate=30,
    flip_method=0,
):
    return (
        "nvarguscamerasrc sensor-id=%d ! "
        "video/x-raw(memory:NVMM), width=%d, height=%d, framerate=%d/1 ! "
        "nvvidconv flip-method=%d ! "
        "video/x-raw, width=%d, height=%d, format=BGRx ! "
        "videoconvert ! "
        "video/x-raw, format=BGR ! appsink"
        % (
            sensor_id,
            capture_width,
            capture_height,
            framerate,
            flip_method,
            display_width,
            display_height,
        )
    )


dispW = 640
dispH = 480
width = dispW
height= dispH

flip  = 0
frame_moved = 0

noiseThreshold = 200

# horrible string ... one long gstreamer launch
# camSet0='nvarguscamerasrc sensor-id=0 ! video/x-raw(memory:NVMM), width=3264, height=2464, format=NV12, framerate=21/1 ! nvvidconv flip-method=' + str(flip)+' ! video/x-raw, width='+str(dispW)+', height='+str(dispH)+', format=BGRx ! videoconvert ! video/x-raw, format=BGR ! appsink'
# camSet1='nvarguscamerasrc sensor-id=1 ! video/x-raw(memory:NVMM), width=3264, height=2464, format=NV12, framerate=21/1 ! nvvidconv flip-method=' + str(flip)+' ! video/x-raw, width='+str(dispW)+', height='+str(dispH)+', format=BGRx ! videoconvert ! video/x-raw, format=BGR ! appsink'
#
# for arducam there is a lens/camera calibration to setup...
# https://docs.arducam.com/Nvidia-Jetson-Camera/Application-note/Fix-Red-Tint-with-ISP-Tuning/
#
# wget https://www.arducam.com/downloads/Jetson/Camera_overrides.tar.gz
# tar zxvf Camera_overrides.tar.gz
# sudo cp camera_overrides.isp /var/nvidia/nvcam/settings/
# sudo chmod 664 /var/nvidia/nvcam/settings/camera_overrides.isp
# sudo chown root:root /var/nvidia/nvcam/settings/camera_overrides.isp


# camSet0 = gstreamer_pipeline( sensor_id=0, 
#                              capture_width=3264,
#                              capture_height=2464,
#                              display_width=dispW,
#                              display_height=dispH,
#                              framerate=21,
#                              flip_method=flip,
#                            )
camSet0 = gstreamer_pipeline( sensor_id=0, 
                             capture_width=1920,
                             capture_height=1080,
                             display_width=dispW,
                             display_height=dispH,
                             framerate=30,
                             flip_method=flip,
                           )
camSet1 = gstreamer_pipeline( sensor_id=1, 
                             capture_width=1920,
                             capture_height=1080,
                             display_width=dispW,
                             display_height=dispH,
                             framerate=30,
                             flip_method=flip,
                           )
# print(camSet1)
# print("------------------------------------")

# cam = cv2.VideoCapture(camSet1)

# or create USB webcam object (arg is 0,1, or 2 depends on CSI cameras installed)
# check v4l2-ctl -d2 --list-formats-ext and see what parms work...
# camSet2 = 'gst-launch-1.0 v4l2src device=/dev/video2 ! image/jpeg,format=MJPG,width=640,height=480,framerate=30/1 ! nvv4l2decoder mjpeg=1 ! nvvidconv ! autovideosink'

camSet2 = 2
cam = cv2.VideoCapture(camSet0)

# fixup USB camera to reasonable size and formatting
if (camSet2 == 2) and (cam.isOpened()) :
    width  = cam.get(cv2.CAP_PROP_FRAME_WIDTH)
    height = cam.get(cv2.CAP_PROP_FRAME_HEIGHT)
#     print(f"Width: {width} x Height: {height}")
    if (width != dispW):
        ret = cam.set(cv2.CAP_PROP_FRAME_WIDTH,  dispW)
        # if not ret:
        #     print("can't set WIDTH")
    if (height != dispH):
        ret = cam.set(cv2.CAP_PROP_FRAME_HEIGHT, dispH)
        # if not ret:
        #     print("can't set HEIGHT")

    ret = cam.set(cv2.CAP_PROP_CONVERT_RGB, True)
    # if not ret:
    #     print("can't set CONVERT_RGB")

    width  = dispW # assume cam.get(cv2.CAP_PROP_FRAME_WIDTH)
    height = dispH # assume cam.get(cv2.CAP_PROP_FRAME_HEIGHT)
    # print(f"New Width: {width} x New Height: {height}")

font = cv2.FONT_HERSHEY_SIMPLEX

while True:
    ret, frame = cam.read()

    # scale down version for comparison speed up, 
    frameSmall = cv2.resize(frame, (0,0), fx=0.33, fy=0.33)

    # change to frame recognizer format
    frameRGB = cv2.cvtColor(frameSmall, cv2.COLOR_BGR2RGB)
    facePositions = face_recognition.face_locations(frameRGB, model='cnn')  # parallel model jetson_nano 
    allEncodings = face_recognition.face_encodings(frameRGB, facePositions) # encode each found face

    for (top, right, bottom, left), faceEncoding in zip(facePositions, allEncodings) :
        name = 'Unknown Person'
        matches = face_recognition.compare_faces(Encodings, faceEncoding) # Encodings is ALL, return array of FFFFT
        if True in matches :
            first_match_index = matches.index(True) # get position of True in matches
            name = Names[first_match_index]
            top    = top*3
            bottom = bottom*3
            left   = left*3
            right  = right*3
            frame = cv2.rectangle( frame, (left, top), (right, bottom),  (0,0,255),2)
            frame = cv2.putText(frame, name, (left, top-6), font, 0.75, (0,255,255),2)

    cv2.imshow('nanoCam',frame)

    if frame_moved == 0:
        cv2.moveWindow('nanoCam',0,0)
        frame_moved = 1

 
    if cv2.waitKey(1) == ord('q'):
        break

cam.release()
cv2.destroyAllWindows()   