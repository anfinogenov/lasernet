#!/usr/bin/env python3

import serial
import sys
import os
import time

arduino = serial.Serial(sys.argv[1], 115200, timeout=1)

file_to_send = open(sys.argv[2], "rb")
received_file = open(sys.argv[2]+".recv", "wb")
send_file_size = os.stat(sys.argv[2]).st_size

data = file_to_send.read(64)

arduino.write(data)
arduino.read(64)
arduino.write(data) # idk why, but first 128 bytes are missing???
arduino.read(64)

print(f"File size: {send_file_size} bytes")
print(f"Predicted transfer time: {round(send_file_size/339.7, 3)} seconds")
t0 = time.time()
while data != b'':
    print(f"\r{file_to_send.tell()*100 // send_file_size}%", end='')
    arduino.write(data)
    received_file.write(arduino.read(64))
    data = file_to_send.read(64)
print(f"\nReal transfer time: {round(time.time() - t0, 3)} seconds")

