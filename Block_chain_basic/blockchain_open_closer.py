from xmlrpc.server import SimpleXMLRPCServer
#import blockchain_class as bc
import default_data
import open_closer_class

openClose = open_closer_class.OpenCloser()

def get_new_id():
	return openClose.get_new_id()
	
def check_close_block(amount):
	return openClose.check_close_block(amount)

def get_id_and_close(amount):
	return openClose.check_and_id(amount)

address_s = default_data.return_address(3)
port_server = int(address_s[1])
address_server = address_s[0]

server = SimpleXMLRPCServer((address_server, port_server))

print("--------------------")
print("Server OpenCloser is up")
print("Address server is: " + address_server)
print("Listening on port: " + str(port_server))
print("--------------------")

server.register_function(get_new_id, "get_id" )
server.register_function(check_close_block, "close_block" )
server.register_function(get_id_and_close, "id_close" )
server.serve_forever()
