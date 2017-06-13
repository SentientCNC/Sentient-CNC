import cv2
import sys
import numpy as np
import datetime
import time
import ctypes

cap = cv2.VideoCapture(0)


print('Beginning Capture Device opening...\n')
print('Capture device opened?', cap.isOpened())

running = "n"

# Instructional message
ctypes.windll.user32.MessageBoxW(
    0, "Setting up image. Press 'q' to quit", "Video Streamer", 1)

# get screen size
screensize = {}
user32 = ctypes.windll.user32
screensize['x'] = user32.GetSystemMetrics(0)
screensize['y'] = user32.GetSystemMetrics(1)


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

    # transform image data into different color spaces
    image = {
        'RGB': cv2.cvtColor(frame, 0),
        'Lab': cv2.cvtColor(frame, cv2.COLOR_RGB2Lab),
        'Luv': cv2.cvtColor(frame, cv2.COLOR_RGB2Luv),
        'HLS': cv2.cvtColor(frame, cv2.COLOR_RGB2HLS)

    }

    # stream image with sample transformations
    idx = 0
    for key in image.keys():

        # image sizing perameters
        im_count = len(image)
        im_length = screensize['x'] // im_count

        name = '{} transformation'.format(key)

        cv2.imshow(name, image[key])
        cv2.resizeWindow(name, im_length, im_length)
        cv2.moveWindow(name, idx * im_length, 0)

        idx += 1

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

    elif status == ord('q'):
        break

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
