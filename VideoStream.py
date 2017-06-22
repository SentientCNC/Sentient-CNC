import cv2
import sys
import numpy as np
import datetime
import time
import ctypes


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

    average_color = np.average(image)  # average _color_per_row, axis=0)
    return average_color


# initialize average color for something to compare to
average_color = 0
im_returned = True
checkpoint = 0

# initualize video capture object
cap = cv2.VideoCapture(0)
im_width = int(cap.get(3))
im_height = int(cap.get(4))
frame_num = 0
running = "n"

while True:
    frame_num += 1

    # reads in next frame
    im_returned, frame = cap.read()

    # Make sure data is coming through the camera
    if not im_returned:
        print('image not returned from capture device.')
        break

    # transform image data into different color spaces
    image = {
        'RGB': cv2.cvtColor(frame, 0),
        # 'Lab': cv2.cvtColor(frame, cv2.COLOR_RGB2Lab),
        # 'Luv': cv2.cvtColor(frame, cv2.COLOR_RGB2Luv),
        # 'HLS': cv2.cvtColor(frame, cv2.COLOR_RGB2HLS)
    }

    # stream image with sample transformations
    idx = 0
    for key in image.keys():

        # image sizing perametersq
        im_count = len(image)

        name = '{} transformation'.format(key)

        if im_count > 1:
            im_width = screensize['x'] // im_count
            cv2.resizeWindow(name, im_width, im_height)
            cv2.moveWindow(name, idx * im_width, 0)
            cv2.imshow(name, image[key])
        else:
            cv2.imshow(name, image[key])

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

        if (abs(newAverageColorGrayscale(image['RGB']) - average_color) > 1):
            print('motion detected')
            print('writing frame {}; label: machine running'.format(frame_num))

        average_color = newAverageColorGrayscale(image['RGB'])
        # cv2.imwrite(
        #     "/home/pi/sentient-cnc/images/good{}.jpg"
        #     .format(datetime.datetime.now()), image)

    elif running == "b":
        print('writing frame {}; label: machine idle'.format(frame_num))
        # cv2.imwrite(
        #     "/home/pi/sentient-cnc/images/bad{}.jpg"
        #     .format(datetime.datetime.now()), image)

        # Release the capture

cap.release()
cv2.destroyAllWindows()

# Save image with file name = timestamp and classification
# classification should
