#!/usr/bin/env python3

import serial
import sys
import serial

arduino = serial.Serial(sys.argv[1], 115200, timeout=1)

while True:
    char_read = arduino.read()
    
    if char_read == b'':
        continue

    while char_read != b'':
        print(char_read.decode('ascii', 'ignore'), end='', flush=True)
        char_read = arduino.read()

    print("")

