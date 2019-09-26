#!/usr/bin/env python3
import socket
import random
from struct import pack
from random import randint

HOST = "8.8.8.8"
PORT = 53 
WEBSITE = "wikipedia.com"

def build_message(message_format, message_body, content):
    message_format += ("B" * len(content))
    message_body = message_body + [ord(c) for c in content]
    return message_format, message_body

name, tld = WEBSITE.split(".")
random_tx_id = randint(1,65535)
flags = 0x0120

base_body = [random_tx_id, flags, 1, 0, 0, 0, len(name)]
base_format = '>HHHHHHB'

format_with_name, body_with_name = build_message(base_format, base_body, name)

format_with_name += "B"
body_with_name.append(len(tld))

message_format, message_body = build_message(format_with_name, body_with_name, tld)

message_format += "BHH"
message_body.extend([0, 1, 1])

print(message_format)
message = pack(message_format, *message_body)

server_address = (HOST, PORT)
with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
    print("Sending message to {} on port {}".format(HOST, PORT))
    s.sendto(message, server_address)

    #print("Waiting to receive message")
    #data, server = s.recvfrom(4096)
    #print("Received message {}".format(data))
    print('closing socket')
    s.close()
