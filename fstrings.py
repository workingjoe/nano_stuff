
cam_id=0
cam0_W=1920
cam0_H=1080
disp0_W=320
disp0_H=240
flip0=0


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
        "video/x-raw(memory:NVMM), width=(int)%d, height=(int)%d, framerate=(fraction)%d/1 ! "
        "nvvidconv flip-method=%d ! "
        "video/x-raw, width=(int)%d, height=(int)%d, format=(string)BGRx ! "
        "videoconvert ! "
        "video/x-raw, format=(string)BGR ! appsink"
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


key = 0
# horrible string ... one long gstreamer launch
uglycamSet0='nvarguscamerasrc sensor-id=0 ! video/x-raw(memory:NVMM), width=3264, height=2464, format=NV12, framerate=21/1 ! nvvidconv flip-method=' + str(flip)+' ! video/x-raw, width='+str(dispW)+', height='+str(dispH)+', format=BGRx ! videoconvert ! video/x-raw, format=BGR ! appsink'

#
# nvarguscamerasrc sensor-id=0 ! video/x-raw(memory:NVMM), width=3264, height=2464, format=NV12, framerate=21/1 ! nvvidconv flip-method=0 ! video/x-raw, width=320, height=240, format=BGRx ! videoconvert ! video/x-raw, format=BGR ! appsink
# 

print(uglycamSet0)

camSet0=(f'nvarguscamerasrc sensor-id={cam_id} ! video/x-raw(memory:NVMM), width={cam0_W}, height={cam0_H}, ' + 
         f'format=NV12, framerate=21/1 ! nvvidconv flip-method={str(flip0)} ' +
         f'! video/x-raw, width={str(disp0_W)}, height={str(disp0_H)}, format=BGRx ' +
         f'! videoconvert ! video/x-raw, format=BGR ! appsink' )

print('-------------------------------------')
print(camSet0)
