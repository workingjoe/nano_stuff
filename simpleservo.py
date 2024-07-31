import time
from adafruit_servokit import ServoKit

myKit = ServoKit(channels=16)

#[0] is  pan left-right
myKit.servo[0].angle = 90
#[1] is pan_up_down
myKit.servo[1].angle = 90

# full sweep one direction
# for i in range(0,180, 1):
#     time.sleep(0.1)
#     myKit.servo[0].angle = i

# # full sweep back 
# for i in range(180,0, -1):
#     time.sleep(0.1)
#     myKit.servo[0].angle = i

# # full sweep down direction
# for i in range(0,180, 1):
#     time.sleep(0.1)
#     myKit.servo[1].angle = i

# # full sweep back up 
# for i in range(180,0, -1):
#     time.sleep(0.1)
#     myKit.servo[1].angle = i
