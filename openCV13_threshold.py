import cv2
import numpy as np 


# print(cv2.__version__)
# print(cv2.getBuildInformation())

# build background, build foreground to then make a composite image

cvLogo = cv2.imread('cv.jpg')
cvLogo = cv2.resize(cvLogo, (320,240))
cvLogoGray = cv2.cvtColor(cvLogo, cv2.COLOR_BGR2GRAY)
cv2.imshow('cv Logo Gray', cvLogoGray)
cv2.moveWindow('cv Logo Gray', 0, 350)

# now create a mask with threshold for backgound
dummy,BGMask = cv2.threshold(cvLogoGray, 220, 255, cv2.THRESH_BINARY)
cv2.imshow('bg_mask', BGMask)
cv2.moveWindow('bg_mask', 385, 100)

# build foreground mask
FGMask = cv2.bitwise_not(BGMask)
cv2.imshow('fg_mask', FGMask)
cv2.moveWindow('fg_mask', 385, 350)

# put original color logo into MASK
ForeGround = cv2.bitwise_and(cvLogo, cvLogo, mask=FGMask)
cv2.imshow('foreground', ForeGround)
cv2.moveWindow('foreground', 703, 350)

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


dispW=320
dispH=240
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
print(camSet1)
print("------------------------------------")


# create CSI camera object
cam = cv2.VideoCapture(camSet1)

# or create USB webcam object (arg is 0,1, or 2 depends on CSI cameras installed)
# cam = cv2.VideoCapture(2)

while True:
    ret, frame = cam.read()

    BGimage = cv2.bitwise_and(frame, frame, mask=BGMask)
    cv2.imshow('BG', BGimage)
    cv2.moveWindow('BG', 703, 100)

    CompositeImage = cv2.add(BGimage, ForeGround)
    cv2.imshow('Composite', CompositeImage)
    cv2.moveWindow('Composite', 1017, 100)


    BlendedImage = cv2.addWeighted(frame, 0.7, CompositeImage, 0.3, 0)
    cv2.imshow('BlendedImage', BlendedImage)
    cv2.moveWindow('BlendedImage', 1017, 350)


    cv2.imshow('theCam', frame)
    cv2.moveWindow('theCam', 0, 100)
    if cv2.waitKey(1) == ord('q'):
        break

# clean up
cam.release()
cv2.destroyAllWindows()
