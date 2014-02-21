import socket
import datetime
import sys
import re

class SocketSender(object):
	"""docstring fos SocketSender"""
	def __init__(self):
		super(SocketSender, self).__init__()
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.server_adress = ('134.214.106.23', 5000)
		self.sock.connect(self.server_adress)

	def actionneur_on(self):
		my_trame_on = 'A55A6B0550000000FF9F1E5330FF'
		self.sock.send(my_trame_on)

	def actionneur_off(self):
		my_trame_off = 'A55A6B0570000000FF9F1E5330FF'
		self.sock.send(my_trame_off)
