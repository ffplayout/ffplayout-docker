#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging
import sys
import time
from logging.handlers import TimedRotatingFileHandler
from subprocess import call

from supervisor.childutils import listener


def main(args):
    logger = logging.getLogger('ffplayout-engine')
    format = logging.Formatter('[%(asctime)s] [%(levelname)s]  %(message)s')
    file_handler = TimedRotatingFileHandler('/var/log/ffplayout/service.log',
                                            when='midnight',
                                            backupCount=7)
    file_handler.setFormatter(format)
    logger.addHandler(file_handler)
    logger.setLevel('INFO')
    logger.info(79 * '-')

    while True:
        logger.info('Listening for events...')
        headers, body = listener.wait(sys.stdin, sys.stdout)

        body = dict([pair.split(':') for pair in body.split(' ')])

        logger.debug('Headers: %r', repr(headers))
        logger.debug('Body: %r', repr(body))

        try:
            if headers['eventname'] == 'PROCESS_STATE_FATAL':
                logger.info('Process entered FATAL state...')
                if not args or body['processname'] in args:
                    logger.error('Killing off supervisord instance ...')
                    call(['/bin/kill', '-15', '1'], stdout=sys.stderr)
                    logger.info('Sent TERM signal to init process')
                    time.sleep(5)
                    logger.critical(
                        'Why am I still alive? Send KILL to all processes...')
                    call(['/bin/kill', '-9', '-1'], stdout=sys.stderr)
        except Exception as e:
            logger.critical('Unexpected Exception: %s', str(e))
            listener.fail(sys.stdout)
            exit(1)
        else:
            listener.ok(sys.stdout)


if __name__ == '__main__':
    main(sys.argv[1:])
