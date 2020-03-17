#									D:\Python\KSIS\Laba1\TCPConnection.py	
import socket, threading, time

class TCPConnection(object):
	"""docstring for TCPConnection"""
	def __init__(self, host, port, signal):
		self.host = host
		self.port = port
		self.client_name = ''
		self.message_signal = signal
		
	def send(self, mtype,receiver, message):
		self.socket.send(bytes(f'{mtype}†{receiver}†[{self.client_name}]†{message}', encoding='UTF-8'))

	def connect(self):
		self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.socket.connect((self.host, self.port))
		self.send('connect', 'Global', 'connected to chat')

		self.shutdown = False
		self.start_TCP_receiving()

	def thread_TCP_receiving(self):
		while not self.shutdown:
			try:
				while not self.shutdown:
					data = self.socket.recv(1024).decode("utf-8").split('†')
						
					self.message = data
					# print(data)
					self.message_signal.emit()
		
					time.sleep(0.2)
			except:
				pass

	def start_TCP_receiving(self):
		Thread_recv_TCP = threading.Thread(target=self.thread_TCP_receiving, daemon = True)
		Thread_recv_TCP.start()

	def disconnect(self):
		self.send('disconnect', 'Global', 'disconnected from chat')
		self.socket.close()
		self.shutdown = True 


if __name__ == "__main__":
	import socket, threading, time

	a = TCPConnection('192.168.56.1', 50007)
	a.connect()
	
	time.sleep(0.05)
	while True:
		if input() == 'q':
			break
	a.disconnect()
