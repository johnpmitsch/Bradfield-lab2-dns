#!/usr/bin/env python3

# Supports A record DNS queries
# ./plow.py wikipedia.org

import socket
import random
import sys
from struct import pack, unpack
from random import randint
from collections import namedtuple

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
    print("Sending DNS query to {} on port {}".format(HOST, PORT))
    s.sendto(message, server_address)

    data, server = s.recvfrom(1000) 
    rhost, rport = server
    print("Received {} bytes from {}:{}".format(len(data), rhost, rport))
    s.close()

# unpack base response
DNSresponse = namedtuple("DNSresponse", "transaction_id flags qdcount ancount nscount arcount name_length")
base = 13
response = DNSresponse._make(unpack(">HHHHHHB", data[0:base]))
name_end = base + response.name_length

# get response domain name
rname = data[base:name_end]

# get tld
tld_size = unpack(">B", data[name_end:name_end+1])[0]
tld_start = name_end + 1
rtld = data[tld_start:tld_start+tld_size]

# combine responses to get response domain
rdomain = (rname + b"." +  rtld).decode("utf-8")

# unpack response answer 
DNSanswer = namedtuple("DNSanswer", "name type dnsclass ttl rdlength ip1 ip2 ip3 ip4")
answer_start = tld_start + tld_size + 7
ranswer = DNSanswer._make(unpack(">HHHHHBBBB", data[answer_start:answer_start+14]))

# build IPv4 address
rip = str(ranswer.ip1) + "." + str(ranswer.ip2) + "." + str(ranswer.ip3) + "." + str(ranswer.ip4)

# return ipv4 address
print("{} - {}".format(rdomain, rip))




