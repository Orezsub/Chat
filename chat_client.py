#									D:\Python\KSIS\Laba1\chat_client.py					
import sys  # sys нужен для передачи argv в QApplication
from PyQt5 import Qt, QtCore, QtGui, QtWidgets, uic
from PyQt5.QtCore import pyqtSignal, QObject
from design import Ui_MainWindow  

def connect_or_disconnect(sender, receiver, client_name):
	if receiver == 'connect':
		clients.append(sender)
		application.ui.ComboBox_Of_Clients.addItem(client_name)
		application.added_connection_address = sender
		application.added_connection_name = client_name
		application.signal.Add_Dialog.emit()

	elif receiver == 'disconnect':
		application.ui.ComboBox_Of_Clients.removeItem(clients.index(sender))
		clients.remove(sender)
		application.delited_connection_address = sender
		application.signal.Del_Dialog.emit()


def change_color(sender, receiver):
	if receiver != GLOBAL:
		for but, addr in button_dict.items():
			if sender == addr and application.addr_to_send != addr:
				change_dialog_button_color(but, RED_COLOR)	

	elif receiver == GLOBAL and application.addr_to_send != GLOBAL:
		for but, addr in button_dict.items():
			if GLOBAL == addr:
				change_dialog_button_color(but, RED_COLOR)


def check_history_request(data, message):
	if data[0] == 'history start':
		for i in reversed(range(len(message_list))):
			if message_list[i][1] == GLOBAL:
				del message_list[i]
		return True
	elif data[1] == 'history':
		message_list.append([data[0],GLOBAL,message])
		return True
		
	elif data[0] == 'history end':
		application.signal.Clear_TEdit.emit()				
		return True
		
	elif data[0] == 'active clients': 
		if len(data) != 2:
			for i in range(1,len(data),2):
				clients.append(data[i+1])
				application.ui.ComboBox_Of_Clients.addItem(data[i])
		return True
	return False


def new_message():
	# print('-->',TCP_socket.message)
	data = TCP_socket.message
	try:
		sender = data[0]
		receiver = data[1]
		client_name = data[2]
		message = data[2]+'†'.join(data[3:])
	except:
		message = ''

	if not check_history_request(data, message):
	
		connect_or_disconnect(sender, receiver, client_name)

		if receiver == 'connect' or receiver == 'disconnect':
			receiver = GLOBAL

		append_text(sender, receiver, message)

		add_dialog_if_no_such(sender, client_name)

		message_list.append([sender, receiver, message])
		
		time.sleep(0.2)
		change_color(sender, receiver)	


def add_dialog_button_if_no_such(address, client_name):
	is_in = False
	for but, addr in button_dict.items():
		if address == addr:
			is_in = True
			return but
	if not is_in:
		button = Qt.QPushButton('{}'.format(client_name))
		button.setStyleSheet(f'background : {BASE_COLOR};')

		Vertical_layout.addWidget(button)
		button_dict[button] = address
		button.clicked.connect(application.buttonClicked)

		return button


def add_dialog():
	address = application.added_connection_address
	client_name = application.added_connection_name
	add_dialog_button_if_no_such(address, client_name)


def del_dialog():
	for but, addr in button_dict.items():
		if application.delited_connection_address == addr:	
			but.setParent(None)


def clear_TEdit():
	add_message_into_TEdit(GLOBAL)


def history_request():
	send_message_to_server('request',GLOBAL, 'history request')


def append_text(sender, receiver, message):
	if receiver == GLOBAL:
		if application.addr_to_send == GLOBAL:
			application.ui.TEdit_Chat_Text.append(message)
	else :
		if application.addr_to_send == sender:
			application.ui.TEdit_Chat_Text.append(message)


def add_dialog_if_no_such(address, client_name):
	is_in = False
	for but, addr in button_dict.items():
		if address == addr:
			is_in = True
			break
	if not is_in:
		application.added_connection_address = address
		application.added_connection_name = client_name
		application.signal.Add_Dialog.emit()


def find_server():	
	UDP_socket.start_UDP_receiving()
	UDP_socket.start_UDP_sending()

	time.sleep(0.05)
	application.ui.Edit_IP.setText(UDP_socket.finded_ip)
	application.ui.Edit_Port.setText(str(50007))


def send_message_to_server(mtype, receiver, message):	
	if message != 'history request':
		time_now = strftime("%H:%M:%S %d-%m-%Y", gmtime())
		mes = f' |{time_now}| {message}'
		message_list.append(['-->',receiver,mes])
	TCP_socket.send(mtype, receiver, message)
	

def log_in():
	application.ui.Btn_Log_In.setDisabled(True)
	application.ui.Btn_Log_Out.setDisabled(False)

	TCP_socket.host = application.ui.Edit_IP.text()
	TCP_socket.port = int(application.ui.Edit_Port.text())

	TCP_socket.client_name = application.ui.Edit_Name.text()
	TCP_socket.connect()
	

def prepare_and_send_message():	
	message = application.ui.TEdit_Input_Message.toPlainText()
	time_now = strftime("%H:%M:%S %d-%m-%Y", gmtime())
	mes = f' |{time_now}| {message}'

	if message:
		application.ui.TEdit_Input_Message.clear()
		send_message_to_server('message', application.addr_to_send, message)
		application.ui.TEdit_Chat_Text.append(f'--> {mes}')
		application.ui.TEdit_Input_Message.setFocus()


def close_connection():
	try:
		TCP_socket.disconnect()
	except:
		pass


def close_all_dialogs():
	for dialog, addr in button_dict.items():
		if addr != GLOBAL:
			dialog.setParent(None)
		else:
			save_dialog = dialog
			save_addr = addr
	button_dict.clear()
	button_dict[save_dialog] = save_addr


def log_out():
	application.ui.Btn_Log_In.setDisabled(False)
	application.ui.Btn_Log_Out.setDisabled(True)
	close_connection()
	close_all_dialogs()
	for i in range(1, application.ui.ComboBox_Of_Clients.count()):
		application.ui.ComboBox_Of_Clients.removeItem(i)
		del clients[i]
	message_list.clear()
	

def add_message_into_TEdit(receiver_address):
	# message[0] - sender, message[1] - receiver, message[2] - message_text
	application.ui.TEdit_Chat_Text.clear()
	if receiver_address == GLOBAL:					
		for message in message_list:
			if message[1] == receiver_address:
				if message[0] == '-->':
					application.ui.TEdit_Chat_Text.append(f'{message[0]} {message[2]}')
				else:
					application.ui.TEdit_Chat_Text.append(f'{message[2]}')
	else:
		for message in message_list:
			if message[1] == receiver_address:
				if message[0] == '-->':
					application.ui.TEdit_Chat_Text.append(f'{message[0]} {message[2]}')
				else:
					application.ui.TEdit_Chat_Text.append(f'{message[2]}')
			elif message[0] == receiver_address and message[1] != GLOBAL:
				application.ui.TEdit_Chat_Text.append(f'{message[2]}')


def change_active_dialog():
	name = application.ui.ComboBox_Of_Clients.currentText()
	address = clients[application.ui.ComboBox_Of_Clients.currentIndex()]

	button = add_dialog_button_if_no_such(address, name)
	button.click()


def change_dialog_button_color(button, color):
	button.setStyleSheet(f'background : {color};')


class Communicate(QObject):
	Add_Dialog = pyqtSignal()
	Del_Dialog = pyqtSignal()
	Clear_TEdit = pyqtSignal()
	new_message = pyqtSignal()


class MainWindow(QtWidgets.QMainWindow):
	def __init__(self):
		super(MainWindow, self).__init__()
		self.ui = Ui_MainWindow()
		self.ui.setupUi(self)
		
		self.signal = Communicate()
		self.signal.new_message.connect(new_message)
		self.signal.Add_Dialog.connect(add_dialog)
		self.added_connection_address = ''
		self.added_connection_name = ''		
		self.signal.Del_Dialog.connect(del_dialog)
		self.delited_connection_address = ''
		self.addr_to_send = GLOBAL
		self.ui.ComboBox_Of_Clients.currentIndexChanged.connect(change_active_dialog)
		self.signal.Clear_TEdit.connect(clear_TEdit)

	def buttonClicked(self):
		sender = self.sender()
		# print(str(sender))
		for but, addr in button_dict.items():
			if sender == but:
				application.addr_to_send = addr
				color = but.styleSheet()
				change_dialog_button_color(but, BASE_COLOR)						
				add_message_into_TEdit(addr)
				break
	
	def closeEvent(self, event): 
		close_connection()
		


if __name__ == "__main__":
	import sys
	import socket
	import threading
	import time
	from UDPConnection import UDPConnection
	from TCPConnection import TCPConnection	
	from time import gmtime, strftime

	GLOBAL = 'Global'

	BASE_COLOR = '#F0F0F0'
	RED_COLOR = '#DB4747'	

	app = QtWidgets.QApplication(sys.argv)
	application = MainWindow()
	application.show()	

	HOST = socket.gethostbyname(socket.gethostname())
	PORT = 50007
	
	UDP_socket = UDPConnection(HOST, PORT)
	TCP_socket = TCPConnection(HOST, PORT, application.signal.new_message)

 
	application.ui.Btn_Find_Server.clicked.connect(find_server)
	application.ui.Btn_Log_In.clicked.connect(log_in)
	application.ui.Btn_Send_Message.clicked.connect(prepare_and_send_message)
	application.ui.Btn_Log_Out.clicked.connect(log_out)
	application.ui.Btn_History_Request.clicked.connect(history_request)

	clients = [GLOBAL]
	button_dict = {}
	message_list = []	

	Vertical_layout = application.ui.verticalLayout
	add_dialog_button_if_no_such(GLOBAL,GLOBAL)

	
	Widget = Qt.QWidget()
	Widget.setLayout(Vertical_layout)


	Scroll_Area = application.ui.scrollArea
	Scroll_Area.setWidget(Widget)


	sys.exit(app.exec_())

