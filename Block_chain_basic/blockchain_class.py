import hashlib
import wallet_class

class Blockchain:
	
	#limit_nonce = 99999999 # limit for the nonce
	'''
	Format of each block
	[0] = id
	[1] = nonce
	[2] = data
	[3] = previous hash
	[4] = current hash
	'''
	#array_chain = [] # block chain

	def create_chain(self, data, n_id = 0, prev_hash = "0", close_hash = False):
		array_e = []
		if n_id == 0:
			array_e.append(str(len(self.array_chain)+1))
		else: 
			array_e.append(str(n_id)) # add id
		nonce = 1234 # dummy nonce
		array_e.append(str(nonce)) # add nonce
		array_e.append(data) # add data
		array_e.append(prev_hash) # add node genesis or previous genesis --> add condition

		my_string_hash = array_e[0]+array_e[1]+array_e[2]+array_e[3] # possible hash
		encode_hash = my_string_hash.encode()
		array_e.append(hashlib.sha256(encode_hash).hexdigest())
		#print (array_e)
		
		if not close_hash:
			self.array_chain.append(array_e)
			return array_e # it is not mandatory start with "000"
			
		for i in range(0,self.limit_nonce):
			#print (nonce)
			array_e[1] = str(i) # add new nonce
			my_string_hash = array_e[0]+array_e[1]+array_e[2]+array_e[3] # possible hash
			encode_hash = my_string_hash.encode()
			array_e[4] = hashlib.sha256(encode_hash).hexdigest()

			if array_e[4][0:self.size_letter_close] == self.letter_close_hash :
				break
		#print(array_e)
		self.array_chain.append(array_e) # Add new element to the chain
		#return array_e # element chain	
		
	def create_chain_next(self, dataU, n_idU, close_hashU):
		self.create_chain(data = dataU, n_id = n_idU, prev_hash = self.return_last_hash(), close_hash = close_hashU)
		
	def create_block_zero(self, n_id, prev_hash):
		data = "0"
		array_e = []
		if n_id == 0:
			array_e.append(str(len(self.array_chain)+1))
		else: 
			array_e.append(str(n_id)) # add id
		nonce = 1234 # dummy nonce
		array_e.append(str(nonce)) # add nonce
		array_e.append(data) # add data
		array_e.append(prev_hash) # add node genesis or previous genesis --> add condition

		my_string_hash = array_e[0]+array_e[1]+array_e[2]+array_e[3] # string for hash
		array_e.append(self.generate_hash(my_string_hash)) # possible hash
		#print(array_e)
		self.array_chain.append(array_e) # Add new element to the chain
		#return array_e # element chain	
	
	'''
	Add transaction to block
	'''
	def add_transaction(self, dataU):
		if self.array_chain[-1][2] == "0":
			self.array_chain[-1][2] = dataU # Delete zero and add transaction
		else:
			self.array_chain[-1][2] = self.array_chain[-1][2] + dataU # Add new transaction
	
	'''
	Add transaction to block and check option to close and generate new block
	'''
	def add_transaction_block(self, dataU, close=False, n_idU = 1):
		self.add_transaction(dataU)
		if close:
			current_data = self.array_chain[-1][0] + self.array_chain[-1][2] + self.array_chain[-1][3]
			self.array_chain[-1][1], self.array_chain[-1][4] = self.generate_hash_close(current_data) # close last block
			self.create_block_zero(n_idU,self.return_last_hash()) # generate new block

	'''
	Generate hash
	'''
	def generate_hash(self, data):
		encode_hash = data.encode()
		return hashlib.sha256(encode_hash).hexdigest()
	
	'''
	Close block and return new hash and nonce
	'''
	def generate_hash_close(self, dataBlock):
		nonce = ""
		hashF = ""
		for i in range(0,self.limit_nonce):
			#print (nonce)
			nonce = str(i) # add new nonce
			my_string_hash = dataBlock + nonce # possible hash
			encode_hash = my_string_hash.encode()
			hashF = hashlib.sha256(encode_hash).hexdigest()
			if hashF[0:self.size_letter_close] == self.letter_close_hash :
				break
				
		return nonce, hashF
	
	'''
	Format of the data of a chain
	hash_owner->hash_transfer:value_to_transfer; 
	Example 1234123fasdlfj->123jfalsdjfa89:234;
	'''
	
	'''
	Search user based on the given data
	'''
	def user_exist(self, user):
		for a in self.array_chain :
			d = a[2] # set data 
			pos_end = 0 # value of the end of the user
			#print (d)
			while pos_end < (len(d)-1) and d != "0":
				middle_t = d.find("->",pos_end)
				first_u = d[pos_end:middle_t]
				#print(first_u)
				pos_end = d.find(":",pos_end)
				second_u = d[middle_t+2:pos_end]
				#print(second_u)
				pos_end = d.find(";",pos_end) + 1
				# Check if the user exist in the data
				if first_u == user or second_u == user:
					return True
		return False
	
	def __init__(self):
		self.limit_nonce = 99999999 # limit of number to try to find a value like 00002sdf2
		self.letter_close_hash = "0000" # first letters to close the hash
		self.size_letter_close = len(self.letter_close_hash) # amount of letters to check
		self.array_chain = [] # block chain 
		
		self.seed_block_chain() # First data

	def return_last_hash(self):
		return self.array_chain[len(self.array_chain)-1][4]
	
	def return_full_chain(self):
		return self.array_chain
		
	'''
	Search and return the amount in which a user is related
	'''
	def total_amount_user(self, user):
		amount = 0
		for a in self.array_chain :
			d = a[2] # set data 
			pos_end = 0 # value of the end of the user
			#print (d)
			while pos_end < (len(d)-1) and d != "0":
				middle_t = d.find("->",pos_end)
				first_u = d[pos_end:middle_t]
				#print(first_u)
				pos_end = d.find(":",pos_end)				
				second_u = d[middle_t+2:pos_end]
				#print(second_u)
				# Check if the user exist in the data
				if first_u == user or second_u == user:
					#print (d[pos_end+1:d.find(";",pos_end)])
					if first_u == user:
						amount = amount + (int(d[pos_end+1:d.find(";",pos_end)])*-1) # the user gives data
					else:
						amount = amount + int(d[pos_end+1:d.find(";",pos_end)]) # the user receives data
				pos_end = d.find(";",pos_end) + 1
					
		return amount
	
	'''
	Check if the amount to transfer is possible 
	a <= b => True
	a > b => False
	'''
	def check_amount_transaction(self, user, amount):
		amountU = self.total_amount_user(user)
		return amount <= amountU and amount > 0 
	
	'''
	Return the amount of transactions in last block
	'''
	def count_transactions_last_block(self):
		trans = self.array_chain[-1][2]
		amountT = 0
		for t in trans:
			if t == ';':
				amountT = amountT+1 # Count transaction
		return amountT
	
	def seed_block_chain(self):
		my_data = "genesis->adan:1000;genesis->eva:1000;genesis->cain:500;genesis->abel:500;"
		self.create_chain(data = my_data, n_id = 1, close_hash = True) # genesis, close block with 4 transactions
		self.create_block_zero(2,self.return_last_hash()) # create empty block
		
		'''
		my_data = "queso->raton:10;"
		self.create_chain(my_data,prev_hash = self.return_last_hash()) # second block
		
		my_data = "queso->raton:10;"
		self.create_chain(my_data,prev_hash = self.return_last_hash(), close_hash = True) # third block
		'''
		
	
#----------------------------------------------------------
'''
if __name__ == "__main__":
	block = Blockchain()
	

'''
#----------------------------------------------------------
# Test
'''
block = Blockchain()

block.seed_block_chain()

print(block.user_exist("raton"))
print(block.user_exist("cheese"))
#print(block.return_full_chain())
print(block.total_amount_user("queso"))

wallet = wallet_class.Wallet()
print(wallet.get_public_hash("raton"))
print(wallet.get_public_hash("raton"))
print(wallet.get_private_hash(wallet.get_public_hash("raton")))
wallet.print_beauty_chain(block.return_full_chain())
'''
