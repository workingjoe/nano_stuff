import cv2
print(cv2.__version__)
import numpy as np
 
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
 
cv2.createTrackbar('hueLower', 'Trackbars', 170,179,nothing)
cv2.createTrackbar('hueUpper', 'Trackbars', 179,179,nothing)
 
cv2.createTrackbar('hue2Lower','Trackbars',  0,179,nothing)
cv2.createTrackbar('hue2Upper','Trackbars', 12,179,nothing)
 
cv2.createTrackbar('satLow', 'Trackbars',120,255,nothing)
cv2.createTrackbar('satHigh','Trackbars',255,255,nothing)
cv2.createTrackbar('valLow', 'Trackbars',100,255,nothing)
cv2.createTrackbar('valHigh','Trackbars',255,255,nothing)
 
 
dispW = 640
dispH = 480
flip  = 0

noiseThreshold = 500

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

cam = cv2.VideoCapture(camSet1)

# or create USB webcam object (arg is 0,1, or 2 depends on CSI cameras installed)
# cam = cv2.VideoCapture(2)


while True:
    ret, frame = cam.read()
    #frame=cv2.imread('smarties.png')

 
    hsv=cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
 
    hueLow=cv2.getTrackbarPos('hueLower', 'Trackbars')
    hueUp=cv2.getTrackbarPos('hueUpper', 'Trackbars')
 
    hue2Low=cv2.getTrackbarPos('hue2Lower', 'Trackbars')
    hue2Up=cv2.getTrackbarPos('hue2Upper', 'Trackbars')
 
    lowSat=cv2.getTrackbarPos('satLow', 'Trackbars')
    upperSat=cv2.getTrackbarPos('satHigh', 'Trackbars')
 
    lowVal=cv2.getTrackbarPos('valLow', 'Trackbars')
    upperVal=cv2.getTrackbarPos('valHigh', 'Trackbars')
 
    lower_Bounds=np.array([hueLow,lowSat,lowVal])
    upper_Bounds=np.array([hueUp,upperSat,upperVal])
 
    lower_Bounds2=np.array([hue2Low,lowSat,lowVal])
    upper_Bounds2=np.array([hue2Up,upperSat,upperVal])
 
    FGmask    = cv2.inRange(hsv,lower_Bounds,upper_Bounds)
    FGmask2   = cv2.inRange(hsv,lower_Bounds2,upper_Bounds2)
    FGmaskComp= cv2.add(FGmask,FGmask2)

    # find contours
    contours, dummy_hierarchy = cv2.findContours(FGmaskComp, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    # -1 is plot all contours
    # cv2.drawContours(frame, contours, -1, (200,200,0),2)
    
    # lets sort out for the biggest, using area lambda function, reverse means BIG to SMALL
    contours = sorted(contours, key = lambda x:cv2.contourArea(x), reverse = True)
    
    # step through each contour array and draw each one greater than some threshold
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area >= noiseThreshold:
            # find bounding rectangle instead
            (x,y,w,h) = cv2.boundingRect(cnt)
            # cv2.drawContours(frame, [cnt], 0, (200,200,0),2)
            cv2.rectangle(frame, (x,y), (x+w, y+h), (200, 200, 0), 2)

    
    # cv2.drawContours(frame, contours, 0, (200,200,0),2)

    cv2.imshow('FGmaskComp',FGmaskComp)
    cv2.moveWindow('FGmaskComp',0,530)
 
    cv2.imshow('nanoCam',frame)
    cv2.moveWindow('nanoCam',0,0)

 
    if cv2.waitKey(1) == ord('q'):
        break

cam.release()
cv2.destroyAllWindows()