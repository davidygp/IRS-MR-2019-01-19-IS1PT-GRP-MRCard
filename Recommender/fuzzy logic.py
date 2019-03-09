def DBS_points_to_cashback(x):
	return x/5
	
def DBS_miles_to_cashback(x):
	if x < 10000:
		return x/2.5
	else:
		return 4000

def citibank_points_to_cashback(x):
	return x/440

def citibank_miles_to_cashback(x):
	return x/165

def standardchartered_points_to_cashback(x):
	return x/320

def standardchartered_miles_to_cashback(x):
	return x/128

def uob_points_to_cashback(x):
	if x < 1000:
		return 0.1*x
	else:
		return 100

def uob_miles_to_cashback(x):
	if x < 1000:
		return 0.1*x
	else:
		return 100
		
def maybank_points_to_cashback(x):
	if x < 15000:
		return x/300
	else:
		return 50
		
def maybank_miles_to_cashback(x):
	if x < 6000:
		return x/750
	else:
		return 50
		
def HSBC_points_to_cashback(x):
	return x/300
	
def HSBC_miles_to_cashback(x):
	return x/120
	
def ocbc_points_to_cashback(x):
	return x/350
	
def ocbc_miles_to_cashback(x):
	return x*2.5
	