#!/usr/bin/env python3

'''
A UDP logging server.

Received messages are written to sys.stdout and a file. It exits gracefully on
SIGINT (Ctrl+C) signal.

Note: it runs only on Python>=3.6.
'''

import os
import sys
import signal
import pickle
import logging
import threading
import socketserver


LOG_SERVER_HOST = '0.0.0.0'
LOG_SERVER_PORT = int(os.getenv(
    'LOG_SERVER_PORT',
    default='60000'
))
LOG_FILENAME = 'udp_server.log'

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

fh = logging.FileHandler(filename=LOG_FILENAME, mode='w')
ch = logging.StreamHandler(stream=sys.stdout)

fh.setLevel(logging.DEBUG)
ch.setLevel(logging.DEBUG)

formatter = logging.Formatter(
    '[%(asctime)s:%(levelname)s:%(hostname)s:P%(process)d'
    ':%(filename)s:%(lineno)d:%(funcName)s()]'
    ': %(message)s'
)

fh.setFormatter(formatter)
ch.setFormatter(formatter)

logger.addHandler(fh)
logger.addHandler(ch)


class LogRecordUDPHandler(socketserver.DatagramRequestHandler):

    def handle(self):
        obj = pickle.loads(self.packet[4:])
        record = logging.makeLogRecord(obj)
        logger.handle(record)


class LogRecordUDPServer(socketserver.UDPServer):

    def __init__(self, *args, **kwargs):
        signal.signal(signal.SIGINT, self.signal_sigint_handler)
        signal.signal(signal.SIGTERM, self.signal_sigint_handler)
        super().__init__(*args, **kwargs)

    def signal_sigint_handler(self, sig, frame):
        print('Ctrl+C pressed! Terminating...')
        self.shutdown()

    def run(self,):
        # in order to call self.shutdown(), self.serve_forever() needs to be
        # running on a separate thread to avoid a deadlock, as per
        # socketserver.BaseServer.shutdown() docstring
        t = threading.Thread(target=self.serve_forever)
        t.start()
        t.join()


if __name__ == '__main__':
    print('Running log server on {}:{}. Press Ctrl+C to exit.'.format(
        LOG_SERVER_HOST, LOG_SERVER_PORT
    ))
    addr = (LOG_SERVER_HOST, LOG_SERVER_PORT)
    with LogRecordUDPServer(addr, LogRecordUDPHandler) as server:
        server.run()
