import cv2
from deepface import DeepFace


class FaceTracker:
    def __init__(self):
        self.face_cascade = cv2.CascadeClassifier(
            cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        self.cap = cv2.VideoCapture(0)

# Start capturing video

    def toBinaryArray(self, image):
        res = []
        for i in range(len(image)):
            for j in range(len(image[i])):
                if image[i][j] // 3 > 140:
                    res.append(1)
                else:
                    res.append(0)
        return res

    def getFace(self):
        ret, frame = self.cap.read()

        # Convert frame to grayscale
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Detect faces in the frame
        face = self.face_cascade.detectMultiScale(
            gray_frame, scaleFactor=1.1, minNeighbors=5, minSize=(40, 40)
        )
        if len(face) == 0:
            return None

        extra_x = 150
        for (x, y, w, h) in face:
            img_width = w + 2 * extra_x
            img_height = 0.5 * img_width
            extra_y = int((img_height - h) / 2)
            crop_img = gray_frame[max(0, y-extra_y):y+h+extra_y,
                                  max(0, x-extra_x):x+w+extra_x]

        # resize to 128x64
        crop_img = cv2.resize(crop_img, (128, 64))
        # increase contrast
        crop_img = cv2.addWeighted(crop_img, 1.7, crop_img, 0, 0)
        ret, thresh = cv2.threshold(crop_img, 140, 255, 0)
        cv2.imshow("Image", thresh)
        cv2.waitKey(1)
        crop_img = self.toBinaryArray(crop_img)

        return crop_img
