
def midCalc(contours):
    if len(contours) >= 2:
        min_length = min(len(contours[0]), len(contours[1]))
        average_points = []
        for i in range(min_length):
            x_avg = int((contours[0][i][0][0] + contours[1][i][0][0]) / 2) # Calculate the average x and y values
            y_avg = int((contours[0][i][0][1] + contours[1][i][0][1]) / 2)
            average_points.append((x_avg, y_avg))

        # Draw the midline
        return average_points
    else:
        pass