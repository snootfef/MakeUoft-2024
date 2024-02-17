import cv2
import mediapipe as mp
import time
from subprocess import call
import numpy as np
INDEX_FINGER_IDX = 8
THUMB_IDX = 4
VOLUME_UPDATE_INTERVAL = 15


class HandDetector:
    def __init__(self):
        self.videoCap = cv2.VideoCapture(0)
        self.lastFrameTime = 0
        self.frame = 0
        self.max_diff = 0
        self.min_diff = 100000
        self.handSolution = mp.solutions.hands
        self.hands = self.handSolution.Hands()

    def run(self):
        while True:
            self.frame += 1
            # reading image
            success, img = self.videoCap.read()
            # showing image on separate window (only if read was successfull)
            if success:
                imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                # fps calculations
                thisFrameTime = time.time()
                fps = 1 / (thisFrameTime - self.lastFrameTime)
                self.lastFrameTime = thisFrameTime
                # write on image fps
                cv2.putText(img, f'FPS:{int(fps)}',
                            (20, 70),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                # recognize hands from out image
                recHands = self.hands.process(img)
                if recHands.multi_hand_landmarks:
                    for hand in recHands.multi_hand_landmarks:
                        # draw the dots on each our image for vizual help
                        for datapoint_id, point in enumerate(hand.landmark):
                            h, w, c = img.shape
                            x, y = int(point.x * w), int(point.y * h)
                            cv2.circle(img, (x, y),
                                       10, (255, 0, 255), cv2.FILLED)
                    if self.frame % VOLUME_UPDATE_INTERVAL == 0:
                        thumb_y = hand.landmark[THUMB_IDX].y
                        index_y = hand.landmark[INDEX_FINGER_IDX].y
                        distance = thumb_y * h - index_y * h
                        # calibrate min and max difference
                        self.min_diff = np.minimum(
                            distance + 50, self.min_diff)
                        self.max_diff = np.maximum(distance, self.max_diff)
                        # change volume on mac os
                        call(["osascript -e 'set volume output volume {}'"
                              .format(np.clip(
                                      (distance/(self.max_diff - self.min_diff)*100),
                                      0, 100))], shell=True)
                        self.frame = 0
                cv2.imshow("CamOutput", img)
                cv2.waitKey(1)
