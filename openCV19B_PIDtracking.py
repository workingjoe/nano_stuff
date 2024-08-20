import cv2
import numpy as np
import time
from adafruit_servokit import ServoKit
from simple_pid.pid import PID as PID  # attempt to use PID controllers for each servo

print(cv2.__version__)

# IDEA is to have PID handle CORRECTIONS from ZERO, 
# so setpoint is ZERO, output_limits are max adjustments per sample
# adjustments are accumulated to position with
pidPan    = PID()
pidPan.Kp = 0.025 # kp proportional gain
pidPan.Ki = 0.004 # ki integral gain
pidPan.Kd = 0.001 # kd derivative gain    
pidPan.setpoint      = 0  # attempt to achieve ZERO error in direction
pidPan.output_limits = (-5, 5)
pidPan.sample_time   = (1 / 30) # assume 30hz frame rate

pidTilt    = PID()
pidTilt.Kp = 0.025 # kp proportional gain
pidTilt.Ki = 0.004 # ki integral gain
pidTilt.Kd = 0.001 # kd derivative gain    
pidTilt.setpoint      = 0        # attempt to achieve ZERO error in direction
pidTilt.output_limits = (-5, 5)
pidTilt.sample_time   = (1 / 30) # assume 30hz frame rate


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
 
# this is default RED cap tracking 
# cv2.createTrackbar('hueLower', 'Trackbars', 170,179,nothing)
# cv2.createTrackbar('hueUpper', 'Trackbars', 179,179,nothing)
 
# cv2.createTrackbar('hue2Lower','Trackbars',  0,179,nothing)
# cv2.createTrackbar('hue2Upper','Trackbars', 12,179,nothing)
 
# cv2.createTrackbar('satLow', 'Trackbars',120,255,nothing)
# cv2.createTrackbar('satHigh','Trackbars',255,255,nothing)
# cv2.createTrackbar('valLow', 'Trackbars',100,255,nothing)
# cv2.createTrackbar('valHigh','Trackbars',255,255,nothing)
 
# this is default GREEN cap tracking
cv2.createTrackbar('hueLower', 'Trackbars', 42,179,nothing)
cv2.createTrackbar('hueUpper', 'Trackbars', 88,179,nothing)
 
cv2.createTrackbar('hue2Lower','Trackbars', 42,179,nothing)
cv2.createTrackbar('hue2Upper','Trackbars', 88,179,nothing)
 
cv2.createTrackbar('satLow', 'Trackbars', 55,255,nothing)
cv2.createTrackbar('satHigh','Trackbars',255,255,nothing)
cv2.createTrackbar('valLow', 'Trackbars', 55,255,nothing)
cv2.createTrackbar('valHigh','Trackbars',255,255,nothing) 
 
dispW = 640
dispH = 480
width = dispW
height= dispH

flip  = 0

noiseThreshold = 200

panValue  = 60   # 90
tiltValue = 124  # 90

# takes a WHILE to establish this ... like 4-6 seconds
print(f"Initializing Servo control -- this takes a few seconds...")
myKit = ServoKit(channels=16)
if (myKit == False):
   print(f"Failed to establish Servo control.")
   exit
else:
    print(f"Servo control established.")

#servo[0] is  pan left-right
myKit.servo[0].angle = panValue
#servo[1] is pan_up_down
myKit.servo[1].angle = tiltValue


def adjust_pan( error=0 ):
    global panValue
    if (panValue + error) < 0 :
        return
    if (panValue + error) > 179 :    
        return 
    panValue += error
    myKit.servo[0].angle = panValue
    return    

def adjust_tilt( error=0 ):
    global tiltValue
    if (tiltValue + error) < 0 :
        return
    if (tiltValue + error) > 179 :    
        return 
    tiltValue += error
    myKit.servo[1].angle = tiltValue
    return    


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
cam = cv2.VideoCapture(camSet2)

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


# tell PID controllers initial conditions
pidPan.set_auto_mode(True,  last_output = 0)
pidTilt.set_auto_mode(True, last_output = 0)

#servo[0] is  pan left-right
myKit.servo[0].angle = panValue
#servo[1] is pan_up_down
myKit.servo[1].angle = tiltValue

# timem for servos to settle and camera to come up
time.sleep(2)

while True:
    ret, frame = cam.read()
    # frame=cv2.imread('smarties.png')

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
#    for cnt in contours:
    if len(contours) > 0 : 
        cnt = contours[0]
        area = cv2.contourArea(cnt)
        if area >= noiseThreshold:
            # find bounding rectangle instead
            (x,y,w,h) = cv2.boundingRect(cnt)
            # cv2.drawContours(frame, [cnt], 0, (200,200,0),2)
            cv2.rectangle(frame, (x,y), (x+w, y+h), (200, 200, 0), 2)

            objX = int(x + w/2)
            objY = int(y + h/2)
            centerX = int(width  / 2)
            centerY = int(height / 2)
            # find out how big error is 
            errorX = (centerX - objX)
            errorY = (centerY - objY)

            errorpanValue = pidPan(errorX)
            # print(f"errorpanValue: {errorpanValue} errorX: {errorX}")
            adjust_pan( errorpanValue )

            errortiltValue = pidTilt(errorY)
            # print(f"errortiltValue: {errortiltValue} errorY: {errorY}")
            adjust_tilt( errortiltValue )
    
    # cv2.drawContours(frame, contours, 0, (200,200,0),2)

    cv2.imshow('FGmaskComp',FGmaskComp)
    cv2.moveWindow('FGmaskComp',0,530)
 
    cv2.imshow('nanoCam',frame)
    cv2.moveWindow('nanoCam',0,0)

 
    if cv2.waitKey(1) == ord('q'):
        print(f"Final panValue: {panValue} Final tiltValue: {tiltValue}")
        break

cam.release()
cv2.destroyAllWindows()