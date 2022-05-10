address_d = [
['172.30.0.10', '8000', 'blockchain'],
['172.30.0.20', '8000', 'coordinator'],
['172.30.0.30', '8000', 'register'],
['172.30.0.40', '8000', 'open_closer'],
['172.30.0.50', '8000', 'wallet']
]

def return_full_address():
	return address_d
	
def return_address(d):
	return address_d[d]
