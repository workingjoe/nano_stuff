import cv2
import numpy as np 


# print(cv2.__version__)
# print(cv2.getBuildInformation())

# create some MASKING images

img1 = np.zeros((480,640,1), np.uint8)  # one number so, GRAY scale
img1[0:480,0:320] = 255 # make all rows, left-half columns a constant white
img2 = np.zeros((480,640,1), np.uint8)  # one number so, GRAY scale
img2[190:290,270:370] = 255 # make box 100 bit box in middle 

bitAnd = cv2.bitwise_and(img1, img2)
bitOR  = cv2.bitwise_or(img1, img2)
bitXOR = cv2.bitwise_xor(img1, img2)


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


dispW=640
dispH=480
flip=0
key = 0
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
print(camSet0)
print("------------------------------------")


# create CSI camera object
cam = cv2.VideoCapture(camSet0)

# or create USB webcam object (arg is 0,1, or 2 depends on CSI cameras installed)
# cam = cv2.VideoCapture(2)

while True:
    ret, frame = cam.read()

    cv2.imshow('anIMG', img1)
    cv2.moveWindow('anIMG', 0, 520)

    cv2.imshow('anIMG2', img2)
    cv2.moveWindow('anIMG2', 705, 0)    

    cv2.imshow('AndIMG', bitAnd)
    cv2.moveWindow('AndIMG', 705, 520)  

    cv2.imshow('OrIMG', bitOR)
    cv2.moveWindow('OrIMG', 1340, 0)  

    cv2.imshow('XorIMG', bitXOR)
    cv2.moveWindow('XorIMG', 1340, 520)  


    cv2.imshow('theCam', frame)
    cv2.moveWindow('theCam', 0, 0)
    if cv2.waitKey(1) == ord('q'):
        break

# clean up
cam.release()
cv2.destroyAllWindows()
