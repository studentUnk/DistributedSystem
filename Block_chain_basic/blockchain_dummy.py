import hashlib
from random import seed
from random import randint

# variables
array_chain = [] # array
array_element = [] # element of the array 
n_id = 1 # Number of the block
limit_nonce = 99999999 # limit for the nonce

def create_chain(n_id, data, prev_hash = "0", close_hash = False):
	array_e = []
	array_e.append(str(n_id)) # add id
	nonce = 1234 # dummy nonce
	array_e.append(str(nonce)) # add nonce
	array_e.append(data) # add data
	array_e.append(prev_hash) # add node genesis or previous genesis --> add condition
	#-- Try 000 for hash
	my_string_hash = array_e[0]+array_e[1]+array_e[2]+array_e[3] # possible hash
	encode_hash = my_string_hash.encode()
	array_e.append(hashlib.sha256(encode_hash).hexdigest())
	print (array_e)
	#seed(1)
	if not close_hash:
		return array_e # it is not mandatory start with "000"
		
	for i in range(0,limit_nonce):
		#nonce = randint(0,999999) # random number
		#print (nonce)
		array_e[1] = str(i) # add new nonce
		my_string_hash = array_e[0]+array_e[1]+array_e[2]+array_e[3] # possible hash
		encode_hash = my_string_hash.encode()
		array_e[4] = hashlib.sha256(encode_hash).hexdigest()
		#print (array_e[4])
		if array_e[4][0:3] == "000":
			break
	#print(array_e)
	return array_e # element chain

def read_chain():
	return array_chain # as a text?
		
# Test dummy chain 
user_input = input("Enter data 1: ")
array_chain.append(create_chain(1, user_input)) # genesis node add
user_input = input("Enter data 2: ")
array_chain.append(create_chain(2, user_input,array_chain[len(array_chain)-1][4])) # add data 2
user_input = input("Enter data 3: ")
array_chain.append(create_chain(3, user_input,array_chain[len(array_chain)-1][4],True)) # add data 3 and close

print ("This is the current chain")
print(array_chain)

# add elements
'''
array_element.append(str(n_id)) # add id

data = "hello node 1"
array_element.append(data) # add data
array_element.append("0") # add node genesis
my_string_hash = array_element[0]+array_element[1]+array_element[2]+array_element[3]
encode_hash = my_string_hash.encode()
array_element.append(hashlib.sha256(encode_hash).hexdigest())
print(array_element)
'''
string = "test"
encode = string.encode()
result = hashlib.sha256(encode)
print(string)
print(result.hexdigest())
