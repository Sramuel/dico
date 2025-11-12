#!/usr/bin/python3

import socket
import sys
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = ""
port = 7777
s.connect((host, port))
while True:
    data = sys.stdin.readline()
    if data == "\n":
        break
    buffer = data.encode("utf-8")
    s.sendall(buffer)
    print((s.recv(1500)).decode("utf-8"), end="")
s.close()