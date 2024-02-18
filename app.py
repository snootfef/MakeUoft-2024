from pyfirmata import Arduino, util, SERVO
import time
from recog import HandRecog as hd
import threading as th


board = Arduino("COM4")
it = util.Iterator(board)
it.start()

leftShoulder = board.get_pin('d:9:s')

def moveServo(servo, degrees):
    servo.write(degrees)  # Move servo to specified position
    
def onWave():
    moveServo(leftShoulder, 150)
    time.sleep(1)
    moveServo(leftShoulder, 0)

def runArduino():
    HD = hd()
    HD.setOnWave(onWave)
    moveServo(leftShoulder, 0)
    while True:
        HD.checkHand()
        time.sleep(0.05)
        
        
runArduino()
