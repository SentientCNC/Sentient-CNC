import cv2
import numpy as np

cap = cv2.VideoCapture(0)

print('Beginning Capture Device opening...\n')
print('Capture device opened?', cap.isOpened())

while True:

    ret, frame = cap.read()
    gray_image = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    cv2.imshow('frame', gray_image)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the capture
cap.release()
cv2.destroyAllWindows()
