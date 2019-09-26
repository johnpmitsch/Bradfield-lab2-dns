#!/usr/bin/env python3
import socket
import sys

HOST = '0.0.0.0'
PORT = 10000

# Create a TCP/IP socket
with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:

    # Bind the socket to the port
    server_address = (HOST, PORT)
    print('starting up on {} port {}'.format(HOST, PORT))
    s.bind(server_address)

    while True:
        print('\nwaiting to receive message')
        data, address = s.recvfrom(4096)

        print('received {} bytes from {}'.format(len(data), address))
        print(data)

        if data:
            sent = s.sendto(data, address)
            print('sent {} bytes back to {}'.format(sent, address))
