import hashlib

class Wallet:
	
	'''
	Return a hash based on the words given
	'''
	def get_public_hash(self, words):
		encode_hash = words.encode()
		return hashlib.sha256(encode_hash).hexdigest()
		
	'''
	Return private hash
	'''
	def get_private_hash(self, public_hash):
		encode_hash = (public_hash+self.private_word).encode()
		return hashlib.sha256(encode_hash).hexdigest()
		
	'''
	Print in a format 'easy-to-read' the data of the block chain
	
	Format of each block
	[0] = id
	[1] = nonce
	[2] = data
	[3] = previous hash
	[4] = current hash
	'''
	def print_beauty_chain(self,block_chain):
		print ("---------Start--------")
		print ("Data in the blockchain")
		for block in block_chain:
			print ("----------------")
			print ("ID: " + block[0])
			print ("Nonce: " + block[1])
			print ("Data: " + block[2])
			print ("Previous hash: " + block[3])
			print ("Current hash: " + block[4])
		print ("---------End----------")
		
	def __init__(self):
		self.private_word = "this is dummy"
	
