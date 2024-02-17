import cv2
import mediapipe as mp
import time

class HandRecog:
    def __init__(self):
        self.cap = cv2.VideoCapture(0)
        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands()
        self.mpDraw = mp.solutions.drawing_utils
        
    def getHand(self):
        success, img = self.cap.read()
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        results = self.hands.process(imgRGB)
        hand = []
        if results.multi_hand_landmarks:
            handlms = results.multi_hand_landmarks[0]
            hand = list(handlms.landmark)
            self.displayHand(handlms, img)
            self.mpDraw.draw_landmarks(img, handlms, self.mpHands.HAND_CONNECTIONS)

        cv2.imshow("Image", img)
        cv2.waitKey(1)
        return hand
        
    def displayHand(self, handlms, img):
        for id, lm in enumerate(handlms.landmark):
            #print(id, lm)
            h, w, c = img.shape
            cx, cy = int(lm.x*w), int(lm.y*h)
            #if id == 5:
            cv2.circle(img, (cx, cy), 15, (139, 0, 0), cv2.FILLED)
        
    def dist(self, p1, p2):
        return ((p2.x - p1.x)**2 + (p2.y - p1.y)**2)**0.5
    
    def handIsOpen(self, hand):
        fingers=[False, False, False, False, False]
        fingers[0] = self.dist(hand[0], hand[4]) > self.dist(hand[0], hand[3])
        fingers[1] = self.dist(hand[0], hand[8]) > self.dist(hand[0], hand[7])
        fingers[2] = self.dist(hand[0], hand[12]) > self.dist(hand[0], hand[11])
        fingers[3] = self.dist(hand[0], hand[16]) > self.dist(hand[0], hand[15])
        fingers[4] = self.dist(hand[0], hand[20]) > self.dist(hand[0], hand[19])
        thumbOut = hand[4].x < hand[5].x and hand[5].x < hand[9].x or hand[4].x > hand[5].x and hand[5].x > hand[9].x
        return all(fingers) and thumbOut
    
    def handUp(self, hand):
        return hand[0].y > hand[12].y
    
    def handMovingDirection(self, history):
        direction = history[1][9].x - history[0][9].x
        direction /= abs(direction) # -1 = left, 1 = right
        for i in range(2, len(history)):
            if direction * (history[i][9].x - history[i-1][9].x) < 0:
                return ""
        return "left" if direction == -1 else "right"
        
    def isWaving(self, directionHistory):
        direction = 0
        count = 0
        for d in directionHistory:
            if d == "":
                continue
            if d == "left" and direction != -1:
                direction = -1
                count += 1
            elif d == "right" and direction != 1:
                direction = 1
                count += 1
        return count >= 4