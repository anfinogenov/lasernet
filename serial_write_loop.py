#!/usr/bin/env python3

import serial
import sys
import threading

arduino = serial.Serial(sys.argv[1], 115200, timeout=1)


def receive_messages():
    while threading.active_count() == 3:
        char_read = arduino.read()
        if char_read == b'':
            continue

        print("\b\bMessage received: ", end='')
        while char_read != b'':
            print(char_read.decode('ascii'), end='', flush=True)
            char_read = arduino.read()
        print("\n> ", end='')


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

recv = threading.Thread(target=receive_messages)
recv.start()
