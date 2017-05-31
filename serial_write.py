#!/usr/bin/env python3

import serial
import sys
import threading

arduino = serial.Serial(sys.argv[1], 115200, timeout=1)

def send_messages():
    while True:
        user_input = input("> ")
        if user_input == '\\quit':
            print("Exiting!")
            return
        user_input = user_input.encode('ascii')

        arduino.write(user_input)

send = threading.Thread(target=send_messages)
send.start()

