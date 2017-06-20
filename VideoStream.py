import cv2
# import sys
import numpy as np
import datetime
# import time
import pyaudio
from audiostream import *

cap = cv2.VideoCapture(0)

moments = []

print('Beginning Capture Device opening...\n')
print('Capture device opened?', cap.isOpened())

running = "n"

# chunk = 1024

# p = pyaudio.PyAudio()
# fulldata = np.array([])
# dry_data = np.array([])

# stream = p.open(format=pyaudio.paInt16,
#                channels=1,
#                rate=16000,
#                input=True,
#                frames_per_buffer=1024)

# in_speech_bf = False

# ##decoder.start_utt()

# while True:
#    if stream.is_stopped():
#        stream.start_stream()
#    buf = stream.read(1024)
#    if buf:
#        stream.stop_stream()
#        decoder.process_raw(buf, False, False)


def newAverageColorGrayscale(image):
    '''
    Finds average color of an image's pixels
    input: image object from cv2
    output: singel pixel value, would return
    3 values if we were not doing grayscale
    '''
    average_color_per_row = np.average(image, axis=0)
    average_color = np.average(average_color_per_row, axis=0)
    return average_color


def callback(in_data, frame_count, time_info, flag):

    global b, a, fulldata, dry_data, frames

    audio_data = np.fromstring(in_data, dtype=np.float32)
    dry_data = np.append(dry_data, audio_data)
    fulldata = np.append(fulldata, audio_data)

    return (audio_data, pyaudio.paContinue)


def test():
    return True


# initialize average color for something to compare to
average_color = 0

# from audiostream
tt = TapTester()

counter = 0
run = True
while run:
    # listen
    audio = tt.listen()

    # initialize camera
    ret, image = cap.read()

    # process the picture
    # image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # how the picture
    cv2.imshow('image', image)

    # listen for keyboard input
    status = cv2.waitKey(1) & 0xFF
    if status == ord('b'):
        print ("bad status")
        running = "b"

    elif status == ord('g'):
        print ("back to normal")
        running = "g"
    elif status == ord('n'):
        running = "n"

    if running == "g":
        if (abs(newAverageColorGrayscale(image) - average_color) > 1):
            print('motion detected')

        average_color = newAverageColorGrayscale(image)
        cv2.imwrite("/home/pi/sentient-cnc/images/good{}.jpg"
                    .format(datetime.datetime.now()), image)
    elif running == "b":
        cv2.imwrite("/home/pi/sentient-cnc/images/bad{}.jpg"
                    .format(datetime.datetime.now()), image)

    moments.append({"audio": audio,
                    "image": image,
                    "timestamp": datetime.datetime.now()
                    })
    if counter > 30:
        run = False
    counter += 1

for moment in moments:
    print(moment["audio"], moment["timestamp"])

# Release the capture
cap.release()
cv2.destroyAllWindows()
