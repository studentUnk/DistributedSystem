from xmlrpc.server import SimpleXMLRPCServer
#import blockchain_class as bc
import default_data
import register_class


def check_syntax_user(user):
	r = register_class.Register()
	return r.check_syntax_user_general(user)
	
def check_syntax_amount(amount):
	r = register_class.Register()
	return r.check_amount_user_general(amount)

def set_data_transfer(userS, userR, amount):
	r = register_class.Register()
	return r.create_data_transfer_format(userS, userR, amount)

address_s = default_data.return_address(2)
port_server = int(address_s[1])
address_server = address_s[0]

server = SimpleXMLRPCServer((address_server, port_server))

print("--------------------")
print("Server Register is up")
print("Address server is: " + address_server)
print("Listening on port: " + str(port_server))
print("--------------------")

server.register_function(check_syntax_user, "check_user" )
server.register_function(check_syntax_amount, "check_amount" )
server.register_function(set_data_transfer, "set_data" )
server.serve_forever()

