import time
import serial #The PySerial module


ser = serial.Serial("COM5", 9600) #Change COM3 to whichever COM port your arduino is in

for i in range(0,10):
    n = input()

    #Sending the file via serial to arduino
    byte_signal = bytes([int(n)])
    ser.write(byte_signal)

    time.sleep(5)