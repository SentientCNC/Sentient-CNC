import cv2
import sys
import numpy as np
import datetime
import time

cap = cv2.VideoCapture(0)


print('Beginning Capture Device opening...\n')
print('Capture device opened?', cap.isOpened())

running = "n"


def newAverageColorGrayscale(image):
    '''
    Finds average color of an image's pixels
    input: image object from cv2
    output: singel pixel value, would return 3 values if we were not doing grayscale
    '''
    average_color_per_row = np.average(image, axis=0)
    average_color = np.average(average_color_per_row, axis=0)
    return average_color


# initialize average color for something to compare to
average_color = 0

while True:
    # initialize camera
    ret, frame = cap.read()

    # take a picture
    image = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # show the picture
    cv2.imshow('frame', image)

    # listen for keyboard input
    status = cv2.waitKey(1) & 0xFF

    if status == ord('b'):
        print("bad status")
        running = "b"

    elif status == ord('g'):
        print("back to normal")
        running = "g"

    elif status == ord('n'):
        running = "n"

    if running == "g":
        if (abs(newAverageColorGrayscale(image) - average_color) > 1):
            print('motion detected')

        average_color = newAverageColorGrayscale(image)
        cv2.imwrite(
            "/home/pi/sentient-cnc/images/good{}.jpg"
            .format(datetime.datetime.now()), image)

    elif running == "b":
        cv2.imwrite(
            "/home/pi/sentient-cnc/images/bad{}.jpg"
            .format(datetime.datetime.now()), image)


# Release the capture
cap.release()
cv2.destroyAllWindows()

# Save image with file name = timestamp and classification
# classification should
