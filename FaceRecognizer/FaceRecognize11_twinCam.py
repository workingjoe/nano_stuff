import rich
from rich import inspect
from rich import pretty
from threading import Thread
import cv2
import time
import numpy as np


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
        "video/x-raw(memory:NVMM),width=%d,height=%d,format=NV12,framerate=%d/1 ! "
        "nvvidconv flip-method=%d ! "
        "video/x-raw,width=%d,height=%d,format=BGRx ! "
        "videoconvert ! "
#        "video/x-raw,format=BGR ! autovideoconvert | xvimagesink -e" # used for command-line
        "video/x-raw,format=BGR ! appsink"
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
# NOTE: This does not work.  It *does* from a command-line, so I don't know what's going on...
# camSetUSB = 'v4l2src device=/dev/video2 ! video/x-raw,width=640,height=480,format=YUY2 ! autovideoconvert ! appsink'                        
camSetUSB = 2

# print(f'camset0 = \n\"{camSet0}\"')

# class to manage a camera
#   -- launch
#   -- operate in independent thread
#   -- collect frames, provide way for user to get frame
class vStream:
    def __init__(self, camSet, wide, high):
        self.width  = wide
        self.height = high

        # for USB use V4L backend, else use defalt CSI/FFMPEG 
        if (camSet == camSetUSB):
            self.capture = cv2.VideoCapture(camSet, cv2.CAP_V4L)
        else:
            self.capture = cv2.VideoCapture(camSet, cv2.CAP_ANY)

        # fixup USB camera to reasonable size and formatting
        if (camSet == camSetUSB) and (self.capture.isOpened()) :
            self.width  = self.capture.get(cv2.CAP_PROP_FRAME_WIDTH)
            self.height = self.capture.get(cv2.CAP_PROP_FRAME_HEIGHT)
        #     print(f"Width: {width} x Height: {height}")
            if (self.width != wide):
                ret = self.capture.set(cv2.CAP_PROP_FRAME_WIDTH,  wide)
                # if not ret:
                #     print("can't set WIDTH")
            if (self.height != high):
                ret = self.capture.set(cv2.CAP_PROP_FRAME_HEIGHT, high)
                # if not ret:
                #     print("can't set HEIGHT")

            ret = self.capture.set(cv2.CAP_PROP_CONVERT_RGB, True)
            # if not ret:
            #     print("can't set CONVERT_RGB")

            # width  = dispW # assume cam.get(cv2.CAP_PROP_FRAME_WIDTH)
            # height = dispH # assume cam.get(cv2.CAP_PROP_FRAME_HEIGHT)
            # print(f"New Width: {width} x New Height: {height}")

        self.theThread = Thread(target=self.update, args = ([]))
        self.theThread.daemon = True
        self.frame = None
        self.theThread.start()

    def update(self):
        while True:
            ret, self.frame = self.capture.read()

    # external GETTER method
    def getFrame(self) :
        return self.frame


camera_1 = vStream(camSet1, dispW, dispH)
# camera_2 = vStream(camSet0, dispW, dispH)
camera_2 = vStream(camSetUSB, dispW, dispH)

while True:
    while camera_1.theThread._started._flag == False:
        print('waiting for camera_1 to start...')
        time.sleep(1)

    while camera_2.theThread._started._flag == False:
        print('waiting for camera_2 to start...')
        time.sleep(1)

    try:

        myFrame1 = camera_1.getFrame()      
        myFrame2 = camera_2.getFrame()
        if myFrame1 is not None and myFrame2 is not None:        
            myComboFrames = np.hstack((myFrame1,myFrame2))
            cv2.imshow('nanoCamCombo',myComboFrames)    
            if frame_moved == 0:
                cv2.moveWindow('nanoCamCombo',0,0)
                frame_moved = 1            

    except:
        print('Frame(s) not available... retrying...')

    
    if cv2.waitKey(1) == ord('q'):
        camera_1.capture.release()
        camera_2.capture.release()

        cv2.destroyAllWindows()
        exit(0)
        break

