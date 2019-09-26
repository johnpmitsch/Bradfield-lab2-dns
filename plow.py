#!/usr/bin/env python3

# Supports A record DNS queries
# ./plow.py wikipedia.org

import socket
import random
import sys
from struct import pack, unpack
from random import randint

HOST = "8.8.8.8"
PORT = 53 

# Check user input
if len(sys.argv) > 1:
    address = sys.argv[1]
else:
    sys.exit("Please pass in a domain!")

# Appends to format and body for a String that will be passed into a Struct object
def build_message(message_format, message_body, content):
    message_format += ("B" * len(content))
    message_body = message_body + [ord(c) for c in content]
    return message_format, message_body

name, tld = address.split(".")
random_tx_id = randint(1,65535)
flags = 0x0120 # preset flags for a basic query

# Build base info and format
base_body = [random_tx_id, flags, 1, 0, 0, 0, len(name)]
base_format = '>HHHHHHB'

# Add URL name
format_with_name, body_with_name = build_message(base_format, base_body, name)

# Add length of tld
format_with_name += "B"
body_with_name.append(len(tld))

# Add TLD
message_format, message_body = build_message(format_with_name, body_with_name, tld)

# Add question type and class
message_format += "BHH"
message_body.extend([0, 1, 1])

# Pack message into binary format
message = pack(message_format, *message_body)

server_address = (HOST, PORT)
data = None

# Query DNS server
with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
    print("Sending message to {} on port {}".format(HOST, PORT))
    s.sendto(message, server_address)

    data, server = s.recvfrom(1000) 
    rhost, rport = server
    print("Received {} bytes from {}:{}".format(len(data), rhost, rport))
    print('Closing socket')
    s.close()

print(len(data))

print(unpack(">HHHHHH", data[0:12]))
