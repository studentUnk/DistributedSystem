import socket
from _thread import *

host = '172.28.1.250' # Server's IP address
port = 65400
port_clients = 65401
hostname = socket.gethostname() # Hostname of the client
local_ip = socket.gethostbyname(hostname) # IP address of the client

flag = "#" # flag for the socket recv function
flag_s = '|update-addr-str|' # flag start data table address client
flag_e = '|update-addr-end|' # flag end data tablle address client
flag_a = '|' # flag for address

client_info = [] # the data of the clients are in bytes
msg_send = [] # check that message has been sent to all the clients -> [thread_id,0-1] 0 = sent 1 = no sent

msg_user = "" # string of the message to be sent to all the other hosts


#------------------------------------------------------------------------------
# Server for the other clients
#------------------------------------------------------------------------------

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

def threaded_client(connection):
	global client_info
	connection.sendall(str.encode(flag + 'Welcome to the Server' + flag))
	data = connection.recv(3000) # client info
	reply = flag + '(Server) Your data: ' + data.decode('utf-8') + flag
	connection.sendall(str.encode(reply)) # Send confirmation of the info to the client
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
	print ("--------------------------")

	ServerSocket.listen(5) # Max 3 connections -> TCP

	client_info = [] # the data of the clients are in bytes

	while True:
		Client, address = ServerSocket.accept() # TCP
		print('Connected to: ' + address[0] + ':' + str(address[1]))
		start_new_thread(threaded_client, (Client, ))
		ThreadCount += 1
		#print('Thread Number: ' + str(ThreadCount))
	ServerSocket.close()
	


#------------------------------------------------------------------------------
# Client
#------------------------------------------------------------------------------


''' # Check why it is not working
def recv_basic(the_socket):
    total_data=[]
    while True:
        data = the_socket.recv(3000)
        if not data: break
        total_data.append(data)
    return ''.join(total_data)
'''

def update_client_table (info):
	#print ("Message to get data: " + info)
	
	count_f = 0
	for i in info:
		if i == flag_a:
			count_f = count_f + 1
	count_f = (int)((count_f/2)-2) # Amount of clients, -2 because there are two flags
	
	pos_s = len(flag_s)+1
	pos_e = 0
	
	for c in range(0,count_f,1):
		# Delete client's info flag
		pos_e = info.find('|',pos_s+1)
		#print (str(pos_s) + "," + str(pos_e))
		info_c = info[(pos_s):pos_e]
		#print (info_c)
		pos_s = pos_e + 2
		
		array_client = []
		
		pos_v = info_c.find("-") # first value
		array_client.append(info_c[:pos_v]) # name info 
		#print (info_c[:pos_v])
		
		pos_v_2 = info_c.find("-",pos_v+1) # second value
		array_client.append(info_c[pos_v+1:pos_v_2]) # ip info
		#print (info_c[pos_v+1:pos_v_2])
		
		array_client.append(info_c[pos_v_2+1:]) # port info
		#print (info_c[pos_v_2+1:])
		
		new_client(array_client) # Start connection with a new client

def new_client (array_client):
	for ci in client_info:
		if ci[0] == array_client[0]: # The connection already exists
			return
	client_info.append(array_client) # Add new client
	if(array_client[0] == hostname): # Trying to connect to the host
		return 
	#print ("Trying to connect to: " + array_client[1]) 
	start_connection_client(array_client[1],array_client[2]) # ip,port 

def check_message(msg, new_msg):
	msg = msg + new_msg # Join strings
	#print ("RAW message: " + new_msg)
	if len(msg) > 2 and msg[-1] == flag and msg[0] == flag and msg.find(flag,2) == len(msg): # ideal message
		#print ("Ideal message?")
		#print (msg[1:len(msg)-1])
		if msg.find(flag_s) != -1:
			#print ("My flag exists and is in : " + str(msg.find(flag_s)))
			update_client_table (msg[1:len(msg)-1])
		msg = ''		
	# assume that the message will always start with '#'
	else:
		#print ("Not ideal message?")
		end_m = msg.find(flag,2)
		if end_m != -1: # There is an end
			#print (msg[1:end_m])
			if msg.find(flag_s) != -1:
				update_client_table (msg[1:end_m])
			msg = msg[end_m+1:] # Some bytes left
	return msg

def input_user():
	global msg_user 
	while(msg_user != "end"):
		msg_user = input("-> ")
		if len(msg_user) > 0:
			if msg_user == "end":
				#print ("the input session has been closed")
				break # Close the connection
			for i in range(0,len(msg_send)):
				msg_send[i][1] = 1 # Set value 1 to send message
		while len(msg_user) != 0:
			full_m = 0 # Check that the message has been send to everyone
			for m in msg_send:
				if m[1] == 1: 
					full_m = 1
					break
			if full_m == 0:
				msg_user = ""
	#print ("end has been send")

def set_connection_client(socket_c):
	#socket_c.sendall((hostname + "->" + "this is my message for you").encode('utf-8'))
	#msg = ""
	global msg_user
	global msg_send
	msg_send.append([get_ident(), 0])
	pos_t = len(msg_send)-1
	while(msg_user != "end"):
		#msg_user = input("-> ")
		#if msg_user != "end" and len(msg_user) != 0:
		if msg_send[pos_t][1] == 1:
			#msg_user_temp = 
			socket_c.sendall((hostname + "->" + msg_user).encode("utf-8"))
			#msg_user = ""
			msg_send[pos_t][1] = 0
	
	
	#socket_c.close()

def start_connection_client(ip_client, port_client):
	try:
		ip_server = ip_client
		port = port_client
		ClientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # TCP
		#ClientSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP
	 
		#print('Setting up connection to server of client ' + ip_client + ':' + port)
		try:
			ClientSocket.connect((ip_server, int(port)))
		except socket.error as e:
			print(str(e))
			
		# Connection to the server	
		start_new_thread(set_connection_client, (ClientSocket, ))
		
		# Server client
		#start_new_thread(start_server_client, ())
		
	except Exception as e:
		print ('Error: the server thread did not start')
		print(e)

def set_connection_server(socket_c):
	rec_msg = ''
	Response = socket_c.recv(3000) # Welcome message from server
	print ("--------------------------")
	rec_msg = check_message(rec_msg,Response.decode('utf-8'))
	print (Response.decode('utf-8'))
	print ("--------------------------")
	
	my_host_data = str(hostname) + "-" + str(local_ip) + "-" + str(port_clients)
	socket_c.sendall(my_host_data.encode('utf-8')) # Send data to the server
	#Response = socket_c.recv(3000)
	#print (Response.decode('utf-8'))
	
	# start client input
	start_new_thread(input_user,())
	
	while True:
		#Input = input('Say Something: ')
		#ClientSocket.sendall(str.encode(Input))
		
		Response = socket_c.recv(3000)
		rec_msg = check_message(rec_msg,Response.decode('utf-8'))
		
		#while rec_msg[0] == flag and rec_msg[-1] == flag: # check that all the data has been read
		while len(rec_msg) != 0:
			if rec_msg[-1] != flag:
				break # there is no more messages
			rec_msg = check_message(rec_msg, '')
		#print(recv_basic(socket_c).decode('utf-8'))
		#print(Response.decode('utf-8'))
		
		#get_values_addr(Response.decode())

	#socket_c.close()

try:
	ip_server = host
	ClientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # TCP
	#ClientSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP
 
	print('Setting up connection to server')
	try:
		ClientSocket.connect((ip_server, port))
	except socket.error as e:
		print(str(e))
		
	# Connection to the server	
	start_new_thread(set_connection_server, (ClientSocket, ))
	
	# Server client
	#start_new_thread(start_server_client, ())
	
except:
	print ('Error: the server thread did not start')

data = 2
while True:
	data = 2


'''
data = ''
while data != 'end':
	data = input ("->")
'''
'''

ClientSocket = socket.socket()

print('Waiting for connection')
try:
    ClientSocket.connect((host, port))
except socket.error as e:
    print(str(e))

#hostname = socket.gethostname()
hostname = 'client_1'
local_ip = socket.gethostbyname(hostname)
my_host_data = str(hostname) + "-" + str(local_ip) + "-" + str(port_clients)
ClientSocket.sendall(my_host_data.encode('utf-8')) # Send data to the server

Response = ClientSocket.recv(1024)
while True:
    #Input = input('Say Something: ')
    #ClientSocket.sendall(str.encode(Input))
    Response = ClientSocket.recv(1024)
    print(Response.decode('utf-8'))

ClientSocket.close()
'''

