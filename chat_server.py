#									D:\Python\KSIS\Laba1\test_server.py	
import socket, threading, time
from time import gmtime, strftime

host = socket.gethostbyname(socket.gethostname())
port = 50007

UDP_socket=socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
UDP_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
UDP_socket.bind(('0.0.0.0', port)) 

TCP_socket=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
TCP_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
TCP_socket.bind((host, port)) 
TCP_socket.listen(10)

clients = {}
message_list = []
names_list = []

def UDP_receiving(name, sock):  # Поточность
	while True:
		try:
			while True:
				data, addr = UDP_socket.recvfrom(1024)
				print(data) 
				print(addr)
				UDP_socket.sendto((str(host)+' '+str(port)).encode("utf-8"), addr)
				time.sleep(0.2)
		except:
			pass

Thread_recv_UDP = threading.Thread(target=UDP_receiving, args=("RecvThread", UDP_socket), daemon = True)
Thread_recv_UDP.start()

def Data_processing(mtype, receiver, client_name, data, addr, ip):
	time_now = strftime("%H:%M:%S %d-%m-%Y", gmtime())

	mes = '†'.join(data)
	message = f' |{time_now} {ip}:{port}| {mes}'
	if receiver == 'Global' and mtype != 'request':
		message_list.append(f'{addr}†history†{client_name}†{message}')
	if mtype == 'connect':
		return f'{addr}†{receiver}†{client_name}† {message}'
	elif mtype == 'message':
		return f'{addr}†{receiver}†{client_name}† :: {message}'
	elif mtype == 'disconnect':
		return f'{addr}†{receiver}†{client_name}† {message}'

def Send_Message_To_Client(message, receiver, connection):
	for client, addr in clients.items():
		if connection != client and (addr == receiver or receiver == 'Global'
									or receiver == 'connect'or receiver == 'disconnect'):
			client.send(bytes(message.encode('utf-8')))

def TCP_receiving(name, connection, address):  # Поточность
	shutdown = False
	while not shutdown:
		# try:
		while not shutdown:
			data = connection.recv(1024).decode('utf-8').split('†')
			print(data)

			message = Data_processing(data[0],data[1],data[2],data[3:], str(address[1]), address[0])

			if data[0] == 'disconnect':
				# print(clients[connection])
				del names_list[names_list.index(clients[connection])-1]
				del names_list[names_list.index(clients[connection])]
				del clients[connection]
				message = Data_processing(data[0],data[0],data[2],data[3:], str(address[1]), address[0])
				# connection.shutdown(socket.SHUT_RDWR)
				shutdown = True	
			elif data[0] == 'connect':
				connection.send(bytes(('active clients†'+'†'.join(names_list)).encode('utf-8')))
				names_list.append(data[2])
				names_list.append(str(address[1]))
				message = Data_processing(data[0],data[0],data[2],data[3:], str(address[1]), address[0])
			elif data[0] == 'request':
				connection.send(bytes('history start† † † '.encode('utf-8')))
				for message in message_list:
					connection.sendall(bytes(message.encode('utf-8')))
					print(message)
					time.sleep(0.2)
				connection.send(bytes('history end† † † '.encode('utf-8')))
				continue

			
			
			# print(message)

			Send_Message_To_Client(message, data[1], connection)
			# print(connection)
			print(message,' ',address)
			
			time.sleep(0.2)
		# except:
		# 	pass

while True:
	connection, address = TCP_socket.accept()
	print("new connection from {address}".format(address=address))
	clients[connection] = str(address[1])
	Thread_recv_TCP = threading.Thread(target=TCP_receiving, args=("RecvThread", connection, address), daemon = True)
	Thread_recv_TCP.start()

