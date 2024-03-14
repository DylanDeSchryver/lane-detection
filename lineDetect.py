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
        (int(width * 0.35), int(height * 0.90)),  # Bottom-left point
        (int(width * 0.48), int(height * 0.72)),  # Top-left point
        (int(width * 0.58), int(height * 0.72)),  # Top-right point
        (int(width * 0.8), int(height * 0.90)),  # Bottom-right point
    ]], np.int32)

    cv2.fillPoly(mask, polygon, 255)
    roi = cv2.bitwise_and(edged, mask)

    # Perspective transform
    pts1 = np.float32([[(int(width * 0.35), int(height * 0.90))], [(int(width * 0.48), int(height * 0.72))],
                       [(int(width * 0.58), int(height * 0.72))], [(int(width * 0.8), int(height * 0.90))]])
    pts2 = np.float32([[0,0], [500,600],
                       [(int(width * 0.58), int(height * 0.72))], [(int(width * 0.8), int(height * 0.90))]])

    # Apply Perspective Transform Algorithm
    matrix = cv2.getPerspectiveTransform(pts1, pts2)
    result = cv2.warpPerspective(frame, matrix, (500, 600))



    # Finding Lines
    lines_list = []
    lines = cv2.HoughLinesP(
        roi,  # Input edge image
        1,  # Distance resolution in pixels
        np.pi / 180,  # Angle resolution in radians
        threshold=20,  # Min number of votes for a valid line
        minLineLength=1,  # Min allowed length of a line
        maxLineGap=100  # Max allowed gap between line segments for joining them
    )

    # Iterate over detected lines
    if lines is not None:
        for line in lines:
            # Extract line endpoints

            x1, y1, x2, y2 = line[0]

            #print(x1, y1, x2, y2)

            lines_list.append((x1, y1, x2, y2))

            cv2.line(frame,(x1,y1), (x2,y2), (0,255,0), 8)

    # Ensure that contours are found before proceeding
    #if len(lines_list) >= 2:

        #for line in lines:

            #cv2.line(frame, (new_x1, new_y1), (new_x2, new_y2), (0, 255, 0), 8)

    # draw midline
    # try:
    #     cv2.polylines(frame, [np.array(midCalc(contours))], False, (0, 0, 255), 4)
    # except cv2.error:
    #     pass

    # display frame

    return cv2.imshow('Contours', frame), cv2.imshow('warp', result)
