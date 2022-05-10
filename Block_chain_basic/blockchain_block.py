from xmlrpc.server import SimpleXMLRPCServer
import blockchain_class as bc
import default_data

block = bc.Blockchain() # Create blockchain object
#block.seed_block_chain() # Set default data of the chain

def search_amount_user(user):
	return block.total_amount_user(user)
	
def get_full_chain():
	return block.return_full_chain()
	
def search_user(user):
	return block.user_exist(user)

def check_amount(user,amount):
	return block.check_amount_transaction(user, int(amount))
	
def create_new_block(data, n_id, closeO):
	block.create_chain_next(data, n_id, closeO)
	return "The new block has been created succesfully"
	
def add_transactions_block(data, close, n_id):
	block.add_transaction_block(data, close, n_id)
	return "The new transaction has been added succesfully"
	
def get_amount_transactions_block():
	return block.count_transactions_last_block()

address_s = default_data.return_address(0)
port_server = int(address_s[1])
address_server = address_s[0]

server = SimpleXMLRPCServer((address_server, port_server))

print("--------------------")
print("Server Blockchain is up")
print("Address server is: " + address_server)
print("Listening on port: " + str(port_server))
print("--------------------")

server.register_function(search_amount_user, "search_amount" )
server.register_function(get_full_chain, "full_chain" )
server.register_function(search_user, "search_user" )
server.register_function(check_amount, "check_amount" )
server.register_function(create_new_block, "new_block" )
server.register_function(add_transactions_block, "add_trans" )
server.register_function(get_amount_transactions_block, "amount_trans")
server.serve_forever()

