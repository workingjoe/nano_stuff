import cv2

print(cv2.__version__)

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
key=0
firstTime=0

#camSet0 = gstreamer_pipeline(sensor_id=0, 
#                             capture_width=3264,
#                             capture_height=2464,
#                             display_width=dispW,
#                             display_height=dispH,
#                             framerate=21,
#                             flip_method=flip,
#                           )

camSet0 = gstreamer_pipeline(sensor_id=0, 
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



# create camera object
cam0 = cv2.VideoCapture(camSet0)
cam1 = cv2.VideoCapture(camSet1)

# USB webcam
# cam2 = cv2.VideoCapture(2)

while True:
    ret, frame  = cam0.read()
    ret, frame2 = cam1.read()

    cv2.imshow('nanoCam', frame)
    if firstTime == 0:
        cv2.moveWindow('nanoCam', 0, 0)

    cv2.imshow('nanoCam2', frame2)
    if firstTime == 0:
        cv2.moveWindow('nanoCam2', 700, 0)


    # new gray frame from original
    gray  = cv2.cvtColor(frame , cv2.COLOR_BGR2GRAY)
    gray2 = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)
    cv2.imshow('grayVideo', gray)
    if firstTime == 0:
        cv2.moveWindow('grayVideo', 0, 520)
    
    cv2.imshow('grayVideo2', gray2)
    if firstTime == 0:
        cv2.moveWindow('grayVideo2', 700, 520)
    

    firstTime = 1

    if cv2.waitKey(1) == ord('q'):
        break

# clean up
cam0.release()
cam1.release()
cv2.destroyAllWindows()

