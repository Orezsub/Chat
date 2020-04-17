
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
		self.NEW_CONTENT = 'new_content'
		self.DEL_CONTENT = 'del_content'
		self.HISTORY_REQUST = 'history_request'
		self.ACTIVE_CLIENTS = 'active_clients'
		self.MAX_MESSAGE_SIZE = 1024

		self.clients = {}
		self.message_list = []
		self.content_list = []
		self.client_id_and_name = {}

		self.signal = Communicate()
		self.signal.new_mes.connect(self.new_mes)

	def process_system_message(self, mtype, client_name, client_id, connection):
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
			connection.send(bytes(f'history_start†'.encode('utf-8')))
			history = ''
			time.sleep(0.2)

			for mes in self.message_list:
				if sys.getsizeof(history+f'{mes}†') >= self.MAX_MESSAGE_SIZE:
					connection.send(bytes(f'history†{history}'.encode('utf-8')))
					history = ''
					time.sleep(0.15)

				history += f'{mes}†'

			connection.send(bytes(f'history†{history}'.encode('utf-8')))
			time.sleep(0.2)
			connection.send(bytes(f'history_end†'.encode('utf-8')))

			time.sleep(0.2)
			loaded_content = ''
			for content_info in self.content_list:
				loaded_content += f'†{content_info[0]}†{content_info[1]}†{content_info[2]}†{content_info[3]}'
			connection.send(bytes(f'loaded_content{loaded_content}'.encode('utf-8')))


	def new_mes(self):
		data = self.socket.get_new_message()
		connection, address = self.socket.get_client_connection_and_address()

		try:
			mtype, recipient, client_name, raw_message, content = data[0], data[1], data[2], data[3:], data[4:]
		except:
			return
		client_id, client_ip = str(address[1]), address[0]

		message = self.prepare_message(mtype, recipient, client_name, raw_message, client_id, client_ip, content)
		self.process_system_message(mtype, client_name, client_id, connection)

		if mtype != self.HISTORY_REQUST:
			self.send_message_to_client(message, recipient, connection)
			self.ui.TEdit_for_server_info.append(f'{message} {address}')


	def prepare_message(self, mtype, recipient, client_name, data, client_id, client_ip, content):
		mes = '†'.join(data)
		message = f' |{client_ip}:{PORT}| {data[0]}'

		if recipient == self.GLOBAL and mtype != self.HISTORY_REQUST:
			self.message_list.append(f'{mtype}†{client_id}†{recipient}†{client_name}†{message}')

		if mtype == self.CONNECT or mtype == self.DISCONNECT:
			return self.message_constructor(mtype, client_id, recipient, client_name, '', message)

		elif mtype == self.MESSAGE:
			return self.message_constructor(mtype, client_id, recipient, client_name, ' :: ', message)

		elif mtype == self.ACTIVE_CLIENTS:
			return self.message_constructor(mtype, client_id, recipient, client_name, '', mes)

		elif mtype == self.NEW_CONTENT:
			if recipient == self.GLOBAL:
				for i in range(0, len(content), 2):
					self.content_list.append([client_id, recipient, content[i], content[i+1]])
					
			return self.message_constructor(mtype, client_id, recipient, client_name, '', message, content)

		elif mtype == self.DEL_CONTENT:
			if recipient == self.GLOBAL:

				for content_info in self.content_list:
					if content_info[2] == content[0]:
						self.content_list.remove(content_info)

			return self.message_constructor(mtype, client_id, recipient, client_name, '', message, content)


	def message_constructor(self, mtype, client_id, recipient, client_name, symblos, message, content=''):
		content_text = '†'.join(content)
		return f'{mtype}†{client_id}†{recipient}†{client_name}†{symblos}{message}†{content_text}'


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
	LISTEN_ALL_HOST = '0.0.0.0'
	
	app = QtWidgets.QApplication(sys.argv)
	application = MainWindow()
	application.show()

	UDP_socket = UDPConnection(HOST, PORT)
	UDP_socket.setsockopt_reuseaddr()
	UDP_socket.bind(LISTEN_ALL_HOST, PORT) 	
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