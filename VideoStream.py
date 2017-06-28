import cv2
# import sys
import numpy as np
import datetime
# import time
import pyaudio
# from audiostream import *
from store_data import data_handler


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


if __name__ == '__main__':

    # Initialize an input (no key creates a value of 255)
    cap = cv2.VideoCapture(0)
    user_input = cv2.waitKey(0) & 0xFF
    data_store = data_handler()
    moments = {}

    # data label dictionary
    label = {ord('b'): 'tool break',
             ord('d'): 'tool dull',
             ord('g'): 'machine okay',
             ord('n'): 'machine problem',
             ord('i'): 'machine idle',
             255: 'No Entry'}

    metadata = {
        'frame_width': cap.get(propId=3),
        'frame_height': cap.get(propId=4),
    }

    running = "n"
    chunk = 1024

    # fulldata = np.array([])
    # dry_data = np.array([])

    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paInt16,
                    channels=1,
                    rate=16000,
                    input=True,
                    frames_per_buffer=1024)

    # in_speech_bf = False

    # ##decoder.start_utt()

    # while True:
    #    if stream.is_stopped():
    #        stream.start_stream()
    #    buf = stream.read(1024)
    #    if buf:
    #        stream.stop_stream()
    #        decoder.process_raw(buf, False, False)

    # initialize average color for something to compare to
    average_color = 0

    # from audiostream
    # tt = TapTester()

    counter = 0
    run = True

    while run:
        # listen
        # audio = tt.listen()

        # read a frame from camera
        ret, image = cap.read()

        # show the picture
        cv2.imshow('image', image)

        # listen for keyboard input
        last_input = user_input
        user_input = cv2.waitKey(1) & 0xFF

        # quitting sequence
        if user_input == ord('q'):
            break

        # keep the last pressed key as label
        if user_input == 255 and last_input != 255:
            user_input = last_input

        moments["audio"] = "aud"
        moments["image"] = image
        moments["timestamp"] = datetime.datetime.now()
        moments["label"] = label.get(user_input, None)
        moments.update(metadata)

        # data_store.write(moments)

        if counter > 30:
            run = False
        counter += 1

    # Release the capture
    cap.release()
    cv2.destroyAllWindows()

    # for moment in moments:
    #     print(moment.get('audio', 'Not Found'))
