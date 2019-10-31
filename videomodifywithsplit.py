import sys
import cv2
import numpy as np
# import global
import videopull as videopull
import videopush as videopush

hog = cv2.HOGDescriptor()
hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())
cv2.startWindowThread()

# set the sauce
# start the threads

source = "people test-converted.mp4"
v_pull = videopull.videopull(source).start()
v_push = videopush.videopush(v_pull.frame).start()

while True:
    key = cv2.waitKey(28)
    if key == 27:
        break

    frame = v_pull.frame
    frame = cv2.resize(frame, (720, 480))
    # change the color to gray for quicker scanning
    gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
    # chopit code
    Lframe1 = gray[0:480, 0:300]
    Rframe1 = gray[0:480, 420:720]
    # search the gray cropped pictures
    cv2.imshow("rightside", Rframe1)
    Lboxes, weights = hog.detectMultiScale(Rframe1, winStride=(8, 8))
    Lboxes = np.array([[x, y, x + w, y + h] for (x, y, w, h) in Lboxes])

    for (xA, yA, xB, yB) in Lboxes:
        # display the detected boxes in the colour picture
        cv2.rectangle(Lframe1, (xA, yA), (xB, yB),
                      (0, 255, 0), 2)

    Rboxes, weights = hog.detectMultiScale(Lframe1, winStride=(8, 8))
    Rboxes = np.array([[x, y, x + w, y + h] for (x, y, w, h) in Rboxes])

    for (xA, yA, xB, yB) in Rboxes:
        # display the detected boxes in the colour picture
        cv2.rectangle(Rframe1, (xA, yA), (xB, yB),
                      (0, 255, 0), 2)
    cv2.imshow("rightside", Rframe1)
    v_push.frame = frame
