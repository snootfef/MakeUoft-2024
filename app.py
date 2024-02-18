from pyfirmata import Arduino, util, SERVO
import time
from recog import HandRecog as hd
import threading as th


board = Arduino("COM5")
it = util.Iterator(board)
it.start()

leftShoulder = board.get_pin('d:9:s')
pin13 = board.get_pin('d:13:o')

def moveServo(servo, degrees):
    servo.write(degrees)  # Move servo to specified position
    
def onWave():
    print("Waving")
    pin13.write(1)
    time.sleep(2)
    pin13.write(0)

def runArduino():
    HD = hd()
    HD.setOnWave(onWave)
    #moveServo(leftShoulder, 0)
    pin13.write(0)
    while True:
        HD.checkHand()
        time.sleep(0.05)
        
        
runArduino()
