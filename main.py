import cv2
from lineDetect import contourDetection
cap = cv2.VideoCapture('white_road.mp4') # Initialize Camera

while True:
    contourDetection(cap) # Line detection

    if cv2.waitKey(50) & 0xFF == ord('q'): # if q is pressed, windows close and video stream ends. Program exits
        break
