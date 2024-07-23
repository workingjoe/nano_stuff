import cv2

build_info = cv2.getBuildInformation()
theVersion = cv2.__version__
print("OpenCV Version:", theVersion)
print("OpenCV Build Information:")
print(build_info)


