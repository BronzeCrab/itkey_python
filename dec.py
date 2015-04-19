#Testing how decorator working

def decorator(test_func):
	def wrapper():
		print 'decorator is working' 
		test_func()   	    
	return wrapper

@decorator
def test_func():
	print 'hello world'
	raise Exception

try:
	test_func()
except Exception:
	pass

