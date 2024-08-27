from threading import Thread
# import cv2
import time

camSet1 = 'gstreamer launch-string'


# class to manage a camera
#   -- launch
#   -- operate in independent thread
#   -- collect frames, provide way for user to get frame
class vStream:
    def __init__(self, whichCamera):
        self.capture = whichCamera # cv2.VideoCapture(whichCamera)
        self.theThread = Thread(target=self.update, args = ([]))
        self.theThread.daemon = True
        self.theThread.start()

    def update(self):
        while True:
            # _, self.frame = self.capture.read()        
            print('.')

    # external method 
    def getFrame(self) :
        return self.frame



camera_1 = vStream(1)
camera_2 = vStream(camSet1)
