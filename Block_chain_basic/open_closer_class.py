class OpenCloser:
	
	'''
	Function to close the block
	amountT = Amount of transactions in the block
	'''
	def check_close_block(self, amountT):
		amountT = amountT + 1 # Current transactions + new transaction
		if amountT % self.number_block_close == 0 and amountT != 0:
			return True # Close the block
		return False 
	'''
	Generate new id for the transaction
	'''	
	def get_new_id(self, check):
		if check:
			self.current_id_chain = self.current_id_chain + 1
		return self.current_id_chain
		
	'''
	Get value to close transaction and new id
	'''
	def check_and_id(self, amount):
		check = self.check_close_block(amount)
		return self.get_new_id(check), check
	
	def __init__(self):
		self.current_id_chain = 2 # Current number of the transaction id ¡THIS NUMBER IS NOT RELATED TO THE CHAIN THOUGH IT SHOULD BE!
		self.number_block_close = 4 # Amount of transactions to be closed
		

