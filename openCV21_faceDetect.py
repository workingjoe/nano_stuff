import cv2
import numpy as np
import time

# NOTE: using model from "haarcascades for opencv"
# https://github.com/opencv/opencv/tree/master/data/haarcascades


print(cv2.__version__)

def nothing(x):
    pass

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


cv2.namedWindow('Trackbars')
cv2.moveWindow('Trackbars',1320,800)
 
 
dispW = 640
dispH = 480
width = dispW
height= dispH

flip  = 0

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
camSet  = camSet2 # camSet0, camSet1, camSet2
cam = cv2.VideoCapture(camSet)

# fixup USB camera to reasonable size and formatting
if (camSet == camSet2) and (cam.isOpened()) :
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

# '/home/bubba/Downloads/Python_stuff/cascade/haarcascade_eye_tree_eyeglasses.xml'
# '/home/bubba/Downloads/Python_stuff/cascade/haarcascade_eye.xml'
# '/home/bubba/Downloads/Python_stuff/cascade/haarcascade_frontalface_alt2.xml'
# '/home/bubba/Downloads/Python_stuff/cascade/haarcascade_frontalface_alt.xml'
# '/home/bubba/Downloads/Python_stuff/cascade/haarcascade_frontalface_default.xml'
# '/home/bubba/Downloads/Python_stuff/cascade/haarcascade_lefteye_2splits.xml'
# '/home/bubba/Downloads/Python_stuff/cascade/haarcascade_righteye_2splits.xml'
# '/home/bubba/Downloads/Python_stuff/cascade/haarcascade_smile.xml'


# face_cascade = cv2.CascadeClassifier('/home/bubba/Downloads/Python_stuff/cascade/haarcascade_frontalface_default.xml')
# face_cascade = cv2.CascadeClassifier('/home/bubba/Downloads/Python_stuff/cascade/haarcascade_frontalface_alt.xml')
face_cascade = cv2.CascadeClassifier('/home/bubba/Downloads/Python_stuff/cascade/haarcascade_frontalface_alt2.xml')
eye_cascade  = cv2.CascadeClassifier('/home/bubba/Downloads/Python_stuff/cascade/haarcascade_eye.xml')

# CUDA variation
# face_cascade = cv2.CascadeClassifier('/home/bubba/Downloads/Python_stuff/cascade/cuda/haarcascade_frontalface_default.xml')
# eye_cascade  = cv2.CascadeClassifier('/home/bubba/Downloads/Python_stuff/cascade/cuda/haarcascade_eye.xml')
# Lefteye_cascade  = cv2.CascadeClassifier('/home/bubba/Downloads/Python_stuff/cascade/cuda/haarcascade_lefteye_2splits.xml')
# Righteye_cascade = cv2.CascadeClassifier('/home/bubba/Downloads/Python_stuff/cascade/cuda/haarcascade_righteye_2splits.xml')


frame_moved = 0
while True:
    ret, frame = cam.read()
    # frame=cv2.imread('smarties.png')

    # remove color to make it easier
    grayFrame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # return array or list of what it finds (args are tweak params)
    faces = face_cascade.detectMultiScale(grayFrame, 1.3, 5)
    # iterate into collection and grab ROI
    for (x,y,width,height) in faces:
       # rectangle (what, (tuple-x,y), (tuple_bottom-x,y), (B,G,R), linewidth)
       frame = cv2.rectangle(frame, (x,y), (x+width,y+height), (0,0,128), 2)

       # look for eyes inside FACE rectangle
       roi_gray  = grayFrame[y:(y+height), x:(x+width)]
       roi_color = frame[y:(y+height), x:(x+width)]
       
       eyes = eye_cascade.detectMultiScale(roi_gray, 1.3, 5)
       # iterate into collection and grab ROI
       for (xEye,yEye,widthEye,heightEye) in eyes:
          # rectangle (what, (tuple-x,y), (tuple_bottom-x,y), (B,G,R), linewidth)
          roi_color = cv2.rectangle(roi_color, (xEye,yEye), (xEye+widthEye,yEye+heightEye), (128,0,0), 2)

    # Lefteyes = Lefteye_cascade.detectMultiScale(grayFrame, 1.3, 5)
    # iterate into collection and grab ROI
    # for (x,y,width,height) in Lefteyes:
    #    # rectangle (what, (tuple-x,y), (tuple_bottom-x,y), (B,G,R), linewidth)
    #    frame = cv2.rectangle(frame, (x,y), (x+width,y+height), (128,0,0), 2)

    # Refteyes = Righteye_cascade.detectMultiScale(grayFrame, 1.3, 5)
    # iterate into collection and grab ROI
    # for (x,y,width,height) in Refteyes:
    #    # rectangle (what, (tuple-x,y), (tuple_bottom-x,y), (B,G,R), linewidth)
    #    frame = cv2.rectangle(frame, (x,y), (x+width,y+height), (128,128,0), 2)

    cv2.imshow('nanoCam',frame)

    if frame_moved == 0:
        cv2.moveWindow('nanoCam',0,0)
        frame_moved = 1

 
    if cv2.waitKey(1) == ord('q'):
        break

cam.release()
cv2.destroyAllWindows()