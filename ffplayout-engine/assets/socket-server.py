#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging
import signal
import socket
import sys
from subprocess import call, check_output

import psutil

logging.basicConfig(
    stream=sys.stdout, level=logging.INFO,
    format='%(asctime)s %(levelname)s %(filename)s: %(message)s')
logger = logging.getLogger('socket-server')


def main(sock):
    while True:
        connection, client_address = sock.accept()
        try:
            logger.debug('connection from: {}'.format(client_address))

            # Receive the data in small chunks and retransmit it
            while True:
                data = connection.recv(7)

                if data == b'start':
                    logger.debug('starting ffplayout-engine...')
                    call(['supervisorctl', 'start', 'ffplayout-engine'])
                    connection.send(b'200')
                if data == b'stop':
                    logger.debug('stopping ffplayout-engine...')
                    call(['supervisorctl', 'stop', 'ffplayout-engine'])
                    connection.send(b'200')
                if data == b'restart':
                    logger.debug('restarting ffplayout-engine...')
                    call(['supervisorctl', 'restart', 'ffplayout-engine'])
                    connection.send(b'200')
                if data == b'reload':
                    logger.debug('reloading ffplayout-engine...')
                    for proc in psutil.process_iter():
                        if 'ffplayout.py' in proc.cmdline():
                            proc.send_signal(signal.SIGHUP)
                    connection.send(b'200')
                if data == b'status':
                    logger.debug('get status from ffplayout-engine...')
                    status = check_output(
                        ['supervisorctl', 'status', 'ffplayout-engine'])

                    status = status.split()[1]

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
    logger.info('Starting up on {} port {}'.format(*server_address))
    sock.bind(server_address)

    # Listen for incoming connections
    sock.listen(1)

    main(sock)
