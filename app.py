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

def runArduino():
    angle=0
    HandDetector = hd()
    while True:
        HandDetector.getHand()
        
        print("Angle: ", leftShoulder.read())
        moveServo(leftShoulder, angle)
        board.digital[13].write(1)
        time.sleep(1)
        board.digital[13].write(0)
        time.sleep(1)
        angle += 10
        if angle >= 180:
            angle = 0
            
        time.sleep(0.05)
runArduino()
