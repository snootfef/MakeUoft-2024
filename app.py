import time
import serial  # The PySerial module
from face import FaceTracker


# Change COM3 to whichever COM port your arduino is in
ser = serial.Serial("COM5", 9600)

FT = FaceTracker()

while True:
    f = FT.getFace()
    if f is None:
        continue
    ser.write(bytes([1]))
    for i in range(len(f)):
        ser.write(bytes(f[i]))
    # byte_signal = bytes(f[i*1024:(i+1)*1024])
    # ser.write(byte_signal)
    time.sleep(1)
