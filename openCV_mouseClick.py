import cv2

print(f'OpenCV Version : ' + cv2.__version__)
# print(cv2.getBuildInformation())


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

# some globals to save 'event' data for use in main
evt   = -1
coord = []  # array
pnt   = ()  # tuple


def mouseClick(event, x, y, flags, params):
    global pnt 
    global coord 
    global evt 
    if event == cv2.EVENT_LBUTTONDOWN:
        print('MouseEvent was ', event)
        print(x, ' , ',y)
        # save selected tuple in pnt array
        pnt = (x,y)
        evt = event
        coord.append(pnt)




dispW = 640
dispH = 480
flip  = 0
key   = 0

# name the window we will be using, so can use it in mouseClick callback setup
cv2.namedWindow('theCam')
cv2.setMouseCallback('theCam', mouseClick)


# horrible string ... one long gstreamer launch
# camSet0='nvarguscamerasrc sensor-id=0 ! video/x-raw(memory:NVMM), width=3264, height=2464, format=NV12, framerate=21/1 ! nvvidconv flip-method=' + str(flip)+' ! video/x-raw, width='+str(dispW)+', height='+str(dispH)+', format=BGRx ! videoconvert ! video/x-raw, format=BGR ! appsink'
# camSet1='nvarguscamerasrc sensor-id=1 ! video/x-raw(memory:NVMM), width=3264, height=2464, format=NV12, framerate=21/1 ! nvvidconv flip-method=' + str(flip)+' ! video/x-raw, width='+str(dispW)+', height='+str(dispH)+', format=BGRx ! videoconvert ! video/x-raw, format=BGR ! appsink'

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
# print(camSet0)
# print("------------------------------------")


# create camera object for CSI connected camera
cam = cv2.VideoCapture(camSet0)

# USB webcam
# cam = cv2.VideoCapture(2)

# update dispW and dispH based on attached camera properties
dispW = int(cam.get(cv2.CAP_PROP_FRAME_WIDTH))
dispH = int(cam.get(cv2.CAP_PROP_FRAME_HEIGHT))

# make box 15 percent of frame
boxW = int(0.15 * dispW)
boxH = int(0.15 * dispH)
# initial x,y for box
posX = 10
posY = 70
# initial deltas for each direction
dx = 2
dy = 2


initial = 0
while True:
    ret, frame = cam.read()

    # modify frame adding some stuff
    # frame = cv2.rectangle(frame, (posX,posY), (posX+boxW, posY+boxH), (128,120,0), 3)

    # if (posX+boxW+dx) > dispW:
    #     dx *= -1
    # if (posY+boxH+dy) > dispH:
    #     dy *= -1
    #
    # if (posX+dx) <= 0:
    #     dx *= -1
    # if (posY+dy) <= 0:
    #     dy *= -1

    # posX += dx
    # posY += dy

    for somePoints in coord:
        cv2.circle(frame, somePoints, 5, (0,0,250),-1)
        font = cv2.FONT_HERSHEY_PLAIN
        myStr = str(somePoints)
        cv2.putText(frame, myStr, somePoints, font, 0.8, (250,250,0), 1)


    cv2.imshow('theCam', frame)
    if (initial == 0):
        cv2.moveWindow('theCam', 0, 0)
        initial = 1

    keyCaught = cv2.waitKey(1)

    if keyCaught == ord('q'):  # 'q' quit 
        break
    if keyCaught == ord('c'):  # 'c' clear
        coord = []
        pnt   = ()
        evt   = -1    

# clean up
cam.release()
cv2.destroyAllWindows()

