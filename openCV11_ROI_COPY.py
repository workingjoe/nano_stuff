import cv2

print(cv2.__version__)
# print(cv2.getBuildInformation())

# some globals to save mouse 'event' data for use in main
evt   = -1
coord = []  # array
upperLeftpnt  = ()  # tuple
lowerRightpnt = ()  # tuple

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

def mouseClick(event, x, y, flags, params):
    global upperLeftpnt 
    global lowerRightpnt

    if event == cv2.EVENT_LBUTTONDOWN:
        print('MouseEvent was LeftButton ', event)
        print(x, ' , ',y)
        # save selected 
        if (len(lowerRightpnt) > 0):
            lowerRightpnt = ()
        upperLeftpnt  = (x,y)
            
    if event == cv2.EVENT_LBUTTONUP:
        print('MouseEvent was LefButtonRelease', event)
        print(x, ' , ',y)
        lowerRightpnt = (x,y)



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
print(camSet1)
print("------------------------------------")

cv2.namedWindow('theCam')
cv2.setMouseCallback('theCam', mouseClick)


# create CSI camera object
cam = cv2.VideoCapture(camSet1)

# or create USB webcam object (arg is 0,1, or 2 depends on CSI cameras installed)
# cam = cv2.VideoCapture(2)

while True:
    ret, frame = cam.read()

    # roi = frame[50:250, 200:400] # roi is not a COPY, it is a REFERENCE

    if (len(lowerRightpnt) > 0):
        # put rectangle in region of interest   
        frame = cv2.rectangle(frame, upperLeftpnt, lowerRightpnt, (128,0,128), 2)

        # tricky indexing row, col [y1:y2,x1:x2]
        roi = frame[ upperLeftpnt[1] : lowerRightpnt[1], 
                     upperLeftpnt[0] : lowerRightpnt[0]].copy() 
 
        cv2.imshow('ROI', roi)
        cv2.moveWindow('ROI', 705, 0)    

    cv2.imshow('theCam', frame)
    cv2.moveWindow('theCam', 0, 0)
    if cv2.waitKey(1) == ord('q'):
        break

# clean up
cam.release()
cv2.destroyAllWindows()

