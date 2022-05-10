import xmlrpc.client
import wallet_class 
import default_data

def search_amount_user():
	address_c = default_data.return_address(1)
	user = input("User reference to search: ")
	with xmlrpc.client.ServerProxy("http://" + address_c[0] + ":" + address_c[1] + "/") as coord:
		print("The user -" + user + "- has an amount in the chain of: " + str(coord.search_data(user)))
		
def get_full_blockchain():
	address_c = default_data.return_address(1)
	w = wallet_class.Wallet()
	with xmlrpc.client.ServerProxy("http://" + address_c[0] + ":" + address_c[1] + "/") as coord:
		w.print_beauty_chain(coord.full_chain())

def register_transaction():
	address_c = default_data.return_address(1)
	userSend = input("User reference that is going to transfer: ")
	userReceive = input("User reference that is going to receive: ")
	amount = input("Amount to transfer: ")
	with xmlrpc.client.ServerProxy("http://" + address_c[0] + ":" + address_c[1] + "/") as coord:
		print(coord.create_block(userSend,userReceive, amount))

def print_menu():
	print("--------------------")
	print("------- Menu -------")
	print("1. Print all the blockchain")
	print("2. Print total amount of an user")
	print("3. Make a transaction")
	print("0. Exit")
	print("--------------------")

print ("Wallet-Client started")
input_u = 1
while input_u != "0":
	print_menu()
	input_u = input("Select option: ")
	print("--------------------")
	if input_u == "1":
		get_full_blockchain()
	elif input_u == "2":
		search_amount_user()
	elif input_u == "3":
		register_transaction()
	else:
		print ("The input is invalid, please try again")
	
print ("Wallet-Client closed")	
		
