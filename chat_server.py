#									D:\Python\KSIS\Laba2\Chat\chat_server.py	
from PyQt5.QtCore import pyqtSignal, QObject
from PyQt5 import QtCore, QtWidgets
from server_design import Ui_MainWindow  


class Communicate(QObject):
	new_mes = pyqtSignal()

class MainWindow(QtWidgets.QWidget):
	def __init__(self):
		super(MainWindow, self).__init__()
		
		self.ui = Ui_MainWindow()
		self.ui.setupUi(self)

		self.GLOBAL = 'Global'
		self.CONNECT = 'connect'
		self.DISCONNECT = 'disconnect'
		self.MESSAGE = 'message'
		self.HISTORY_REQUST = 'history_request'
		self.ACTIVE_CLIENTS = 'active_clients'

		self.clients = {}
		self.message_list = []
		self.client_id_and_name = {}

		self.signal = Communicate()
		self.signal.new_mes.connect(self.new_mes)

	def process_not_main_message(self, mtype, client_name, client_id, connection):
		if mtype == self.DISCONNECT:
			self.client_id_and_name.pop(self.clients[connection])
			self.clients.pop(connection)
			
		elif mtype == self.CONNECT:
			active_clients = ''
			for _id, _name in self.client_id_and_name.items():
				active_clients += f'†{_name}†{_id}'

			connection.send(bytes(f'active_clients{active_clients}'.encode('utf-8')))
			self.client_id_and_name[client_id] = client_name

		elif mtype == self.HISTORY_REQUST:
			history = '†'.join(self.message_list)
			connection.sendall(bytes(f'history†{history}'.encode('utf-8')))


	def new_mes(self):
		data = self.socket.get_new_message()
		connection, address = self.socket.get_client_connection_and_address()

		mtype, recipient, client_name, raw_message = data[0], data[1], data[2], data[3:]
		client_id, client_ip = str(address[1]), address[0]

		message = self.message_constructor(mtype, recipient, client_name, raw_message, client_id, client_ip)
		self.process_not_main_message(mtype, client_name, client_id, connection)			

		if mtype != self.HISTORY_REQUST:
			self.send_message_to_client(message, recipient, connection)
			self.ui.TEdit_for_server_info.append(f'{message} {address}')
	

	def message_constructor(self, mtype, recipient, client_name, data, client_id, client_ip):
		mes = '†'.join(data)		
		message = f' |{client_ip}:{PORT}| {mes}'		

		if recipient == self.GLOBAL and mtype != self.HISTORY_REQUST:
			self.message_list.append(f'{mtype}†{client_id}†{recipient}†{client_name}†{message}')


		if mtype == self.CONNECT or mtype == self.DISCONNECT:
			return f'{mtype}†{client_id}†{recipient}†{client_name}† {message}'

		elif mtype == self.MESSAGE:
			return f'{mtype}†{client_id}†{recipient}†{client_name}† :: {message}'

		elif mtype == self.ACTIVE_CLIENTS:
			return f'{mtype}†{client_id}†{recipient}†{client_name}†{mes}'


	def send_message_to_client(self, message, recipient, connection):		
		for client, addr in self.clients.items():
			if connection != client and (addr == recipient or recipient == self.GLOBAL):
				client.send(bytes(message.encode('utf-8')))


	def set_socket(self, socket):
		self.socket = socket


	def thread(self):
		while True:
			connection, address = self.socket.accept()
			self.clients[connection] = str(address[1])


	def start_threading(self):
		socket_thread = threading.Thread(target=self.thread, daemon = True)
		socket_thread.start()

if __name__ == "__main__":
	import socket, threading, time, sys
	from time import gmtime, strftime
	from UDPConnection import UDPConnection
	from TCPConnection import TCPConnection	

	HOST = socket.gethostbyname(socket.gethostname())
	PORT = 50007
	
	app = QtWidgets.QApplication(sys.argv)
	application = MainWindow()
	application.show()

	UDP_socket = UDPConnection(HOST, PORT)
	UDP_socket.setsockopt_reuseaddr()
	UDP_socket.bind('0.0.0.0', PORT) 	
	UDP_socket.send_address_to_sender()
	UDP_socket.start_UDP_receiving()
		
	TCP_socket = TCPConnection(application.signal.new_mes)
	TCP_socket.setsockopt_reuseaddr()
	TCP_socket.bind(HOST, PORT)
	TCP_socket.listen(10)
	TCP_socket.set_server_socket()

	application.set_socket(TCP_socket)
	application.start_threading()

	
	sys.exit(app.exec())