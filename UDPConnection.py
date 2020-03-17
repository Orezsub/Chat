#									D:\Python\KSIS\Laba1\UDPConnection.py	
import socket, threading, time

class UDPConnection():
	"""docstring for UDPConnection"""
	def __init__(self, host, port):
		# super(UDPConnection, self).__init__()
		self.host = host
		self.port = port
		self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
		self.shutdown = False
		self.finded_ip = ''


	def send_to(self, message):
		self.socket.sendto(f'{message}'.encode("utf-8"), ('<broadcast>', self.port))

	def thread_UDP_sending(self):
		while not self.shutdown:
			try:
				while not self.shutdown:
					self.send_to(f'{str(self.host)} {str(self.port)}')
					
					time.sleep(2)
			except:
				pass

	def thread_UDP_receiving(self):		
		while not self.shutdown:
			try:
				while not self.shutdown:
					data, addr = self.socket.recvfrom(1024)
					message = data.decode("utf-8").split()
					# print(message+';;')
					self.finded_ip = message[0]
					
					self.shutdown = True
					time.sleep(0.2)
			except:
				pass


	def start_UDP_sending(self):
		Thread_send_UDP = threading.Thread(target = self.thread_UDP_sending, daemon = True)
		Thread_send_UDP.start()

	def start_UDP_receiving(self):
		Thread_recv_UDP = threading.Thread(target = self.thread_UDP_receiving, daemon = True)
		Thread_recv_UDP.start()

	def stop(self):
		self.shutdown = True 
		self.socket.close()
		
if __name__ == "__main__":

	a = UDPConnection('192.168.1.56', 50007)
	a.send_to('lol')
	a.start_UDP_receiving()
	a.start_UDP_sending()
	while True:
		pass
	print(a.socket)