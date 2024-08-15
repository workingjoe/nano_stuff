
import numpy as np
import time
from simple_pid.pid import PID as PID  # attempt to use PID controllers for each servo



def nothing(x):
    pass

panValue  = 58   # 90
goalValue = 0


pidPan    = PID(Kp=0.1, Ki=0.1, Kd=0.1)
pidPan.Kp = 0.1 # kp proportional gain
pidPan.Ki = 0.1 # ki integral gain
pidPan.Kd = 0.1 # kd derivative gain    
pidPan.setpoint = 0        # attempt to achieve ZERO error in direction
pidPan.output_limits = (-179, 179)
pidPan.sample_time   = (1) # assume frame rate

pidPan.set_auto_mode(True,  last_output = panValue)

pidPan.setPoint  = goalValue   # 0.0

reverse = 1;
while True:
    time.sleep(1)
 
    testpanValue = pidPan(panValue)    
    print(f"testpanValue : {testpanValue} -and- panValue: {panValue}")
    
    panValue = panValue + reverse * (testpanValue * 2)
    if panValue > 170:
        reverse = reverse * -1

    if panValue < 10:
        reverse = reverse * -1
 

