from xmlrpc.server import SimpleXMLRPCServer
import xmlrpc.client
import wallet_class 
import default_data

# Value user must be string
def search_amount_user(user):
	address_c = default_data.return_address(1)
	#user = input("User reference to search: ")
	with xmlrpc.client.ServerProxy("http://" + address_c[0] + ":" + address_c[1] + "/") as coord:
		return ("The user -" + user + "- has an amount in the chain of: " + str(coord.search_data(user)))
		
def get_full_blockchain():
	address_c = default_data.return_address(1)
	w = wallet_class.Wallet()
	with xmlrpc.client.ServerProxy("http://" + address_c[0] + ":" + address_c[1] + "/") as coord:
		#return w.print_beauty_chain(coord.full_chain())
		return coord.full_chain()

# Values userSend, userReceive, amount must be string
def register_transaction(userSend, userReceive, amount):
	address_c = default_data.return_address(1)
	#userSend = input("User reference that is going to transfer: ")
	#userReceive = input("User reference that is going to receive: ")
	#amount = input("Amount to transfer: ")
	with xmlrpc.client.ServerProxy("http://" + address_c[0] + ":" + address_c[1] + "/") as coord:
		return (coord.create_block(userSend,userReceive, amount))

address_s = default_data.return_address(4)
port_server = int(address_s[1])
address_server = address_s[0]

server = SimpleXMLRPCServer((address_server, port_server))

print("--------------------")
print("Server Wallet is up")
print("Address server is: " + address_server)
print("Listening on port: " + str(port_server))
print("--------------------")

server.register_function(search_amount_user, "search_amount_user" )
server.register_function(get_full_blockchain, "get_full_blockchain" )
server.register_function(register_transaction, "register_transaction" )
server.serve_forever()
