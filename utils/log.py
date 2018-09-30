'''
A logging client.

Writes log messages on a local file, sys.stdout and to a udp log server.
The logger behaviour is changed with a LoggerAdapter to add an attribute
(`hostname`) to the formatter.

Example of usage:
from log import logger
logger.debug('This message will be logged with DEBUG level.')
logger.info('This message will be logged with INFO level.')
'''

import sys
import socket
import logging
import logging.handlers
import settings as stt

LOG_FILENAME = stt.LOG_FILE_NAME
LOG_SERVER_HOST = stt.LOG_SERVER_HOST
LOG_SERVER_PORT = int(stt.LOG_SERVER_PORT)

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

fh = logging.FileHandler(filename=LOG_FILENAME, mode='w')
ch = logging.StreamHandler(stream=sys.stdout)
dh = logging.handlers.DatagramHandler(LOG_SERVER_HOST, LOG_SERVER_PORT)

fh.setLevel(logging.DEBUG)
ch.setLevel(logging.DEBUG)
dh.setLevel(logging.DEBUG)

formatter = logging.Formatter(
    '[%(asctime)s:%(levelname)s:%(hostname)s:P%(process)d'
    ':%(filename)s:%(lineno)d:%(funcName)s()]'
    ': %(message)s'
)

fh.setFormatter(formatter)
ch.setFormatter(formatter)
dh.setFormatter(formatter)

logger.addHandler(fh)
logger.addHandler(ch)
logger.addHandler(dh)

adapter = logging.LoggerAdapter(logger, {'hostname': socket.gethostname()})
logger = adapter
