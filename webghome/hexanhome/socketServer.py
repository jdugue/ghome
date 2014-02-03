import logging
from socketIO_client import SocketIO

logging.basicConfig(level=logging.DEBUG)

socketIO = SocketIO('localhost', 8080)