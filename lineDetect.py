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

    # Perspective transform
    pts1 = np.float32([[570, 490], [740, 490],
                       [500, 700], [1100, 700]])
    for val in pts1:
        cv2.circle(frame, (int(val[0]), int(val[1])), 5, (0, 255, 0), -1)

    pts2 = np.float32([[570, 0], [740, 0],
                       [500, 700], [1100, 700]])

    # Apply Perspective Transform Algorithm
    matrix = cv2.getPerspectiveTransform(pts1, pts2)
    result = cv2.warpPerspective(edged, matrix, (1200, 700))

    height, width = result.shape

    # only focus lower half of the screen
    polygon = np.array([[
        (int(width * 0), int(height * 1)),  # Bottom-left point
        (int(width * 0.2), int(height * 0.22)),  # Top-left point
        (int(width * 0.68), int(height * 0.22)),  # Top-right point
        (int(width * 0.9), int(height * 1)),  # Bottom-right point
    ]], np.int32)

    mask = np.zeros_like(result)

    cv2.fillPoly(mask, polygon, 255)

    roi = cv2.bitwise_and(result, mask)

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

    return cv2.imshow('Contours', frame), cv2.imshow('warp', result), cv2.imshow('mask',mask), cv2.imshow('roi',roi)
