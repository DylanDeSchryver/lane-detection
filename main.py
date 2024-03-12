import cv2
from lineDetect import contourDetection
cap = cv2.VideoCapture('turnPWPVIDEO.mp4') # Initialize Camera

while True:
    contourDetection(cap) # Line detection

    if cv2.waitKey(1) & 0xFF == ord('q'): # if q is pressed, windows close and video stream ends. Program exits
        break
