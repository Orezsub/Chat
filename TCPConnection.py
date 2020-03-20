#									D:\Python\KSIS\Laba2\Chat\TCPConnection.py	
from PyQt5 import QtCore, QtWidgets
import socket, threading, time
from time import gmtime, strftime


class TCPConnection(QtWidgets.QWidget):
	"""docstring for TCPConnection"""
	def __init__(self, signal):
		super().__init__()
		self.GLOBAL = 'Global'
		self.CONNECT = 'connect'
		self.DISCONNECT = 'disconnect'

		self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.client_name = ''
		self.message_signal = signal
		self.is_server = False


	def send(self, mtype,receiver, message):
		time_now = strftime("%H:%M:%S %d-%m-%Y", gmtime())
		message = f' |{time_now}| {message}'
		try:
			self.socket.send(bytes(f'{mtype}†{receiver}†[{self.client_name}]†{message}', encoding='UTF-8'))
		except OSError:
			pass
		

	def connect(self):
		self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.socket.connect((self.host, self.port))
		self.send(self.CONNECT, self.GLOBAL, 'connected to chat')

		self.start_TCP_receiving(None,None)

	def setsockopt_reuseaddr(self):
		self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

	def bind(self, host, port):
		self.socket.bind((host, port))

	def listen(self, count):
		self.socket.listen(count)

	def accept(self):
		connection, address = self.socket.accept()
		self.start_TCP_receiving(connection, address)
		return connection, address

	def set_server_socket(self):
		self.is_server = True

	def set_client_connection_and_address(self, connection, address):
		self.connection = connection
		self.address = address

	def get_client_connection_and_address(self):
		return self.connection, self.address

	def set_new_message(self, message):
		self.message = message

	def get_new_message(self):
		return self.message

	def set_host_and_port(self, host, port):
		self.host = host
		self.port = port

	def set_client_name(self, client_name):
		self.client_name = client_name

	def thread_TCP_receiving(self, connection, address):
		while not self.shutdown:
			try:
				while not self.shutdown:
					if self.is_server:
						data = connection.recv(1024).decode("utf-8").split('†')
						self.set_client_connection_and_address(connection, address)

					else:
						data = self.socket.recv(1024).decode("utf-8").split('†')
						
					# print(data)
					self.set_new_message(data)
					self.message_signal.emit()

					time.sleep(0.2)
			except:
				self.shutdown = True

	def start_TCP_receiving(self, connection, address):
		self.shutdown = False		
		Thread_recv_TCP = threading.Thread(target=self.thread_TCP_receiving,
									args=(connection, address), daemon = True)			
		Thread_recv_TCP.start()

	def disconnect(self):
		self.send(self.DISCONNECT, self.GLOBAL, 'disconnected from chat')
		self.shutdown = True 
		self.socket.close()


if __name__ == "__main__":
	import socket, threading, time

	a = TCPConnection('192.168.56.1', 50007)
	a.connect()
	
	time.sleep(0.05)
	while True:
		if input() == 'q':
			break
	a.disconnect()
