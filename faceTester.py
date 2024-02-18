from face import FaceTracker
import time
FT = FaceTracker()
while True:
    f = FT.getFace()
    time.sleep(0.05)
