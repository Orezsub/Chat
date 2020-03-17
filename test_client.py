#									D:\Python\KSIS\Laba1\test_client.py	
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

	def send_to(self, message):
		self.socket.sendto(f'{message}'.encode("utf-8"), ('<broadcast>', self.port))

	def UDP_sending(self):  # Поточность
		# global shutdown
		while not self.shutdown:
			try:
				while not self.shutdown:
					# UDP_socket.sendto((str(host)+' '+str(port)).encode("utf-8"),('<broadcast>',port))
					# UDP_socket.sendto(f'{str(host)} {str(port)}'.encode("utf-8"),('<broadcast>',port))
					self.send_to('lll')
					
					# print(shutdown)
					time.sleep(2)
			except:
				pass

	def start(self):
		Thread_send_UDP = threading.Thread(target = self.UDP_sending, daemon = True)
		Thread_send_UDP.start()
		
if __name__ == "__main__":
		a = UDPConnection('192.168.1.56', 50007)
		a.send_to('lol')
		a.start()
		while True:
			pass
		print(a.socket)