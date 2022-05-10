class Register:
	
	'''
	Check syntax of the user that is going to transfer
	It is necesary to ckeck if it is a number to allow to use a hash as a user reference
	'''
	def check_syntax_user_general(self, user):
		for u in user:
			if not u.isalpha() and not u.isnumeric():
				return False # It is not valid
		return True
	
	'''
	Check amount that is going to be transfered
	'''
	def check_amount_user_general(self, amount):
		amount_s = str(amount) # Check that the values as a string
		for a in amount:
			if not a.isnumeric():
				return False # It is not valid
		return True
	
	'''
	Create data to transfer
	userS->userR:amount;
	'''
	def create_data_transfer_format(self, userS, userR, amount):
		s_r = "->"
		amountT = ":"
		endT = ";"
		return str(userS) + s_r + str(userR) + amountT + str(amount) + endT
			
