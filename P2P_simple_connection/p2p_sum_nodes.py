# All in one
from _thread import *
from xmlrpc.server import SimpleXMLRPCServer
import socket
import xmlrpc.client

hostname = socket.gethostname() # Hostname of the client
local_ip = socket.gethostbyname(hostname) # IP address of the client
port = '8000' # Default port for all

flag = True # flag for the socket recv function
#flag_neighbor = True # flag to ask to neighbors

black_list = []
white_list = []

ip_first_request = '' # IP Address of the first request

# Set default neighbors in the network for communication
array_neighbors = {
	'172.16.8.1': ['172.16.8.2','172.16.8.3','172.16.8.4'],
	'172.16.8.2': ['172.16.8.1','172.16.8.4','172.16.8.5'],
	'172.16.8.3': ['172.16.8.1','172.16.8.4','172.16.8.6'],
	'172.16.8.4': ['172.16.8.1','172.16.8.2','172.16.8.3','172.16.8.5','172.16.8.6'],
	'172.16.8.5': ['172.16.8.2','172.16.8.4','172.16.8.6'],
	'172.16.8.6': ['172.16.8.3','172.16.8.4','172.16.8.5'],
} 

# My numbers, for now the numbers must be only numbers greater than zero
array_numbers = []

# Server 
server = SimpleXMLRPCServer((local_ip, int(port)))

'''
 Return the total value of the numbers
 action -> two values (get) to return total sum | (free) to free again the value
 flag   -> two values (True) it can transmit the total | (False) it cannot transmit the sum
 ip_requestor -> IP of the user who is askig for the total
'''
def return_total_number(action):
	global flag
	global black_list_request_get
	global black_list_request_free
	global ip_first_request
	if (action == 'get'):
		if flag:
			flag = False
			black_list_request_free = []
			#ip_first_request = ip_requestor
			return my_values()			
	else:
		flag = True
		black_list_request_get = []
	return 0 # No values or the value has been already sent

'''
Ask for information to the neighbors
'''
def return_total_neighbors(action):
	total = 0
	global array_neighbors
	global local_ip
	#global ip_first_request
	global port
	global black_list
	global white_list
	
	neighbors = array_neighbors[local_ip]
	black_list.append(local_ip)
	white_list = []

	for n in neighbors:
		found = False
		#for b in black_list_request_get:
		for b in black_list:
			if b == n:
				found = True
				break
		if not found:
			value = ask_total(n,port,action,black_list)
			if (value != -1):
				total = total + value			
		
	return total		

'''
Add address to black_list
black_list_r -> neighbors addresses 
'''
def add_black_list (black_list_r):
	global black_list
	global local_ip
	for b in black_list_r:
		found = False
		for b2 in black_list:
			if b == b2:
				found = True
				break
		if not found:
			black_list.append(b) # previous addresses
	#black_list.append(local_ip) # my own address

'''
Add address to white_list	
white_list_r -> neighbors addresses
'''
def add_white_list (white_list_r):
	global white_list
	global local_ip
	for b in white_list_r:
		found = False
		for b2 in white_list:
			if b == b2:
				found = True
				break
		if not found:
			white_list.append(b) # previous addresses
	white_list.append(local_ip) # add own address... you cannot send a signal to free yourself you must do it by yourself!!!
	
'''
Get all the information of the neighbors (what they can return?) and itself
action -> "get" nodes trying to get total number
       -> "free" nodes trying to get freedom again
black_list -> ip address rejected for communication
'''
def get_total_values(action, black_list):
	add_black_list(black_list)	
	return return_total_number(action) + return_total_neighbors("get")	


'''
Function to connect to the other neighbors
ip_neighbor -> ip to connect
port -> port to connect
action -> "get" nodes trying to get total number
       -> "free" nodes trying to get freedom again
black_list -> ip address rejected for communication       
'''
def ask_total(ip_neighbor, port, action, black_list):
	value = 0
	try:
		with xmlrpc.client.ServerProxy("http://" + ip_neighbor + ":" + port + "/") as ask_value:
			value = ask_value.total_number(action, black_list)
	except:
		print ("Error in the conection to -> " + ip_neighbor)
		value = 0
	return value

'''
Get total for all the nodes connected
'''
def total_neighbor():
	return my_values() + return_total_neighbors("get") # my_value + value_neighbor

'''
Free the nodes --- white list	
white_list -> ip address rejected for communication     
'''
def free_black_list(white_list_u):
	global black_list
	global white_list
	global array_neighbors
	global port
	global flag
	black_list = []
	add_white_list(white_list_u)
	for a in array_neighbors: # Send message for freedom to all the neighbors that still has no order!
		found = False
		for w in white_list:
			if w == a:
				found = True
				break
		if not found:
			try:
				with xmlrpc.client.ServerProxy("http://" + a + ":" + port + "/") as free:
					value = free.free_list(white_list)
			except:
				print ("Error in the conection for freedom -> " + a)
	flag = True # Free the option to send data of the node
	return True
		

'''
Calculate total of own values
'''
def my_values():
	total = 0
	for n in array_numbers:
		total = total + n
	return total

'''
Add a new value to the current list
'''
def add_value():
	input_value = input("Introduce new number: ")
	global array_numbers
	array_numbers.append(int(input_value))
	print ("New value has been added")

'''
Print current state of the white_list and the black_list
'''
def print_black_list():
	global white_list
	global black_list
	print ("white_list----")
	print (white_list)
	print ("black_list----")
	print (black_list)

'''
Options user
'''
def print_menu():
	print("--------------------")
	print("Available options")
	print("1. Total of the network")
	print("2. My values")
	print("3. My total")
	print("4. Add a new value")
	print("5. Print black list")
	
'''
Options menu
'''
def menu():
	while True: # No end...
		print_menu()
		input_u = input("Select option: ")
		if input_u == "1":
			print ("Please wait while all the nodes send the information...")
			total = str(total_neighbor())
			free_black_list(white_list)
			print("--------------------")
			print ("The total sum of all the nodes connected is: " + total)
		elif input_u == "2":
			print (array_numbers)
		elif input_u == "3":
			print (my_values())
		elif input_u == "4":
			add_value()
		elif input_u == "5":
			print_black_list()

print("--------------------")
print("Server is up")
print("Address server is: " + local_ip)
print("Listening on port: " + str(port))
print("--------------------")

try:
	start_new_thread(menu, ( )) #start thread to show menu for the host
except:
	print ('Error starting menu user')

server.register_function(get_total_values, "total_number" ) # Function to return the total number
server.register_function(free_black_list, "free_list" ) # Function to free the values again
server.serve_forever()
