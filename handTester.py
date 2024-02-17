from recog import HandRecog as hd
import time

HD = hd()
def onWave():
    print("Hello!")
    
HD.setOnWave(onWave)

while True:
    HD.checkHand()
    time.sleep(0.05)
    
    