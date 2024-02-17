import pyfirmata
import time
from recog import HandDetector as hd


board = pyfirmata.Arduino("COM3", baudrate=57600)

while True:
    board.digital[13].write(1)
    time.sleep(1)
    board.digital[13].write(0)
    time.sleep(1)
