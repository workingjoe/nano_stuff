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


dispW = 640
dispH = 480
flip  = 0
key   = 0
# horrible string ... one long gstreamer launch
# camSet0='nvarguscamerasrc sensor-id=0 ! video/x-raw(memory:NVMM), width=3264, height=2464, format=NV12, framerate=21/1 ! nvvidconv flip-method=' + str(flip)+' ! video/x-raw, width='+str(dispW)+', height='+str(dispH)+', format=BGRx ! videoconvert ! video/x-raw, format=BGR ! appsink'
# camSet1='nvarguscamerasrc sensor-id=1 ! video/x-raw(memory:NVMM), width=3264, height=2464, format=NV12, framerate=21/1 ! nvvidconv flip-method=' + str(flip)+' ! video/x-raw, width='+str(dispW)+', height='+str(dispH)+', format=BGRx ! videoconvert ! video/x-raw, format=BGR ! appsink'

camSet0 = gstreamer_pipeline( sensor_id=0, 
                             capture_width=3264,
                             capture_height=2464,
                             display_width=dispW,
                             display_height=dispH,
                             framerate=21,
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


# create camera object
cam = cv2.VideoCapture(camSet1)

# USB webcam
# cam = cv2.VideoCapture(2)

while True:
    ret, frame = cam.read()
    # modify frame adding some stuff
    # rectangle (what, (tuple-x,y), (tuple_bottom-x,y), (B,G,R), linewidth)
    frame = cv2.rectangle(frame, (140,100), (180, 140), (128,0,128), 4)
    # frame = cv2.rectangle(frame, (180,100), (220, 140), (0,200,0), 7)
    # rectangle (what, (center-tuple-x,y), radius, (B,G,R), linewidth)
    frame = cv2.circle(frame, (320,240), 30, (0,0,80), -1) 
    # font needed for text
    fnt = cv2.FONT_HERSHEY_DUPLEX
    # now putTEXT (what, text, (upper-left_tuplex,y), font, fontScale, (B,G,R),
    #             thickness=1, lineType=LINE_8, bool bottomLeftOrigin=false
    frame = cv2.putText(frame, 'Hey There!', (300,300), fnt, 0.6, (55,200,60),1)

    frame = cv2.line(frame, (10,10), (dispW-10,dispH-10), (0,20,0), 4)
    frame = cv2.arrowedLine(frame, (20,333), (333,10),(255,255,0), 1)


    cv2.imshow('theCam', frame)
    cv2.moveWindow('theCam', 0,0)

    if cv2.waitKey(1) == ord('q'):
        break

# clean up
cam.release()
cv2.destroyAllWindows()

