from xmlrpc.server import SimpleXMLRPCServer

import xmlrpc.client
import default_data
#from _thread import *


'''
Search the data of the user
'''
def search_data_user(user):
	address_c = default_data.return_address(0)
	value = 0
	with xmlrpc.client.ServerProxy("http://" + address_c[0] + ":" + address_c[1] + "/") as block:
		value=block.search_amount(user)
	return value
	#return 234

def get_full_chain():
	address_block = default_data.return_address(0)
	value = 0
	with xmlrpc.client.ServerProxy("http://" + address_block[0] + ":" + address_block[1] + "/") as block:
		value=block.full_chain()
	return value
	#return 234

'''
Function to register the transaction between two users
userS = user that is going to transfer
userR = user that is going to receive
amount = amount that userS is going to transfer to userR
'''
def coord_create_block(userS, userR, amount):
	r = check_data_transaction(userS, userR, amount) # Check the data
	if r != 'OK':
		return "Error - " + r # Return cause of invalid data
	
	r = check_user_transaction(userS, userR) # Check users exist
	if r != 'OK':
		return "Error - " + r # Return the user that does not exist
		
	r = check_amount(userS, amount)
	if r != 'OK':
		return "Error - " + r # Return that the amount to transfer is invalid
	
	
	new_id, open_close = get_id_open_close(get_amount_block()) # Return data for the new transaction
	
	return register_data_coord_block(get_data_format(userS, userR, amount), new_id, open_close)

'''
Check the data
'''	
def check_data_transaction(userS, userR, amount):
	address_data = default_data.return_address(2) # get information of register server
	
	valueC = 0
	with xmlrpc.client.ServerProxy("http://" + address_data[0] + ":" + address_data[1] + "/") as s:
		valueC = s.check_user(userS)
	if not valueC:
		return "The user transfer is not valid, please check the reference"
		
	valueC = 0
	with xmlrpc.client.ServerProxy("http://" + address_data[0] + ":" + address_data[1] + "/") as s:
		valueC = s.check_user(userR)
	if not valueC:
		return "The user receiver is not valid, please check the reference"
	
	valueC = 0
	with xmlrpc.client.ServerProxy("http://" + address_data[0] + ":" + address_data[1] + "/") as s:
		valueC = s.check_amount(amount)
	if not valueC:
		return "The amount is not valid, please check the data introduced"
	
	return 'OK'
	
def check_user_transaction(userS, userR):
	if not check_user_exists(userS): 
		return "The user -" + userS + "- that is going to transfer does not exist in the chain"
	if not check_user_exists(userR):
		return "The user -" + userR + "- that is goint to receive does not exist in the chain"
	return "OK"
	
'''
Check if user exists
True exist | False does not exist
'''
def check_user_exists(user):
	address_data = default_data.return_address(0)
	with xmlrpc.client.ServerProxy("http://" + address_data[0] + ":" + address_data[1] + "/") as s:
		return s.search_user(user)
	return False

'''
Check if an user can transfer the amount given
'''
def check_amount(user, amount):
	address_data = default_data.return_address(0)
	r = False
	with xmlrpc.client.ServerProxy("http://" + address_data[0] + ":" + address_data[1] + "/") as s:
		r = s.check_amount(user, amount)
	if not r:
		return "The amount " + amount + " of the user -" + user + "- is not valid to transfer"
	return "OK"

'''
Get new id for the transaction and if it should be closed
'''	
def get_id_open_close(amount):
	address_data = default_data.return_address(3)
	with xmlrpc.client.ServerProxy("http://" + address_data[0] + ":" + address_data[1] + "/") as s:
		return s.id_close(amount)
	'''
	n_id = -1
	with xmlrpc.client.ServerProxy("http://" + address_data[0] + ":" + address_data[1] + "/") as s:
		n_id = s.get_id()
		
	blockC = False
	with xmlrpc.client.ServerProxy("http://" + address_data[0] + ":" + address_data[1] + "/") as s:
		blockC = s.close_block()
		
	return n_id, blockC
	'''

def register_data_coord_block(data, n_id, openC):
	address_data = default_data.return_address(0)
	with xmlrpc.client.ServerProxy("http://" + address_data[0] + ":" + address_data[1] + "/") as s:
		#return s.new_block(data, n_id, openC)
		return s.add_trans(data, openC, n_id)
		
''' 
Get format of the data to transfer
'''
def get_data_format(userS, userR, amount):
	address_data = default_data.return_address(2)
	with xmlrpc.client.ServerProxy("http://" + address_data[0] + ":" + address_data[1] + "/") as s:
		return s.set_data(userS, userR, amount)		

'''
Get amount of transactions in the last block
'''
def get_amount_block():
	address_data = default_data.return_address(0)
	with xmlrpc.client.ServerProxy("http://" + address_data[0] + ":" + address_data[1] + "/") as s:
		return s.amount_trans()
	

def coord_consult_dir():
	return "nothing"

def coord_close_block():
	return "nothing"

address_s = default_data.return_address(1)
port_server = int(address_s[1])
address_server = address_s[0]
server = SimpleXMLRPCServer((address_server, port_server))

print("--------------------")
print("Server Coordinator is up")
print("Address server is: " + address_server)
print("Listening on port: " + str(port_server))
print("--------------------")

server.register_function(coord_create_block, "create_block" )
server.register_function(search_data_user, "search_data" )
server.register_function(get_full_chain, "full_chain" )
server.serve_forever()

''' 
Create five threads with each connection that must have the coordinator
'''

