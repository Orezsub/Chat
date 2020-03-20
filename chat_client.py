#									D:\Python\KSIS\Laba2\Chat\chat_client.py					
import sys  # sys нужен для передачи argv в QApplication
from PyQt5 import Qt, QtCore, QtGui, QtWidgets, uic
from PyQt5.QtCore import pyqtSignal, QObject
from client_design import Ui_MainWindow  


class Communicate(QObject):
	new_message = pyqtSignal()


class MainWindow(QtWidgets.QMainWindow):
	
	def __init__(self):
		super(MainWindow, self).__init__()

		self.ui = Ui_MainWindow()
		self.ui.setupUi(self)		

		self.GLOBAL = 'Global'
		self.CONNECT = 'connect'
		self.DISCONNECT = 'disconnect'
		self.ARROW = '-->'

		self.BASE_COLOR = '#F0F0F0'
		self.RED_COLOR = '#DB4747'

		self.clients = [self.GLOBAL]
		self.button_dict = {}
		self.message_list = []
		
		self.signal = Communicate()
		self.signal.new_message.connect(self.new_message)
		self.recipient_address = self.GLOBAL

		self.Vertical_layout = self.ui.verticalLayout
		self.add_dialog_button_if_no_such(self.GLOBAL, self.GLOBAL)
		
		Widget = Qt.QWidget()
		Widget.setLayout(self.Vertical_layout)

		Scroll_Area = self.ui.scrollArea
		Scroll_Area.setWidget(Widget)

	def buttonClicked(self):
		sender = self.sender()
		for but, addr in self.button_dict.items():
			if sender == but:
				self.recipient_address = addr
				
				self.change_dialog_button_color(but, self.BASE_COLOR)						
				self.display_all_messages_from_sender(addr)
				break


	def change_dialog_button_color(self, button, color):
		button.setStyleSheet(f'background : {color};')


	def find_dialog_button_for_change_color(self, sender, recipient):
		if recipient != self.GLOBAL:
			for but, addr in self.button_dict.items():
				if sender == addr and self.recipient_address != addr:
					self.change_dialog_button_color(but, self.RED_COLOR)	

		elif recipient == self.GLOBAL and self.recipient_address != self.GLOBAL:
			for but, addr in self.button_dict.items():
				if self.GLOBAL == addr:
					self.change_dialog_button_color(but, self.RED_COLOR)


	def add_dialog_button_if_no_such(self, sender_address, client_name):
		for but, addr in self.button_dict.items():
			if sender_address == addr:
				return but

		button = Qt.QPushButton(f'{client_name}')
		button.setStyleSheet(f'background : {self.BASE_COLOR};')

		self.Vertical_layout.addWidget(button)
		self.button_dict[button] = sender_address
		button.clicked.connect(self.buttonClicked)

		return button
	

	def append_new_message_into_chat(self, sender, recipient, message):
		if recipient == self.GLOBAL and self.recipient_address == self.GLOBAL:
				self.ui.TEdit_Chat_Text.append(message)

		elif recipient != self.GLOBAL and self.recipient_address == sender:
				self.ui.TEdit_Chat_Text.append(message)


	def del_dialog_button(self, address):
		for but, addr in self.button_dict.items():
			if address == addr:	
				but.setParent(None)


	def if_any_connect_or_disconnect(self, mtype, sender, client_name):
		if mtype == self.CONNECT:
			self.clients.append(sender)
			self.ui.ComboBox_Of_Clients.addItem(client_name)

		elif mtype == self.DISCONNECT:
			self.ui.ComboBox_Of_Clients.removeItem(self.clients.index(sender))
			self.clients.remove(sender)
			self.del_dialog_button(sender)


	def display_all_messages_from_sender(self, recipient_address):
		# message[0] - sender, message[1] - recipient, message[2] - message_text
		self.ui.TEdit_Chat_Text.clear()
		if recipient_address == self.GLOBAL:					
			for message in self.message_list:
				if message[1] == recipient_address:

					if message[0] == self.ARROW:
						self.ui.TEdit_Chat_Text.append(f'{message[0]} {message[2]}')
					else:
						self.ui.TEdit_Chat_Text.append(f'{message[2]}')

		else:
			for message in self.message_list:
				if message[1] == recipient_address:

					if message[0] == self.ARROW:
						self.ui.TEdit_Chat_Text.append(f'{message[0]} {message[2]}')
					else:
						self.ui.TEdit_Chat_Text.append(f'{message[2]}')
						
				elif message[0] == recipient_address and message[1] != self.GLOBAL:
					self.ui.TEdit_Chat_Text.append(f'{message[2]}')


	def check_not_main_message(self, data):
		if data[0] == 'history':
			for i in reversed(range(len(self.message_list))):
				if self.message_list[i][1] == self.GLOBAL:
					del self.message_list[i] 

			for i in range(1,len(data),5):
				self.message_list.append([data[i+1],data[i+2],f'{data[i+3]} :: {data[i+4]}'])

			for but, addr in self.button_dict.items():
				if addr == self.GLOBAL:
					but.click()
			return True
			
		elif data[0] == 'active_clients': 
			if len(data) != 2:
				for i in range(1,len(data),2):
					self.ui.ComboBox_Of_Clients.addItem(data[i])
					self.clients.append(data[i+1])
			return True

		return False


	def new_message(self):
		data = self.TCP_socket.get_new_message()

		if not self.check_not_main_message(data):
			mtype = data[0]
			sender = data[1]
			recipient = data[2]
			client_name = data[3]
			message = data[3]+'†'.join(data[4:])

			self.if_any_connect_or_disconnect(mtype, sender, client_name)
			self.append_new_message_into_chat(sender, recipient, message)
			self.add_dialog_button_if_no_such(sender, client_name)

			self.message_list.append([sender, recipient, message])
			
			time.sleep(0.2)
			self.find_dialog_button_for_change_color(sender, recipient)	


	def find_server(self):
		client_host = socket.gethostbyname(socket.gethostname())
		client_port = 50007

		UDP_socket = UDPConnection(client_host, client_port)
		UDP_socket.setsockopt_broadcast()

		UDP_socket.start_UDP_receiving()
		UDP_socket.start_UDP_sending()

		time.sleep(0.05)
		host, port = UDP_socket.get_finded_ip_and_port()
		self.ui.Edit_IP.setText(host)
		self.ui.Edit_Port.setText(str(port))
		UDP_socket.stop()	


	def log_in(self):
		self.ui.Btn_Log_In.setDisabled(True)
		self.ui.Btn_Log_Out.setDisabled(False)
		self.ui.Btn_Send_Message.setDisabled(False)
		self.ui.Btn_History_Request.setDisabled(False)

		host = self.ui.Edit_IP.text()
		port = int(self.ui.Edit_Port.text())

		self.TCP_socket.set_host_and_port(host, port)
		self.TCP_socket.set_client_name(self.ui.Edit_Name.text())

		self.TCP_socket.connect()


	def prepare_and_send_message(self):	
		message = self.ui.TEdit_Input_Message.toPlainText()
		if message:
			self.send_message_to_server('message', self.recipient_address, message, True)
	

	def send_message_to_server(self, mtype, recipient, message, print_message):
		time_now = strftime("%H:%M:%S %d-%m-%Y", gmtime())
		mes = f' |{time_now}| {message}'

		if mtype != 'history_request':			
			self.message_list.append([self.ARROW, recipient, mes])
		self.TCP_socket.send(mtype, recipient, message)

		if print_message:
			self.ui.TEdit_Input_Message.clear()
			self.ui.TEdit_Chat_Text.append(f'--> {mes}')
			self.ui.TEdit_Input_Message.setFocus()
	

	def log_out(self):
		self.ui.Btn_Log_In.setDisabled(False)
		self.ui.Btn_Log_Out.setDisabled(True)
		self.ui.Btn_Send_Message.setDisabled(True)
		self.ui.Btn_History_Request.setDisabled(True)

		self.close_connection()
		self.close_all_dialogs()
		for i in range(1, self.ui.ComboBox_Of_Clients.count()):
			self.ui.ComboBox_Of_Clients.removeItem(i)
			del self.clients[i]
		self.message_list.clear()
			

	def close_connection(self):
		self.TCP_socket.disconnect()

	def close_all_dialogs(self):
		for dialog, addr in self.button_dict.items():
			if addr != self.GLOBAL:
				dialog.setParent(None)
			else:
				save_dialog = dialog
				save_addr = addr
		self.button_dict.clear()
		self.button_dict[save_dialog] = save_addr


	def history_request(self):
		self.send_message_to_server('history_request', self.GLOBAL, 'history request', False)


	def change_active_dialog(self):
		name = self.ui.ComboBox_Of_Clients.currentText()
		address = self.clients[self.ui.ComboBox_Of_Clients.currentIndex()]

		button = self.add_dialog_button_if_no_such(address, name)
		button.click()


	def set_TCP_socket(self, socket):
		self.TCP_socket = socket

	def closeEvent(self, event): 
		self.close_connection()
		


if __name__ == "__main__":
	import sys
	import socket
	import threading
	import time
	from UDPConnection import UDPConnection
	from TCPConnection import TCPConnection	
	from time import gmtime, strftime


	app = QtWidgets.QApplication(sys.argv)
	application = MainWindow()
	application.show()	
	

	TCP_socket = TCPConnection(application.signal.new_message)
	application.set_TCP_socket(TCP_socket)

	application.ui.Btn_Find_Server.clicked.connect(application.find_server)
	application.ui.Btn_Log_In.clicked.connect(application.log_in)
	application.ui.Btn_Send_Message.clicked.connect(application.prepare_and_send_message)
	application.ui.Btn_Log_Out.clicked.connect(application.log_out)
	application.ui.Btn_History_Request.clicked.connect(application.history_request)
	application.ui.ComboBox_Of_Clients.currentIndexChanged.connect(application.change_active_dialog)


	sys.exit(app.exec_())