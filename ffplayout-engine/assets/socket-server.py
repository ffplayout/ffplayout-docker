#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import signal
import socket
from subprocess import call

import psutil


def main(sock):
    while True:
        connection, client_address = sock.accept()
        try:
            print('connection from', client_address)

            # Receive the data in small chunks and retransmit it
            while True:
                data = connection.recv(16)

                if data == b'start':
                    print('start ffplayout-engine')
                    call(['supervisorctl', 'start', 'ffplayout-engine'])
                    connection.send(
                        ('HTTP/1.1 200 OK\nContent-Type: text/plain\n'
                         '\nstarted ffplayout-engine\n').encode())
                if data == b'stop':
                    print('stop ffplayout-engine')
                    call(['supervisorctl', 'stop', 'ffplayout-engine'])
                    connection.send(
                        ('HTTP/1.1 200 OK\nContent-Type: text/plain\n'
                         '\nstopped ffplayout-engine\n').encode())
                if data == b'restart':
                    print('restart ffplayout-engine')
                    call(['supervisorctl', 'restart', 'ffplayout-engine'])
                    connection.send(
                        ('HTTP/1.1 200 OK\nContent-Type: text/plain\n'
                         '\nrestarted ffplayout-engine\n').encode())
                if data == b'reload':
                    print('reload ffplayout-engine')
                    for proc in psutil.process_iter():
                        if 'ffplayout.py' in proc.cmdline():
                            proc.send_signal(signal.SIGHUP)

                    connection.send(
                        ('HTTP/1.1 200 OK\nContent-Type: text/plain\n'
                         '\nreloaded ffplayout-engine\n').encode())
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
