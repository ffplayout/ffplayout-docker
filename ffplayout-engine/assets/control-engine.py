#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import socket
from argparse import ArgumentParser

# ------------------------------------------------------------------------------
# argument parsing
# ------------------------------------------------------------------------------

stdin_parser = ArgumentParser(
    description='control ffplayout-engine over socket server')

stdin_parser.add_argument(
    '-m', '--message', help='send: start, stop, restart, reload'
)

stdin_args = stdin_parser.parse_args()

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect the socket to the port where the server is listening
server_address = ('localhost', 64233)
sock.connect(server_address)

try:
    # Send data
    sock.sendall(str.encode(stdin_args.message))

    # Look for the response
    amount_received = 0
    amount_expected = len(stdin_args.message)

    while amount_received < amount_expected:
        data = sock.recv(95).decode('utf-8')
        amount_received += len(data)
        print('{}'.format(data))

finally:
    sock.close()
