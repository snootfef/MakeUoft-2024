import pyfirmata
import time
from recog import HandDetector as hd

ARDUINO_PORT = "/dev/somewhere"

board = pyfirmata.Arduino(ARDUINO_PORT)

while True:
    board.digital[13].write(1)
    time.sleep(1)
    board.digital[13].write(0)
    time.sleep(1)
