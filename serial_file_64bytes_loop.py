#!/usr/bin/env python3

import serial
import sys
import os
import time
import hashlib
import math

arduino = serial.Serial(sys.argv[1], 115200, timeout=1)

file_to_send = open(sys.argv[2], "rb")
received_file = open(sys.argv[2]+".recv", "wb")
send_file_size = os.stat(sys.argv[2]).st_size

data = file_to_send.read(64)

arduino.write(data)
arduino.read(64)
arduino.write(data)  # idk why, but first 128 bytes are missing???
arduino.read(64)

packets_sent = 0
mode = ""
if len(sys.argv) >= 4:
    mode = sys.argv[3]

bytes_in_second = 339.7
if mode == "md5":
    bytes_in_second = bytes_in_second * 64 / 80  # 16 additional bytes for every 64 bytes of data
else:
    bytes_in_second = bytes_in_second * 64 / 66  # 2 additional bytes

print(f"File size: {send_file_size} bytes")
print(f"Connection speed: {round(bytes_in_second/1024, 3)} KB/s")
print(f"""Predicted transfer time: 
    {math.floor(send_file_size/bytes_in_second/60)}m {math.ceil(send_file_size/bytes_in_second)%60}s""")

t0 = time.time()
while data != b'':
    print(f"\r{file_to_send.tell()*100 // send_file_size}% - {packets_sent} packets...", end='')
    
    check_sum = b''
    if mode == "md5":
        check_sum = bytes.fromhex(hashlib.md5(data).hexdigest())
    else:
        check_sum = ((sum(data)+0xFDDF) % 0xFFFF).to_bytes(2, byteorder='little', signed=False)

    arduino.write(data)
    received_data = arduino.read(64)
    
    arduino.write(check_sum)
    received_sum = arduino.read(len(check_sum))

    if mode == "md5":
        if bytes.fromhex(hashlib.md5(received_data).hexdigest()) != received_sum:
            print(" MD5 hash error! Retrying...", end=' ')
            print(f"Expected sum: {hashlib.md5(received_data).hexdigest()}, received: {received_sum.hex()}")
            continue
    else:
        if received_sum != ((sum(received_data)+0xFDDF) % 0xFFFF).to_bytes(2, byteorder='little', signed=False):
            print(" control sum error! Retrying...")
            continue

    packets_sent += 1
    received_file.write(received_data)
    data = file_to_send.read(64)

print(f"\nReal transfer time: {round(time.time() - t0, 3)} seconds")
print(f"64B packets sent: {packets_sent}")
