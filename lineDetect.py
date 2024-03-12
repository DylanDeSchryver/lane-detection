import cv2
import numpy as np
from midline import midCalc


def contourDetection(cap):

    ret, frame = cap.read()

    # Grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    #Gaussion Blur
    blurred = cv2.GaussianBlur(gray, (3, 3), 0)

    # Find Canny edges
    edged = cv2.Canny(blurred, 30, 200)

    height, width = edged.shape
    mask = np.zeros_like(edged)
    # only focus lower half of the screen
    polygon = np.array([[
        (int(width * 0.001), int(height * 0.70)),  # Bottom-left point
        (int(width * 0.36), int(height * 0.32)),  # Top-left point
        (int(width * 0.58), int(height * 0.32)),  # Top-right point
        (int(width * 0.999), int(height * 0.70)),  # Bottom-right point
    ]], np.int32)

    cv2.fillPoly(mask, polygon, 255)
    roi = cv2.bitwise_and(edged, mask)

    # Apply the defined ROI on the processed edge image


    # Finding Contours
    contours, hierarchy = cv2.findContours(roi, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    # Ensure that contours are found before proceeding
    if len(contours) >= 2:
        # Sort contours by area to find the largest ones (2 curved lines)
        contours = sorted(contours, key=cv2.contourArea, reverse=True)[:4]

        # Draw all contours within the ROI
        for contour in contours:
            #contour += (r_x, r_y)  # Offset contour points to match ROI in the original frame
            cv2.drawContours(frame, [contour], -1, (0, 255, 0), 4)

    # draw midline
    try:
        cv2.polylines(frame, [np.array(midCalc(contours))], False, (0, 0, 255), 4)
    except cv2.error:
        pass

    # display frame

    return cv2.imshow('Contours', frame), cv2.imshow('mask', roi)