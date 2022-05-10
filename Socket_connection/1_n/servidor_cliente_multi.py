import socket
from _thread import *

host = '172.28.0.10' # Server's IP address
port = 65400
port_clients = 65401
hostname = socket.gethostname() # Hostname of the client
local_ip = socket.gethostbyname(hostname) # IP address of the client

flag = "#" # flag for the socket recv function
flag_s = '|update-addr-str|' # flag start data table address client
flag_e = '|update-addr-end|' # flag end data tablle address client
flag_a = '|' # flag for address
flag_file = "sendFile" # flag for the file

client_info = [] # the data of the clients are in bytes


#------------------------------------------------------------------------------
# Server for the other clients
#------------------------------------------------------------------------------

# The client's server is just going to listen

'''
try:
	ServerSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # Restart address if it is in use
	ServerSocket.bind((local_ip, port_clients))
except socket.error as e:
	print(str(e))

print ("--------------------------")
print('Server available')
print ("--------------------------")

ServerSocket.listen(5) # Max 3 connections -> TCP

client_info = [] # the data of the clients are in bytes
'''

def receive_file(socketA):
	fileA = open("/files_Shared/audio.wav", "wb") # create file if it does not exist ("data.wav","wb") -> root of the python file /home/my_drive/folder/
	load = 1
	frames = 3000
	while (load): # exits if the value is zero or null
		load = socketA.recv(frames)
		while (load):
			fileA.write(load)
			load = socketA.recv(frames)
		fileA.close()
	

def threaded_client(connection):
	#global client_info
	#connection.sendall(str.encode(flag + 'Welcome to the Server' + flag))
	#data = connection.recv(3000) # client info
	#reply = flag + '(Server) Your data: ' + data.decode('utf-8') + flag
	#connection.sendall(str.encode(reply)) # Send confirmation of the info to the client
	#client_info.append(data) # Add info client to global variable of client addresses
	'''
	for d in client_info:
			connection.sendall(d) # Send the addresses that exists in the server
	'''
	size_client_info = 1
	while True:
		data = connection.recv(3000) # client info
		if not data:
			break
		print(data.decode('utf-8')) # Print message of other clients
		if data.decode('utf-8') == flag_file:
			#print("confirmation?")
			connection.sendall(str.encode(flag_file)) # Send confirmation for data
			receive_file(connection) # Accept file
			
		'''
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
		'''
	connection.close()

'''
while True:
	Client, address = ServerSocket.accept() # TCP
	print('Connected to: ' + address[0] + ':' + str(address[1]))
	start_new_thread(threaded_client, (Client, ))
	ThreadCount += 1
	print('Thread Number: ' + str(ThreadCount))
ServerSocket.close()
'''

def start_server_client():
	ServerSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # TCP
	try:
		ServerSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # Restart address if it is in use
		ServerSocket.bind((local_ip, port_clients))
	except socket.error as e:
		print(str(e))

	print ("--------------------------")
	print('Server available')
	print('IP: ' + local_ip)
	print('Port: ' + str(port_clients))
	print ("--------------------------")

	ServerSocket.listen(15) # Max 3 connections -> TCP

	client_info = [] # the data of the clients are in bytes

	ThreadCount = 0	
	
	while True:
		Client, address = ServerSocket.accept() # TCP
		print('Connected to: ' + address[0] + ':' + str(address[1]))
		start_new_thread(threaded_client, (Client, ))
		ThreadCount += 1
		print('Thread Number: ' + str(ThreadCount))
	ServerSocket.close()
	
start_server_client()
