# code base on https://codezup.com/socket-server-with-multiple-clients-model-multithreading-python/
import socket
import os
from _thread import *

ServerSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # TCP
#ServerSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP
host = '172.28.1.250' # Default IP address assigned in LAN 
port = 65400
ThreadCount = 0

flag = '#'

try:
	ServerSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # Restart address if it is in use
	ServerSocket.bind((host, port))
except socket.error as e:
	print(str(e))

print ("--------------------------")
print('Server available')
print('IP: ' + host)
print ("--------------------------")

ServerSocket.listen(15) # Max 10 connections -> TCP

client_info = [] # the data of the clients are in bytes

def threaded_client(connection):
	global client_info
	connection.sendall(str.encode(flag + 'Welcome to the Server' + flag))
	data = connection.recv(3000) # client info
	reply = flag + '(Server) Your data: ' + data.decode('utf-8') + flag
	connection.sendall(str.encode(reply)) # Send confirmation of the info to the client
	# Wait for confirmation of the client
	
	client_info.append(data) # Add info client to global variable of client addresses
	'''
	for d in client_info:
			connection.sendall(d) # Send the addresses that exists in the server
	'''
	size_client_info = 1
	while True:
		if size_client_info != len(client_info):  # Update address table if the size has changed
			connection.sendall(str.encode(flag + "|update-addr-str|")) # Flags to update address table
			#print("Size_client new info " + str(size_client_info))
			#print (client_info)
			for d in client_info:
				connection.sendall(str.encode("|")+d+str.encode("|")) # Send current addresses
			size_client_info = len(client_info)
			connection.sendall(str.encode("|update-addr-end|" + flag))
		if not data:
			break
		#connection.sendall(str.encode(reply))
	connection.close()

while True:
	Client, address = ServerSocket.accept() # TCP
	print('Connected to: ' + address[0] + ':' + str(address[1]))
	start_new_thread(threaded_client, (Client, ))
	ThreadCount += 1
	print('Thread Number: ' + str(ThreadCount))
ServerSocket.close()
