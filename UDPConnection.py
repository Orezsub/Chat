#									D:\Python\KSIS\Laba2\Chat\UDPConnection.py	
import socket, threading, time

class UDPConnection():
	"""docstring for UDPConnection"""
	def __init__(self, host, port):
		# super(UDPConnection, self).__init__()
		self.host = host
		self.port = port
		self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		self.finded_ip = ''
		self.finded_port = 0
		self.send_addr_to_sender = False

	def setsockopt_broadcast(self):
		self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

	def setsockopt_reuseaddr(self):
		self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

	def send_address_to_sender(self):
		self.send_addr_to_sender = True

	def bind(self, host, port):
		self.socket.bind((host, port))

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
					print(message)
					self.finded_ip = message[0]
					self.finded_port = message[1]

					if self.send_addr_to_sender:
						self.socket.sendto((f'{self.host} {str(self.port)}').encode("utf-8"), addr)
					
					# self.shutdown = True
					time.sleep(0.2)
			except OSError:
				pass


	def start_UDP_sending(self):
		self.shutdown = False
		Thread_send_UDP = threading.Thread(target = self.thread_UDP_sending, daemon = True)
		Thread_send_UDP.start()

	def start_UDP_receiving(self):
		self.shutdown = False
		Thread_recv_UDP = threading.Thread(target = self.thread_UDP_receiving, daemon = True)
		Thread_recv_UDP.start()

	def get_finded_ip_and_port(self):
		return self.finded_ip, self.finded_port

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