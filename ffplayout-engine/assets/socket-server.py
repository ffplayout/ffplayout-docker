#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import signal
import socket
from subprocess import call, check_output

import psutil


def main(sock):
    while True:
        connection, client_address = sock.accept()
        try:
            print('connection from', client_address)

            # Receive the data in small chunks and retransmit it
            while True:
                data = connection.recv(7)

                if data == b'start':
                    print('start ffplayout-engine')
                    call(['supervisorctl', 'start', 'ffplayout-engine'])
                    connection.send(b'200')
                if data == b'stop':
                    print('stop ffplayout-engine')
                    call(['supervisorctl', 'stop', 'ffplayout-engine'])
                    connection.send(b'200')
                if data == b'restart':
                    print('restart ffplayout-engine')
                    call(['supervisorctl', 'restart', 'ffplayout-engine'])
                    connection.send(b'200')
                if data == b'reload':
                    print('reload ffplayout-engine')
                    for proc in psutil.process_iter():
                        if 'ffplayout.py' in proc.cmdline():
                            proc.send_signal(signal.SIGHUP)
                    connection.send(b'200')
                if data == b'status':
                    print('get status from ffplayout-engine')
                    status = check_output(
                        ['supervisorctl', 'status', 'ffplayout-engine'])

                    status = status.split()[1].encode()

                    connection.send(status)
                else:
                    break

        finally:
            connection.close()


if __name__ == '__main__':
    # Create a TCP/IP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Bind the socket to the port
    server_address = ('0.0.0.0', 64233)
    print('Starting up on {} port {}'.format(*server_address))
    sock.bind(server_address)

    # Listen for incoming connections
    sock.listen(1)

    main(sock)
